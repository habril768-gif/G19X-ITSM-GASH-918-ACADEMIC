import { useEffect, useRef, useState } from 'react';

export default function Users({ api, user, onSelfRevoked }) {
  const [catalog, setCatalog] = useState(null), [result, setResult] = useState(null);
  const [page, setPage] = useState(1), [revision, setRevision] = useState(0);
  const [loading, setLoading] = useState(true), [busy, setBusy] = useState(false);
  const [error, setError] = useState(''), [message, setMessage] = useState('');
  const [editor, setEditor] = useState(null), [uncertain, setUncertain] = useState(false);
  const [form, setForm] = useState({ nombre_completo: '', email: '', password: '', departamento_id: '', rol_id: '3', is_active: true, reason: '' });
  const active = useRef(true), pending = useRef(false);
  const allowed = user.rol === 'ADMIN_RH';
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    if (!allowed) return;
    const controller = new AbortController(); setLoading(true); setResult(null); setError('');
    Promise.all([api.request('/users/options', { signal: controller.signal }), api.request(`/users?page=${page}&page_size=20`, { signal: controller.signal })])
      .then(([options, users]) => { if (!controller.signal.aborted) { setCatalog(options); setResult(users); } })
      .catch(e => { if (!controller.signal.aborted) setError(e.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [api, page, revision, allowed]);
  if (!allowed) return <p role="alert">Esta sección requiere Admin RH.</p>;
  function open(person) {
    setEditor(person || { id: null }); setError(''); setMessage(''); setUncertain(false);
    setForm({ nombre_completo: person?.nombre_completo || '', email: person?.email || '', password: '',
      departamento_id: person?.departamento_id || user.departamento_id || '', rol_id: String(person?.rol_id || 3),
      is_active: person?.is_active ?? true, reason: '' });
  }
  function close() { setEditor(null); setForm(f => ({ ...f, password: '' })); setUncertain(false); }
  function field(key, value) { setForm(f => ({ ...f, [key]: value })); }
  async function submit(event) {
    event.preventDefault(); if (pending.current || uncertain) return;
    if (!form.nombre_completo.trim() || (editor.id && !form.reason.trim())) { setError('Escribe nombre y motivo de modificación.'); return; }
    if (!catalog.departments.some(d => d.id === form.departamento_id)) { setError('Selecciona un departamento activo.'); return; }
    if (!editor.id && !form.password.trim()) { setError('Escribe una contraseña válida.'); return; }
    const body = { nombre_completo: form.nombre_completo.trim(), departamento_id: form.departamento_id, rol_id: Number(form.rol_id),
      ...(editor.id ? { is_active: form.is_active, reason: form.reason.trim() } : { email: form.email.trim().toLowerCase(), password: form.password }) };
    pending.current = true; setBusy(true); setError('');
    try {
      const receipt = await api.request(editor.id ? `/users/${editor.id}` : '/users', { method: editor.id ? 'PUT' : 'POST', body });
      if (!active.current) return;
      if (editor.id === user.id && receipt.sessions_revoked) { onSelfRevoked(); return; }
      setMessage(editor.id ? `Cambios guardados. ${receipt.sessions_revoked ? 'Se ejecutó la revocación de sesiones.' : 'Sin cambio de permisos.'} Casos ajustados: ${receipt.cases_adjusted ?? 0}.` : 'Cuenta creada. La contraseña no se conserva en el formulario.');
      close(); setPage(1); setRevision(v => v + 1);
    } catch (failure) {
      if (active.current) {
        const unknown = failure.status === undefined || failure.status === 0 || failure.status >= 500;
        setUncertain(unknown);
        setError(unknown ? 'No se pudo confirmar el resultado. Actualiza el listado antes de repetir la operación.'
          : failure.status === 409 ? 'Existe un conflicto. Verifica correo duplicado, que quede un RH local activo o que los casos afectados permitan el cambio. No se guardaron cambios parciales.' : failure.message);
      }
    } finally { pending.current = false; if (active.current) { setBusy(false); setForm(f => ({ ...f, password: '' })); } }
  }
  return <section><div className="section-heading"><div><span className="eyebrow">ADMINISTRACIÓN RH</span><h1>Usuarios</h1><p className="muted">Administra cuentas y permisos con revisión de casos asignados.</p></div><button className="primary" disabled={loading || busy || !catalog} onClick={() => open(null)}>Crear usuario</button></div>
    {error && <p className="error" role="alert">{error}</p>}{message && <p className="notice" role="status">{message}</p>}
    <button onClick={() => { close(); setRevision(v => v + 1); }} disabled={busy}>Actualizar listado</button>
    {editor && catalog && <form className="card user-editor" onSubmit={submit}><h2>{editor.id ? 'Editar usuario' : 'Crear cuenta local'}</h2><fieldset disabled={busy || uncertain}><legend className="sr-only">Datos de usuario</legend>
      <label>Nombre completo<input required maxLength={200} value={form.nombre_completo} onChange={e => field('nombre_completo', e.target.value)} /></label>
      {!editor.id ? <><label>Correo de la cuenta<input required type="email" maxLength={320} autoComplete="off" value={form.email} onChange={e => field('email', e.target.value)} /></label><label>Contraseña inicial<input required type="password" minLength={12} maxLength={128} autoComplete="new-password" value={form.password} onChange={e => field('password', e.target.value)} /></label><p className="help">12–128 caracteres. Comunícala por un canal privado autorizado; nunca la incluyas en capturas.</p></> : <p>Cuenta: <strong>{form.email}</strong></p>}
      <div className="form-row"><label>Departamento del usuario<select required value={form.departamento_id} onChange={e => field('departamento_id', e.target.value)}><option value="">Selecciona departamento</option>{catalog.departments.map(d => <option key={d.id} value={d.id}>{d.nombre}</option>)}</select></label><label>Rol del usuario<select required value={form.rol_id} onChange={e => field('rol_id', e.target.value)}>{catalog.roles.map(r => <option key={r.id} value={r.id}>{r.nombre}</option>)}</select></label></div>
      {editor.id && <><label className="check-label"><input type="checkbox" checked={form.is_active} onChange={e => field('is_active', e.target.checked)} />Cuenta activa</label><label>Motivo administrativo<textarea required maxLength={2000} rows={3} value={form.reason} onChange={e => field('reason', e.target.value)} /></label><p className="notice">Cambiar rol, departamento o activación revoca sesiones y revisa casos. La API impedirá dejar el sistema sin RH local activo. Si cambias tus propios permisos, tendrás que iniciar sesión otra vez.</p></>}
      <button className="primary">{busy ? 'Guardando…' : editor.id ? 'Guardar usuario' : 'Crear cuenta'}</button></fieldset><button type="button" disabled={busy} onClick={close}>Cancelar</button></form>}
    {loading && <p role="status">Cargando usuarios…</p>}{result && <div className="card case-list user-list"><div className="table-scroll"><table><caption className="sr-only">Directorio administrativo de usuarios</caption><thead><tr><th>Persona</th><th>Rol</th><th>Departamento</th><th>Cuenta</th><th>Acciones</th></tr></thead><tbody>{result.items.map(person => <tr key={person.id}><td>{person.nombre_completo}<small>{person.email}</small></td><td>{catalog?.roles.find(r => r.id === person.rol_id)?.nombre || person.rol_id}</td><td>{catalog?.departments.find(d => d.id === person.departamento_id)?.nombre || 'Departamento no disponible'}</td><td>{person.is_active ? 'Activa' : 'Inactiva'}</td><td><button disabled={busy} aria-label={`Editar ${person.nombre_completo}`} onClick={() => open(person)}>Editar</button></td></tr>)}</tbody></table></div>{result.items.length === 0 && <p className="empty">No hay usuarios en esta página.</p>}</div>}
    <div className="pager"><button disabled={loading || busy || page === 1} onClick={() => { close(); setPage(v => v - 1); }}>Anterior</button><span>Página {page}{result ? ` de ${Math.max(1, Math.ceil(result.total / 20))}` : ''}</span><button disabled={loading || busy || !result || page * 20 >= result.total} onClick={() => { close(); setPage(v => v + 1); }}>Siguiente</button></div>
  </section>;
}
