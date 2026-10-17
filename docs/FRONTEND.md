# Panel React — primera entrega (0.1.0)

Implementado el 17 de octubre de 2026, conectado a la API 0.8.0 existente. Incluye login, listado paginado con filtros, detalle e historial de lectura. RF-8 parcial: todavía no hay formulario de registro, validación/asignación/transiciones ni administración de usuarios en pantalla. Las operaciones de escritura siguen disponibles en Swagger. No se presenta el frontend como MVP completo.

## Inicio local

Desde la raíz del proyecto mantener Docker Desktop abierto y servicios activos con docker compose up -d --wait. Para el frontend:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Abrir http://127.0.0.1:5173/. Node 24 fue usado para verificar esta entrega. Versiones fijadas en package.json y package-lock.json: React/React DOM 19.3.1, Vite 8.3.4, plugin React 6.1.2, Vitest 5.0.5, jsdom 29.1.1. Guía de Vite consultada: https://vite.dev/guide/ . En Windows se usa npm.cmd para evitar restricciones de npm.ps1.

El servidor escucha solo en 127.0.0.1:5173, con puerto estricto: si está ocupado falla en vez de cambiar de dirección. Vite reenvía /api a 127.0.0.1:8000, sin modificar CORS del backend ni introducir claves en el navegador. No necesita .env frontend. Nunca copiar contraseñas, claves OpenAI ni POSTGRES_PASSWORD a variables VITE_. No editar el .env del backend para iniciar la interfaz.

Si el proceso iniciado por el asistente termina, volver a ejecutar npm.cmd run dev en la carpeta frontend. La terminal debe permanecer abierta. npm run build genera dist ignorado por Git; no despliega. Publicar requiere proxy /api, HTTPS y configuración de servidor aprobada: Vite dev no constituye despliegue productivo.

## Uso

Iniciar sesión con una cuenta local ya provisionada y su contraseña. No hay registro público ni contraseña compartida. Tras entrar se consultan solo incidencias autorizadas por la API. Total corresponde a la consulta filtrada autorizada, no a un total global. Paginación de 20. Filtros: ID/título, estado, prioridad, categoría, responsable y fechas de creación UTC. El rango se valida antes de enviar. Categorías/directorio mínimo provienen de /incidents/options.

Abrir un título para consultar descripción, ámbito, prioridad, acceso, validación, responsable (ID), resolución y eventos. Historial paginado por API; se muestran acciones/fechas y motivo cuando está permitido. No se exponen copias completas de detalle de auditoría en esta vista. La ausencia de acción de creación en pantalla no afecta las rutas API existentes. IA pendiente/omitida/fallida se comunica como estado; no se invoca IA desde el frontend.

El token vive solo en memoria de la instancia de cliente. No localStorage, sessionStorage, URL ni cookies. Recargar la página exige nuevo login. Logout intenta revocar en API y limpia identidad/detalle/listados inmediatamente; si no se confirma servidor se informa que puede seguir vigente hasta expiración. 401/403 de la sesión retiran datos y vuelven a login. Una respuesta tardía de una sesión anterior no elimina la nueva. Fetch con cache no-store, AbortController y comprobación de respuesta vigente evitan recuperar listas anteriores tras navegar. Ante 404 del historial se retira el detalle; nunca se sustituyen controles API con botones. No se usan HTML del usuario ni renderizado sin escape.

Accesibilidad básica: campos etiquetados, formularios con teclado, foco visible, mensajes de error alert/carga status y tablas con encabezados; estilos adaptables a móvil. No se declara auditoría WCAG ni revisión visual exhaustiva. La vista de detalle interna no implementa enlaces profundos persistentes todavía.

## Verificación realizada

- npm test: 9 pruebas en 2 archivos aprobadas, 17.97s. UI en jsdom con fetch simulado; no acredita login real, navegador completo ni matriz de permisos del servidor.
- npm run build: compilación correcta con Vite 8.3.4 (17 módulos, 442ms en ejecución final).
- HTTP real: / en puerto 5173 devuelve 200 y /api/health devuelve status=ok/service=plurione-api a través del proxy.
- Instalación: npm reportó 0 vulnerabilidades en 94 paquetes al instalar; no sustituye una auditoría futura.
- CI frontend preparado con npm ci/test/build; ejecución remota no observada todavía.
- No se ejecutó otra vez el backend: la evidencia previa de 77 aprobadas/3 PostgreSQL omitidas/1 advertencia permanece separada.

Primera instalación encontró error de certificado; se completó con NODE_OPTIONS=--use-system-ca limitado al proceso de instalación, usando certificados del sistema y manteniendo TLS. No se modificó configuración persistente ni se desactivó verificación de certificados. Se conserva lockfile reproducible.

## Verificación manual pendiente

Abrir login, iniciar sesión con Admin RH, comprobar listado, filtrar y abrir un caso. Cerrar sesión y comprobar que no queda información privada; repetir con empleado/supervisor habilitado. Validar visualmente escritorio/móvil y recorrido con API real. No guardar contraseña/token en capturas. Evidencia prevista 58-panel-react-incidencias.png: únicamente área del listado con datos simulados, evitando identidad real y cualquier consola de red. La apertura del navegador por el asistente no acredita estas pruebas.