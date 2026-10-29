# Solo lectura: CPU por proceso durante una muestra breve; sin cerrar aplicaciones.
param([ValidateRange(1, 15)][int]$Seconds = 5)
$before = @{}
$unavailable = 0
Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        if ($null -ne $_.CPU) { $before[$_.Id] = [double]$_.CPU }
        else { $unavailable++ }
    } catch { $unavailable++ }
}
$clock = [Diagnostics.Stopwatch]::StartNew()
Start-Sleep -Seconds $Seconds
$after = @(Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        if ($before.ContainsKey($_.Id) -and $null -ne $_.CPU) {
            [pscustomobject]@{ nombre = $_.ProcessName; pid = $_.Id; delta = [double]$_.CPU - $before[$_.Id] }
        }
    } catch { $unavailable++ }
})
$clock.Stop()
$elapsed = $clock.Elapsed.TotalSeconds
$cores = [Environment]::ProcessorCount
$top = @($after | Where-Object { $_.delta -gt 0 } | ForEach-Object {
    [pscustomobject]@{ nombre = $_.nombre; pid = $_.pid;
        cpu_equipo_porcentaje = [Math]::Round(100 * $_.delta / $elapsed / $cores, 2) }
} | Sort-Object cpu_equipo_porcentaje -Descending | Select-Object -First 10)
[pscustomobject]@{
    duracion_s = [Math]::Round($elapsed, 2)
    cpu_logicas = $cores
    procesos_comparados = $after.Count
    lecturas_no_disponibles = $unavailable
    mayores_consumos = $top
    limites = 'Muestra actual posterior a la carga, CPU aproximada normalizada por equipo. Omite procesos nuevos, inaccesibles o terminados. No explica retrospectivamente la corrida ni autoriza cerrar procesos.'
} | ConvertTo-Json -Depth 4
