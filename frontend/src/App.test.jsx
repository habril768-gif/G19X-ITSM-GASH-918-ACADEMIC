import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, it, expect, vi } from 'vitest';
import App from './App.jsx';

const user = { id: 'test-user', nombre_completo: 'Persona Demo', rol: 'ADMIN_RH' };
const incident = { id: 'test-case', titulo: 'Caso simulado visible', status: 'PENDIENTE', priority: null, created_at: '2026-10-17T12:00:00Z', is_confidential: false };
const ok = data => ({ ok: true, status: 200, json: async () => data });
beforeEach(() => {
  global.fetch = vi.fn(async url => {
    if (url.endsWith('/auth/login')) return ok({ access_token: 'memory-test-token' });
    if (url.endsWith('/auth/me')) return ok(user);
    if (url.endsWith('/auth/logout')) return { ok: true, status: 204 };
    if (url.endsWith('/ai')) return ok({ enabled: false, eligible: true, ai_status: 'PENDIENTE', job: null });
    if (url.endsWith('/participants')) return ok({ items: [] });
    if (url.endsWith('/incidents/options')) return ok({ categories: [], participants: [], departments: [] });
    if (url.includes('/history?')) return ok({ items: [{ id: 'e', accion: 'CREADO', fecha: incident.created_at }], total: 1 });
    if (url.endsWith('/incidents/test-case')) return ok({ ...incident, descripcion: 'Descripción ficticia', scope: 'PERSONA', ai_status: 'OMITIDA', classification_valid: false });
    return ok({ items: [incident], total: 1 });
  });
});
async function login() {
  const ui = userEvent.setup();
  await ui.type(screen.getByLabelText('Correo electrónico'), 'demo@example.invalid');
  await ui.type(screen.getByLabelText('Contraseña'), 'Ficticia-123456');
  await ui.click(screen.getByRole('button', { name: /Entrar a PluriOne/ }));
  await screen.findByRole('button', { name: incident.titulo });
  return ui;
}
it('inicio de sesión, consulta del detalle y logout retiran datos privados', async () => {
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: incident.titulo }));
  await screen.findByText('Descripción ficticia', { selector: 'p' });
  await screen.findByText('CREADO');
  expect(screen.getByText(/Asistencia IA omitida/)).toBeTruthy();
  await ui.click(screen.getByRole('button', { name: 'Cerrar sesión' }));
  await screen.findByRole('heading', { name: 'Inicia sesión' });
  expect(screen.queryByText('Descripción ficticia', { selector: 'p' })).toBeNull();
  expect(localStorage.length).toBe(0); expect(sessionStorage.length).toBe(0);
});
it('un 401 durante filtrado limpia datos y regresa al login', async () => {
  render(<App />); const ui = await login();
  const original = fetch.getMockImplementation();
  fetch.mockImplementation((url, opts) => url.includes('q=expire') ? Promise.resolve({ ok: false, status: 401 }) : original(url, opts));
  await ui.type(screen.getByLabelText('Buscar por título o ID'), 'expire');
  await ui.click(screen.getByRole('button', { name: 'Aplicar filtros' }));
  await screen.findByRole('heading', { name: 'Inicia sesión' });
  expect(screen.queryByText(incident.titulo)).toBeNull();
});
it('muestra vacío cuando API no devuelve casos y no inventa resultados', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation((url, opts) => url.includes('/incidents?') ? Promise.resolve(ok({ items: [], total: 0 })) : original(url, opts));
  render(<App />);
  const ui = userEvent.setup();
  await ui.type(screen.getByLabelText('Correo electrónico'), 'demo@example.invalid');
  await ui.type(screen.getByLabelText('Contraseña'), 'Ficticia-123456');
  await ui.click(screen.getByRole('button', { name: /Entrar a PluriOne/ }));
  await screen.findByText('No hay casos en esta consulta');
  expect(screen.getByText('0')).toBeTruthy();
});
it('consulta paginación y filtros en servidor', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation((url, opts) => url.includes('/incidents?') ? Promise.resolve(ok({ items: [incident], total: 21 })) : original(url, opts));
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: 'Siguiente →' }));
  await waitFor(() => expect(fetch.mock.calls.some(([url]) => url.includes('page=2'))).toBe(true));
  await screen.findByText('Página 2 de 2');
  await ui.selectOptions(screen.getByLabelText('Estado'), 'EN_REVISION');
  await ui.click(screen.getByRole('button', { name: 'Aplicar filtros' }));
  await waitFor(() => expect(fetch.mock.calls.some(([url]) => url.includes('page=1') && url.includes('status=EN_REVISION'))).toBe(true));
});

it('retira el detalle si pierde acceso al consultar otra página del historial', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation((url, opts) => url.includes('/history?page=2') ? Promise.resolve({ ok: false, status: 404 })
    : url.includes('/history?') ? Promise.resolve(ok({ items: [{ id: 'e', accion: 'CREADO', fecha: incident.created_at }], total: 21 })) : original(url, opts));
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: incident.titulo }));
  await screen.findByText('Descripción ficticia', { selector: 'p' });
  await screen.findByText('CREADO');
  await ui.click(screen.getByRole('button', { name: 'Siguiente' }));
  await screen.findByRole('alert');
  await waitFor(() => expect(screen.queryByText('Descripción ficticia', { selector: 'p' })).toBeNull());
});

it('retira la sesión y el directorio al modificar los permisos propios', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, opts) => {
    if (url.endsWith('/users/options')) return ok({ departments: [{ id: 'd', nombre: 'Demo' }], roles: [{ id: 1, nombre: 'ADMIN_RH' }, { id: 3, nombre: 'EMPLEADO' }] });
    if (url.includes('/users?')) return ok({ items: [{ ...user, email: 'demo@example.invalid', departamento_id: 'd', rol_id: 1, is_active: true }], total: 1 });
    if (url.endsWith('/users/test-user')) return ok({ id: user.id, updated: true, sessions_revoked: true, cases_adjusted: 0 });
    return original(url, opts);
  });
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: /Usuarios/ }));
  await ui.click(await screen.findByRole('button', { name: 'Editar Persona Demo' }));
  await ui.selectOptions(screen.getByLabelText('Rol del usuario'), '3');
  await ui.type(screen.getByLabelText('Motivo administrativo'), 'Cambio simulado de permisos');
  const reads = fetch.mock.calls.filter(([url]) => url.includes('/users?')).length;
  await ui.click(screen.getByRole('button', { name: 'Guardar usuario' }));
  await screen.findByRole('heading', { name: 'Inicia sesión' });
  expect(screen.queryByRole('table')).toBeNull();
  expect(screen.getByText(/Cambiaste los permisos de tu cuenta/)).toBeTruthy();
  expect(fetch.mock.calls.filter(([url]) => url.includes('/users?')).length).toBe(reads);
});

it('retira expediente e historial cuando declarar participante elimina acceso', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, opts) => {
    if (url.endsWith('/incidents/options')) return ok({ categories: [], affected_employees: [], departments: [], participants: [{ ...user, departamento_id: 'd' }] });
    if (url.endsWith('/participants')) return opts?.method === 'POST' ? ok({ id: incident.id, received: true, can_view: false }) : ok({ items: [] });
    return original(url, opts);
  });
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: incident.titulo }));
  await ui.selectOptions(await screen.findByLabelText('Nuevo participante'), user.id);
  await ui.type(screen.getByLabelText('Relación con el hecho'), 'Participación simulada propia');
  await ui.click(screen.getByRole('button', { name: 'Declarar participante' }));
  await screen.findByText(/Tu cuenta ya no puede consultar este expediente/);
  expect(screen.queryByText('Descripción ficticia', { selector: 'p' })).toBeNull();
  expect(screen.queryByRole('heading', { name: 'Historial del caso' })).toBeNull();
  expect(screen.queryByLabelText('Nuevo participante')).toBeNull();
});

it.each(['ADMIN_RH', 'SUPERVISOR', 'EMPLEADO'])('permite cambiar contraseña a %s y vuelve al login sin datos privados', async rol => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, opts) => {
    if (url.endsWith('/auth/me')) return ok({ ...user, rol });
    if (url.endsWith('/auth/change-password')) return { ok: true, status: 204 };
    return original(url, opts);
  });
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: 'Cambiar contraseña' }));
  await ui.type(screen.getByLabelText('Contraseña actual'), 'Actual-simulada-123');
  await ui.type(screen.getByLabelText('Nueva contraseña'), 'Nueva-simulada-123');
  await ui.type(screen.getByLabelText('Confirmar nueva contraseña'), 'Nueva-simulada-123');
  await ui.click(screen.getByRole('button', { name: 'Guardar nueva contraseña' }));
  await screen.findByRole('heading', { name: 'Inicia sesión' });
  expect(screen.getByText(/Contraseña actualizada/)).toBeTruthy();
  expect(screen.queryByText(incident.titulo)).toBeNull();
  expect(screen.getByLabelText('Contraseña').value).toBe('');
  expect(localStorage.length).toBe(0); expect(sessionStorage.length).toBe(0);
});

it('navega de incidencias al catálogo de departamentos y vuelve sin mezclar vistas', async () => {
  const original = fetch.getMockImplementation();
  fetch.mockImplementation((url, opts) => url.includes('/departments?') ? Promise.resolve(ok({ items: [{ id: 'd', nombre: 'Departamento UI simulado', is_active: true }], total: 1 })) : original(url, opts));
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: /Departamentos/ }));
  await screen.findByText('Departamento UI simulado');
  expect(screen.queryByText(incident.titulo)).toBeNull();
  await ui.click(screen.getByRole('button', { name: /Incidencias/ }));
  await screen.findByRole('button', { name: incident.titulo });
  expect(screen.queryByText('Departamento UI simulado')).toBeNull();
});

it('solicita IA y muestra sugerencia sin sustituir la clasificación humana', async () => {
  let queued = false, completed = false;
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, opts) => {
    if (url.endsWith('/incidents/options')) return ok({ categories: [{ id: 2, nombre: 'Conflictos' }], participants: [], affected_employees: [], departments: [] });
    if (url.endsWith('/ai')) {
      if (opts.method === 'POST') { queued = true; return ok({ received: true, queue_available: true }); }
      return ok({ enabled: true, eligible: true, job: queued ? { status: completed ? 'COMPLETADA' : 'PENDIENTE', attempts: 1, current: true } : null,
        suggestion: completed ? { result: 'CLASIFICADA', category_id: 2, priority: 1, suggestion: 'Sugerencia ficticia de IA.', reason: 'Prueba simulada.' } : null });
    }
    return original(url, opts);
  });
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: incident.titulo }));
  await ui.type(await screen.findByLabelText('Texto simulado para la IA'), 'Desacuerdo ficticio sobre una tarea.');
  await ui.click(screen.getByLabelText('Confirmo que el texto es completamente simulado'));
  await ui.click(screen.getByLabelText('Revisé que no contiene identificadores personales'));
  await ui.click(screen.getByRole('button', { name: 'Confirmar texto y solicitar IA' }));
  await screen.findByText(/Solicitud IA registrada/);
  completed = true;
  await ui.click(await screen.findByRole('button', { name: 'Actualizar asistencia IA' }));
  await screen.findByText('Sugerencia ficticia de IA.');
  expect(screen.getByLabelText('Categoría oficial').value).toBe('');
  expect(screen.getByLabelText('Prioridad oficial').value).toBe('');
}, 15000);

it('gestiona un ciclo completo y recarga detalle e historial después de cada cambio', async () => {
  const state = { ...incident, descripcion: 'Caso ficticio', scope: 'PERSONA', affected_employee_id: 'e', ai_status: 'PENDIENTE', classification_valid: false, assigned_to: null };
  const events = [];
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, opts) => {
    if (url.endsWith('/incidents/options')) return ok({ categories: [{ id: 2, nombre: 'Conflictos' }], affected_employees: [{ id: 'e', departamento_id: 'd' }], participants: [{ id: 'admin', nombre_completo: 'RH Demo', rol: 'ADMIN_RH', departamento_id: 'd' }] });
    if (url.endsWith('/participants')) return ok({ items: [] });
    if (url.includes('/history?')) return ok({ items: [...events], total: events.length });
    if (url.endsWith('/classification') || url.endsWith('/transitions')) {
      const body = JSON.parse(opts.body);
      if (url.endsWith('/classification')) Object.assign(state, body, { classification_valid: true });
      else Object.assign(state, body);
      events.unshift({ id: String(events.length + 1), accion: body.reason ? 'REAPERTURA' : 'ACTUALIZADO', fecha: incident.created_at });
      return ok({ ...state });
    }
    if (url.endsWith('/incidents/test-case')) return ok({ ...state });
    return original(url, opts);
  });
  render(<App />); const ui = await login();
  await ui.click(screen.getByRole('button', { name: incident.titulo }));
  await screen.findByLabelText('Categoría oficial');
  await ui.selectOptions(screen.getByLabelText('Categoría oficial'), '2');
  await ui.selectOptions(screen.getByLabelText('Prioridad oficial'), '2');
  await ui.click(screen.getByRole('button', { name: 'Confirmar clasificación' }));
  await waitFor(() => expect(screen.getByRole('button', { name: 'Iniciar revisión' }).disabled).toBe(false));
  await ui.selectOptions(screen.getByLabelText('Responsable para revisión'), 'admin');
  await ui.click(screen.getByRole('button', { name: 'Iniciar revisión' }));
  await screen.findByLabelText('Resolución del caso');
  await ui.type(screen.getByLabelText('Resolución del caso'), 'Resolución simulada');
  await ui.click(screen.getByRole('button', { name: 'Registrar resolución' }));
  await screen.findByLabelText('Confirmo el cierre del caso con la resolución registrada');
  await ui.click(screen.getByLabelText('Confirmo el cierre del caso con la resolución registrada'));
  await ui.click(screen.getByRole('button', { name: 'Cerrar caso' }));
  await screen.findByText('Caso cerrado.');
  await screen.findByLabelText('Motivo de reapertura');
  await ui.type(screen.getByLabelText('Motivo de reapertura'), 'Nueva información ficticia');
  await ui.click(screen.getByRole('button', { name: 'Reabrir con motivo' }));
  await screen.findByText('REAPERTURA');
  await screen.findByLabelText('Resolución del caso');
  expect(fetch.mock.calls.filter(([url]) => url.endsWith('/transitions')).map(([, opts]) => JSON.parse(opts.body).status)).toEqual(['EN_REVISION', 'RESUELTA', 'CERRADA', 'EN_REVISION']);
}, 15000);


it('enlace de correo espera login y consulta el UUID con la cuenta autenticada', async () => {
  const id = '12345678-1234-1234-1234-123456789abc';
  window.history.replaceState(null, '', `/?incident=${id}`);
  const original = fetch.getMockImplementation();
  fetch.mockImplementation(async (url, options) => url.endsWith(`/incidents/${id}`)
    ? ok({ ...incident, id, descripcion: 'Expediente desde correo', scope: 'PERSONA', ai_status: 'OMITIDA' }) : original(url, options));
  try {
    render(<App />);
    expect(fetch).not.toHaveBeenCalled();
    const ui = userEvent.setup();
    await ui.type(screen.getByLabelText('Correo electrónico'), 'demo@example.invalid');
    await ui.type(screen.getByLabelText('Contraseña'), 'Ficticia-123456');
    await ui.click(screen.getByRole('button', { name: /Entrar a PluriOne/ }));
    await screen.findByText('Expediente desde correo', { selector: 'p' });
    expect(fetch.mock.calls.some(([url, options]) => url.endsWith(`/incidents/${id}`) && options.headers.Authorization === 'Bearer memory-test-token')).toBe(true);
  } finally { window.history.replaceState(null, '', '/'); }
}, 30000);
