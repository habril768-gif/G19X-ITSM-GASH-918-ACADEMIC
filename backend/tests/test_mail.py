"""Correo: eventos, confidencialidad al despachar, fallos y captura SMTP local."""
import smtplib, socketserver, threading
from datetime import timedelta
from email import message_from_bytes
from types import SimpleNamespace
from uuid import UUID, uuid4
from unittest.mock import Mock
import pytest
from sqlalchemy import select,func,event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.core.security import utcnow
from app.models import MailDelivery, AuditEvent, Incident, IncidentParticipant
from app.services.mail import queue_event,process_one
from app.mail.smtp import SMTPTransport,DeliveryError
from test_incidents import world,create

@pytest.fixture(autouse=True)
def safe_env(monkeypatch):
    for key in ('SMTP_USERNAME','SMTP_PASSWORD','SMTP_FROM','WEB_BASE_URL','SMTP_TLS','SMTP_HOST','SMTP_PORT','MAIL_MODE'):
        monkeypatch.delenv(key,raising=False)
    monkeypatch.setenv('MAIL_ENABLED','true')

def jobs(db,case,kind=None):
    db.expire_all()
    query=select(MailDelivery).where(MailDelivery.case_id==UUID(case))
    if kind: query=query.where(MailDelivery.kind==kind)
    return db.scalars(query).all()

def factory(db): return lambda:Session(db.bind,expire_on_commit=False)

def ready(c,s,a,case):
    s['user']=a['admin']
    assert c.put(f'/incidents/{case}/classification',json={'category_id':2,'priority':2}).status_code==200
    assert c.post(f'/incidents/{case}/transitions',json={'status':'EN_REVISION','assigned_to':str(a['super'].id)}).status_code==200

def test_creation_independent_rh_and_duplicate_event(world):
    c,db,a,s,*_=world
    ident=create(c,participants=[{'user_id':str(a['admin'].id),'declaration_reason':'Conflicto simulado'}])
    rows=jobs(db,ident); assert len(rows)==1 and rows[0].recipient_id==a['admin2'].id
    audit=db.get(AuditEvent,rows[0].event_id)
    queue_event(db,db.get(Incident,UUID(ident)),audit); db.commit()
    assert len(jobs(db,ident))==1
    transport=Mock(); assert process_one(factory(db),transport)
    assert jobs(db,ident)[0].status=='ENVIADA'
    assert transport.send.call_args.args[0]=='admin2@example.invalid'
    assert not process_one(factory(db),transport)

def test_no_independent_rh_logs_omission(world):
    c,db,a,s,*_=world
    ident=create(c,participants=[{'user_id':str(a[name].id),'declaration_reason':'Simulado'} for name in ('admin','admin2')])
    row=jobs(db,ident)[0]
    assert row.status=='OMITIDA' and row.recipient_id is None and row.error=='Sin destinatario autorizado'
    transport=Mock(); assert not process_one(factory(db),transport); transport.send.assert_not_called()

@pytest.mark.parametrize('change',['inactive','department','participant','promotion'])
def test_permission_rechecked_before_dispatch(world,change):
    c,db,a,s,one,two=world; ident=create(c)
    for name in ('admin','admin2'):
        if change=='inactive': a[name].is_active=False
        elif change=='department': db.get(type(one),a[name].departamento_id).is_active=False
        elif change=='participant': db.add(IncidentParticipant(incidencia_id=UUID(ident),user_id=a[name].id,declaration_reason='Simulado'))
        else: a[name].rol_id=3
    db.commit(); transport=Mock()
    while process_one(factory(db),transport): pass
    assert all(r.status=='OMITIDA' for r in jobs(db,ident)); transport.send.assert_not_called()

def test_permission_change_after_durable_claim_also_omits(world):
    c,db,a,s,*_=world; ident=create(c); counter=0
    def changing_factory():
        nonlocal counter
        counter+=1
        if counter==2:
            a['admin'].is_active=a['admin2'].is_active=False; db.commit()
        return Session(db.bind,expire_on_commit=False)
    transport=Mock(); assert process_one(changing_factory,transport)
    assert any(r.status=='OMITIDA' and r.attempts==1 for r in jobs(db,ident))
    transport.send.assert_not_called()

def test_assignment_resolution_reopening_and_no_extra_emails(world):
    c,db,a,s,*_=world; ident=create(c); ready(c,s,a,ident)
    assert len(jobs(db,ident,'ASIGNACION'))==1
    assert c.put(f'/incidents/{ident}/assignment',json={'assigned_to':str(a['super'].id)}).status_code==200
    assert len(jobs(db,ident,'ASIGNACION'))==1
    assert c.post(f'/incidents/{ident}/transitions',json={'status':'RESUELTA','resolution_text':'Resolución simulada'}).status_code==200
    resolved=jobs(db,ident,'RESOLUCION'); assert len(resolved)==1 and resolved[0].recipient_id==a['employee'].id
    assert c.post(f'/incidents/{ident}/transitions',json={'status':'CERRADA'}).status_code==200
    assert len(jobs(db,ident,'RESOLUCION'))==1
    assert len(jobs(db,ident,'CIERRE'))==1
    assert c.post(f'/incidents/{ident}/transitions',json={'status':'EN_REVISION','reason':'Nueva revisión simulada'}).status_code==200
    assert len(jobs(db,ident,'REAPERTURA'))==1
    transport=Mock()
    while process_one(factory(db),transport): pass
    assert jobs(db,ident,'RESOLUCION')[0].status=='OMITIDA'
    assert jobs(db,ident,'REAPERTURA')[0].status=='ENVIADA'
    assert jobs(db,ident,'CIERRE')[0].status=='OMITIDA'

def test_confidential_resolution_never_mails_reporter_or_affected(world):
    c,db,a,s,*_=world; ident=create(c,is_confidential=True); s['user']=a['admin']
    assert c.put(f'/incidents/{ident}/classification',json={'category_id':2,'priority':1}).status_code==200
    assert c.post(f'/incidents/{ident}/transitions',json={'status':'EN_REVISION','assigned_to':str(a['admin2'].id)}).status_code==200
    assert c.post(f'/incidents/{ident}/transitions',json={'status':'RESUELTA','resolution_text':'Simulado privado'}).status_code==200
    row=jobs(db,ident,'RESOLUCION')[0]; assert row.status=='OMITIDA' and row.recipient_id is None

def test_old_assignment_suppressed_after_confidential_reassignment(world):
    c,db,a,s,*_=world; ident=create(c); ready(c,s,a,ident)
    # Ruta real de protección: nuevo responsable se notifica dentro de la misma transacción.
    assert c.put(f'/incidents/{ident}/confidentiality',json={'is_confidential':True,'reason':'Protección simulada','assigned_to':str(a['admin2'].id)}).status_code==200
    rows=jobs(db,ident,'ASIGNACION'); assert {r.recipient_id for r in rows}=={a['super'].id,a['admin2'].id}
    transport=Mock()
    while process_one(factory(db),transport): pass
    assert next(r for r in jobs(db,ident,'ASIGNACION') if r.recipient_id==a['super'].id).status=='OMITIDA'
    assert 'super@example.invalid' not in [call.args[0] for call in transport.send.call_args_list]

@pytest.mark.parametrize('transient,expected_attempts',[(True,4),(False,1)])
def test_bounded_retries_sanitized_failures_and_rh_status(world,transient,expected_attempts):
    c,db,a,s,*_=world; ident=create(c)
    # Solo un destinatario para medir intentos sin mezclar trabajos.
    a['admin2'].is_active=False; db.commit()
    transport=Mock(); transport.send.side_effect=DeliveryError(transient)
    for _ in range(6):
        for row in jobs(db,ident): row.available_at=utcnow()-timedelta(seconds=1)
        db.commit(); process_one(factory(db),transport)
    row=next(r for r in jobs(db,ident) if r.recipient_id==a['admin'].id)
    assert row.status=='FALLIDA' and row.attempts==expected_attempts
    assert transport.send.call_count==expected_attempts
    assert c.get(f'/incidents/{ident}/mail').status_code==403
    s['user']=a['super']; assert c.get(f'/incidents/{ident}/mail').status_code==403
    s['user']=a['admin']; result=c.get(f'/incidents/{ident}/mail')
    assert result.status_code==200 and result.headers['cache-control']=='no-store'
    assert 'FALLIDA' in result.text and 'recipient_id' not in result.text and '@' not in result.text
    db.add(IncidentParticipant(incidencia_id=UUID(ident),user_id=a['admin'].id,declaration_reason='Simulado')); db.commit()
    assert c.get(f'/incidents/{ident}/mail').status_code==404

def test_disabled_worker_preserves_outbox(world,monkeypatch):
    c,db,a,s,*_=world; ident=create(c); monkeypatch.setenv('MAIL_ENABLED','false')
    transport=Mock(); assert not process_one(factory(db),transport)
    assert all(row.attempts==0 and row.status=='PENDIENTE' for row in jobs(db,ident)); transport.send.assert_not_called()

def test_outbox_failure_rolls_back_creation_and_audit(world):
    c,db,a,s,*_=world
    def fail(conn, cursor, statement, parameters, context, executemany):
        compiled = getattr(context, 'compiled', None)
        table = getattr(getattr(compiled, 'statement', None), 'table', None)
        if table is not None and table.name == 'mail_deliveries' and statement.lstrip().upper().startswith('INSERT'):
            raise SQLAlchemyError('Simulado')
    event.listen(db.bind,'before_cursor_execute',fail)
    try:
        result=c.post('/incidents',json={'titulo':'Simulado','descripcion':'Ficticio','incident_date':'2026-10-18'})
        assert result.status_code==503
    finally: event.remove(db.bind,'before_cursor_execute',fail)
    assert db.scalar(select(func.count()).select_from(Incident))==0
    assert db.scalar(select(func.count()).select_from(AuditEvent))==0
    assert db.scalar(select(func.count()).select_from(MailDelivery))==0

def test_expired_lease_recovers_without_new_event(world):
    c,db,a,s,*_=world; ident=create(c); rows=jobs(db,ident)
    row=rows[0]; row.status='EN_PROCESO'; row.attempts=1; row.lease_token=uuid4(); row.lease_until=utcnow()-timedelta(seconds=1); db.commit()
    transport=Mock()
    while process_one(factory(db),transport): pass
    recovered=next(r for r in jobs(db,ident) if r.id==row.id)
    assert recovered.status=='ENVIADA' and recovered.attempts==2
    assert len(jobs(db,ident))==2

def test_real_local_smtp_capture_contains_only_reference_and_link(monkeypatch):
    messages=[]
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            self.wfile.write(b'220 local capture\r\n')
            while line:=self.rfile.readline():
                command=line.split(b' ',1)[0].strip().upper()
                if command==b'DATA':
                    self.wfile.write(b'354 data\r\n'); chunks=[]
                    while (part:=self.rfile.readline()) not in (b'.\r\n',b''):
                        chunks.append(part)
                    messages.append(b''.join(chunks)); self.wfile.write(b'250 accepted\r\n')
                elif command==b'QUIT': self.wfile.write(b'221 bye\r\n'); return
                else: self.wfile.write(b'250 local\r\n')
    with socketserver.TCPServer(('127.0.0.1',0),Handler) as server:
        thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
        monkeypatch.setenv('SMTP_HOST','127.0.0.1'); monkeypatch.setenv('SMTP_PORT',str(server.server_address[1]))
        case,delivery=uuid4(),uuid4()
        try: SMTPTransport().send('recipient@example.invalid',case,delivery)
        finally: server.shutdown(); thread.join(timeout=2)
    assert len(messages)==1
    msg=message_from_bytes(messages[0]); text=msg.get_payload(decode=True).decode('utf-8')
    assert f'/?incident={case}' in text and str(case) in str(msg['Subject'])
    assert msg['Message-ID']==f'<{delivery}@plurione.invalid>'
    assert 'recipient@example.invalid' not in text and 'resolución' not in text.lower()

@pytest.mark.parametrize('code,transient',[(450,True),(550,False)])
def test_smtp_classifies_recipient_refusal_without_saving_raw_error(monkeypatch,code,transient):
    smtp=Mock(); smtp.send_message.side_effect=smtplib.SMTPRecipientsRefused({'demo@example.invalid':(code,b'SECRET RAW')})
    monkeypatch.setattr(smtplib,'SMTP',Mock(return_value=smtp))
    with pytest.raises(DeliveryError) as exc: SMTPTransport().send('demo@example.invalid',uuid4(),uuid4())
    assert exc.value.transient is transient and 'SECRET' not in str(exc.value)

def test_capture_rejects_external_host_and_header_injection(monkeypatch):
    monkeypatch.setenv('SMTP_HOST','smtp.example.invalid')
    with pytest.raises(ValueError): SMTPTransport()
    monkeypatch.setenv('SMTP_HOST','localhost')
    smtp=Mock(); monkeypatch.setattr(smtplib,'SMTP',smtp)
    with pytest.raises(DeliveryError): SMTPTransport().send('a@example.invalid\nBcc: evil@example.invalid',uuid4(),uuid4())
    smtp.assert_not_called()


def test_socket_cleanup_failure_does_not_retry_accepted_data(monkeypatch):
    smtp=Mock(); smtp.send_message.return_value={}; smtp.close.side_effect=OSError('Simulado')
    monkeypatch.setattr(smtplib,'SMTP',Mock(return_value=smtp))
    SMTPTransport().send('demo@example.invalid',uuid4(),uuid4())
    smtp.send_message.assert_called_once()

def test_external_transport_requires_tls_and_verifies_starttls(monkeypatch):
    monkeypatch.setenv('MAIL_MODE','external'); monkeypatch.setenv('SMTP_HOST','smtp.example.invalid')
    monkeypatch.setenv('WEB_BASE_URL','https://plurione.example.invalid')
    with pytest.raises(ValueError): SMTPTransport()
    monkeypatch.setenv('SMTP_TLS','starttls'); monkeypatch.setenv('SMTP_USERNAME','simulated-user'); monkeypatch.setenv('SMTP_PASSWORD','simulated-secret')
    smtp=Mock(); smtp.send_message.return_value={}
    monkeypatch.setattr(smtplib,'SMTP',Mock(return_value=smtp))
    SMTPTransport().send('demo@example.invalid',uuid4(),uuid4())
    context=smtp.starttls.call_args.kwargs['context']
    assert context.check_hostname and context.verify_mode==2
    calls=[item[0] for item in smtp.method_calls]
    assert calls.index('starttls') < calls.index('login') < calls.index('send_message')


def test_pending_assignment_still_notifies_when_same_manager_starts_review(world):
    c,db,a,s,*_=world; ident=create(c); s['user']=a['admin']
    assert c.put(f'/incidents/{ident}/assignment',json={'assigned_to':str(a['super'].id)}).status_code==200
    assignment_id=jobs(db,ident,'ASIGNACION')[0].id
    ready(c,s,a,ident)
    transport=Mock()
    while process_one(factory(db),transport): pass
    rows=jobs(db,ident,'ASIGNACION')
    assert len(rows)==1 and rows[0].id==assignment_id and rows[0].status=='ENVIADA'
    assert [call.args[0] for call in transport.send.call_args_list]==['super@example.invalid']
