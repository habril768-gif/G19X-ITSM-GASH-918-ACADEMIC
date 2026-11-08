# PluriOne

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V. Proyecto académico G19X-ITSM-GASH-918-ACADEMIC, desarrollado por Gilian Abril Sánchez Hernández.

## Qué permite hacer

Registrar incidencias de personas o del entorno de trabajo; consultar expedientes según rol y departamento; validar su clasificación, asignar responsables y gestionar revisión, resolución, cierre y reapertura. Incluye confidencialidad, revisión independiente de participantes y auditoría de operaciones.

La interfaz React permite gestionar cuentas y departamentos, solicitar una sugerencia IA con texto simulado revisado y consultar el seguimiento de correos. Los avisos se capturan localmente en Mailpit. La analítica exporta únicamente agregados protegidos a Power BI Desktop.

## Estado y límites

El núcleo, el correo local y la analítica están implementados. La entrega se
completa con los recorridos y documentos de la [matriz de aceptación](docs/ACEPTACION_ENTREGA.md).
RNF-2 está aprobado en el entorno HTTP QA Linux de la
[evidencia 270](docs/evidencias/270-rnf2-linux-ci-aprobado.json).
La instalación y recuperación de copia conservan sus alcances en las evidencias
[255](docs/evidencias/255-instalacion-nueva-nucleo-reinicio.json) y
[256](docs/evidencias/256-recuperacion-copia-app-permisos-bi.json).
Consulta el [MVP](docs/MVP.md) y el [plan de cierre](docs/BACKLOG.md).

El entorno está destinado a pruebas locales con datos ficticios. La IA propone; una persona autorizada confirma categoría y prioridad. La evaluación del modelo mide un conjunto simulado, no garantiza su desempeño en casos nuevos. La supresión por privacidad puede dejar todos los indicadores vacíos; un valor suprimido nunca equivale a cero.

## Requisitos

- Git y Docker Desktop iniciado con motor Linux y Docker Compose.
- Node.js 20.19 o posterior dentro de la rama 20, o Node.js 22.12 o superior, con npm.
- Power BI Desktop para consultar el informe; es opcional para usar el panel web.
- Python solo para desarrollo sin contenedores o pruebas aisladas; la imagen backend incluye su entorno.

El arranque requiere configurar `POSTGRES_PASSWORD` en `.env` y asignar una contraseña privada al primer Admin RH. Para asistencia IA, configura `OPENAI_API_KEY` y activa el perfil `ai`; su uso puede consumir saldo. El núcleo funciona con la IA desactivada. El perfil de correo local utiliza Mailpit; un SMTP externo requiere su configuración y, cuando corresponda, credenciales propias. Las versiones técnicas necesarias para reproducibilidad se conservan en Dockerfiles, dependencias y migraciones.

## Arranque local en cinco pasos

Ejecuta los comandos desde la raíz del repositorio, salvo donde se indica otra carpeta. Si ya tienes datos y cuentas, consérvalos: no repitas el alta inicial ni la carga DEMO.

### 1. Preparar la configuración

Si todavía no existe `.env`:

```powershell
Copy-Item .env.example .env
```

Completa localmente `POSTGRES_PASSWORD`. Si `.env` ya existe, agrega únicamente lo que falte; no lo sobrescribas ni lo compartas.

### 2. Iniciar los servicios

```powershell
docker compose config --quiet
docker compose up -d --build --wait
```

### 3. Aplicar y verificar las migraciones

```powershell
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic check
```

Comprueba [salud de la API](http://127.0.0.1:8000/health) y [conexión y esquema](http://127.0.0.1:8000/health/db). La primera no verifica la base de datos. Ajusta la URL si cambiaste `API_PORT`.

### 4. Crear el primer administrador, solo en una instalación nueva

```powershell
docker compose exec api python -m app.manage_users bootstrap-admin --email admin@plurione.local --name "Administrador RH"
```

Introduce y confirma la contraseña cuando se solicite. No hay contraseña predeterminada ni registro público. Para cuentas adicionales y restablecimiento consulta [autenticación](docs/AUTENTICACION.md) y [administración](docs/ADMIN_USUARIOS.md). La [carga DEMO y cuentas de prueba](docs/DATOS_DEMO.md) es opcional: incluye seis correos ficticios y el comando para asignarles contraseña local de forma privada.

### 5. Abrir el panel web

En una terminal adicional:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Abre [PluriOne](http://127.0.0.1:5173/) e inicia sesión con tu cuenta. Mantén la terminal abierta. El proxy de desarrollo toma `API_PORT` del `.env` de la raíz. El puerto predeterminado es 8000. Reinicia Vite después de cambiarlo.

## Integraciones opcionales

| Módulo | Instrucciones | Consideración |
| --- | --- | --- |
| Asistencia IA | [Configuración y revisión](docs/IA.md) | Worker con perfil `ai`; clave solo en su entorno; revisión humana obligatoria |
| Correo | [Captura y seguimiento](docs/CORREO.md) | Perfil `mail`; Mailpit captura pruebas y no demuestra entrega a buzones externos |
| Power BI | [Analítica](docs/ANALITICA.md) e [informe](powerbi/README.md) | Cuenta de lectura y agregados; no conectar con la cuenta administradora |

## Organización del repositorio

| Carpeta | Contenido |
| --- | --- |
| `backend/` | API FastAPI, servicios, modelos, workers, migraciones y pruebas |
| `frontend/` | Panel React y pruebas de componentes |
| `infra/` | Guía del entorno Docker local |
| `powerbi/` | Consultas, medidas e informe guardado |
| `scripts/` | Actualización de módulos y ejecución controlada de evaluaciones |
| `docs/` | Requisitos, manuales, alcance, QA y evidencias |

## Configuración de tres procesos API

El perfil opcional usa tres procesos API; la validación de rendimiento y sus límites
se consultan en la [evidencia 270](docs/evidencias/270-rnf2-linux-ci-aprobado.json).
El arranque de cinco pasos usa el Compose base de un proceso. Para operar con la cantidad de procesos validada, usa en el paso 2:

```powershell
docker compose -f compose.yaml -f compose.rnf2.yaml config --quiet
docker compose -f compose.yaml -f compose.rnf2.yaml up -d --build --wait
```

Conserva ambos `-f` en futuros `up`; perfiles opcionales de correo/IA siguen sus guías. El override solo cambia el comando API, sin borrar datos ni activar proveedores. [Reproducir la formal y conocer alcance/consumo](docs/PRUEBA_RENDIMIENTO.md#configuración-de-tres-procesos-validada-para-rnf-2).

## Validación y documentación

Para pruebas del backend sigue [la guía de desarrollo](backend/README.md) y [PostgreSQL aislado](docs/PRUEBAS_POSTGRESQL.md). Para frontend, desde su carpeta ejecuta `npm.cmd test` y `npm.cmd run build`. Las pruebas de componentes no sustituyen un recorrido real por roles.

El [índice documental](docs/README.md) organiza la lectura. El [manual técnico](docs/MANUAL_TECNICO.md) explica operación y límites. El estado vigente está en MVP, backlog, entregables y trazabilidad; los cambios anteriores se consultan en la bitácora y Git.

## Uso de inteligencia artificial

Se utilizó Codex como apoyo para elaborar código, pruebas, documentación y casos simulados de evaluación. Las revisiones de etiquetas confirmadas por la autora y las ejecuciones están registradas en la documentación de evaluación; no equivalen a aprobación externa de la plataforma.

La plataforma usa OpenAI mediante LangChain para sugerir clasificación sobre texto simulado revisado explícitamente. La sugerencia no modifica por sí sola la decisión oficial. Las salidas y los resultados requieren revisión humana; no se presentan como asesoría laboral ni protocolos de emergencia.


### Mantenimiento de redes de las pruebas QA

Si Docker informa que agotó los pools de direcciones, consultar [el procedimiento de redes QA](docs/PRUEBA_RENDIMIENTO.md#mantenimiento-de-redes-qa). La herramienta revisa por defecto y permite liberar hasta dos redes QA vacías y registradas; conserva contenedores, volúmenes y reportes.


### Evidencia de rendimiento

La fila A01 de la matriz conserva la validación existente. Los reportes históricos,
el protocolo y los comandos de diagnóstico están en la [guía de rendimiento](docs/PRUEBA_RENDIMIENTO.md).
El trabajo de cierre actual se concentra en aceptación por roles y documentación.
