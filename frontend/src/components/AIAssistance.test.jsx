import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, expect, it, vi } from 'vitest';
import AIAssistance from './AIAssistance.jsx';
import { ApiError } from '../services/api.js';
let api, updated, lost, status;
beforeEach(() => {
  updated = vi.fn(); lost = vi.fn(); status = { enabled: true, eligible: true, ai_status: 'PENDIENTE', job: null };
  api = { request: vi.fn(async (path, opts) => opts?.method === 'POST' ? { received: true, queue_available: false } : status) };
});
async function start() {
  render(<AIAssistance api={api} data={{ id: 'case', descripcion: 'Descripción original que no se copia' }} options={{ categories: [{ id: 2, nombre: 'Conflictos' }] }} onUpdated={updated} onAccessLost={lost} />);
  await screen.findByText(/Sin solicitud revisada/); return userEvent.setup();
}
async function fill(ui) {
  await ui.type(screen.getByLabelText('Texto simulado para la IA'), 'Un hecho simulado mínimo para clasificar.');
  await ui.click(screen.getByLabelText('Confirmo que el texto es completamente simulado'));
  await ui.click(screen.getByLabelText('Revisé que no contiene identificadores personales'));
}
it('no copia descripción y exige confirmaciones antes de escribir', async () => {
  const ui = await start(); expect(screen.getByLabelText('Texto simulado para la IA').value).toBe('');
  fireEvent.submit(screen.getByRole('form', { name: 'Solicitar asistencia IA' }));
  expect(screen.getByRole('alert').textContent).toContain('confirma');
  expect(api.request.mock.calls.filter(([, opts]) => opts?.method === 'POST')).toHaveLength(0);
});
it('registra texto revisado, no afirma resultado y limpia formulario tras acuse', async () => {
  const ui = await start(); await fill(ui);
  await ui.click(screen.getByRole('button', { name: 'Confirmar texto y solicitar IA' }));
  expect(api.request).toHaveBeenLastCalledWith('/incidents/case/ai', { method: 'POST', body: {
    ai_input_text: 'Un hecho simulado mínimo para clasificar.', confirmed_simulated: true, confirmed_no_identifiers: true,
  } });
  expect(updated.mock.calls[0][0]).toContain('procesamiento está pendiente');
  expect(screen.getByLabelText('Texto simulado para la IA').value).toBe('');
});
it.each(['disabled', 'ineligible', 'pending'])('no ofrece envío con condición %s', async kind => {
  if (kind === 'disabled') status.enabled = false;
  if (kind === 'ineligible') status.eligible = false;
  if (kind === 'pending') status.job = { status: 'PENDIENTE', attempts: 0, current: true };
  render(<AIAssistance api={api} data={{ id: 'case' }} options={{ categories: [] }} onUpdated={updated} onAccessLost={lost} />);
  await waitFor(() => expect(screen.queryByText('Consultando asistencia…')).toBeNull());
  expect(screen.queryByRole('form', { name: 'Solicitar asistencia IA' })).toBeNull();
});
it('abstención se muestra como revisión manual sin categoría forzada', async () => {
  status.job = { status: 'COMPLETADA', attempts: 1, current: true };
  status.suggestion = { result: 'SIN_CLASIFICACION', suggestion: 'Pedir aclaración.', reason: 'Ambiguo.' };
  render(<AIAssistance api={api} data={{ id: 'case' }} options={{ categories: [] }} onUpdated={updated} onAccessLost={lost} />);
  await screen.findByText('IA sin clasificación: requiere aclaración o criterio humano');
  expect(screen.queryByText(/Categoría sugerida/)).toBeNull();
});
it('respuesta incierta bloquea reenvío hasta actualizar', async () => {
  const ui = await start(); await fill(ui); api.request.mockRejectedValueOnce(new ApiError(0, 'Sin red'));
  await ui.click(screen.getByRole('button', { name: 'Confirmar texto y solicitar IA' }));
  expect(screen.getByRole('alert').textContent).toContain('Actualiza');
  expect(screen.getByRole('button', { name: 'Confirmar texto y solicitar IA' }).closest('fieldset').disabled).toBe(true);
  expect(updated).not.toHaveBeenCalled();
});

it('retira expediente cuando consulta de IA responde 404', async () => {
  api.request.mockRejectedValue(new ApiError(404, 'Caso no disponible'));
  render(<AIAssistance api={api} data={{ id: 'case' }} options={{ categories: [] }} onUpdated={updated} onAccessLost={lost} />);
  await waitFor(() => expect(lost).toHaveBeenCalledWith('Caso no disponible'));
  expect(screen.queryByLabelText('Texto simulado para la IA')).toBeNull();
});
