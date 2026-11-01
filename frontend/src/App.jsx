import { useEffect, useRef, useState } from 'react';
import { createApi, caseQuery } from './services/api.js';
import NewIncident from './pages/NewIncident.jsx';
import Users from './pages/Users.jsx';
import Departments from './pages/Departments.jsx';
import PasswordChange from './pages/PasswordChange.jsx';
import CaseManagement from './components/CaseManagement.jsx';

const statuses = { PENDIENTE: 'Pendiente', EN_REVISION: 'En revisión', RESUELTA: 'Resuelta', CERRADA: 'Cerrada' };
const priorities = { 1: 'Alta', 2: 'Media', 3: 'Baja' };
const roles = { ADMIN_RH: 'Administración RH', SUPERVISOR: 'Supervisión', EMPLEADO: 'Empleado' };
const emptyFilters = { q: '', status: '', priority: '', category_id: '', assigned_to: '', created_from: '', created_to: '' };
const dateLabel = value => value ? new Date(value).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' }) : 'Sin registro';

function Brand() { return <div className="brand"><span className="brand-mark" aria-hidden="true">P<span>•</span></span><span>PluriOne<small>GESTIÓN DE INCIDENCIAS</small></span></div>; }
function ErrorMessage({ children }) { return children ? <p className="error" role="alert">{children}</p> : null; }
function Badge({ value }) { return <span className={`badge ${value?.toLowerCase()}`}>{statuses[value] || value}</span>; }

function Login({ api, onLogin, notice }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  async function submit(event) {
    event.preventDefault(); setBusy(true); setError('');
    try { onLogin(await api.login(email.trim(), password)); }
    catch (failure) { setError(failure.message); }
    finally { setPassword(''); setBusy(false); }
  }
  return <main className="login-layout">
    <section className="login-story"><Brand /><div><span className="eyebrow">UN ESPACIO PARA ATENDER</span><h1>Cada situación<br />merece seguimiento.</h1><p>Registra, consulta y acompaña las incidencias de tu equipo desde un mismo lugar.</p><div className="story-line" /><p className="story-note">Acceso según tu rol.<br />Atención con criterio humano.</p></div><small>PluriOne · Proyecto académico</small></section>
    <section className="login-form"><form onSubmit={submit}><span className="eyebrow">BIENVENIDO DE NUEVO</span><h2>Inicia sesión</h2><p className="muted">Utiliza la cuenta que te asignó Recursos Humanos.</p>{notice && <p role="status" className="notice">{notice}</p>}<ErrorMessage>{error}</ErrorMessage>
      <label>Correo electrónico<input type="email" autoComplete="username" required value={email} onChange={e => setEmail(e.target.value)} /></label>
      <label>Contraseña<input type="password" autoComplete="current-password" required maxLength={128} value={password} onChange={e => setPassword(e.target.value)} /></label>
      <button className="primary wide" disabled={busy}>{busy ? 'Ingresando…' : 'Entrar a PluriOne →'}</button><p className="help">¿Necesitas acceso o recuperar tu contraseña? Contacta al administrador de la plataforma.</p>
    </form></section>
  </main>;
}

function CaseDetail({ id, api, user, onBack }) {
  const accessLost = useRef(false);
  const [revision, setRevision] = useState(0);
  const [message, setMessage] = useState('');
  const [data, setData] = useState(null);
  const [history, setHistory] = useState({ items: [], total: 0 });
  const [historyPage, setHistoryPage] = useState(1);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(true);
  useEffect(() => {
    const controller = new AbortController(); setData(null); setError(''); setBusy(true);
    api.request(`/incidents/${id}`, { signal: controller.signal }).then(result => { if (!controller.signal.aborted && !accessLost.current) setData(result); })
      .catch(e => { if (!controller.signal.aborted) setError(e.message); }).finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [id, api, revision]);
  useEffect(() => {
    const controller = new AbortController(); setHistory({ items: [], total: 0 });
    api.request(`/incidents/${id}/history?page=${historyPage}&page_size=20`, { signal: controller.signal }).then(result => { if (!controller.signal.aborted) setHistory(result); })
      .catch(e => { if (!controller.signal.aborted) { setError(e.message); if (e.status === 404) { accessLost.current = true; setData(null); } } });
    return () => controller.abort();
  }, [id, historyPage, api, revision]);
  return <section><button className="text-button" onClick={onBack}>← Volver a incidencias</button><ErrorMessage>{error}</ErrorMessage>{message && <p className="notice" role="status">{message}</p>}{busy && <p role="status">Cargando expediente…</p>}
    {data && <><div className="section-heading"><div><span className="eyebrow">EXPEDIENTE</span><h1>{data.titulo}</h1><p className="muted id">{data.id}</p></div><Badge value={data.status} /></div>
      <div className="detail-grid"><article className="card"><h2>Descripción del caso</h2><p className="description">{data.descripcion}</p><dl><dt>Fecha del hecho</dt><dd>{data.incident_date}</dd><dt>Ámbito</dt><dd>{data.scope === 'ENTORNO' ? 'Entorno de trabajo' : 'Persona'}</dd><dt>Prioridad</dt><dd>{priorities[data.priority] || 'Por definir'}</dd><dt>Confidencialidad</dt><dd>{data.is_confidential ? 'Acceso restringido a RH independiente' : 'Acceso según rol y departamento'}</dd><dt>Clasificación</dt><dd>{data.classification_valid ? 'Validación vigente' : 'Requiere validación humana'}</dd></dl></article>
      <article className="card"><h2>Seguimiento</h2><p className="notice">{data.ai_status === 'OMITIDA' ? 'Asistencia IA omitida. Este caso requiere clasificación manual.' : data.ai_status === 'FALLIDA' ? 'La asistencia IA no pudo completarse. El caso puede atenderse manualmente.' : data.ai_status === 'COMPLETADA' ? 'La asistencia IA tiene una respuesta registrada; requiere revisión humana.' : 'Asistencia IA pendiente. Puedes consultar el seguimiento disponible.'}</p><dl><dt>Registrada</dt><dd>{dateLabel(data.created_at)}</dd><dt>Responsable</dt><dd className="id">{data.assigned_to || 'Sin asignar'}</dd><dt>Resolución</dt><dd className="description">{data.resolution_text || 'Sin resolución registrada'}</dd><dt>Resuelta</dt><dd>{dateLabel(data.resolved_at)}</dd><dt>Cerrada</dt><dd>{dateLabel(data.closed_at)}</dd></dl></article></div>
      <CaseManagement data={data} user={user} api={api} onUpdated={text => { setMessage(text); setHistoryPage(1); setRevision(r => r + 1); }} onAccessLost={text => { accessLost.current = true; setData(null); setHistory({ items: [], total: 0 }); setError(text); }} />
      <article className="card history"><h2>Historial del caso</h2><p className="muted">Se muestran los eventos permitidos para tu cuenta.</p><ol>{history.items.map(item => <li key={item.id}><strong>{item.accion.replaceAll('_', ' ')}</strong><time dateTime={item.fecha}>{dateLabel(item.fecha)}</time>{item.detalle?.reason && <p>{item.detalle.reason}</p>}</li>)}</ol>{history.total === 0 && <p>Sin eventos disponibles.</p>}<div className="pager"><button disabled={historyPage <= 1} onClick={() => setHistoryPage(p => p - 1)}>Anterior</button><span>Página {historyPage}</span><button disabled={historyPage * 20 >= history.total} onClick={() => setHistoryPage(p => p + 1)}>Siguiente</button></div></article>
    </>}
  </section>;
}

function Cases({ api, user, onSelect }) {
  const [draft, setDraft] = useState(emptyFilters);
  const [filters, setFilters] = useState(emptyFilters);
  const [page, setPage] = useState(1);
  const [retry, setRetry] = useState(0);
  const [result, setResult] = useState(null);
  const [options, setOptions] = useState(null);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [optionsError, setOptionsError] = useState('');
  useEffect(() => {
    const controller = new AbortController();
    api.request('/incidents/options', { signal: controller.signal }).then(value => { if (!controller.signal.aborted) setOptions(value); })
      .catch(e => { if (!controller.signal.aborted) setOptionsError(e.message); });
    return () => controller.abort();
  }, [api]);
  useEffect(() => {
    const controller = new AbortController(); setBusy(true); setResult(null); setError('');
    api.request(caseQuery(filters, page), { signal: controller.signal }).then(value => { if (!controller.signal.aborted) setResult(value); })
      .catch(e => { if (!controller.signal.aborted) setError(e.message); }).finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [api, filters, page, retry]);
  function apply(event) {
    event.preventDefault();
    if (draft.created_from && draft.created_to && draft.created_from > draft.created_to) { setError('La fecha inicial debe ser anterior o igual a la final.'); return; }
    setPage(1); setFilters({ ...draft });
  }
  function field(key, value) { setDraft(previous => ({ ...previous, [key]: value })); }
  const managers = options?.participants.filter(p => ['ADMIN_RH', 'SUPERVISOR'].includes(p.rol)) || [];
  return <section><div className="section-heading"><div><span className="eyebrow">PANEL OPERATIVO</span><h1>Incidencias</h1><p className="muted">{user.rol === 'EMPLEADO' ? 'Consulta tus casos y su seguimiento.' : 'Da seguimiento a los casos disponibles para tu cuenta.'}</p></div><div className="total"><strong>{result ? result.total : '—'}</strong><span>casos en esta consulta</span></div></div>
    <form className="card filters" onSubmit={apply}><div className="filter-top"><label className="search">Buscar por título o ID<input type="search" value={draft.q} onChange={e => field('q', e.target.value)} placeholder="Buscar incidencia…" maxLength={200} /></label><label>Estado<select value={draft.status} onChange={e => field('status', e.target.value)}><option value="">Todos los estados</option>{Object.entries(statuses).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></label><label>Prioridad<select value={draft.priority} onChange={e => field('priority', e.target.value)}><option value="">Todas</option>{Object.entries(priorities).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></label></div>
      <details><summary>Más filtros</summary><div className="filter-more"><label>Categoría<select value={draft.category_id} onChange={e => field('category_id', e.target.value)}><option value="">Todas</option>{options?.categories.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}</select></label><label>Responsable<select value={draft.assigned_to} onChange={e => field('assigned_to', e.target.value)}><option value="">Todos</option>{user.rol !== 'EMPLEADO' && <option value="unassigned">Sin responsable</option>}{managers.map(p => <option key={p.id} value={p.id}>{p.nombre_completo}</option>)}</select></label><label>Creación desde (UTC)<input type="date" value={draft.created_from} onChange={e => field('created_from', e.target.value)} /></label><label>Creación hasta (UTC)<input type="date" value={draft.created_to} onChange={e => field('created_to', e.target.value)} /></label></div></details><ErrorMessage>{optionsError}</ErrorMessage><div className="filter-actions"><button type="button" onClick={() => { setDraft(emptyFilters); setFilters({ ...emptyFilters }); setPage(1); }}>Limpiar filtros</button><button className="primary" type="submit" disabled={busy}>Aplicar filtros</button></div></form>
    <ErrorMessage>{error}</ErrorMessage>{error && <button onClick={() => setRetry(v => v + 1)}>Reintentar</button>}
    <div className="card case-list" aria-busy={busy}>{busy ? <p className="empty" role="status">Cargando incidencias…</p> : result?.items.length === 0 ? <div className="empty"><span aria-hidden="true">○</span><h2>No hay casos en esta consulta</h2><p>Prueba otros filtros o consulta nuevamente más tarde.</p></div> : result && <div className="table-scroll"><table><caption className="sr-only">Incidencias disponibles para tu cuenta</caption><thead><tr><th>Caso</th><th>Estado</th><th>Prioridad</th><th>Creación</th><th>Acceso</th></tr></thead><tbody>{result.items.map(item => <tr key={item.id}><td><button className="case-link" onClick={() => onSelect(item.id)}>{item.titulo}</button><small className="id">{item.id}</small></td><td><Badge value={item.status} /></td><td><span className={`priority priority-${item.priority}`}>{priorities[item.priority] || 'Por definir'}</span></td><td>{dateLabel(item.created_at)}</td><td>{item.is_confidential ? 'Restringido' : 'Según rol'}</td></tr>)}</tbody></table></div>}</div>
    <div className="pager"><button disabled={busy || page === 1} onClick={() => setPage(p => p - 1)}>← Anterior</button><span>Página {page}{result ? ` de ${Math.max(1, Math.ceil(result.total / 20))}` : ''}</span><button disabled={busy || !result || page * 20 >= result.total} onClick={() => setPage(p => p + 1)}>Siguiente →</button></div>
  </section>;
}

export function incidentFromLocation(search) {
  const id = new URLSearchParams(search).get('incident');
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id || '') ? id : null;
}

export default function App() {
  const [user, setUser] = useState(null);
  const [selected, setSelected] = useState(() => incidentFromLocation(window.location.search));
  const [notice, setNotice] = useState('');
  const [creating, setCreating] = useState(false);
  const [usersVisible, setUsersVisible] = useState(false);
  const [departmentsVisible, setDepartmentsVisible] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [passwordBusy, setPasswordBusy] = useState(false);
  const api = useRef(null);
  if (!api.current) api.current = createApi(() => { setUser(null); setSelected(null); setCreating(false); setUsersVisible(false); setDepartmentsVisible(false); setPasswordVisible(false); setNotice('Tu sesión terminó o cambió el acceso de tu cuenta. Inicia sesión nuevamente.'); });
  function logout() {
    const pending = api.current.logout();
    setUser(null); setSelected(null); setCreating(false); setUsersVisible(false); setDepartmentsVisible(false); setPasswordVisible(false); setNotice('Cerraste tu sesión.');
    pending.catch(() => { setNotice('Se retiró la sesión de este navegador. No se pudo confirmar el cierre en el servidor; la sesión vencerá según su vigencia.'); });
  }
  if (!user) return <Login api={api.current} notice={notice} onLogin={value => { setNotice(''); setUser(value); }} />;
  const list = () => { setSelected(null); setCreating(false); setUsersVisible(false); setDepartmentsVisible(false); setPasswordVisible(false); };
  return <div className="workspace"><aside className="sidebar"><Brand /><p className="sidebar-label">ESPACIO DE TRABAJO</p><button className="nav-item" disabled={passwordBusy} onClick={list}>▤ <span>Incidencias</span></button><button className="nav-item" disabled={passwordBusy} onClick={() => { setSelected(null); setUsersVisible(false); setDepartmentsVisible(false); setPasswordVisible(false); setCreating(true); }}>＋ <span>Nueva incidencia</span></button>{user.rol === 'ADMIN_RH' && <button className="nav-item" disabled={passwordBusy} onClick={() => { setSelected(null); setCreating(false); setPasswordVisible(false); setDepartmentsVisible(false); setUsersVisible(true); }}>⚙ <span>Usuarios</span></button>}{user.rol === 'ADMIN_RH' && <button className="nav-item" disabled={passwordBusy} onClick={() => { list(); setDepartmentsVisible(true); }}>▦ <span>Departamentos</span></button>}<div className="sidebar-foot"><strong>Un seguimiento más claro.</strong><p>La información se comparte según los permisos de cada cuenta.</p></div></aside>
    <div className="main-area"><header className="topbar"><span>Gestión de incidencias laborales</span><div className="account"><div><strong>{user.nombre_completo}</strong><small>{roles[user.rol] || user.rol}</small></div><button disabled={passwordBusy} onClick={() => { list(); setPasswordVisible(true); }}>Cambiar contraseña</button><button disabled={passwordBusy} onClick={logout}>Cerrar sesión</button></div></header><main className="content">{passwordVisible ? <PasswordChange api={api.current} onBusy={setPasswordBusy} onBack={list} onChanged={() => { api.current.clear(); setUser(null); list(); setNotice('Contraseña actualizada. Se revocaron tus sesiones. Inicia sesión con la nueva contraseña.'); }} onUncertain={() => { api.current.clear(); setUser(null); list(); setNotice('No se pudo confirmar el cambio de contraseña. Por precaución se retiró esta sesión. Intenta iniciar sesión; si no puedes acceder, contacta al operador.'); }} /> : departmentsVisible ? <Departments api={api.current} user={user} /> : usersVisible ? <Users api={api.current} user={user} onSelfRevoked={() => { api.current.clear(); setUser(null); setSelected(null); setCreating(false); setUsersVisible(false); setDepartmentsVisible(false); setPasswordVisible(false); setNotice('Cambiaste los permisos de tu cuenta. Inicia sesión de nuevo.'); }} /> : creating ? <NewIncident api={api.current} user={user} onBack={list} onOpen={id => { setCreating(false); setSelected(id); }} /> : selected ? <CaseDetail key={selected} id={selected} api={api.current} user={user} onBack={list} /> : <Cases api={api.current} user={user} onSelect={setSelected} />}</main><footer>PluriOne · Entorno académico · Utiliza datos simulados</footer></div>
  </div>;
}
