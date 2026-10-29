param(
    [switch]$Ejecutar
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$evaluationRoot = Join-Path $projectRoot 'docs/evaluacion_ia'
$pythonPath = Join-Path $projectRoot 'backend/.venv/Scripts/python.exe'
$frozenRoot = Join-Path $evaluationRoot 'aceptacion-v2'
$manifestPath = Join-Path $frozenRoot 'manifest.json'

if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw 'Falta la version de aceptacion-v2. No se hicieron llamadas.'
}
if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw 'Falta el entorno Python de backend. Revisa la instalacion; no se hicieron llamadas.'
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.labels_frozen -ne $true -or $manifest.author_conformity.reported -ne $true -or $manifest.prompt_version -ne 'plurione-classify-v2') {
    throw 'La version v2 no esta fijada con conformidad registrada. No se hicieron llamadas.'
}

Push-Location (Join-Path $projectRoot 'backend')
try {
    & $pythonPath -m app.ai.run_evaluation --dataset $frozenRoot
    if ($LASTEXITCODE -ne 0) { throw 'No paso la validacion de archivos. No se hicieron llamadas.' }
}
finally { Pop-Location }

if (-not $Ejecutar) {
    Write-Host 'Comprobacion terminada sin llamadas. Para evaluar, agrega -Ejecutar; puede generar cargos.'
    return
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker no esta disponible. Abre Docker Desktop y revisa su instalacion.'
}
Push-Location $projectRoot
try {
    & docker compose --profile ai build ai-worker
    if ($LASTEXITCODE -ne 0) { throw 'No se construyo la imagen; no se inicio la evaluacion.' }

    Write-Host 'Evaluacion externa: hasta 55 intentos acumulados. Puede generar cargos.'
    $mount = $evaluationRoot + ':/evaluation'
    & docker compose --profile ai run --rm --no-deps --volume $mount ai-worker python -m app.ai.run_evaluation --dataset /evaluation/aceptacion-v2 --output /evaluation/ejecucion-v2 --max-calls 55 --execute --confirm-reviewed-simulated
    $evaluationExit = $LASTEXITCODE
    if ($evaluationExit -ne 0) {
        throw 'Evaluacion incompleta. Conserva ejecucion-v2 y comparte el mensaje final; no borres el diario ni cambies de carpeta.'
    }
    Write-Host 'Ejecucion registrada. Resultados en docs/evaluacion_ia/ejecucion-v2/reporte.json.'
    Write-Host 'Completar llamadas no equivale a alcanzar las metas ni a aceptar calidad.'
}
finally { Pop-Location }
