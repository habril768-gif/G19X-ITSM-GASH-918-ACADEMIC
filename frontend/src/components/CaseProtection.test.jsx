import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, it, expect, vi } from 'vitest';
import CaseProtection from './CaseProtection.jsx';
import { ApiError } from '../services/api.js';
const data = { id: 'case', status: 'EN_REVISION', is_confidential: true, affected_employee_id: 'employee' };
const options = { participants: [{ id: 'super', nombre_completo: 'Supervisor Demo', rol: 'SUPERVISOR' }, { id: 'admin', nombre_completo: 'RH Demo', rol: 'ADMIN_RH' }] };
const relation = { user_id: 'super', review_status: 'DECLARADO', declaration_reason: 'Motivo original simulado', review_reason: null };
let api, updated, lost;
beforeEach(() => { api = { request: vi.fn(async () => ({ id: 'case', received: true, can_view: true })) }; updated = vi.fn(); lost = vi.fn(); });
function setup(relations = [], user = { id: 'admin', rol: 'ADMIN_RH' }, item = data) {
  render(<CaseProtection api={api} data={item} user={user} options={options} relations={relations} onUpdated={updated} onAccessLost={lost} />);
  return userEvent.setup();
}
it('supervisor no tiene formularios y caso cerrado exige reapertura', () => {
  const view = render(<CaseProtection api={api} data={data} user={{ rol: 'SUPERVISOR' }} options={options} relations={[]} onUpdated={updated} onAccessLost={lost} />);
  expect(screen.queryByRole('form')).toBeNull(); view.unmount();
  setup([], { rol: 'ADMIN_RH' }, { ...data, status: 'CERRADA' });
  expect(screen.getByText(/Reabre el caso/)).toBeTruthy();
  expect(screen.queryByRole('form')).toBeNull();
});
it('retira confidencialidad solo mediante operación expresa con motivo', async () => {
  const ui = setup();
  await ui.click(screen.getByLabelText('Caso confidencial'));
  await ui.type(screen.getByLabelText('Motivo de confidencialidad'), 'Retiro simulado');
  await ui.click(screen.getByRole('button', { name: 'Guardar confidencialidad' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(api.request.mock.calls[0]).toEqual(['/incidents/case/confidentiality', { method: 'PUT', body: { is_confidential: false, reason: 'Retiro simulado' } }]);
});
it('declarar participante gestor maneja pérdida de acceso con acuse mínimo', async () => {
  api.request.mockResolvedValue({ id: 'case', received: true, can_view: false });
  const ui = setup();
  await ui.selectOptions(screen.getByLabelText('Nuevo participante'), 'admin');
  await ui.type(screen.getByLabelText('Relación con el hecho'), 'Declaración simulada');
  await ui.click(screen.getByRole('button', { name: 'Declarar participante' }));
  await waitFor(() => expect(lost).toHaveBeenCalled());
  expect(updated).not.toHaveBeenCalled();
  expect(api.request.mock.calls[0][1].body).toEqual({ user_id: 'admin', declaration_reason: 'Declaración simulada' });
});
it('confirma o descarta con motivo sin reescribir declaración ni enviar privacidad', async () => {
  const ui = setup([relation]);
  expect(screen.getByText('Declaración: Motivo original simulado')).toBeTruthy();
  await ui.selectOptions(screen.getByLabelText('Decisión sobre Supervisor Demo'), 'DESCARTADO');
  await ui.type(screen.getByLabelText('Motivo de revisión de Supervisor Demo'), 'Corrección ficticia');
  await ui.click(screen.getByRole('button', { name: 'Guardar revisión de Supervisor Demo' }));
  await waitFor(() => expect(updated).toHaveBeenCalled());
  expect(api.request.mock.calls[0]).toEqual(['/incidents/case/participants/super/review', { method: 'PUT', body: { review_status: 'DESCARTADO', reason: 'Corrección ficticia' } }]);
});
it('impide autorrevisión y repetición de participante', () => {
  setup([{ ...relation, user_id: 'admin' }]);
  expect(screen.getByText('No puedes revisar tu propia relación.')).toBeTruthy();
  expect(screen.queryByLabelText('Decisión sobre RH Demo')).toBeNull();
  expect(screen.queryByRole('option', { name: /RH Demo/ })).toBeNull();
});
it('muestra rechazo sin confirmar cambio y bloquea repetición ante red incierta', async () => {
  api.request.mockRejectedValue(new ApiError(409, 'No se puede retirar protección'));
  const ui = setup();
  await ui.type(screen.getByLabelText('Motivo de confidencialidad'), 'Prueba');
  await ui.click(screen.getByRole('button', { name: 'Guardar confidencialidad' }));
  await screen.findByText('No se puede retirar protección');
  expect(updated).not.toHaveBeenCalled();
  api.request.mockRejectedValue(new ApiError(0, 'Red'));
  await ui.click(screen.getByRole('button', { name: 'Guardar confidencialidad' }));
  await screen.findByText(/Resultado no confirmado/);
  expect(screen.getByRole('group', { name: 'Protección del expediente' }).disabled).toBe(true);
});
