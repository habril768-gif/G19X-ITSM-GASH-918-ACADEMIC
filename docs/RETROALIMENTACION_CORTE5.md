# Atención de la retroalimentación del corte 5

La revisión del 6 de noviembre de 2026 verificó los cambios del corte 4 en
`84d9ad8`, incluido el recorrido A14 de la evidencia 285. La ficha distingue
esa revisión de código de la prueba funcional del 2 de noviembre sobre
`ec4e6e4`. Para esta última, el equipo evaluador reportó instalación desde
un clon limpio, 516 pruebas de backend con PostgreSQL y 71 de frontend
aprobadas, con resultado «con observaciones». La referencia de 8.6 es
orientativa. La calificación final corresponde a la siguiente evaluación.

| Criterios | Corrección del 7 de noviembre | Comprobación |
| --- | --- | --- |
| 2754–2756 | Vite lee `API_PORT` de la raíz con 8000 por omisión. README indica versiones compatibles de Node y el comando de PostgreSQL recupera sus diagonales. | Configuración con puerto alternativo, valor por omisión y rechazo de puerto inválido. Petición HTTP por el proxy con reescritura de `/api`. Compilación del frontend. |
| 2757–2758 | El expediente muestra el nombre del responsable a Admin RH y Supervisor con acceso. Empleado ve «Asignado» cuando corresponde. | Pruebas de renderizado y de visibilidad por rol en la API. |
| 2759–2760 | El cliente conserva el detalle textual de un 409. Departamentos muestra la causa cuando la API la proporciona. | Pruebas de mensaje específico y del respaldo genérico. |
| 2761–2762 | Los casos nuevos con IA desactivada se crean con `OMITIDA` y una indicación de clasificación manual. | Prueba de creación y consulta con `AI_ENABLED=false`. La causa de confidencialidad mantiene prioridad. |
| 2763 | Se corrigieron palabras y cifras pegadas en la introducción y la tabla A01–A14. | Comprobación de las líneas 3 a 26 de la matriz. |

El recorrido A14 registrado en [285](evidencias/285-corte4-a14-recorrido-manual-confirmado.json)
fue verificado por el equipo evaluador el 6 de noviembre. Las capturas
[286](evidencias/286-corte4-a14-refuerzo-visual.json) documentan consultas de
expedientes y administración como respaldo adicional. La evaluación final
y la capacitación se registran por separado.


La compilación y 73 pruebas de frontend pasaron con Node 24.13.1. La suite
local de backend terminó con 496 pruebas aprobadas, 147 subpruebas aprobadas
y 22 integraciones PostgreSQL omitidas en esa ejecución. En la primera
ejecución falló la preparación de la prueba nueva de responsable porque usaba
un ID de texto donde el ORM esperaba UUID. Se corrigió el fixture y se repitió
la suite. El resultado del corte anterior con PostgreSQL pertenece al commit
que probó el equipo evaluador. Esta revisión pasó también el ejecutor aislado con PostgreSQL 18.6.
Se aplicaron las migraciones dos veces y Alembic no detectó cambios
pendientes. Pasaron 518 pruebas y 147 subpruebas, con cero fallos, errores
u omisiones. El ejecutor confirmó el cierre del servidor temporal.
