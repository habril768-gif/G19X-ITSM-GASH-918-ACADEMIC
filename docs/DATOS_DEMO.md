# Usuarios simulados para pruebas

## Alcance

El comando carga dos departamentos identificados como DEMO y seis usuarios: un Admin RH, dos Supervisores y tres Empleados. No crea incidencias, contraseñas ni cuentas de Microsoft. Los correos usan example.invalid y los identificadores Entra son ficticios.

| Cuenta ficticia | Rol | Departamento |
| --- | --- | --- |
| admin@example.invalid | Admin RH | DEMO - Recursos Humanos |
| supervisor-rh@example.invalid | Supervisor | DEMO - Recursos Humanos |
| supervisor-operaciones@example.invalid | Supervisor | DEMO - Operaciones |
| empleado-rh@example.invalid | Empleado | DEMO - Recursos Humanos |
| empleado-operaciones-1@example.invalid | Empleado | DEMO - Operaciones |
| empleado-operaciones-2@example.invalid | Empleado | DEMO - Operaciones |

## Ejecutar desde la raíz del repositorio

Con Docker Desktop abierto y las migraciones vigentes aplicadas según el README:

```powershell
docker compose up -d --build --wait
docker compose exec api python -m app.seed_demo --confirm-demo
```

Primera ejecución: departamentos_creados=2 y usuarios_creados=6. Al repetir sin cambios: ambos contadores son 0. No usar en una base de producción. El comando exige confirmación explícita y rechaza APP_ENV distinto de development o test; el valor por defecto es development para este entorno local.

La carga usa una transacción, no actualiza cuentas existentes ni las reactiva. Si faltan roles o existe un conflicto, revierte toda la ejecución y devuelve un mensaje sin credenciales. Los UUID son deterministas para repetir la carga. Un conflicto no se resuelve borrando datos: revisar la base seleccionada y reportar el error.

Guardar la salida como docs/evidencias/07-usuarios-demo.png. La ejecución PostgreSQL y su repetición están verificadas mediante las evidencias 07 y 08; ver REPORTE_QA.md.

## Diferencia respecto a autenticación

La autenticación vigente es local; no requiere Microsoft Entra ID. La carga DEMO crea registros sin contraseña. Para habilitar una cuenta ficticia ya cargada, el operador asigna una contraseña privada desde una terminal interactiva:

```powershell
docker compose exec api python -m app.manage_users set-password --email empleado-operaciones-1@example.invalid
```

Repite el comando para las cuentas de la tabla que necesites probar. Introduce una contraseña de 12 a 128 caracteres y confírmala cuando se solicite; no se publica una contraseña compartida. El primer administrador de una instalación nueva se crea con `bootstrap-admin`, como explica el README. No uses correos o datos de personas reales.

## Validación

Las pruebas test_seed_demo.py ejecutan solo las tablas roles, departamentos y users en SQLite con claves foráneas habilitadas. Comprueban carga repetible, conservación de bajas, roles y reversión transaccional. No sustituyen la ejecución real PostgreSQL ni prueban permisos de incidencias. Las incidencias ficticias se registran desde el panel con una cuenta habilitada; esta carga no las crea.
