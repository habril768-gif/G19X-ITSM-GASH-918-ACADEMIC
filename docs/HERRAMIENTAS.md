# Herramientas del entorno

Revisión del 15 de octubre de 2026, sin instalar ni modificar herramientas del sistema.

| Herramienta | Estado observado | Acción |
| --- | --- | --- |
| Git | Disponible | Ninguna |
| VS Code | Disponible | Ninguna |
| Python | 3.11.0 | API inicial probada; actualización de mantenimiento recomendable, sin bloquear este avance |
| Node.js | 24.13.1 | Disponible para futuro frontend |
| npm | 11.8.0 | Disponible |
| Docker | No disponible en PATH; autora confirma no instalado | Instalar Docker Desktop con motor Linux/WSL 2 |
| WSL | wsl.exe presente, consulta de estado devuelve acceso denegado en el entorno | Verificar desde PowerShell del equipo; no se puede afirmar que WSL 2 esté habilitado |
| Power BI Desktop | No detectado en rutas habituales; inventario Store bloqueado | Confirmar manualmente antes de instalar; necesario en etapa analítica |

PostgreSQL y Redis se descargarán como imágenes al ejecutar Docker Compose; no requieren instalación nativa. FastAPI y Uvicorn ya están en el entorno virtual. Las dependencias de React y de integración IA se instalarán dentro del proyecto cuando corresponda.

Descargas oficiales:

- https://docs.docker.com/desktop/setup/install/windows-install/
- https://learn.microsoft.com/windows/wsl/install
- https://learn.microsoft.com/power-bi/fundamentals/desktop-get-the-desktop

Después de instalar Docker Desktop y reiniciar si lo solicita, ejecutar docker version y docker compose version. Verificar wsl --version y wsl --status desde PowerShell externo. No se ha comprobado virtualización del hardware en esta revisión.
