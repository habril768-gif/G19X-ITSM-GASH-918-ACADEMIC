"""CPU del generador y CPU global Windows por fase; sin procesos ajenos ni secretos."""
import os
import time


def host_counters():
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        idle, kernel, user = wintypes.FILETIME(), wintypes.FILETIME(), wintypes.FILETIME()
        if not ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            return None
        def value(row): return (row.dwHighDateTime << 32) | row.dwLowDateTime
        return value(idle), value(kernel) + value(user)
    except (AttributeError, OSError):
        return None


def stamp():
    return {"wall": time.perf_counter(), "process": time.process_time(), "host": host_counters()}


def summarize(before, after):
    elapsed = after["wall"] - before["wall"]
    if elapsed <= 0:
        return {"estado": "INTERVALO_INVALIDO"}
    process = max(0, after["process"] - before["process"])
    cpus = os.cpu_count() or 1
    result = {"duracion_s": elapsed, "cpu_logicas": cpus, "generador_cpu_s": process,
        "generador_cpu_porcentaje_un_nucleo": process / elapsed * 100,
        "generador_cpu_porcentaje_equipo": process / elapsed / cpus * 100,
        "host_cpu_porcentaje": None, "host_estado": "NO_DISPONIBLE",
        "limites": "CPU proceso incluye todos sus hilos; no Docker. Host incluye otras aplicaciones/VM. Medias de fase, no picos ni causa única; GetSystemTimes Windows."}
    if before["host"] is not None and after["host"] is not None:
        idle = after["host"][0] - before["host"][0]
        total = after["host"][1] - before["host"][1]
        if total > 0 and 0 <= idle <= total:
            result["host_cpu_porcentaje"] = 100 * (total - idle) / total
            result["host_estado"] = "OK"
    return result


def baseline():
    """Tres intervalos de CPU global, sin crear carga ni consultar procesos."""
    rows = []
    before = stamp()
    for _ in range(3):
        time.sleep(2)
        after = stamp()
        measured = summarize(before, after)
        rows.append({"duracion_s": measured.get("duracion_s"),
            "cpu_global_porcentaje": measured.get("host_cpu_porcentaje"),
            "estado": measured.get("host_estado", measured.get("estado"))})
        before = after
    valid = [r for r in rows if r["estado"] == "OK" and r["cpu_global_porcentaje"] is not None
             and r["duracion_s"] is not None and r["duracion_s"] > 0]
    duration = sum(r["duracion_s"] for r in valid)
    return {"modo": "CPU_GLOBAL_SIN_CARGA_GENERADA", "intervalos": rows,
        "intervalos_validos": len(valid), "intervalos_totales": len(rows),
        "media_cpu_global_porcentaje": sum(r["cpu_global_porcentaje"] * r["duracion_s"] for r in valid) / duration if duration else None,
        "limites": "Muestra actual de CPU global Windows; otras aplicaciones pueden estar activas. No identifica procesos, no recrea la corrida previa ni acredita RNF-2. No disponible se conserva como null."}


def main(argv=None):
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Comprobación de solo lectura de CPU global, unos seis segundos.")
    parser.add_argument('--baseline', action='store_true', required=True)
    parser.parse_args(argv)
    print(json.dumps(baseline(), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
