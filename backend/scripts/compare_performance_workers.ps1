param([switch]$ConfirmIsolatedQA)
$ErrorActionPreference = 'Stop'
if (-not $ConfirmIsolatedQA) { throw 'Confirma el QA aislado con -ConfirmIsolatedQA. No hubo cambios.' }
$comparisonRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$comparisonPython = Join-Path $comparisonRoot 'backend\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $comparisonPython -PathType Leaf)) { throw 'No se encontró Python del proyecto.' }
Push-Location $comparisonRoot
try {
    foreach ($workerCount in @(1, 2)) {
        Write-Host "Comparación breve: $workerCount proceso(s) API. Se conservan diez clientes y cien casos iniciales nuevos."
        $networkOutput = & $comparisonPython -B backend/scripts/release_performance_networks.py --apply --limit 2
        $networkExit = $LASTEXITCODE
        Write-Output $networkOutput
        if ($networkExit -ne 0) { throw 'Falló la revisión de redes QA; comparación detenida.' }
        $networkState = $networkOutput | ConvertFrom-Json
        if (@($networkState.eliminadas).Count -ne 2 -or @($networkState.fallidas).Count -ne 0 -or @($networkState.omitidas_al_revalidar).Count -ne 0) {
            throw 'No se liberaron exactamente dos redes QA sin fallos/omisiones; comparación detenida.'
        }
        & $comparisonPython -B backend/scripts/provision_performance_qa.py --mode smoke --api-workers $workerCount --confirm-isolated-qa
        if ($LASTEXITCODE -ne 0) { throw 'Una prueba quedó incompleta; no se continúa ni se reintenta automáticamente.' }
    }
    Write-Host 'Dos reportes de smoke terminados. Comparar p95, errores, CPU y auditoría antes de decidir. Esto no acredita RNF-2.'
}
finally { Pop-Location }
