# Autenticación y cuentas locales

## Funcionamiento

El acceso utiliza correo y contraseña con Argon2id. Las sesiones duran una hora, usan un token opaco revocable y se validan contra usuario y departamento activos. El panel conserva el token en memoria. No hay registro público, contraseña predeterminada ni integración activa con Entra ID.

## Preparar la base

Sigue el [arranque principal](../README.md) y aplica `alembic upgrade head` antes de crear cuentas. Comprueba `/health/db`. No ejecutes bootstrap de nuevo si ya existe un administrador con credencial local; actualizar el esquema no exige recrear usuarios.

## Crear el primer administrador

Desde la raíz:

```powershell
docker compose exec api python -m app.manage_users bootstrap-admin --email admin@plurione.local --name "Administrador RH"
```

Se solicita y confirma una contraseña de 12 a 128 caracteres, sin mostrarla. El ejemplo es una cuenta local; puedes elegir otro correo. El comando crea el departamento Recursos Humanos si falta y registra la operación de forma transaccional. Solo el operador autorizado debe ejecutarlo.

## Administrar credenciales

Admin RH puede crear usuarios desde el panel o `POST /users`, de acuerdo con los permisos. El login no acepta que el usuario elija su rol. Consulta [administración](ADMIN_USUARIOS.md) y [RH independiente](ADMIN_INDEPENDIENTE.md).

Para restablecer una contraseña por operador, sin escribirla en argumentos:

```powershell
docker compose exec api python -m app.manage_users set-password --email usuario@example.invalid
```

La operación no reactiva cuentas dadas de baja y revoca sesiones. La carga DEMO no asigna contraseñas; deben provisionarse explícitamente. El cambio personal desde el panel o `POST /auth/change-password` exige la contraseña actual y también revoca todas las sesiones, incluida la actual.

## Verificar una sesión

En el panel: inicia sesión, consulta lo permitido por tu rol y cierra sesión. En Swagger: ejecuta `POST /auth/login`, copia temporalmente el token a Authorize (solo el valor, sin anteponer Bearer), consulta `GET /auth/me` y ejecuta `POST /auth/logout`. El token revocado debe recibir 401 al consultar de nuevo.

No captures el cuerpo del login, el diálogo Authorize, encabezados ni comandos que contengan tokens. Las evidencias de autenticación deben mostrar únicamente resultados sanitizados.

## Controles y límites

Cinco fallos bloquean temporalmente el correo durante 15 minutos. El mensaje no revela si la cuenta existe. El servidor comprueba permisos y revocación en cada solicitud; logout revoca la sesión actual. Usuarios y departamentos inactivos no obtienen acceso.

MFA, CAPTCHA y recuperación automática por correo quedan fuera del alcance actual. Antes de exposición externa se requieren HTTPS, control global de tráfico y mantenimiento operativo de sesiones/contadores. La aceptación completa de roles y concurrencia permanece en [backlog](BACKLOG.md) y [QA](REPORTE_QA.md).
