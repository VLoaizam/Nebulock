import { useState } from 'react'
import './App.css'

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/cipher'

async function request(path, payload) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.error ?? 'Ocurrió un error inesperado');
  }
  return data;
}

function Accordion({ title, description, open, onToggle, children }) {
  return (
    <section className={`accordion ${open ? 'open' : ''}`}>
      <button className="accordion-toggle" onClick={onToggle}>
        {title}
      </button>
      {open && (
        <div className="accordion-body">
          <p>{description}</p>
          {children}
        </div>
      )}
    </section>
  );
}

function DualForm({ label, placeholder, value, onChange, resultLabel, resultValue, onAction, onReverse, error, disabled }) {
  return (
    <div className="dual-form">
      <label>
        {label}
        <textarea
          placeholder={placeholder}
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
      </label>
      <div className="dual-buttons">
        <button type="button" onClick={onAction} disabled={disabled}>
          Encriptar
        </button>
        <button type="button" onClick={onReverse} disabled={disabled}>
          Desencriptar
        </button>
      </div>
      {error && <span className="inline-error">{error}</span>}
      <div className="accordion-output">
        <span>{resultLabel}</span>
        <code>{resultValue}</code>
      </div>
    </div>
  );
}

function App() {
  const [status, setStatus] = useState('');
  const [errors, setErrors] = useState({
    numeric: '',
    periodic: '',
  });

  const [numericInput, setNumericInput] = useState('');
  const [numericResult, setNumericResult] = useState('');

  const [periodicInput, setPeriodicInput] = useState('');
  const [periodicResult, setPeriodicResult] = useState('');

  const [openPanel, setOpenPanel] = useState('numeric');
  const busy = Boolean(status);

  const showError = (field, message) => {
    setErrors((prev) => ({ ...prev, [field]: message }));
  };

  const ensureValue = (field, value, message) => {
    if (!value || !value.trim()) {
      showError(field, message);
      return false;
    }
    showError(field, '');
    return true;
  };

  const runAction = async (label, field, fn) => {
    setStatus(label);
    if (field) showError(field, '');
    try {
      await fn();
    } catch (err) {
      showError(field, err.message || 'Ocurrió un error inesperado');
    } finally {
      setStatus('');
    }
  };

  return (
    <main className="app-container">
      <header className="hero">
        <h1>Nebulock</h1>
      </header>

      <div className="intro">
        <ul>
          <li>Primera capa: transforma texto y códigos numéricos.</li>
          <li>Segunda capa: traduce códigos y símbolos químicos.</li>
        </ul>
      </div>

      <div className="accordion-list">
        <Accordion
          title="1. Capa numérica"
          description="Opera con la encriptación numérica."
          open={openPanel === 'numeric'}
          onToggle={() => setOpenPanel(openPanel === 'numeric' ? null : 'numeric')}
        >
          <DualForm
            label="Texto o códigos"
            placeholder="Escribe texto o códigos separados por espacios"
            value={numericInput}
            onChange={setNumericInput}
            resultLabel="Resultado"
            resultValue={numericResult}
            error={errors.numeric}
            disabled={busy}
            onAction={() => {
              if (!ensureValue('numeric', numericInput, 'Ingresa texto o códigos.')) {
                return;
              }
              runAction('Encriptando', 'numeric', async () => {
                const data = await request('/encrypt/', { text: numericInput });
                setNumericResult(data.codes ?? '');
              });
            }}
            onReverse={() => {
              if (!ensureValue('numeric', numericInput, 'Ingresa texto o códigos.')) {
                return;
              }
              runAction('Desencriptando', 'numeric', async () => {
                const data = await request('/decrypt/', { codes: numericInput });
                setNumericResult(data.text ?? '');
              });
            }}
          />
        </Accordion>

        <Accordion
          title="2. Capa periódica"
          description="Aplica la encriptación basada en elementos químicos."
          open={openPanel === 'periodic'}
          onToggle={() => setOpenPanel(openPanel === 'periodic' ? null : 'periodic')}
        >
          <DualForm
            label="Códigos o símbolos"
            placeholder="Ej: 26 41 33 o Fe Nb As"
            value={periodicInput}
            onChange={setPeriodicInput}
            resultLabel="Resultado"
            resultValue={periodicResult}
            error={errors.periodic}
            disabled={busy}
            onAction={() => {
              if (!ensureValue('periodic', periodicInput, 'Ingresa los datos para encriptar.')) {
                return;
              }
              runAction('Capa periódica', 'periodic', async () => {
                const data = await request('/periodic/encrypt/', { codes: periodicInput });
                setPeriodicResult((data.periodic ?? []).join(' '));
              });
            }}
            onReverse={() => {
              if (!ensureValue('periodic', periodicInput, 'Ingresa los datos para desencriptar.')) {
                return;
              }
              runAction('Revirtiendo', 'periodic', async () => {
                const data = await request('/periodic/decrypt/', { periodic: periodicInput });
                setPeriodicResult(data.codes ?? '');
              });
            }}
          />
        </Accordion>
      </div>

      <footer className="status-banner">
        <p className="status">
          {status ? `⌛ ${status}...` : 'Listo para enviar nuevas solicitudes.'}
        </p>
      </footer>
    </main>
  );
}

export default App
