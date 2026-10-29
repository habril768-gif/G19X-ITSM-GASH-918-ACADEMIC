import { useEffect, useState } from 'react';

const kinds = { CREACION: 'Creación', ASIGNACION: 'Asignación', RESOLUCION: 'Resolución', REAPERTURA: 'Reapertura', CIERRE: 'Cierre' };
const states = { PENDIENTE: 'Pendiente', EN_PROCESO: 'En proceso', ENVIADA: 'Aceptada por SMTP', FALLIDA: 'Entrega no confirmada', OMITIDA: 'Omitida' };

export default function MailStatus({ api, caseId, onAccessLost }) {
  const [page, setPage] = useState(1), [retry, setRetry] = useState(0);
  const [result, setResult] = useState(null), [error, setError] = useState('');
  useEffect(() => {
    const controller = new AbortController(); setResult(null); setError('');
    api.request(`/incidents/${caseId}/mail?page=${page}&page_size=20`, { signal: controller.signal })
      .then(value => { if (!controller.signal.aborted) setResult({ ...value, items: Array.isArray(value.items) ? value.items : [] }); })
      .catch(failure => { if (!controller.signal.aborted) { setResult(null); setError(failure.message); if (failure.status === 404) onAccessLost(failure.message); } });
    return () => controller.abort();
  }, [api, caseId, page, retry]);
  return <article className="card management"><h2>Notificaciones por correo</h2>
    <p>Consulta los envíos y omisiones del expediente. La aceptación por SMTP no confirma lectura ni recepción en el buzón.</p>
    <button onClick={() => setRetry(value => value + 1)}>Actualizar correos</button>
    {error && <p role="alert" className="error">{error}</p>}
    {!result && !error && <p role="status">Consultando correos…</p>}
    {result && <>{result.items.length === 0 && <p>Sin eventos de correo registrados.</p>}
      <ul>{result.items.map(item => <li key={item.id}><strong>{kinds[item.kind] || 'Evento'}: {states[item.status] || item.status}</strong>
        <p>Intentos: {item.attempts}/4.{item.error && ` ${item.error}`}</p></li>)}</ul>
      <div className="pager"><button disabled={page === 1} onClick={() => setPage(value => value - 1)}>Correos anteriores</button><span>Página {page}</span><button disabled={page * 20 >= result.total} onClick={() => setPage(value => value + 1)}>Más correos</button></div>
    </>}
  </article>;
}
