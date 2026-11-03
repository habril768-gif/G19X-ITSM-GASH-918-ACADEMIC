# Atención de la retroalimentación del corte 4

Revisión recibida el 2 de noviembre de 2026 sobre el commit ec4e6e4.
La referencia de la revisión es orientativa; no es una calificación ni aceptación institucional.
Fecha de entrega fijada por la autora: **5 de noviembre de 2026**.

| Observación | Cambio o comprobación | Estado |
| --- | --- | --- |
| 1. MVP por alcance y espacios normales | Objetivo y funciones al principio; antecedentes en bitácora; README resumido | Publicado en 96fe0d3; evidencia 273 |
| 2. Matriz de aceptación | Prioridad A09, A10 y A14, con registros manuales reales | A09 comprobado en275 y A10 en279; Recorrido A14 acotado comprobado en285 |
| 3. Fecha en el plan | Fecha de entrega y calendario del 2 al 5 de noviembre en MVP y backlog | Documentado por decisión de la autora |
| 4. Commits pequeños y seguidos | Un trabajo por commit; menos de 3 000 líneas cambiadas | Avances del 2 y 3 de noviembre; commits pequeños, sin alterar fechas anteriores |
| 5. Líneas Python legibles | API de incidencias, modelos y CLI de cuenta BI | Formato local274 y CI278 aprobados |

## Comprobaciones del corte

| ID | Criterio | Estado |
| --- | --- | --- |
| 1665 | MVP empieza con objetivo | Publicado en96fe0d3 |
| 1666 | Sin secciones fechadas del 31 de octubre en MVP | Publicado en96fe0d3; reubicadas en bitácora |
| 1667 | Sin «API,10 clientes» en README | Publicado en96fe0d3 |
| 1668 | A09 con al menos un correo negativo y evidencia | Comprobado en275; capturas276 y277 |
| 1669 | A10 con caso confidencial y dos roles | Comprobado en279; capturas280–284 |
| 1670 | A14 con recorrido del manual | Comprobado en285: recorrido de cuatro secciones y aclaraciones del manual; capacitación y aceptación formal no acreditadas |
| 1671 | Backlog con fecha de entrega | 5 de noviembre de 2026, fijada por la autora |
| 1672 | MVP con fecha de entrega | 5 de noviembre de 2026, fijada por la autora |
| 1673 | Commits nuevos en al menos dos días | Actividad real del 2 de noviembre y consolidación del recorrido el 3; comprobar fechas de publicación en Git |
| 1674 | Ningún commit nuevo supera 3 000 líneas | Commit documental 96fe0d3: 2 417 líneas; comprobar cada publicación |
| 1675 | API sin líneas de más de 160 caracteres | Verificado: máximo 151; evidencia 274 |
| 1676 | Modelos sin líneas de más de 160 caracteres | Verificado: máximo 147; evidencia 274 |

## Orden de los recorridos

1. A09: usar cuentas ficticias y comprobar en Mailpit que un destinatario inactivo
   no recibe el aviso. Incluir un control positivo para saber que el correo funciona.
2. A10: consultar un caso confidencial con Empleado y Supervisor, registrando lo
   observado y lo denegado; contrastar que RH independiente puede consultar el caso.
3. A14: seguir las secciones pertinentes del manual de usuario y corregir las diferencias
   reales de etiquetas, acciones o resultados. No contar una lectura del manual como recorrido.

Conservar casos anteriores y evidencias. Registrar fallos o pruebas no ejecutadas
sin marcar las casillas como aprobadas. A01 permanece cerrado en su alcance documentado.
