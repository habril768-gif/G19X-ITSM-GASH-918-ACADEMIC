# Herramientas del proyecto

| Herramienta | Uso | Fuente de configuración |
| --- | --- | --- |
| Git | Historial de cambios verificables | Repositorio y bitácora |
| Docker Desktop y Compose | Entorno local API, PostgreSQL, Redis y workers | Dockerfile, compose.yaml y override BI |
| Python | Backend y pruebas; opcional fuera de contenedores | Dockerfile y requirements |
| Node.js y npm | Panel React y build | package.json y package-lock.json |
| Power BI Desktop | Modelo e informe analítico local | Carpeta powerbi y guía ANALITICA.md |
| PostgreSQL nativo | Ejecución de pruebas en clúster temporal aislado | PRUEBAS_POSTGRESQL.md; no requerido para Compose |

Docker y Power BI ya tienen ejecuciones documentadas en el proyecto; no se consideran pendientes de instalación por el inventario inicial. Esto no certifica la disponibilidad actual de cada herramienta en otra máquina. Sigue el [README](../README.md) para requisitos y el [reporte QA](REPORTE_QA.md) para resultados observados. Los números necesarios para reproducir el entorno se conservan en sus archivos técnicos, no como una cronología en las guías.
