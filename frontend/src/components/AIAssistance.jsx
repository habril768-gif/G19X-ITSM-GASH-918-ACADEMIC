import { useEffect, useRef, useState } from 'react';

export default function AIAssistance({ api, data, options, onUpdated, onAccessLost }) {
  const [status, setStatus] = useState(null), [error, setError] = useState(''), [busy, setBusy] = useState(false), [uncertain, setUncertain] = useState(false);
  const [text, setText] = useState(''), [simulated, setSimulated] = useState(false), [reviewed, setReviewed] = useState(false);
  const active = useRef(true), pending = useRef(false);
  useEffect(() => {
    active.current = true; const controller = new AbortController();
    api.request(`/incidents/${data.id}/ai`, { signal: controller.signal })
      .then(value => { if (!controller.signal.aborted) setStatus(value); })
      .catch(e => { if (!controller.signal.aborted) { setError(e.message); if (e.status === 404) onAccessLost(e.message); } });
    return () => { active.current = false; controller.abort(); };
  }, [api, data.id]);
  const waiting = status?.job && ['PENDIENTE', 'EN_PROCESO'].includes(status.job.status);
  const completed = status?.job?.current && status.job.status === 'COMPLETADA';
  const allowed = status?.enabled && status.eligible && !waiting && !completed;
  async function submit(event) {
    event.preventDefault(); if (pending.current || uncertain || !allowed) return;
    if (!text.trim() || !simulated || !reviewed) { setError('Escribe texto simulado y confirma su revisión.'); return; }
    pending.current = true; setBusy(true); setError('');
    try {
      const receipt = await api.request(`/incidents/${data.id}/ai`, { method: 'POST', body: {
        ai_input_text: text.trim(), confirmed_simulated: simulated, confirmed_no_identifiers: reviewed,
      } });
      if (active.current) {
        setText(''); setSimulated(false); setReviewed(false);
        onUpdated(receipt.already_requested ? 'La solicitud IA ya estaba registrada; consulta su seguimiento.'
          : receipt.queue_available ? 'Solicitud IA registrada. La clasificación oficial sigue requiriendo validación humana.'
          : 'Solicitud registrada. El procesamiento está pendiente; puedes continuar manualmente.');
      }
    } catch (e) {
      if (active.current) {
        if (e.status === 404) { onAccessLost(e.message); return; }
        const unknown = !e.status || e.status >= 500; setUncertain(unknown);
        setError(unknown ? 'No se confirmó el resultado. Actualiza el seguimiento antes de repetir.' : e.message);
      }
    } finally { pending.current = false; if (active.current) setBusy(false); }
  }
  const suggestion = status?.suggestion;
  return <article className="card management"><h2>Asistencia de IA</h2>
    <p className="notice">La IA solo sugiere. La categoría y prioridad oficiales se confirman en Clasificación humana.</p>
    {error && <p role="alert" className="error">{error}</p>}{!status && !error && <p role="status">Consultando asistencia…</p>}
    <button disabled={busy} onClick={() => onUpdated('Seguimiento IA actualizado.')}>Actualizar asistencia IA</button>
    {status && <><p>Trabajo: {status.job?.status || 'Sin solicitud revisada'}. {status.job && `Intentos: ${status.job.attempts}/3.`}</p>
      {status.reason && <p className="notice">{status.reason}</p>}
      {!status.enabled && <p>Asistencia sin activar. Puedes clasificar manualmente.</p>}
      {!status.eligible && <p>Este expediente requiere atención manual en su estado o condiciones actuales.</p>}
      {status.job && !status.job.current && <p>La solicitud anterior corresponde a otra versión del contenido.</p>}
      {suggestion && <section><h3>{suggestion.result === 'SIN_CLASIFICACION' ? 'IA sin clasificación: requiere aclaración o criterio humano' : 'Sugerencia pendiente de validación humana'}</h3>
        {suggestion.result === 'CLASIFICADA' && <p>Categoría sugerida: {options.categories.find(c => c.id === suggestion.category_id)?.nombre || 'Revisa el catálogo'}. Prioridad sugerida: {({ 1: 'Alta', 2: 'Media', 3: 'Baja' })[suggestion.priority]}.</p>}
        <p className="description">{suggestion.suggestion}</p><p className="description">Motivo: {suggestion.reason}</p>
      </section>}
      {status.reviewed_text && <details><summary>Texto simulado revisado de la solicitud</summary><p className="description">{status.reviewed_text}</p></details>}
      {allowed && <form aria-label="Solicitar asistencia IA" onSubmit={submit}><fieldset className="management-fields" disabled={busy || uncertain}><legend className="sr-only">Revisión previa al envío</legend>
        <label>Texto simulado para la IA<textarea required maxLength={4000} rows={4} value={text} onChange={e => setText(e.target.value)} /></label>
        <p className="help">Escribe solo hechos mínimos ficticios. No copies nombres, correos, identificadores ni datos reales. La descripción original no se envía automáticamente.</p>
        <label className="check-label"><input type="checkbox" required checked={simulated} onChange={e => setSimulated(e.target.checked)} />Confirmo que el texto es completamente simulado</label>
        <label className="check-label"><input type="checkbox" required checked={reviewed} onChange={e => setReviewed(e.target.checked)} />Revisé que no contiene identificadores personales</label>
        <p className="notice">Se comprobarán permisos y confidencialidad antes de enviar. Una petición externa ya iniciada no puede retirarse; si cambian sus condiciones, la respuesta se descarta para uso operativo.</p>
        <button className="primary">{busy ? 'Registrando…' : 'Confirmar texto y solicitar IA'}</button>
      </fieldset></form>}
    </>}
  </article>;
}
