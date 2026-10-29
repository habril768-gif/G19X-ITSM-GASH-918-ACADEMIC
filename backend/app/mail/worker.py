"""Consulta durable cada dos segundos; sin claves de IA ni correos en logs."""
import argparse, time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_engine
from app.mail.smtp import SMTPTransport, DeliveryError
from app.services.mail import enabled, process_one

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--once',action='store_true'); args=parser.parse_args()
    if not enabled(): print('Correo desactivado; eventos conservados.'); return 0
    try: transport=SMTPTransport()
    except (ValueError,DeliveryError): print('Configuración SMTP no válida; revisa variables locales.'); return 2
    def factory(): return Session(get_engine(),expire_on_commit=False)
    try:
        while True:
            try:
                handled=process_one(factory,transport)
                if args.once: print('Evento atendido.' if handled else 'Sin eventos pendientes.'); return 0
                if not handled: time.sleep(2)
            except SQLAlchemyError:
                if args.once: print('No se confirmó el procesamiento del evento.'); return 1
                time.sleep(5)
    except KeyboardInterrupt: return 0

if __name__=='__main__': raise SystemExit(main())
