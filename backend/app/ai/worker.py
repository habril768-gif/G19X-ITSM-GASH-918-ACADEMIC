"""Worker ejecutable: avisos Redis más recuperación de la cola durable en PostgreSQL."""
import argparse
import os
import time
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.ai import queue
from app.ai.provider import OpenAIClassifier
from app.core.database import get_engine
from app.services.ai import enabled, process_one


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    if not enabled():
        print('IA desactivada; la clasificación manual continúa disponible.'); return 0
    key = os.environ.get('OPENAI_API_KEY', '').strip()
    if not key or not os.environ.get('OPENAI_MODEL', '').strip():
        print('Configura clave y modelo localmente antes de iniciar el worker.'); return 2
    provider = OpenAIClassifier(key)
    def factory(): return Session(get_engine(), expire_on_commit=False)
    try:
        while True:
            try:
                handled = process_one(factory, provider)
                if args.once:
                    print('Trabajo atendido.' if handled else 'Sin trabajos disponibles.'); return 0
                if not handled and not queue.wait():
                    time.sleep(5)
            except SQLAlchemyError:
                if args.once:
                    print('No se pudo consultar la cola durable.'); return 1
                time.sleep(5)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
