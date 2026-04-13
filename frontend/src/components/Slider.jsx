import { useState, useEffect } from "react";

export default function Slider({ label, name, min, max, step, value, unit, onChange }) {
  // Local string copy — lets the user type freely without interference
  const [inputVal, setInputVal] = useState(String(value));

  // Keep in sync when the slider (or external state) changes
  useEffect(() => {
    setInputVal(String(value));
  }, [value]);

  const commit = (raw) => {
    const num = parseFloat(raw);
    if (isNaN(num)) {
      setInputVal(String(value)); 
      return;
    }
    const clamped = Math.min(max, Math.max(min, num));
    setInputVal(String(clamped));
    onChange(name, clamped);
  };

  return (
    <div className="field">
      <label>{label}</label>
      <div className="field-row">
        {/* SLIDER — always uses the committed parent value */}
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => {
            const v = Number(e.target.value);
            setInputVal(String(v));
            onChange(name, v);
          }}
        />

        <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          {/* NUMBER INPUT — uses local string state; commits on blur / Enter */}
          <input
            type="number"
            min={min}
            max={max}
            step={step}
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}   // free editing
            onBlur={(e)   => commit(e.target.value)}        // commit on blur
            onKeyDown={(e) => {
              if (e.key === "Enter") commit(e.target.value);
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
