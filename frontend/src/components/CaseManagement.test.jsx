import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, it, expect, vi } from 'vitest';
import CaseManagement from './CaseManagement.jsx';
import { ApiError } from '../services/api.js';

const admin = { id: 'admin', rol: 'ADMIN_RH' };
const initial = { id: 'case', status: 'PENDIENTE', scope: 'PERSONA', titulo: 'Simulado', descripcion: 'Texto ficticio',
  affected_employee_id: 'employee', reported_department_id: 'dep', category_id: 2, priority: 2, classification_valid: true, assigned_to: 'super', is_confidential: false };
const catalog = {
  categories: [{ id: 2, nombre: 'Conflictos' }, { id: 4, nombre: 'Riesgos' }],
  affected_employees: [{ id: 'employee', departamento_id: 'dep' }],
  participants: [{ id: 'super', nombre_completo: 'Supervisor Demo', rol: 'SUPERVISOR', departamento_id: 'dep' },
    { id: 'admin', nombre_completo: 'RH Demo', rol: 'ADMIN_RH', departamento_id: 'rh' },
    { id: 'other', nombre_completo: 'Supervisor Otro', rol: 'SUPERVISOR', departamento_id: 'other-dep' }],
};
let api, updated, lost;
beforeEach(() => {
  api = { request: vi.fn(async path => path === '/incidents/options' ? catalog : path.endsWith('/participants') ? { items: [] } : initial) };
  updated = vi.fn(); lost = vi.fn();
});
async function start(changes = {}, user = admin) {
  render(<CaseManagement data={{ ...initial, ...changes }} user={user} api={api} onUpdated={updated} onAccessLost={lost} />);
  await screen.findByRole('form', { name: changes.status === 'CERRADA' ? 'Cambiar estado' : 'Clasificación humana' });
  return userEvent.setup();
}
function writes() { return api.request.mock.calls.filter(([, opts]) => opts?.body); }

it('empleado no recibe controles ni descarga directorio de gestión', () => {
  render(<CaseManagement data={initial} user={{ rol: 'EMPLEADO' }} api={api} onUpdated={updated} onAccessLost={lost} />);
  expect(screen.queryByText('Gestionar incidencia')).toBeNull();
  expect(api.request).not.toHaveBeenCalled();
});
it('confirma clasificación y exige validación para iniciar revisión', async () => {
  const ui = await start({ classification_valid: false });
  expect(screen.getByRole('button', { name: 'Iniciar revisión' }).disabled).toBe(true);
  await ui.selectOptions(screen.getByLabelText('Prioridad oficial'), '1');
  await ui.click(screen.getByRole('button', { name: 'Confirmar clasificación' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0]).toEqual(['/incidents/case/classification', { method: 'PUT', body: { category_id: 2, priority: 1 } }]);
});
it('asigna y empieza revisión solo con candidatos del caso', async () => {
  const ui = await start();
  expect(within(screen.getByLabelText('Responsable del caso')).queryByRole('option', { name: /Supervisor Otro/ })).toBeNull();
  await ui.selectOptions(screen.getByLabelText('Responsable del caso'), 'admin');
  await ui.click(screen.getByRole('button', { name: 'Guardar responsable' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0][1].body).toEqual({ assigned_to: 'admin' });
  await ui.click(screen.getByRole('button', { name: 'Iniciar revisión' }));
  await waitFor(() => expect(writes()).toHaveLength(2));
  expect(writes()[1][1]).toEqual({ method: 'POST', body: { status: 'EN_REVISION', assigned_to: 'admin' } });
});
it('caso confidencial excluye supervisores y gestores involucrados', async () => {
  const original = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => path.endsWith('/participants') ? Promise.resolve({ items: [{ user_id: 'admin', review_status: 'CONFIRMADO' }] }) : original(path, opts));
  await start({ is_confidential: true });
  expect(within(screen.getByLabelText('Responsable del caso')).queryByRole('option', { name: /Supervisor Demo/ })).toBeNull();
  expect(within(screen.getByLabelText('Responsable del caso')).queryByRole('option', { name: /RH Demo/ })).toBeNull();
});
it('ENTORNO solo permite categoría Riesgos', async () => {
  await start({ scope: 'ENTORNO', affected_employee_id: null, category_id: 4 });
  expect(within(screen.getByLabelText('Categoría oficial')).queryByText('Conflictos')).toBeNull();
});
it('resuelve con texto y conserva decisión oficial en servidor', async () => {
  const ui = await start({ status: 'EN_REVISION' });
  await ui.type(screen.getByLabelText('Resolución del caso'), 'Acción simulada');
  await ui.click(screen.getByRole('button', { name: 'Registrar resolución' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0][1]).toEqual({ method: 'POST', body: { status: 'RESUELTA', resolution_text: 'Acción simulada' } });
});
it('admin confirma cierre y supervisor no puede cerrar ni reabrir', async () => {
  const view = render(<CaseManagement data={{ ...initial, status: 'RESUELTA' }} user={admin} api={api} onUpdated={updated} onAccessLost={lost} />);
  const ui = userEvent.setup();
  await screen.findByRole('form', { name: 'Cerrar caso' });
  await ui.click(screen.getByRole('button', { name: 'Cerrar caso' }));
  expect(writes()).toHaveLength(0);
  await ui.click(screen.getByLabelText('Confirmo el cierre del caso con la resolución registrada'));
  await ui.click(screen.getByRole('button', { name: 'Cerrar caso' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0][1].body).toEqual({ status: 'CERRADA' });
  view.unmount();
  render(<CaseManagement data={{ ...initial, status: 'RESUELTA' }} user={{ rol: 'SUPERVISOR' }} api={api} onUpdated={updated} onAccessLost={lost} />);
  await screen.findByText('Solo Admin RH independiente puede cerrar o reabrir este caso.');
  expect(screen.queryByRole('button', { name: 'Cerrar caso' })).toBeNull();
  expect(screen.queryByRole('button', { name: 'Reabrir con motivo' })).toBeNull();
});
it('reabre con motivo y responsable aun si debe revalidarse después', async () => {
  const ui = await start({ status: 'CERRADA', classification_valid: false });
  await ui.type(screen.getByLabelText('Motivo de reapertura'), 'Información adicional ficticia');
  await ui.selectOptions(screen.getByLabelText('Responsable para revisión'), 'admin');
  await ui.click(screen.getByRole('button', { name: 'Reabrir con motivo' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0][1].body).toEqual({ status: 'EN_REVISION', assigned_to: 'admin', reason: 'Información adicional ficticia' });
});
it('edita contenido y solicita refrescar vigencia', async () => {
  const ui = await start();
  await ui.click(screen.getByText('Editar título y descripción'));
  await ui.clear(screen.getByLabelText('Descripción del caso'));
  await ui.type(screen.getByLabelText('Descripción del caso'), 'Descripción corregida simulada');
  await ui.click(screen.getByRole('button', { name: 'Guardar contenido' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(writes()[0][1].body.descripcion).toBe('Descripción corregida simulada');
});
it('rechazo 404 retira expediente, y fallo incierto no reintenta solo', async () => {
  const original = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => opts?.body ? Promise.reject(new ApiError(404, 'Sin acceso')) : original(path, opts));
  const ui = await start();
  await ui.click(screen.getByRole('button', { name: 'Confirmar clasificación' }));
  await waitFor(() => expect(lost).toHaveBeenCalledWith('Sin acceso'));
  api.request.mockImplementation((path, opts) => opts?.body ? Promise.reject(new ApiError(0, 'Red')) : original(path, opts));
  await ui.click(screen.getByRole('button', { name: 'Confirmar clasificación' }));
  await screen.findByText(/Actualiza el expediente antes de repetir/);
  expect(screen.getByRole('group', { name: 'Acciones disponibles' }).disabled).toBe(true);
  expect(writes()).toHaveLength(2);
});
