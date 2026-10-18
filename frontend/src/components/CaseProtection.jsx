import { useEffect, useRef, useState } from 'react';

export default function CaseProtection({ api, data, user, options, relations, onUpdated, onAccessLost }) {
  const [error, setError] = useState(''), [busy, setBusy] = useState(false), [uncertain, setUncertain] = useState(false);
  const [privacy, setPrivacy] = useState(data.is_confidential), [privacyReason, setPrivacyReason] = useState('');
  const [participant, setParticipant] = useState(''), [declaration, setDeclaration] = useState('');
  const [reviews, setReviews] = useState({});
  const active = useRef(true), pending = useRef(false);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  if (user.rol !== 'ADMIN_RH') return null;
  if (!['PENDIENTE', 'EN_REVISION'].includes(data.status)) return <article className="card management"><h2>Protección del expediente</h2><p>Reabre el caso antes de modificar confidencialidad o participantes.</p></article>;
  const choices = (options.participants || []).filter(p => p.id !== data.affected_employee_id && !relations.some(r => r.user_id === p.id));
  async function save(suffix, body, method = 'PUT') {
    if (pending.current || uncertain) return;
    pending.current = true; setBusy(true); setError('');
    try {
      const receipt = await api.request(`/incidents/${data.id}/${suffix}`, { method, body });
      if (receipt.received !== true || typeof receipt.can_view !== 'boolean') throw new Error('Acuse no confirmado');
      if (active.current) {
        if (!receipt.can_view) onAccessLost('Se guardó la operación. Tu cuenta ya no puede consultar este expediente; conserva su referencia.');
        else onUpdated('Protección actualizada. Se recargaron expediente, relaciones e historial.');
      }
    } catch (failure) {
      if (active.current) {
        if (failure.status === 404) { onAccessLost(failure.message); return; }
        const unknown = failure.status === undefined || failure.status === 0 || failure.status >= 500;
        setUncertain(unknown);
        setError(unknown ? 'Resultado no confirmado. Actualiza el expediente antes de repetir.' : failure.message);
      }
    } finally { pending.current = false; if (active.current) setBusy(false); }
  }
  function reviewField(id, key, value) { setReviews(old => ({ ...old, [id]: { ...old[id], [key]: value } })); }
  return <article className="card management"><h2>Confidencialidad y participantes</h2><p className="notice">Solo RH independiente puede revisar relaciones. Involucrar a un gestor activa protección de inmediato; declararte a ti mismo puede quitarte acceso. Descartar una relación no retira confidencialidad automáticamente. Se conserva la declaración original.</p>
    {error && <p role="alert" className="error">{error}</p>}
    {uncertain && <button onClick={() => onUpdated('Expediente actualizado.')}>Actualizar expediente</button>}
    <fieldset className="management-fields" disabled={busy || uncertain}><legend className="sr-only">Protección del expediente</legend>
      <form aria-label="Cambiar confidencialidad" onSubmit={e => { e.preventDefault(); if (!privacyReason.trim()) { setError('Escribe el motivo de confidencialidad.'); return; } save('confidentiality', { is_confidential: privacy, reason: privacyReason.trim() }); }}><h3>Confidencialidad</h3><label className="check-label"><input type="checkbox" checked={privacy} onChange={e => setPrivacy(e.target.checked)} />Caso confidencial</label><label>Motivo de confidencialidad<textarea required rows={2} maxLength={2000} value={privacyReason} onChange={e => setPrivacyReason(e.target.value)} /></label><button>Guardar confidencialidad</button><p className="help">La API reasigna a RH elegible si el responsable pierde acceso, o devuelve a Pendiente si falta uno. No permite retirar protección con gestor involucrado.</p></form>
      <form aria-label="Añadir participante" onSubmit={e => { e.preventDefault(); if (!choices.some(p => p.id === participant) || !declaration.trim()) { setError('Selecciona participante y explica su relación.'); return; } save('participants', { user_id: participant, declaration_reason: declaration.trim() }, 'POST'); }}><h3>Completar participantes</h3><label>Nuevo participante<select required value={participant} onChange={e => setParticipant(e.target.value)}><option value="">Selecciona una persona</option>{choices.map(p => <option key={p.id} value={p.id}>{p.nombre_completo} · {p.rol}</option>)}</select></label><label>Relación con el hecho<textarea required rows={2} maxLength={2000} value={declaration} onChange={e => setDeclaration(e.target.value)} /></label><button disabled={relations.length >= 20}>Declarar participante</button></form>
      <section className="relations"><h3>Relaciones declaradas</h3>{relations.length === 0 && <p>Sin participantes adicionales.</p>}{relations.map(row => {
        const name = options.participants?.find(p => p.id === row.user_id)?.nombre_completo || 'Participante fuera del directorio activo';
        const review = reviews[row.user_id] || {};
        return <form className="participant-card" aria-label={`Revisar relación de ${name}`} key={row.user_id} onSubmit={e => { e.preventDefault(); if (!review.reason?.trim() || !review.status) { setError('Selecciona decisión y escribe el motivo de revisión.'); return; } save(`participants/${row.user_id}/review`, { review_status: review.status, reason: review.reason.trim() }); }}><strong>{name}</strong><p>Estado: {row.review_status}</p><p className="description">Declaración: {row.declaration_reason}</p>{row.review_reason && <p className="description">Última revisión: {row.review_reason}</p>}
          {row.user_id === user.id ? <p>No puedes revisar tu propia relación.</p> : <><label>Decisión sobre {name}<select required value={review.status || ''} onChange={e => reviewField(row.user_id, 'status', e.target.value)}><option value="">Selecciona decisión</option><option value="CONFIRMADO" disabled={row.review_status === 'CONFIRMADO'}>Confirmar</option><option value="DESCARTADO" disabled={row.review_status === 'DESCARTADO'}>Descartar</option></select></label><label>Motivo de revisión de {name}<textarea required rows={2} maxLength={2000} value={review.reason || ''} onChange={e => reviewField(row.user_id, 'reason', e.target.value)} /></label><button>Guardar revisión de {name}</button></>}
        </form>;
      })}</section>
    </fieldset>{busy && <p role="status">Guardando protección…</p>}
  </article>;
}
