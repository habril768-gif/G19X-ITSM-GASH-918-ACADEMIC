# Frontend PluriOne

React 0.6.0: departamentos con historial, acceso, cambio de contraseña personal, listado/filtros, registro y gestión de expediente, protección/participantes y administración de cuentas. Guía [FRONTEND.md](../docs/FRONTEND.md).

Desde frontend: npm.cmd ci para instalación; npm.cmd run dev para http://127.0.0.1:5173/. Mantener API/Docker activos y terminal abierta. Verificar npm.cmd test y npm.cmd run build. Sin token persistente ni .env frontend. Esta ampliación no requiere dependencias ni migración nuevas. Departamentos requieren API 0.9.0 y migración 0004; comprobación UI real pendiente. Ver ../docs/DEPARTAMENTOS.md.

React 0.5.0, 17 de octubre de 2026: pantalla de cambio de contraseña para todos los roles, reutilizando /auth/change-password. Confirma nueva credencial, limpia campos y vuelve al login al guardar; resultado incierto retira sesión local sin reenvío. Sin migración ni backend nuevo. RF-1/RF-8 parciales; comprobación real/evidencia 67 y departamentos pendientes. Uso y límites en FRONTEND.md.
