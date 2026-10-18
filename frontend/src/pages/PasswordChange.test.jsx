import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, expect, it, vi } from 'vitest';
import PasswordChange from './PasswordChange.jsx';
import { ApiError } from '../services/api.js';

let api, changed, uncertain, busy;
beforeEach(() => {
  api = { request: vi.fn().mockResolvedValue(null) }; changed = vi.fn(); uncertain = vi.fn(); busy = vi.fn();
});
function start() {
  render(<PasswordChange api={api} onChanged={changed} onUncertain={uncertain} onBusy={busy} onBack={vi.fn()} />);
  return userEvent.setup();
}
async function fill(ui, confirm = 'Nueva-simulada-123') {
  await ui.type(screen.getByLabelText('Contraseña actual'), 'Anterior-simulada-123');
  await ui.type(screen.getByLabelText('Nueva contraseña'), 'Nueva-simulada-123');
  await ui.type(screen.getByLabelText('Confirmar nueva contraseña'), confirm);
}
it('no envía contraseñas cuando la confirmación difiere', async () => {
  const ui = start(); await fill(ui, 'Diferente-simulada-123');
  await ui.click(screen.getByRole('button', { name: 'Guardar nueva contraseña' }));
  expect(screen.getByRole('alert').textContent).toContain('confirmación');
  expect(api.request).not.toHaveBeenCalled();
});
it('envía solo credenciales requeridas, confirma y limpia campos', async () => {
  const ui = start(); await fill(ui);
  await ui.click(screen.getByRole('button', { name: 'Guardar nueva contraseña' }));
  expect(api.request).toHaveBeenCalledWith('/auth/change-password', { method: 'POST', body: { current_password: 'Anterior-simulada-123', new_password: 'Nueva-simulada-123' } });
  expect(changed).toHaveBeenCalledOnce();
  for (const input of document.querySelectorAll('input')) expect(input.value).toBe('');
  expect(localStorage.length).toBe(0); expect(sessionStorage.length).toBe(0);
});
it('contraseña actual rechazada limpia campos sin dar éxito', async () => {
  api.request.mockRejectedValue(new ApiError(400, 'Mensaje externo no mostrado'));
  const ui = start(); await fill(ui);
  await ui.click(screen.getByRole('button', { name: 'Guardar nueva contraseña' }));
  expect(screen.getByRole('alert').textContent).toContain('contraseña actual');
  expect(changed).not.toHaveBeenCalled(); expect(uncertain).not.toHaveBeenCalled();
  for (const input of document.querySelectorAll('input')) expect(input.value).toBe('');
});
it('resultado incierto retira sesión sin reintentar la escritura', async () => {
  api.request.mockRejectedValue(new ApiError(0, 'Sin conexión'));
  const ui = start(); await fill(ui);
  await ui.click(screen.getByRole('button', { name: 'Guardar nueva contraseña' }));
  expect(uncertain).toHaveBeenCalledOnce(); expect(changed).not.toHaveBeenCalled();
  expect(api.request).toHaveBeenCalledOnce();
});
it('bloquea doble envío y cancelación mientras espera respuesta', async () => {
  let resolve; api.request.mockImplementation(() => new Promise(done => { resolve = done; }));
  const ui = start(); await fill(ui);
  const form = screen.getByRole('button', { name: 'Guardar nueva contraseña' }).closest('form');
  fireEvent.submit(form); fireEvent.submit(form);
  expect(api.request).toHaveBeenCalledOnce();
  expect(screen.getByRole('button', { name: 'Cancelar' }).disabled).toBe(true);
  expect(busy).toHaveBeenCalledWith(true);
  resolve(null); await waitFor(() => expect(changed).toHaveBeenCalledOnce());
  expect(busy).toHaveBeenLastCalledWith(false);
});
