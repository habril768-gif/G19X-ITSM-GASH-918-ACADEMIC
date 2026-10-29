"""Provisiona por operador una cuenta exclusiva para vistas agregadas."""
import argparse,getpass
from sqlalchemy.exc import SQLAlchemyError
from psycopg import Error as PsycopgError
from app.core.database import get_engine
from app.reporting.access import provision,ReportingAccessError

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--username',default='plurione_bi'); args=parser.parse_args()
    try:
        password=getpass.getpass('Contraseña nueva de lectura (16–128 caracteres): ')
        if password!=getpass.getpass('Confirma la contraseña: '):
            print('Las contraseñas no coinciden; no se crearon cuentas.'); return 2
        with get_engine().begin() as connection: provision(connection,args.username,password)
        print('Cuenta de lectura creada. Usa solo las dos vistas del esquema analytics en Power BI.'); return 0
    except ReportingAccessError as exc:
        print(str(exc)); return 2
    except (SQLAlchemyError,PsycopgError,ValueError):
        print('No se confirmó la creación de la cuenta; revisa esquema y permisos del operador.'); return 1
    except (KeyboardInterrupt,EOFError):
        print('Operación cancelada.'); return 2

if __name__=='__main__': raise SystemExit(main())
