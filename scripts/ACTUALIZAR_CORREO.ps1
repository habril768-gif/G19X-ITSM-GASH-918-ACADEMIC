$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Abre Docker Desktop antes de continuar.' }
Push-Location $projectRoot
try {
    & docker compose --profile mail up -d postgres redis mailpit
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmaron los servicios de captura; operación detenida.' }
    & docker compose --profile mail build api mail-worker
    if ($LASTEXITCODE -ne 0) { throw 'No se construyeron las imágenes; operación detenida.' }
    & docker compose --profile mail run --rm --no-deps api python -m alembic upgrade head
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmó la migración vigente; operación detenida. Conserva los datos y revisa el mensaje.' }
    & docker compose --profile mail up -d api mail-worker
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmó la actualización; revisa el mensaje y conserva los datos.' }
    Write-Host 'Correo de prueba preparado. Abre http://127.0.0.1:8025 (o MAILPIT_PORT configurado).'
    Write-Host 'Crea una incidencia simulada nueva, revisa el buzón y el seguimiento de correos en RH.'
    Write-Host 'No se enviaron correos reales ni se crearon usuarios o incidencias con este script.'
}
finally { Pop-Location }
