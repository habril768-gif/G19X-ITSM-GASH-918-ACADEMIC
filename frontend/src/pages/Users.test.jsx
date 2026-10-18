import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, it, expect, vi } from 'vitest';
import Users from './Users.jsx';
import { ApiError } from '../services/api.js';
const admin = { id: 'admin', rol: 'ADMIN_RH', departamento_id: 'dep' };
const person = { id: 'employee', nombre_completo: 'Empleado Demo', email: 'demo@example.invalid', departamento_id: 'dep', rol_id: 3, is_active: true };
const options = { roles: [{ id: 1, nombre: 'ADMIN_RH' }, { id: 2, nombre: 'SUPERVISOR' }, { id: 3, nombre: 'EMPLEADO' }], departments: [{ id: 'dep', nombre: 'Demo' }, { id: 'other', nombre: 'Otro' }] };
let api, self;
beforeEach(() => {
  self = vi.fn();
  api = { request: vi.fn(async (path, opts) => opts?.body ? { id: person.id, updated: true, sessions_revoked: true, cases_adjusted: 1 }
    : path === '/users/options' ? options : { items: [person], total: 1 }) };
});
async function start(user = admin) {
  render(<Users api={api} user={user} onSelfRevoked={self} />);
  await screen.findByRole('button', { name: 'Editar Empleado Demo' });
  return userEvent.setup();
}
function writes() { return api.request.mock.calls.filter(([, opts]) => opts?.body); }
it('prohíbe sección y lecturas administrativas para empleado', () => {
  render(<Users api={api} user={{ rol: 'EMPLEADO' }} onSelfRevoked={self} />);
  expect(screen.getByRole('alert').textContent).toContain('Admin RH');
  expect(api.request).not.toHaveBeenCalled();
});
it('crea cuenta con contraseña privada y la retira del formulario', async () => {
  const ui = await start();
  await ui.click(screen.getByRole('button', { name: 'Crear usuario' }));
  await ui.type(screen.getByLabelText('Nombre completo'), 'Nueva Persona Demo');
  await ui.type(screen.getByLabelText('Correo de la cuenta'), 'nueva@example.invalid');
  await ui.type(screen.getByLabelText('Contraseña inicial'), 'Ficticia-123456');
  await ui.click(screen.getByRole('button', { name: 'Crear cuenta' }));
  await screen.findByText('Cuenta creada. La contraseña no se conserva en el formulario.');
  expect(writes()[0]).toEqual(['/users', { method: 'POST', body: { nombre_completo: 'Nueva Persona Demo', departamento_id: 'dep', rol_id: 3, email: 'nueva@example.invalid', password: 'Ficticia-123456' } }]);
  expect(screen.queryByLabelText('Contraseña inicial')).toBeNull();
  expect(localStorage.length).toBe(0);
});
it('modifica rol, departamento y baja con motivo y muestra ajustes', async () => {
  const ui = await start();
  await ui.click(screen.getByRole('button', { name: 'Editar Empleado Demo' }));
  await ui.selectOptions(screen.getByLabelText('Rol del usuario'), '2');
  await ui.selectOptions(screen.getByLabelText('Departamento del usuario'), 'other');
  await ui.click(screen.getByLabelText('Cuenta activa'));
  await ui.type(screen.getByLabelText('Motivo administrativo'), 'Cambio ficticio');
  await ui.click(screen.getByRole('button', { name: 'Guardar usuario' }));
  await screen.findByText(/Casos ajustados: 1/);
  expect(writes()[0][1].body).toEqual({ nombre_completo: 'Empleado Demo', departamento_id: 'other', rol_id: 2, is_active: false, reason: 'Cambio ficticio' });
  expect(writes()[0][1].body.password).toBeUndefined();
});
it('cambiar permisos propios retira sesión sin leer con token revocado', async () => {
  const ui = await start({ ...admin, id: 'employee' });
  await ui.click(screen.getByRole('button', { name: 'Editar Empleado Demo' }));
  await ui.type(screen.getByLabelText('Motivo administrativo'), 'Cambio propio simulado');
  const reads = api.request.mock.calls.length;
  await ui.click(screen.getByRole('button', { name: 'Guardar usuario' }));
  await waitFor(() => expect(self).toHaveBeenCalledOnce());
  expect(api.request.mock.calls.length).toBe(reads + 1);
});
it('conflicto no aplica cambios ficticios ni altera listado', async () => {
  const original = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => opts?.body ? Promise.reject(new ApiError(409, 'Conflicto')) : original(path, opts));
  const ui = await start();
  await ui.click(screen.getByRole('button', { name: 'Editar Empleado Demo' }));
  await ui.type(screen.getByLabelText('Motivo administrativo'), 'Prueba');
  await ui.click(screen.getByRole('button', { name: 'Guardar usuario' }));
  await screen.findByText(/Existe un conflicto/);
  expect(screen.getByLabelText('Cuenta activa').checked).toBe(true);
  expect(self).not.toHaveBeenCalled();
});
it('pagina el directorio en servidor', async () => {
  const original = api.request.getMockImplementation();
  api.request.mockImplementation((path, opts) => path.startsWith('/users?') ? Promise.resolve({ items: [person], total: 21 }) : original(path, opts));
  const ui = await start();
  await ui.click(screen.getByRole('button', { name: 'Siguiente' }));
  await screen.findByText('Página 2 de 2');
  expect(api.request.mock.calls.some(([path]) => path.includes('page=2'))).toBe(true);
});
