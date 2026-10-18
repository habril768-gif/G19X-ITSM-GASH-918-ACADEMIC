import { useEffect, useRef, useState } from 'react';

export default function Departments({ api, user }) {
  const [result, setResult] = useState(null), [page, setPage] = useState(1), [revision, setRevision] = useState(0);
  const [loading, setLoading] = useState(true), [busy, setBusy] = useState(false), [uncertain, setUncertain] = useState(false);
  const [editor, setEditor] = useState(null), [form, setForm] = useState({ nombre: '', reason: '', is_active: true });
  const [error, setError] = useState(''), [message, setMessage] = useState('');
  const [selected, setSelected] = useState(null), [history, setHistory] = useState(null), [historyPage, setHistoryPage] = useState(1), [historyError, setHistoryError] = useState('');
  const active = useRef(true), pending = useRef(false);
  const allowed = user.rol === 'ADMIN_RH';
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    if (!allowed) return;
    const controller = new AbortController(); setLoading(true); setResult(null); setError('');
    api.request(`/departments?page=${page}&page_size=20`, { signal: controller.signal })
      .then(value => { if (!controller.signal.aborted) setResult(value); })
      .catch(e => { if (!controller.signal.aborted) setError(e.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [api, page, revision, allowed]);
  useEffect(() => {
    if (!allowed || !selected) return;
    const controller = new AbortController(); setHistory(null); setHistoryError('');
    api.request(`/departments/${selected.id}/history?page=${historyPage}&page_size=20`, { signal: controller.signal })
      .then(value => { if (!controller.signal.aborted) setHistory(value); })
      .catch(e => { if (!controller.signal.aborted) setHistoryError(e.status === 404 ? 'Departamento no disponible.' : e.message); });
    return () => controller.abort();
  }, [api, selected, historyPage, allowed]);
  if (!allowed) return <p role="alert">Esta sección requiere Admin RH.</p>;
  function close() { setEditor(null); setForm({ nombre: '', reason: '', is_active: true }); }
  function refresh() { close(); setUncertain(false); setSelected(null); setHistory(null); setRevision(v => v + 1); }
  function open(row) {
    setEditor(row || { id: null }); setForm({ nombre: row?.nombre || '', reason: '', is_active: row?.is_active ?? true }); setError(''); setMessage('');
  }
  async function submit(event) {
    event.preventDefault(); if (pending.current || uncertain) return;
    if (!form.nombre.trim() || !form.reason.trim()) { setError('Escribe nombre y motivo.'); return; }
    pending.current = true; setBusy(true); setError(''); setMessage('');
    try {
      await api.request(editor.id ? `/departments/${editor.id}` : '/departments', {
        method: editor.id ? 'PUT' : 'POST', body: { nombre: form.nombre.trim(), reason: form.reason.trim(), ...(editor.id ? { is_active: form.is_active } : {}) },
      });
      if (active.current) { refresh(); setPage(1); setMessage('Departamento guardado. El cambio y su motivo quedaron registrados.'); }
    } catch (e) {
      if (active.current) {
        const unknown = !e.status || e.status >= 500; setUncertain(unknown);
        setError(unknown ? 'No se pudo confirmar el resultado. Actualiza el listado antes de repetir.'
          : e.status === 409 ? 'No se guardó el cambio: revisa nombre duplicado, usuarios activos o incidencias abiertas vinculadas.'
          : e.status === 404 ? 'Departamento no disponible. Actualiza el listado.' : e.message);
      }
    } finally { pending.current = false; if (active.current) setBusy(false); }
  }
  return <section><div className="section-heading"><div><span className="eyebrow">ADMINISTRACIÓN RH</span><h1>Departamentos</h1><p className="muted">Catálogo e historial administrativo.</p></div><button className="primary" disabled={loading || busy || uncertain} onClick={() => open(null)}>Crear departamento</button></div>
    <p className="notice">La baja conserva el historial. Primero deben trasladarse o desactivarse los usuarios activos y atenderse las incidencias abiertas vinculadas. No se elimina personal ni se modifican casos automáticamente.</p>
    {error && <p className="error" role="alert">{error}</p>}{message && <p className="notice" role="status">{message}</p>}
    <button disabled={busy} onClick={refresh}>Actualizar departamentos</button>
    {editor && <form className="card user-editor" onSubmit={submit}><h2>{editor.id ? 'Editar departamento' : 'Nuevo departamento'}</h2><fieldset disabled={busy || uncertain}><legend className="sr-only">Datos del departamento</legend>
      <label>Nombre del departamento<input required maxLength={120} value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} /></label>
      {editor.id && <label className="check-label"><input type="checkbox" checked={form.is_active} onChange={e => setForm(f => ({ ...f, is_active: e.target.checked }))} />Departamento activo</label>}
      <label>Motivo del cambio de departamento<textarea required maxLength={2000} rows={3} value={form.reason} onChange={e => setForm(f => ({ ...f, reason: e.target.value }))} /></label>
      <button className="primary">{busy ? 'Guardando…' : 'Guardar departamento'}</button></fieldset><button type="button" disabled={busy} onClick={close}>Cancelar</button></form>}
    {loading && <p role="status">Cargando departamentos…</p>}{result && <div className="card case-list user-list"><div className="table-scroll"><table><caption className="sr-only">Catálogo administrativo de departamentos</caption><thead><tr><th>Departamento</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>{result.items.map(row => <tr key={row.id}><td>{row.nombre}</td><td>{row.is_active ? 'Activo' : 'Inactivo'}</td><td><button disabled={busy || uncertain} aria-label={`Editar departamento ${row.nombre}`} onClick={() => open(row)}>Editar</button> <button disabled={busy} aria-label={`Historial de ${row.nombre}`} onClick={() => { setSelected(row); setHistoryPage(1); }}>Historial</button></td></tr>)}</tbody></table></div>{result.items.length === 0 && <p>No hay departamentos en esta página.</p>}</div>}
    <div className="pager"><button disabled={loading || busy || page <= 1} onClick={() => { close(); setPage(v => v - 1); }}>Anterior</button><span>Página {page}{result ? ` de ${Math.max(1, Math.ceil(result.total / 20))}` : ''}</span><button disabled={loading || busy || !result || page * 20 >= result.total} onClick={() => { close(); setPage(v => v + 1); }}>Siguiente</button></div>
    {selected && <article className="card history"><h2>Historial: {selected.nombre}</h2>{historyError && <p role="alert" className="error">{historyError}</p>}{!history && !historyError && <p role="status">Cargando historial…</p>}{history && <><ol>{history.items.map(row => <li key={row.id}><strong>{row.detalle.operation}</strong><time dateTime={row.fecha}>{new Date(row.fecha).toLocaleString('es-MX')}</time><p className="description">{row.detalle.reason}</p><p>Nombre: {row.detalle.before?.nombre || 'Sin registro anterior'} → {row.detalle.after.nombre}. Estado: {row.detalle.after.is_active ? 'Activo' : 'Inactivo'}.</p></li>)}</ol>{history.total === 0 && <p>Sin cambios registrados en esta auditoría. Los departamentos anteriores a esta función no reciben eventos retrospectivos.</p>}<div className="pager"><button disabled={historyPage <= 1} onClick={() => setHistoryPage(v => v - 1)}>Historial anterior</button><span>Página {historyPage}</span><button disabled={historyPage * 20 >= history.total} onClick={() => setHistoryPage(v => v + 1)}>Historial siguiente</button></div></>}</article>}
  </section>;
}
