import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, expect, it, vi } from 'vitest';
import Departments from './Departments.jsx';
import { ApiError } from '../services/api.js';
const admin = { rol: 'ADMIN_RH' };
const row = { id: 'dep', nombre: 'DEMO temporal', is_active: true };
let api;
beforeEach(() => { api = { request: vi.fn(async (path, opts) => opts?.body ? row : path.includes('/history?') ? {
  items: [{ id: 'event', fecha: '2026-10-17T12:00:00Z', detalle: { operation: 'CREADO', reason: 'Motivo de prueba', before: null, after: row } }], total: 1,
} : { items: [row], total: 1 }) }; });
async function start() { render(<Departments api={api} user={admin} />); await screen.findByRole('button', { name: 'Editar departamento DEMO temporal' }); return userEvent.setup(); }
function writes() { return api.request.mock.calls.filter(([, opts]) => opts?.body); }
it('empleado no ve directorio ni hace lecturas', () => {
  render(<Departments api={api} user={{ rol: 'EMPLEADO' }} />);
  expect(screen.getByRole('alert').textContent).toContain('Admin RH'); expect(api.request).not.toHaveBeenCalled();
});
it('crea departamento con nombre y motivo y recarga listado', async () => {
  const ui = await start(); await ui.click(screen.getByRole('button', { name: 'Crear departamento' }));
  await ui.type(screen.getByLabelText('Nombre del departamento'), 'QA nuevo');
  await ui.type(screen.getByLabelText('Motivo del cambio de departamento'), 'Prueba UI');
  await ui.click(screen.getByRole('button', { name: 'Guardar departamento' }));
  await screen.findByText(/Departamento guardado/);
  expect(writes()[0]).toEqual(['/departments', { method: 'POST', body: { nombre: 'QA nuevo', reason: 'Prueba UI' } }]);
  await waitFor(() => expect(api.request.mock.calls.filter(([path]) => path.includes('/departments?')).length).toBe(2));
});
it('edita estado con motivo sin borrar ni trasladar personal', async () => {
  const ui = await start(); await ui.click(screen.getByRole('button', { name: 'Editar departamento DEMO temporal' }));
  await ui.click(screen.getByLabelText('Departamento activo'));
  await ui.type(screen.getByLabelText('Motivo del cambio de departamento'), 'Baja temporal de prueba');
  await ui.click(screen.getByRole('button', { name: 'Guardar departamento' }));
  expect(writes()[0]).toEqual(['/departments/dep', { method: 'PUT', body: { nombre: row.nombre, is_active: false, reason: 'Baja temporal de prueba' } }]);
});
it('409 no simula cambio ni éxito', async () => {
  const ui = await start(); await ui.click(screen.getByRole('button', { name: 'Editar departamento DEMO temporal' }));
  api.request.mockRejectedValueOnce(new ApiError(409, 'Conflicto'));
  await ui.type(screen.getByLabelText('Motivo del cambio de departamento'), 'Prueba rechazada');
  await ui.click(screen.getByRole('button', { name: 'Guardar departamento' }));
  expect(screen.getByRole('alert').textContent).toContain('usuarios activos');
  expect(screen.queryByText(/Departamento guardado/)).toBeNull(); expect(screen.getByText('Activo')).toBeTruthy();
});
it('respuesta incierta bloquea edición hasta actualizar, sin reenvío automático', async () => {
  const ui = await start(); await ui.click(screen.getByRole('button', { name: 'Editar departamento DEMO temporal' }));
  api.request.mockRejectedValueOnce(new ApiError(0, 'Sin conexión'));
  await ui.type(screen.getByLabelText('Motivo del cambio de departamento'), 'Prueba incierta');
  await ui.click(screen.getByRole('button', { name: 'Guardar departamento' }));
  expect(screen.getByRole('alert').textContent).toContain('confirmar');
  expect(screen.getByRole('button', { name: 'Guardar departamento' }).closest('fieldset').disabled).toBe(true);
  expect(screen.getByRole('button', { name: 'Crear departamento' }).disabled).toBe(true);
  expect(writes()).toHaveLength(1);
  await ui.click(screen.getByRole('button', { name: 'Actualizar departamentos' }));
  await waitFor(() => expect(screen.getByRole('button', { name: 'Crear departamento' }).disabled).toBe(false));
});
it('historial y directorio usan páginas del servidor', async () => {
  const ui = await start(); await ui.click(screen.getByRole('button', { name: 'Historial de DEMO temporal' }));
  await screen.findByText('Motivo de prueba');
  expect(api.request.mock.calls.some(([path]) => path === '/departments/dep/history?page=1&page_size=20')).toBe(true);
  api.request.mockResolvedValue({ items: [row], total: 21 });
  await ui.click(screen.getByRole('button', { name: 'Actualizar departamentos' }));
  await waitFor(() => expect(screen.getByRole('button', { name: 'Siguiente' }).disabled).toBe(false));
  await ui.click(screen.getByRole('button', { name: 'Siguiente' }));
  await waitFor(() => expect(api.request.mock.calls.some(([path]) => path === '/departments?page=2&page_size=20')).toBe(true));
});
