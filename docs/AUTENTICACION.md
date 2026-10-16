> Actualización: la autenticación se introdujo en 0002; la API 0.4.0 requiere ahora head 0003 para /health/db. Aplicar el último head conserva cuentas/sesiones. El procedimiento de login no cambia.

# Autenticación local FastAPI

## Decisión vigente

El 15 de octubre de 2026 la autora sustituyó Microsoft Entra ID por autenticación local. No se necesitan Azure, consentimiento institucional, client ID ni secreto Microsoft. Las aplicaciones registradas previamente no se utilizan; no se eliminaron ni modificaron desde este proyecto.

API 0.3.0; esquema 0002. Contraseñas Argon2id; sesiones de una hora con token aleatorio Bearer. No se usan JWT ni cookies en esta entrega. La futura interfaz conservará el token en memoria, sin guardarlo en URL o almacenamiento persistente del navegador. Un despliegue externo exige HTTPS y controles de tráfico adicionales.

## Actualizar la base existente

Desde la raíz con Docker Desktop abierto:

```powershell
docker compose up -d --build --wait
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
```

Se espera 0002 (head). La migración conserva IDs, usuarios DEMO, incidencias e historial. external_id y tenant_id pasan a opcionales; las nuevas cuentas locales no necesitan valores ficticios. Se añade unicidad del correo sin distinguir mayúsculas y tres tablas de autenticación. Si existen correos duplicados, la migración fallará de forma transaccional: revisar y resolver cuentas; nunca borrar datos para saltar el conflicto. No ejecutar downgrade: la reversión automática de 0002 está deshabilitada para preservar credenciales y cuentas locales.

/health sigue público. /health/db exige revisión 0002 y responderá 503 antes de migrar.

## Crear el primer Admin RH

```powershell
docker compose exec api python -m app.manage_users bootstrap-admin --email admin@plurione.local --name "Administrador RH"
```

Se pedirá una contraseña de 12 a 128 caracteres y su confirmación. No se mostrará al escribirla. El correo de ejemplo es solo para pruebas locales; no necesita enviar correo. Puedes elegir otro correo. No hay contraseña predeterminada.

El comando crea un departamento Recursos Humanos si falta y un administrador nuevo. No modifica usuarios existentes ni permite segundo bootstrap si ya hay un Admin RH con credencial local. Deben estar aplicados los catálogos. La operación se audita y es transaccional. Solo un operador con acceso al servidor debe ejecutar este comando.

## Probar en /docs

1. POST /auth/login: introduce tu correo y contraseña en JSON y ejecuta.
2. Copia access_token de la respuesta. Es una credencial temporal: no incluirlo en capturas, commits ni mensajes.
3. Pulsa Authorize y pega solo el token en HTTPBearer, sin anteponer Bearer. Confirma y cierra el diálogo.
4. GET /auth/me debe devolver el usuario, rol y departamento, sin hashes.
5. POST /auth/logout devuelve 204; volver a ejecutar /auth/me con el mismo token debe devolver 401.

Capturas previstas: 09-migracion-auth-local.png, 10-auth-me.png y 11-logout-sesion-revocada.png. No capturar el cuerpo de respuesta del login, el diálogo Authorize, encabezados Authorization ni comandos curl que contengan el token. Puede capturarse el estado HTTP y JSON de /auth/me ocultando credenciales y datos personales.

## Usuarios y contraseñas

- POST /users: solo Admin RH; requiere email, password, nombre_completo, departamento_id y rol_id (1 Admin RH, 2 Supervisor, 3 Empleado). No acepta rol durante login. No existe registro público.
- POST /auth/change-password: contraseña actual y nueva; revoca todas las sesiones, incluso la actual. Se necesita login nuevamente.
- Restablecimiento inicial por operador, sin escribir contraseña en el comando:

```powershell
docker compose exec api python -m app.manage_users set-password --email usuario@example.invalid
```

Esta operación no reactiva usuarios dados de baja y revoca sesiones. Las seis cuentas DEMO continúan sin contraseña hasta provisionarlas explícitamente. No se dan credenciales fijas al seed. Se registran altas y cambios de contraseña sin sus valores.

## Controles y límites

La API valida expiración y revocación y consulta usuario/departamento activo en cada solicitud. Logout revoca solo el token actual. Cinco fallos por correo bloquean 15 minutos; se usa el mismo mensaje para cuentas inexistentes, inactivas y contraseñas incorrectas. El control es persistente en PostgreSQL, con bloqueo de fila para solicitudes concurrentes.

No hay CAPTCHA, MFA, recuperación por correo, interfaz React, administración completa de bajas o rate limiting global por IP en esta entrega. Antes de exponer públicamente se necesitan HTTPS, limitación global de intentos, revisión de permisos operativos y mantenimiento de sesiones expiradas/contadores antiguos. El backend local de desarrollo sigue limitado a loopback por Compose.

Para una futura integración externa se conserva id interno; cualquier vinculación a Entra requerirá verificación explícita de identidad. No se implementa ahora.

Referencias: [FastAPI y hash de contraseñas](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) y [gestión de sesiones OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html). Se toma el hash Argon2id de la guía; las sesiones de este proyecto son opacas, no JWT.
