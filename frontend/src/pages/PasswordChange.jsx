import { useEffect, useRef, useState } from 'react';

export default function PasswordChange({ api, onChanged, onUncertain, onBusy, onBack }) {
  const [current, setCurrent] = useState(''), [password, setPassword] = useState(''), [confirmation, setConfirmation] = useState('');
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  const active = useRef(true), pending = useRef(false);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  async function submit(event) {
    event.preventDefault(); if (pending.current) return;
    if (!current || !password.trim() || password.length < 12 || password.length > 128 || password !== confirmation) {
      setError('Escribe la contraseña actual y una nueva de 12–128 caracteres. La confirmación debe coincidir.'); return;
    }
    pending.current = true; setBusy(true); onBusy(true); setError('');
    try {
      await api.request('/auth/change-password', { method: 'POST', body: { current_password: current, new_password: password } });
      if (active.current) onChanged();
    } catch (failure) {
      if (active.current) {
        if (!failure.status || failure.status >= 500) onUncertain();
        else setError(failure.status === 400 ? 'No se pudo verificar la contraseña actual. Revisa tus datos.' : failure.message);
      }
    } finally {
      pending.current = false; onBusy(false);
      if (active.current) { setCurrent(''); setPassword(''); setConfirmation(''); setBusy(false); }
    }
  }
  return <section><span className="eyebrow">MI CUENTA</span><h1>Cambiar contraseña</h1>
    <p className="notice">Al guardar se revocan todas tus sesiones. Tendrás que iniciar sesión con la nueva contraseña.</p>
    <form className="card user-editor" onSubmit={submit}>
      {error && <p role="alert" className="error">{error}</p>}
      <fieldset disabled={busy}><legend className="sr-only">Credenciales personales</legend>
        <label>Contraseña actual<input required type="password" autoComplete="current-password" maxLength={128} value={current} onChange={e => setCurrent(e.target.value)} /></label>
        <label>Nueva contraseña<input required type="password" autoComplete="new-password" minLength={12} maxLength={128} value={password} onChange={e => setPassword(e.target.value)} /></label>
        <label>Confirmar nueva contraseña<input required type="password" autoComplete="new-password" minLength={12} maxLength={128} value={confirmation} onChange={e => setConfirmation(e.target.value)} /></label>
        <button className="primary">{busy ? 'Guardando…' : 'Guardar nueva contraseña'}</button>
      </fieldset>
      <button type="button" disabled={busy} onClick={onBack}>Cancelar</button>
      <p className="help">No incluyas contraseñas en capturas. Si perdiste la actual, solicita el restablecimiento al operador.</p>
    </form>
  </section>;
}
