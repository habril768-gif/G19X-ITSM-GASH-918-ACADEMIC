# Operador: administrador RH independiente adicional

Solo el operador con acceso a la terminal del servidor ejecuta esta operación. No hay endpoint público ni enlace de autoservicio. El operador autoriza una nueva cuenta administrativa; no revisa el contenido de casos ni descarta relaciones. En producción debe verificar por un canal administrativo la identidad y autorización de la persona, fuera del formulario de incidencias. Una persona involucrada no puede usar una segunda cuenta para eludir su exclusión: el MVP no verifica identidad humana entre cuentas; la asignación a otra persona es responsabilidad del operador y constituye limitación conocida.

Desde la raíz del proyecto, tras aplicar la actualización:

```powershell
docker compose up -d --build --wait
docker compose exec api python -m app.manage_users provision-independent-admin --email rh.independiente@example.invalid --name "RH Independiente Demo" --department "Recursos Humanos" --reason "Disponibilidad de gestor independiente para pruebas académicas"
```

El correo anterior es ficticio y válido solo para demostración local; no recibe mensajes. En uso real autorizado, usar los datos de la otra persona designada. El motivo es administrativo: no incluir texto ni datos sensibles del expediente, porque los argumentos pueden quedar en historial de terminal.

La contraseña se solicita dos veces sin mostrarse, nunca se pasa como argumento ni se añade a .env. Longitud 12–128. El comando exige terminal interactiva: si no puede ocultar entrada, cancela en lugar de usar eco. No usar redirecciones ni docker exec -T para esta operación.

Requiere que exista el administrador local inicial. Crea usuario nuevo con UUID nuevo, rol ADMIN_RH, departamento activo y hash Argon2id. Si el departamento indicado no existe, lo crea; si está inactivo rechaza. No modifica ni reutiliza correos existentes, ni sus roles/credenciales. bootstrap-admin sigue reservado al primer administrador; set-password mantiene recuperación de cuenta existente.

Auditoría: USUARIO_ACTUALIZADO dirigido a affected_user_id, actor nulo por operación del servidor, origen OPERADOR_SERVIDOR, operación provision-independent-admin y motivo administrativo. Nunca guarda contraseña o hash en el evento. Usuario, credencial, departamento nuevo y evento se confirman juntos; cualquier fallo revierte la transacción. En PostgreSQL comparte bloqueo advisory con bootstrap para serializar altas del operador; concurrencia real aún pendiente de prueba.

Crear al nuevo RH no cambia participantes, confidencialidad, estado ni responsable de ningún caso. La cuenta nueva debe iniciar sesión con su propia contraseña y gestionar solo expedientes permitidos por las reglas actuales. El gestor involucrado sigue excluido. No hay autoasignación ni retirada automática de protección. La independencia real depende de que el operador designe otra persona; un UUID nuevo no la demuestra.

Prueba manual prevista: ejecutar comando, iniciar sesión con cuenta nueva y GET /auth/me (ADMIN_RH); comprobar caso de prueba con administrador original declarado, acceso original rechazado y nuevo RH permitido. Capturar solo resultados sin token/Curl/contraseña. No crear ni declarar al administrador original sobre el único caso de trabajo sin disponer antes de otra cuenta independiente. El recorrido básico tiene evidencia parcial; consultar la sección de resultados y QA antes de repetirlo.

## Resultado manual posterior

Aplicación y ejecución reportadas por la autora; sesión de RH Independiente Demo verificada en evidencia 34. Recorrido manual 35–37 con límites en REVISION_RH_INDEPENDIENTE.md. Las instrucciones de prueba anteriores dejan de estar completamente pendientes, pero auditoría real del alta y concurrencia todavía no se acreditan.
