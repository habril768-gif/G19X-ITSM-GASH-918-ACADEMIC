# PluriOne

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V. Proyecto académico G19X-ITSM-GASH-918-ACADEMIC, desarrollado por Gilian Abril Sánchez Hernández.

## Qué permite hacer

Registrar incidencias de personas o del entorno de trabajo; consultar expedientes según rol y departamento; validar su clasificación, asignar responsables y gestionar revisión, resolución, cierre y reapertura. Incluye confidencialidad, revisión independiente de participantes y auditoría de operaciones.

La interfaz React permite gestionar cuentas y departamentos, solicitar una sugerencia IA con texto simulado revisado y consultar el seguimiento de correos. Los avisos se capturan localmente en Mailpit. La analítica exporta únicamente agregados protegidos a Power BI Desktop.

## Estado y límites

El núcleo, correo y analítica tienen implementación y evidencia. El correo cuenta con un recorrido básico real; Power BI tiene conexión e informe guardado. **La entrega integral continúa pendiente**: RNF-2 aún no alcanza el p95 requerido; faltan instalación/recuperación operativa completa, aceptación integral y actividades reales de capacitación. Existen recorridos acotados por rol y pruebas de Power BI, con sus límites registrados. Consulta el [alcance del MVP](docs/MVP.md), el [plan de cierre](docs/BACKLOG.md) y la [evidencia de QA](docs/REPORTE_QA.md).

El entorno está destinado a pruebas locales con datos ficticios. La IA propone; una persona autorizada confirma categoría y prioridad. La evaluación del modelo mide un conjunto simulado, no garantiza su desempeño en casos nuevos. La supresión por privacidad puede dejar todos los indicadores vacíos; un valor suprimido nunca equivale a cero.

## Requisitos

- Git y Docker Desktop iniciado con motor Linux y Docker Compose.
- Node.js compatible con las dependencias fijadas en `frontend/package-lock.json` y npm.
- Power BI Desktop para consultar el informe; es opcional para usar el panel web.
- Python solo para desarrollo sin contenedores o pruebas aisladas; la imagen backend incluye su entorno.

No se necesita una clave OpenAI para el núcleo. La asistencia IA requiere activación y credenciales propias; puede consumir saldo. Las versiones técnicas necesarias para reproducibilidad se conservan en Dockerfiles, dependencias y migraciones.

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

Abre [PluriOne](http://127.0.0.1:5173/) e inicia sesión con tu cuenta. Mantén la terminal abierta. El proxy de desarrollo apunta a la API local; si cambias su puerto, ajusta `frontend/vite.config.js`.

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

## Rendimiento local validado

RNF-2 cumplió con **tres procesos API**,10 clientes,30 s de calentamiento y300 s medidos:35.216 solicitudes sin errores,p95 listado123,81/detalle113,27/creación194,04/actualización167,77ms. [Evidencia y límites de hardware/protocolo](docs/evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json). Esto no cierra los demás pendientes del MVP ni acredita cualquier equipo o proveedor externo.

El arranque de cinco pasos usa el Compose base de un proceso. Para operar con la cantidad de procesos validada, usa en el paso2:

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


### Validación formal de rendimiento con control previo

El [comando formal condicionado](docs/PRUEBA_RENDIMIENTO.md#corrida-formal-con-control-previo) comprueba CPU previa y libera hasta dos redes QA vacías antes de iniciar la ventana formal existente. Si no cumple las condiciones de arranque, termina sin generar carga. No cambia el criterio RNF-2 ni acredita rendimiento por sí solo.


Para parámetros de conexión y controles diagnósticos opcionales, consulta el [manual técnico](docs/MANUAL_TECNICO.md) y la [guía de rendimiento](docs/PRUEBA_RENDIMIENTO.md). Los diagnósticos breves no acreditan RNF-2.
