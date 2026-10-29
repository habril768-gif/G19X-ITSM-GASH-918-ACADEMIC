$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Abre Docker Desktop antes de continuar.' }
Push-Location $projectRoot
try {
    & docker compose -f compose.yaml -f compose.bi.yaml up -d postgres redis
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmaron PostgreSQL/Redis; operación detenida.' }
    & docker compose -f compose.yaml -f compose.bi.yaml build api
    if ($LASTEXITCODE -ne 0) { throw 'No se construyó API; operación detenida.' }
    & docker compose -f compose.yaml -f compose.bi.yaml run --rm --no-deps api python -m alembic upgrade head
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmó migración vigente; conserva los datos y revisa el mensaje.' }
    & docker compose -f compose.yaml -f compose.bi.yaml up -d api
    if ($LASTEXITCODE -ne 0) { throw 'No se confirmó actualización de API; operación detenida.' }
    Write-Host 'Vistas preparadas; conexión local 127.0.0.1:5433 (o BI_POSTGRES_PORT configurado).'
    Write-Host 'Siguiente: docker compose exec api python -m app.manage_reporting_user'
    Write-Host 'No uses la cuenta administradora de PostgreSQL en Power BI. No se crearon datos de demostración.'
}
finally { Pop-Location }
