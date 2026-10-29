# Panel web de PluriOne

React ofrece acceso, cambio de contraseña, registro, consulta y gestión de expedientes, clasificación humana, participantes, confidencialidad, usuarios, departamentos, asistencia IA y seguimiento de correo según permisos.

## Ejecutar

Inicia primero la API y aplica las migraciones siguiendo la [guía principal](../README.md). Desde `frontend/`:

```powershell
npm.cmd ci
npm.cmd run dev
```

Abre http://127.0.0.1:5173/. Mantén la terminal abierta. El proxy `/api` de `vite.config.js` apunta a http://127.0.0.1:8000; ajústalo si cambias el puerto API. No se necesita `.env` frontend. La sesión se conserva en memoria; recargar exige volver a iniciar sesión.

## Verificar

```powershell
npm.cmd test
npm.cmd run build
```

Las pruebas de componentes usan servicios simulados y no acreditan por sí solas permisos reales o aceptación integral. Consulta [la guía funcional](../docs/FRONTEND.md), [el alcance](../docs/MVP.md) y [QA](../docs/REPORTE_QA.md). El build genera los archivos web; la configuración productiva de su servidor y HTTPS está fuera del arranque local.
