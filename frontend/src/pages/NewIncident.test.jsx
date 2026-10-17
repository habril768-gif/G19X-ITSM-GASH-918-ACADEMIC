import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, it, expect, vi } from 'vitest';
import NewIncident from './NewIncident.jsx';
import { ApiError } from '../services/api.js';

const employee = { id: 'employee', nombre_completo: 'Empleado Demo', rol: 'EMPLEADO', departamento_id: 'dep' };
const options = {
  affected_employees: [{ id: 'employee', nombre_completo: 'Empleado Demo', rol: 'EMPLEADO' }],
  participants: [{ id: 'employee', nombre_completo: 'Empleado Demo', rol: 'EMPLEADO' }, { id: 'super', nombre_completo: 'Supervisor Demo', rol: 'SUPERVISOR' }],
  departments: [{ id: 'dep', nombre: 'Departamento Demo' }], categories: [],
};
let api;
beforeEach(() => { api = { request: vi.fn(async path => path === '/incidents/options' ? options : { id: 'receipt-id', received: true, can_view: true }) }; });
async function start(user = employee) {
  const onOpen = vi.fn(); const onBack = vi.fn();
  render(<NewIncident api={api} user={user} onOpen={onOpen} onBack={onBack} />);
  await screen.findByLabelText('Título');
  const ui = userEvent.setup();
  await ui.type(screen.getByLabelText('Título'), 'Reporte ficticio');
  await ui.type(screen.getByLabelText('Descripción'), 'Descripción simulada para la prueba.');
  return { ui, onOpen, onBack };
}
function posts() { return api.request.mock.calls.filter(([path, opts]) => path === '/incidents' && opts?.method === 'POST'); }

it('empleado registra sobre sí mismo y acuse abre solo expediente permitido', async () => {
  const { ui, onOpen } = await start();
  expect(screen.queryByRole('combobox', { name: 'Empleado afectado' })).toBeNull();
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  await screen.findByRole('heading', { name: 'Recibimos tu reporte' });
  expect(posts()).toHaveLength(1);
  expect(posts()[0][1].body).toMatchObject({ affected_employee_id: 'employee', scope: 'PERSONA', participants: [] });
  expect(posts()[0][1].body.created_by).toBeUndefined();
  expect(posts()[0][1].body.status).toBeUndefined();
  await ui.click(screen.getByRole('button', { name: 'Consultar expediente' }));
  expect(onOpen).toHaveBeenCalledWith('receipt-id');
});
it('ENTORNO envía departamento sin inventar afectado ni participantes de empleado', async () => {
  const { ui } = await start();
  await ui.selectOptions(screen.getByLabelText('Ámbito'), 'ENTORNO');
  expect(screen.queryByLabelText('Agregar participante')).toBeNull();
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  await screen.findByText('Recibimos tu reporte');
  expect(posts()[0][1].body.reported_department_id).toBe('dep');
  expect(posts()[0][1].body.affected_employee_id).toBeUndefined();
  expect(posts()[0][1].body.participants).toEqual([]);
});
it('acuse confidencial sin acceso no ofrece expediente y exige comprender aviso', async () => {
  const request = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => path === '/incidents' ? Promise.resolve({ id: 'private-reference', received: true, can_view: false }) : request(path, opts));
  const { ui } = await start();
  await ui.click(screen.getByLabelText('Solicitar confidencialidad'));
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  expect(posts()).toHaveLength(0);
  await ui.click(screen.getByLabelText('Comprendo las restricciones de acceso de este reporte'));
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  await screen.findByText('private-reference');
  expect(screen.queryByRole('button', { name: 'Consultar expediente' })).toBeNull();
  expect(screen.queryByText('Reporte ficticio')).toBeNull();
});
it('participante gestor requiere relación y activa aviso preventivo', async () => {
  const { ui } = await start();
  await ui.selectOptions(screen.getByLabelText('Agregar participante'), 'super');
  await ui.click(screen.getByRole('button', { name: 'Agregar' }));
  await ui.type(screen.getByLabelText('Relación de Supervisor Demo'), 'Relación ficticia');
  await ui.click(screen.getByLabelText('Comprendo las restricciones de acceso de este reporte'));
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  await screen.findByText('Recibimos tu reporte');
  expect(posts()[0][1].body.participants).toEqual([{ user_id: 'super', declaration_reason: 'Relación ficticia' }]);
});
it('fallo de red no reenvía automáticamente ni invita a duplicar el reporte', async () => {
  const request = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => path === '/incidents' ? Promise.reject(new ApiError(0, 'Red')) : request(path, opts));
  const { ui } = await start();
  await ui.click(screen.getByRole('button', { name: 'Registrar incidencia' }));
  await screen.findByRole('alert');
  expect(screen.getByText(/Revisa el listado antes de enviar otro/)).toBeTruthy();
  expect(screen.getByRole('button', { name: 'Registrar incidencia' }).disabled).toBe(true);
  expect(posts()).toHaveLength(1);
});
it('gestor elige afectado y una respuesta tardía no permite doble envío', async () => {
  let finish;
  const request = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => path === '/incidents' ? new Promise(resolve => { finish = resolve; }) : request(path, opts));
  const { ui } = await start({ ...employee, id: 'admin', rol: 'ADMIN_RH' });
  await ui.selectOptions(screen.getByLabelText('Empleado afectado'), 'employee');
  await ui.dblClick(screen.getByRole('button', { name: 'Registrar incidencia' }));
  expect(posts()).toHaveLength(1);
  finish({ id: 'once-only', received: true, can_view: true });
  await screen.findByText('once-only');
  expect(posts()[0][1].body.affected_employee_id).toBe('employee');
});
