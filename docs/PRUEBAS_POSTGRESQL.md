# Pruebas PostgreSQL aisladas

Verificado el 17 de octubre de 2026. Se distinguen dos entornos: PostgreSQL 18.6 instalado localmente y PostgreSQL 17 del job existente de GitHub Actions. El proyecto de desarrollo conserva su configuración PostgreSQL 17 en Compose; no se actualizó ni se utilizó su base para estas pruebas.

## Repetir con un comando

Desde la raíz del proyecto, con las dependencias de desarrollo ya instaladas en backend/.venv:

~~~powershell
.ackend.venvScriptspython.exe backendscripts	est_postgres_isolated.py
~~~

El ejecutor detecta los binarios bajo Program Files/PostgreSQL en Windows. También acepta --pg-bin con una carpeta bin explícita. No descarga PostgreSQL ni depende del acceso al daemon de Docker. En otros sistemas puede localizar initdb en PATH o recibir --pg-bin. No debe ejecutarse con privilegios de administrador/root.

Crea un clúster nuevo dentro de .pgdata/run-*, un puerto disponible en 127.0.0.1 y una base plurione_test_* con credencial aleatoria. Solo el proceso hijo recibe POSTGRES_*/PGPASSWORD de prueba. No lee .env, no cambia variables del proceso padre, no publica credenciales ni se conecta a la base de desarrollo. Ejecuta upgrade head dos veces, alembic check y toda la suite con RUN_DB_TESTS=1.

Lee el resultado JUnit antes de retirar recursos y exige pruebas ejecutadas con cero fallos, errores y omisiones. Un fallo conserva código de salida distinto de cero; no se declara aprobada una ejecución parcial. Al terminar intenta detener el servidor y elimina únicamente su propia carpeta, validando directorio padre, prefijo y marcador. Si no confirma la parada, conserva datos temporales; una interrupción forzada también puede dejar restos ignorados por Git.

## Guardas de las integraciones

Al activar RUN_DB_TESTS=1, pytest_sessionstart exige nombre plurione_test o plurione_test_*, host localhost/127.0.0.1 y credencial presente. Las integraciones comprueban además current_database() contra la configuración. Estas guardas previenen equivocaciones de configuración; no sustituyen aislamiento frente a un operador que deliberadamente configure mal un entorno.

El CI existente usa base plurione_test en un servicio PostgreSQL 17 dedicado y satisface esas guardas. La ejecución normal sin RUN_DB_TESTS conserva las integraciones omitidas a propósito; eso no contradice que ya se ejecutaron en el entorno aislado.

## Resultados

- Ejecución local final: PostgreSQL 18.6, 103 aprobadas, 0 omitidas, 1 advertencia previa Starlette/httpx, 21.70s de pytest.
- Migraciones 0001–0004 aplicadas en clúster nuevo; upgrade repetido sin fallo y alembic check sin diferencias.
- Cinco integraciones PostgreSQL: catálogo/esquema, identidad externa reservada única, conservación de datos al migrar, bloqueos administrativos entre transacciones y rollback de departamento/auditoría.
- Ocho pruebas nuevas de guardas/ejecutor comprueban rechazo de destinos de desarrollo/remotos, configuración dedicada y retirada o conservación de recursos ante fallo.
- El resto de la suite incluye pruebas de servicios/HTTP con SQLite: ejecutar la suite con PostgreSQL disponible no convierte automáticamente todas esas pruebas en pruebas PostgreSQL.
- GitHub Actions del commit c8ad75c terminó exitosamente en el job postgres-integration con PostgreSQL 17, upgrades, check y pytest. Corresponde al código anterior a las nuevas guardas/dos integraciones; aún no acredita su ejecución remota.

La prueba de unicidad reservada ahora usa correos diferentes y exige específicamente uq_users_entra: antes otro duplicado podía satisfacer el rechazo. Esto no habilita autenticación Entra ID. Las pruebas de bloqueos usan conexiones independientes y lock_timeout de servidor; verifican exclusión de escritura/lectura y coexistencia de lectores. El rollback usa una transacción exterior/savepoints y falla deliberadamente la auditoría, sin persistir fixtures.

## Límites y evidencia

No se certifican todas las carreras posibles de asignación, cambio de rol, sesión, protección o IA, ni la matriz completa de UI. Las nuevas pruebas no acreditan por sí solas migración/check en la base de desarrollo. Frontend sin cambios y sin repetición de sus 55 pruebas previas.

Evidencia estructurada, sin nueva captura manual: [69-postgresql-integracion.json](evidencias/69-postgresql-integracion.json). CI observado: https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/39090144556.

Hubo un primer bloqueo por captura de pipes heredados al iniciar PostgreSQL en Windows. Se corrigió usando salida descartada para procesos de control y salida explícita para las verificaciones. La repetición completa pasó y retiró su servidor/carpeta. El intento inicial dejó .pgdata/run-gykzcxje: pg_ctl status indicó servidor detenido y el puerto propio ya no aceptaba conexión. La revisión automática rechazó su borrado manual por exigir una aprobación de sandbox deshabilitada; se conserva ignorado, sin reintentar ese borrado por otra vía.

## Correo por eventos — esquema 0006

API 0.11.0/React 0.8.0, esquema 0006: correo por eventos con permisos vigentes, outbox transaccional y panel de seguimiento RH. Captura local Mailpit preparada, sin correo real ni llamadas IA. Guía [CORREO.md](CORREO.md) en docs: script `scripts/ACTUALIZAR_CORREO.ps1` desde raíz construye, migra y actualiza API/worker con perfil mail. Validación local documentada en evidencia 85; recorrido Docker/buzón/navegador y aceptación integral pendientes. Se conservan usuarios, incidencias y evaluaciones anteriores.

## Analítica agregada — esquema 0007

API 0.12.0/esquema 0007: vistas agregadas con supresión en PostgreSQL, cuenta de lectura exclusiva y plantillas de importación Power BI. 201 pruebas backend aprobadas en PostgreSQL aislado; sin .pbix ni conexión Desktop acreditados. Seguir ANALITICA.md en docs y powerbi/README.md. Desde raíz: scripts/ACTUALIZAR_ANALITICA.ps1; después docker compose exec api python -m app.manage_reporting_user. Puerto opcional solo 127.0.0.1:5433 y contraseña interactiva. No usar cuenta administradora en Power BI ni reducir mínimos si todo queda suprimido. Evidencia 93. Recorrido de correo ya registrado en 86–92.
