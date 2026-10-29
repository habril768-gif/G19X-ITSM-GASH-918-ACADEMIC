import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { it, expect, vi } from 'vitest';
import MailStatus from './MailStatus.jsx';
import { incidentFromLocation } from '../App.jsx';

it('muestra fallo y omisión, permite actualizar sin repetir el envío', async () => {
  const api = { request: vi.fn(async () => ({ total: 2, items: [
    { id: '1', kind: 'RESOLUCION', status: 'FALLIDA', attempts: 4, error: 'No se confirmó la entrega' },
    { id: '2', kind: 'CREACION', status: 'OMITIDA', attempts: 0, error: 'Sin destinatario autorizado' },
  ] })) };
  render(<MailStatus api={api} caseId="case" onAccessLost={vi.fn()} />);
  await screen.findByText('Resolución: Entrega no confirmada');
  expect(screen.getByText('Creación: Omitida')).toBeTruthy();
  expect(screen.getByRole('button', { name: 'Más correos' }).disabled).toBe(true);
  await userEvent.click(screen.getByRole('button', { name: 'Actualizar correos' }));
  await waitFor(() => expect(api.request).toHaveBeenCalledTimes(2));
  expect(api.request.mock.calls.every(([, options]) => !options.method && !options.body)).toBe(true);
});

it('retira el resultado anterior cuando se pierde acceso', async () => {
  const lost = vi.fn(); const api = { request: vi.fn().mockResolvedValueOnce({ total: 1, items: [{ id: '1', kind: 'CREACION', status: 'ENVIADA', attempts: 1 }] })
    .mockRejectedValueOnce({ status: 404, message: 'Incidencia no encontrada' }) };
  render(<MailStatus api={api} caseId="case" onAccessLost={lost} />);
  await screen.findByText('Creación: Aceptada por SMTP');
  await userEvent.click(screen.getByRole('button', { name: 'Actualizar correos' }));
  await waitFor(() => expect(lost).toHaveBeenCalledWith('Incidencia no encontrada'));
  expect(screen.queryByText('Creación: Aceptada por SMTP')).toBeNull();
});

it('el enlace de correo solo selecciona UUID; nunca concede autenticación', () => {
  expect(incidentFromLocation('?incident=12345678-1234-1234-1234-123456789abc')).toBe('12345678-1234-1234-1234-123456789abc');
  expect(incidentFromLocation('?incident=https://example.invalid')).toBeNull();
  expect(incidentFromLocation('?incident=<script>')).toBeNull();
  expect(incidentFromLocation('')).toBeNull();
});


it('identifica el aviso de cierre sin afirmar entrega al buzón', async () => {
  const api = { request: vi.fn(async () => ({ total: 1, items: [
    { id: 'close', kind: 'CIERRE', status: 'ENVIADA', attempts: 1 },
  ] })) };
  render(<MailStatus api={api} caseId="case" onAccessLost={vi.fn()} />);
  await screen.findByText('Cierre: Aceptada por SMTP');
  expect(screen.getByText(/no confirma lectura ni recepción/)).toBeTruthy();
});
