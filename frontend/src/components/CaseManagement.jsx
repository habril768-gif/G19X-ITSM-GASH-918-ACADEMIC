import CaseProtection from './CaseProtection.jsx';
import { useEffect, useRef, useState } from 'react';

export default function CaseManagement({ data, user, api, onUpdated, onAccessLost }) {
  const [options, setOptions] = useState(null);
  const [relations, setRelations] = useState([]);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const [retry, setRetry] = useState(0);
  const active = useRef(true), pending = useRef(false);
  const [category, setCategory] = useState(String(data.category_id || (data.scope === 'ENTORNO' ? 4 : '')));
  const [priority, setPriority] = useState(String(data.priority || ''));
  const [assignee, setAssignee] = useState(data.assigned_to || '');
  const [resolution, setResolution] = useState('');
  const [reason, setReason] = useState('');
  const [confirmed, setConfirmed] = useState(false);
  const [title, setTitle] = useState(data.titulo);
  const [description, setDescription] = useState(data.descripcion);
  const manager = ['ADMIN_RH', 'SUPERVISOR'].includes(user.rol);
  const editable = ['PENDIENTE', 'EN_REVISION'].includes(data.status);
  const admin = user.rol === 'ADMIN_RH';
  const reopening = ['RESUELTA', 'CERRADA'].includes(data.status);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    if (!manager) return;
    const controller = new AbortController(); setOptions(null); setError('');
    Promise.all([api.request('/incidents/options', { signal: controller.signal }), api.request(`/incidents/${data.id}/participants`, { signal: controller.signal })])
      .then(([catalog, participants]) => { if (!controller.signal.aborted) { setOptions(catalog); setRelations(participants.items || []); } })
      .catch(e => { if (!controller.signal.aborted) { setError(e.message); if (e.status === 404) onAccessLost(e.message); } });
    return () => controller.abort();
  }, [api, data.id, manager, retry]);
  if (!manager) return null;
  const excluded = new Set([data.affected_employee_id, ...relations.filter(p => ['DECLARADO', 'CONFIRMADO'].includes(p.review_status)).map(p => p.user_id)]);
  const department = data.scope === 'ENTORNO' ? data.reported_department_id : options?.affected_employees?.find(p => p.id === data.affected_employee_id)?.departamento_id;
  const candidates = (options?.participants || []).filter(p => !excluded.has(p.id) && (p.rol === 'ADMIN_RH' || (p.rol === 'SUPERVISOR' && !data.is_confidential && p.departamento_id === department)));
  const categories = (options?.categories || []).filter(p => data.scope !== 'ENTORNO' || p.id === 4);
  async function save(suffix, body, message, method = 'PUT') {
    if (pending.current || uncertain) return;
    pending.current = true; setBusy(true); setError('');
    try {
      await api.request(`/incidents/${data.id}/${suffix}`, { method, body });
      if (active.current) onUpdated(message);
    } catch (e) {
      if (active.current) {
        if (e.status === 404) { onAccessLost(e.message); return; }
        const unknown = e.status === undefined || e.status === 0 || e.status >= 500;
        setUncertain(unknown);
        setError(unknown ? 'No se pudo confirmar el resultado. Actualiza el expediente antes de repetir una operación.' : e.message);
      }
    } finally { pending.current = false; if (active.current) setBusy(false); }
  }
  function checkAssignee() {
    if (candidates.some(p => p.id === assignee)) return true;
    setError('Selecciona un responsable elegible.'); return false;
  }
  function transition(event) {
    event.preventDefault();
    if (data.status === 'PENDIENTE' || reopening) {
      if (!checkAssignee()) return;
      if (reopening && !reason.trim()) { setError('Escribe el motivo de reapertura.'); return; }
      save('transitions', { status: 'EN_REVISION', assigned_to: assignee, ...(reopening ? { reason: reason.trim() } : {}) }, reopening ? 'Caso reabierto; ciclo anterior conservado en historial.' : 'Caso en revisión.', 'POST');
    } else if (data.status === 'EN_REVISION') {
      if (!resolution.trim()) { setError('Escribe la resolución.'); return; }
      save('transitions', { status: 'RESUELTA', resolution_text: resolution.trim() }, 'Resolución registrada.', 'POST');
    }
  }
  function assigneeSelect(label) { return <label>{label}<select required value={assignee} onChange={e => setAssignee(e.target.value)}><option value="">Selecciona un responsable</option>{candidates.map(p => <option key={p.id} value={p.id}>{p.nombre_completo} · {p.rol}</option>)}</select></label>; }
  return <><article className="card management"><h2>Gestionar incidencia</h2><p className="muted">El servidor verifica permisos y registra cada operación en el historial.</p>
    {error && <p className="error" role="alert">{error}</p>}
    {!options && !error && <p role="status">Cargando opciones de gestión…</p>}
    {!options && error && <button onClick={() => setRetry(v => v + 1)}>Reintentar opciones de gestión</button>}
    <button type="button" onClick={() => onUpdated('Expediente actualizado.')} disabled={busy}>Actualizar expediente</button>
    {options && <fieldset className="management-fields" disabled={busy || uncertain}><legend className="sr-only">Acciones disponibles</legend>
      {editable && <><form aria-label="Clasificación humana" onSubmit={e => { e.preventDefault(); save('classification', { category_id: Number(category), priority: Number(priority) }, 'Clasificación validada.'); }}><h3>Clasificación humana</h3><div className="form-row"><label>Categoría oficial<select required value={category} onChange={e => setCategory(e.target.value)}><option value="">Selecciona categoría</option>{categories.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}</select></label><label>Prioridad oficial<select required value={priority} onChange={e => setPriority(e.target.value)}><option value="">Selecciona prioridad</option><option value="1">Alta</option><option value="2">Media</option><option value="3">Baja</option></select></label></div><button className="primary">Confirmar clasificación</button></form>
      <form aria-label="Asignación" onSubmit={e => { e.preventDefault(); if (checkAssignee()) save('assignment', { assigned_to: assignee }, 'Responsable actualizado.'); }}><h3>Asignación</h3>{assigneeSelect('Responsable del caso')}<button>Guardar responsable</button></form></>}
      {(editable || (admin && reopening)) && <form aria-label="Cambiar estado" onSubmit={transition}><h3>{reopening ? 'Reabrir caso' : data.status === 'PENDIENTE' ? 'Iniciar revisión' : 'Resolver caso'}</h3>
        {(data.status === 'PENDIENTE' || reopening) && assigneeSelect('Responsable para revisión')}
        {reopening && <><p className="notice">La resolución y las fechas anteriores se conservarán en el historial.</p><label>Motivo de reapertura<textarea required maxLength={2000} value={reason} onChange={e => setReason(e.target.value)} /></label></>}
        {data.status === 'EN_REVISION' && <label>Resolución del caso<textarea required maxLength={10000} rows={3} value={resolution} onChange={e => setResolution(e.target.value)} /></label>}
        {!reopening && !data.classification_valid && <p className="notice">Confirma una clasificación vigente antes de avanzar.</p>}
        <button className="primary" disabled={!reopening && !data.classification_valid}>{reopening ? 'Reabrir con motivo' : data.status === 'PENDIENTE' ? 'Iniciar revisión' : 'Registrar resolución'}</button>
      </form>}
      {admin && data.status === 'RESUELTA' && <form aria-label="Cerrar caso" onSubmit={e => { e.preventDefault(); if (confirmed) save('transitions', { status: 'CERRADA' }, 'Caso cerrado.', 'POST'); }}><h3>Cerrar caso</h3><label className="check-label"><input type="checkbox" required checked={confirmed} onChange={e => setConfirmed(e.target.checked)} />Confirmo el cierre del caso con la resolución registrada</label><button className="primary">Cerrar caso</button></form>}
      {editable && <details><summary>Editar título y descripción</summary><form aria-label="Editar contenido" onSubmit={e => { e.preventDefault(); if (!title.trim() || !description.trim()) { setError('Escribe título y descripción.'); return; } save('content', { titulo: title.trim(), descripcion: description.trim() }, 'Contenido actualizado. Revisa la vigencia de la clasificación.'); }}><p className="notice">Cambiar la descripción exige revalidar la clasificación. El contenido anterior se conserva en el historial.</p><label>Título del caso<input required maxLength={200} value={title} onChange={e => setTitle(e.target.value)} /></label><label>Descripción del caso<textarea required maxLength={10000} rows={4} value={description} onChange={e => setDescription(e.target.value)} /></label><button>Guardar contenido</button></form></details>}
      {!editable && !admin && <p>Solo Admin RH independiente puede cerrar o reabrir este caso.</p>}
    </fieldset>}{busy && <p role="status">Guardando operación…</p>}
  </article>{options && <CaseProtection api={api} data={data} user={user} options={options} relations={relations} onUpdated={onUpdated} onAccessLost={onAccessLost} />}</>;
}
