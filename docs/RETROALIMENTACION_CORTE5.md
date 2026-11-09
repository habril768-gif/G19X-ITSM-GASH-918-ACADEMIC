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


### 2026-11-08 — Arranque local y nombre del responsable

La instalación de demostración recibió los archivos de 5381b03. El panel
respondió HTTP 200 y la ruta de salud por el proxy confirmó PostgreSQL.
El esquema de la API incluye assigned_to_name. La captura de la autora
muestra a Admin RH consultando el caso ficticio cerrado «Prueba IA — piso
mojado», con «RH Independiente Demo» en el campo Responsable. El
[registro 292](evidencias/292-corte5-arranque-y-responsable-ui.json) conserva
el resultado y el hash de la captura 293. Quedan las comprobaciones visuales
de conflictos de Departamentos y del alta con IA desactivada.


### 2026-11-08 — Conflicto de nombre en Departamentos

La captura aportada por la autora muestra que, al intentar guardar
«DEMO - PRUEBA 1» como departamento nuevo, el panel de Admin RH mantiene
el formulario y muestra «Ya existe un departamento con ese nombre».
El [registro 292](evidencias/292-corte5-arranque-y-responsable-ui.json)
incorpora el resultado visual y el hash de la captura 294. Queda comprobar
en pantalla el mensaje de un alta ficticia con IA desactivada.


### 2026-11-08 — Primer intento del recorrido de IA

La captura 295 del caso ficticio «QA Corte 5 — IA desactivada» muestra
«Asistencia IA pendiente». Compose resuelve AI_ENABLED como activo en
api. El agente no pudo consultar el contenedor por falta de acceso al
motor de Docker. El [registro 292](evidencias/292-corte5-arranque-y-responsable-ui.json)
conserva la captura y su hash. La demostración del mensaje de IA desactivada
requiere iniciar la API con AI_ENABLED=false y registrar un caso nuevo.


### 2026-11-08 — Cierre del recorrido local del corte 5

La salida de PowerShell aportada por la autora muestra plurione-api-1
Healthy y enabled() igual a False después de iniciar la API con
AI_ENABLED=false para la prueba. En el segundo caso ficticio, de Entorno
de trabajo, Seguimiento muestra «Asistencia IA no configurada.
Clasificación manual.». La captura 296 documenta el resultado. El estado
del expediente es Pendiente, como corresponde a un alta sin clasificar.

El [registro 292](evidencias/292-corte5-arranque-y-responsable-ui.json)
reúne la comprobación de arranque y proxy, el nombre del responsable
como Admin RH, el aviso de departamento duplicado y el recorrido de IA
desactivada. Se conservaron las capturas 293 a 296 con sus hashes, incluido
el primer intento con IA pendiente. La demostración local de estos cambios
quedó completada. La evaluación final institucional sigue pendiente.
