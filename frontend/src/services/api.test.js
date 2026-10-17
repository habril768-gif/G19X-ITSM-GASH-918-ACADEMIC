import { describe, it, expect, vi } from 'vitest';
import { createApi, caseQuery } from './api.js';

describe('sesiones y consultas', () => {
  it('transmite token solo en cabecera y limpia sesión en 401', async () => {
    const expired = vi.fn(); const api = createApi(expired);
    global.fetch = vi.fn().mockResolvedValue({ ok: false, status: 401 });
    api.setToken('simulated-test-token');
    await expect(api.request('/incidents')).rejects.toMatchObject({ status: 401 });
    expect(expired).toHaveBeenCalledOnce();
    expect(fetch.mock.calls[0][0]).toBe('/api/incidents');
    expect(fetch.mock.calls[0][1].headers.Authorization).toBe('Bearer simulated-test-token');
    expect(localStorage.length).toBe(0); expect(sessionStorage.length).toBe(0);
    fetch.mockResolvedValue({ ok: true, status: 200, json: async () => ({}) });
    await api.request('/incidents');
    expect(fetch.mock.lastCall[1].headers.Authorization).toBeUndefined();
  });
  it('un 401 tardío de sesión anterior no borra la nueva', async () => {
    const expired = vi.fn(); const api = createApi(expired); let respond;
    global.fetch = vi.fn().mockImplementationOnce(() => new Promise(resolve => { respond = resolve; }));
    api.setToken('old-test'); const pending = api.request('/incidents');
    api.setToken('new-test'); respond({ ok: false, status: 401 });
    await expect(pending).rejects.toMatchObject({ status: 401 });
    expect(expired).not.toHaveBeenCalled();
    fetch.mockResolvedValue({ ok: true, status: 200, json: async () => ({}) });
    await api.request('/auth/me'); expect(fetch.mock.lastCall[1].headers.Authorization).toBe('Bearer new-test');
  });
  it('logout conserva token para revocarlo y lo elimina inmediatamente de memoria', async () => {
    const api = createApi(); api.setToken('logout-test');
    global.fetch = vi.fn().mockResolvedValue({ ok: true, status: 204 });
    await api.logout();
    expect(fetch.mock.calls[0][0]).toBe('/api/auth/logout');
    expect(fetch.mock.calls[0][1].headers.Authorization).toBe('Bearer logout-test');
    fetch.mockResolvedValue({ ok: true, status: 200, json: async () => ({}) });
    await api.request('/incidents'); expect(fetch.mock.lastCall[1].headers.Authorization).toBeUndefined();
  });
  it('codifica filtros y paginación sin incluir valores vacíos', () => {
    const path = caseQuery({ q: 'Prueba & seguimiento', status: 'PENDIENTE', category_id: '', priority: 2 }, 3);
    const params = new URL(path, 'http://test').searchParams;
    expect(params.get('q')).toBe('Prueba & seguimiento'); expect(params.get('page')).toBe('3');
    expect(params.get('priority')).toBe('2'); expect(params.has('category_id')).toBe(false);
  });
});
