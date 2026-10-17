import { useEffect, useRef, useState } from 'react';

function today() {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

export default function NewIncident({ api, user, onBack, onOpen }) {
  const employee = user.rol === 'EMPLEADO';
  const [options, setOptions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retry, setRetry] = useState(0);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const [receipt, setReceipt] = useState(null);
  const [acknowledged, setAcknowledged] = useState(false);
  const [participantId, setParticipantId] = useState('');
  const [form, setForm] = useState({ titulo: '', descripcion: '', incident_date: today(), scope: 'PERSONA',
    affected_employee_id: employee ? user.id : '', reported_department_id: user.departamento_id || '', is_confidential: false, participants: [] });
  const active = useRef(true);
  const submitting = useRef(false);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    const controller = new AbortController(); setLoading(true); setError('');
    api.request('/incidents/options', { signal: controller.signal }).then(value => { if (!controller.signal.aborted) setOptions(value); })
      .catch(e => { if (!controller.signal.aborted) setError(e.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [api, retry]);
  function change(key, value) { setForm(old => ({ ...old, [key]: value })); setAcknowledged(false); }
  const affected = options?.affected_employees.find(p => p.id === form.affected_employee_id);
  const isManager = id => options?.participants.some(p => p.id === id && ['ADMIN_RH', 'SUPERVISOR'].includes(p.rol));
  const privateExpected = form.is_confidential || ['ADMIN_RH', 'SUPERVISOR'].includes(affected?.rol) || form.participants.some(p => isManager(p.user_id));
  const mayDeclare = !employee || form.scope === 'PERSONA';
  const available = options?.participants.filter(p => p.id !== form.affected_employee_id && !form.participants.some(item => item.user_id === p.id)) || [];
  function addParticipant() {
    if (!participantId || !available.some(p => p.id === participantId) || form.participants.length >= 20) return;
    change('participants', [...form.participants, { user_id: participantId, declaration_reason: '' }]); setParticipantId('');
  }
  async function submit(event) {
    event.preventDefault(); if (submitting.current || uncertain || receipt) return;
    setError('');
    if (!form.titulo.trim() || !form.descripcion.trim()) { setError('Escribe un título y una descripción.'); return; }
    if (form.scope === 'PERSONA' && !affected) { setError('Selecciona un empleado permitido.'); return; }
    if (form.scope === 'ENTORNO' && !options.departments.some(d => d.id === form.reported_department_id)) { setError('Selecciona el departamento reportado.'); return; }
    if (form.participants.some(p => !p.declaration_reason.trim())) { setError('Explica la relación de cada participante.'); return; }
    if (privateExpected && !acknowledged) { setError('Confirma que leíste el aviso de confidencialidad.'); return; }
    const body = { titulo: form.titulo.trim(), descripcion: form.descripcion.trim(), incident_date: form.incident_date,
      scope: form.scope, is_confidential: form.is_confidential,
      ...(form.scope === 'PERSONA' ? { affected_employee_id: form.affected_employee_id } : { reported_department_id: form.reported_department_id }),
      participants: mayDeclare ? form.participants.map(p => ({ ...p, declaration_reason: p.declaration_reason.trim() })) : [] };
    submitting.current = true; setBusy(true);
    try {
      const result = await api.request('/incidents', { method: 'POST', body });
      if (result.received !== true || typeof result.id !== 'string' || typeof result.can_view !== 'boolean') throw new Error('No se pudo confirmar el acuse del registro.');
      if (active.current) { setReceipt(result); setForm(old => ({ ...old, titulo: '', descripcion: '', participants: [] })); }
    } catch (failure) {
      if (active.current) {
        const unknown = failure.status === undefined || failure.status === 0 || failure.status >= 500;
        setUncertain(unknown);
        setError(unknown ? 'No se pudo confirmar si el registro se completó. Revisa el listado antes de enviar otro para evitar duplicados. Si era confidencial, consulta a RH con el contexto de tu reporte.' : failure.message);
      }
    } finally { submitting.current = false; if (active.current) setBusy(false); }
  }
  if (receipt) return <section className="card receipt" aria-labelledby="receipt-title"><span className="eyebrow">ACUSE DE RECEPCIÓN</span><h1 id="receipt-title">Recibimos tu reporte</h1><p>Conserva este identificador como referencia:</p><p className="id receipt-id">{receipt.id}</p>
    {receipt.can_view ? <><p>Tu cuenta tiene acceso al expediente.</p><button className="primary" onClick={() => onOpen(receipt.id)}>Consultar expediente</button></>
      : <p className="notice">Este caso tiene acceso restringido. Tu cuenta recibe únicamente este acuse; no puede consultar su estado posterior ni el resultado.</p>}
    <button onClick={onBack}>Volver al listado</button></section>;
  return <section><button className="text-button" onClick={onBack} disabled={busy}>← Volver a incidencias</button><div className="section-heading"><div><span className="eyebrow">NUEVO REPORTE</span><h1>Registrar incidencia</h1><p className="muted">Describe lo sucedido con claridad. Utiliza únicamente datos simulados en este entorno académico.</p></div></div>
    {error && <p className="error" role="alert">{error}</p>}{loading && <p role="status">Cargando opciones permitidas…</p>}
    {!loading && !options && <button onClick={() => setRetry(v => v + 1)}>Reintentar opciones</button>}
    {options && !loading && <form onSubmit={submit} className="card incident-form"><fieldset disabled={busy || uncertain}><legend>Datos del reporte</legend>
      <label>Título<input required maxLength={200} value={form.titulo} onChange={e => change('titulo', e.target.value)} /></label>
      <label>Descripción<textarea required maxLength={10000} rows={5} value={form.descripcion} onChange={e => change('descripcion', e.target.value)} /></label>
      <div className="form-row"><label>Fecha del hecho<input type="date" required value={form.incident_date} onChange={e => change('incident_date', e.target.value)} /></label>
      <label>Ámbito<select value={form.scope} onChange={e => { setForm(old => ({ ...old, scope: e.target.value, participants: [], affected_employee_id: employee ? user.id : '' })); setParticipantId(''); setAcknowledged(false); }}><option value="PERSONA">Persona</option><option value="ENTORNO">Entorno de trabajo</option></select></label></div>
      {form.scope === 'PERSONA' ? employee ? <p>Empleado afectado: <strong>{user.nombre_completo}</strong>. Solo puedes registrar casos personales sobre ti.</p>
        : <label>Empleado afectado<select required value={form.affected_employee_id} onChange={e => { setForm(old => ({ ...old, affected_employee_id: e.target.value, participants: old.participants.filter(p => p.user_id !== e.target.value) })); setAcknowledged(false); }}><option value="">Selecciona un empleado</option>{options.affected_employees.map(p => <option key={p.id} value={p.id}>{p.nombre_completo}</option>)}</select></label>
        : <label>Departamento reportado<select required value={form.reported_department_id} onChange={e => change('reported_department_id', e.target.value)}><option value="">Selecciona departamento</option>{options.departments.map(d => <option key={d.id} value={d.id}>{d.nombre}</option>)}</select><span className="muted">Un riesgo del entorno no requiere persona afectada.</span></label>}
      {employee && form.scope === 'PERSONA' && <p className="help">Reporta situaciones que te afecten. Los reportes como testigo exclusivamente sobre terceros quedan fuera de este formulario.</p>}
      {mayDeclare && <section className="participants-form"><h2>Otros participantes</h2><p className="muted">Opcional. Explica su relación con el hecho; el afectado ya está incluido.</p><div className="form-row"><label>Agregar participante<select value={participantId} onChange={e => setParticipantId(e.target.value)}><option value="">Selecciona una persona</option>{available.map(p => <option key={p.id} value={p.id}>{p.nombre_completo} · {p.rol}</option>)}</select></label><button type="button" onClick={addParticipant} disabled={!participantId || form.participants.length >= 20}>Agregar</button></div>
      {form.participants.map(item => <div className="participant-card" key={item.user_id}><label>Relación de {options.participants.find(p => p.id === item.user_id)?.nombre_completo || 'participante'}<textarea required rows={2} maxLength={2000} value={item.declaration_reason} onChange={e => change('participants', form.participants.map(p => p.user_id === item.user_id ? { ...p, declaration_reason: e.target.value } : p))} /></label><button type="button" onClick={() => change('participants', form.participants.filter(p => p.user_id !== item.user_id))}>Quitar participante</button></div>)}</section>}
      <label className="check-label"><input type="checkbox" checked={form.is_confidential} onChange={e => change('is_confidential', e.target.checked)} />Solicitar confidencialidad</label>
      <p className="notice">La confidencialidad, incluida la que se activa al involucrar a un gestor, restringe el caso a RH independiente. Quien no tenga acceso recibirá solo un acuse, sin seguimiento ni resultado. La clasificación y atención requieren revisión humana.</p>
      {privateExpected && <label className="check-label"><input type="checkbox" required checked={acknowledged} onChange={e => setAcknowledged(e.target.checked)} />Comprendo las restricciones de acceso de este reporte</label>}
      <button className="primary" type="submit" disabled={busy || uncertain}>{busy ? 'Registrando…' : 'Registrar incidencia'}</button>
    </fieldset></form>}
  </section>;
}
