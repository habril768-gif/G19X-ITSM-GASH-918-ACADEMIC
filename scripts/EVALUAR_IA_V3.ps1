param(
    [switch]$Ejecutar
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$evaluationRoot = Join-Path $projectRoot 'docs/evaluacion_ia'
$pythonPath = Join-Path $projectRoot 'backend/.venv/Scripts/python.exe'
$frozenRoot = Join-Path $evaluationRoot 'aceptacion-v3'
$manifestPath = Join-Path $frozenRoot 'manifest.json'

if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    if ($Ejecutar) { throw 'Falta fijar aceptacion-v3 tras revision. No se hicieron llamadas.' }
    $frozenRoot = Join-Path $evaluationRoot 'candidato-v3'
    $manifestPath = Join-Path $frozenRoot 'manifest.json'
}
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw 'Falta el conjunto v3. No se hicieron llamadas.'
}
if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw 'Falta el entorno Python de backend. Revisa la instalacion; no se hicieron llamadas.'
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($manifest.prompt_version -ne 'plurione-classify-v3') { throw 'Version de prompt distinta. No se hicieron llamadas.' }
if ($Ejecutar -and ($manifest.labels_frozen -ne $true -or $manifest.author_conformity.reported -ne $true)) {
    throw 'La version v3 no esta fijada con conformidad registrada. No se hicieron llamadas.'
}

Push-Location (Join-Path $projectRoot 'backend')
try {
    & $pythonPath -m app.ai.run_evaluation --dataset $frozenRoot
    if ($LASTEXITCODE -ne 0) { throw 'No paso la validacion de archivos. No se hicieron llamadas.' }
}
finally { Pop-Location }

if (-not $Ejecutar) {
    if ($manifest.labels_frozen -eq $true -and $manifest.author_conformity.reported -eq $true) {
        Write-Host 'Comprobacion terminada sin llamadas. Para evaluar, agrega -Ejecutar; puede generar cargos.'
    }
    else {
        Write-Host 'Borrador verificado sin llamadas. Falta registrar revision y fijar etiquetas antes de ejecutar.'
    }
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
    & docker compose --profile ai run --rm --no-deps --volume $mount ai-worker python -m app.ai.run_evaluation --dataset /evaluation/aceptacion-v3 --output /evaluation/ejecucion-v3 --max-calls 55 --execute --confirm-reviewed-simulated
    $evaluationExit = $LASTEXITCODE
    if ($evaluationExit -ne 0) {
        throw 'Evaluacion incompleta. Conserva ejecucion-v3 y comparte el mensaje final; no borres el diario ni cambies de carpeta.'
    }
    Write-Host 'Ejecucion registrada. Resultados en docs/evaluacion_ia/ejecucion-v3/reporte.json.'
    Write-Host 'Completar llamadas no equivale a alcanzar las metas ni a aceptar calidad.'
    Write-Host 'Revisa aciertos por prioridad, errores Media/Baja y pares en reporte.json.'
}
finally { Pop-Location }
