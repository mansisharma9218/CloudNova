export default function Slider({ label, name, min, max, step, value, unit, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <div className="field-row">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={e => onChange(name, Number(e.target.value))}
        />
        <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <input
            type="number"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={e => {
              const val = Math.min(max, Math.max(min, Number(e.target.value)));
              onChange(name, val);
            }}
            style={{
              width: "65px",
              background: "rgba(62,207,255,0.06)",
              border: "1px solid rgba(62,207,255,0.15)",
              borderRadius: "6px",
              color: "var(--accent)",
              fontFamily: "var(--font-mono)",
              fontSize: "0.85rem",
              padding: "0.25rem 0.5rem",
              textAlign: "center",
              outline: "none",
              MozAppearance: "textfield",
              appearance: "textfield",
            }}
          />
          {unit && (
            <span style={{ fontSize: "0.7rem", color: "var(--muted)", whiteSpace: "nowrap" }}>
              {unit}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}