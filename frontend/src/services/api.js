export class ApiError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

// La sesión vive en memoria. Nunca usar localStorage, sessionStorage ni URLs.
export function createApi(onExpired = () => {}) {
  let token = null;
  async function request(path, { method = 'GET', body, signal, anonymous = false } = {}) {
    const sentToken = anonymous ? null : token;
    let response;
    try {
      response = await fetch(`/api${path}`, {
        method, signal, cache: 'no-store', credentials: 'omit',
        headers: { ...(body ? { 'Content-Type': 'application/json' } : {}), ...(sentToken ? { Authorization: `Bearer ${sentToken}` } : {}) },
        ...(body ? { body: JSON.stringify(body) } : {}),
      });
    } catch (error) {
      if (error.name === 'AbortError') throw error;
      throw new ApiError(0, 'No se pudo conectar con el servicio. Comprueba que la plataforma esté iniciada.');
    }
    if (!response.ok) {
      if ((response.status === 401 || response.status === 403) && sentToken && sentToken === token) {
        token = null;
        onExpired();
      }
      const message = response.status === 401 ? (anonymous ? 'Correo o contraseña incorrectos, o acceso temporalmente bloqueado.' : 'La sesión terminó. Inicia sesión nuevamente.')
        : response.status === 403 ? 'Tu cuenta no tiene acceso a esta operación.'
        : response.status === 404 ? 'El caso no está disponible o no tienes permiso para consultarlo.'
        : response.status === 422 ? 'Revisa los datos ingresados.'
        : 'El servicio no pudo completar la solicitud. Inténtalo nuevamente.';
      throw new ApiError(response.status, message);
    }
    return response.status === 204 ? null : response.json();
  }
  return {
    request,
    setToken(value) { token = value; },
    clear() { token = null; },
    async login(email, password) {
      const result = await request('/auth/login', { method: 'POST', anonymous: true, body: { email, password } });
      token = result.access_token;
      try { return await request('/auth/me'); }
      catch (error) { token = null; throw error; }
    },
    logout() {
      const pending = request('/auth/logout', { method: 'POST' });
      token = null;
      return pending;
    },
  };
}

export function caseQuery(filters, page = 1) {
  const params = new URLSearchParams({ page: String(page), page_size: '20' });
  for (const [key, value] of Object.entries(filters)) if (String(value).trim()) params.set(key, String(value).trim());
  return `/incidents?${params}`;
}
