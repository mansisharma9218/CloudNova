/**
 * AdvisorPage.jsx — Cloud Cost Advisor
 *
 * Changes:
 *  • Calls /api/predict/instance in parallel with /api/predict to get
 *    ML-ranked specific instance recommendations per provider.
 *  • Renders a new "Recommended Instances" panel showing instance_type,
 *    vcpu, ram, predicted hourly + monthly cost per provider.
 *  • Usage hours default changed to 720; label updated.
 *  • Caches last input hash — skips API call if inputs haven't changed.
 */

import { useState, useRef } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer,
} from "recharts";

import api from "../api/cloudApi";
import { PROVIDER_COLORS } from "../constants/providerColors";
import { CHART_TOOLTIP_STYLE } from "../constants/ChartTooltipStyle";
import Slider from "../components/Slider";
import StatCard from "../components/StatCard";
import ProviderBars from "../components/ProviderBars";

const REGIONS = [
  { value: "us-east",  label: "US East" },
  { value: "us-west",  label: "US West" },
  { value: "europe",   label: "Europe" },
  { value: "asia",     label: "Asia Pacific" },
];

const PRICING_MODELS = [
  { value: "on-demand",    label: "On-Demand" },
  { value: "1yr-reserved", label: "1-Year Reserved" },
  { value: "3yr-reserved", label: "3-Year Reserved" },
  { value: "spot",         label: "Spot / Preemptible" },
];

const PROVIDER_BADGE = {
  AWS:   { bg: "rgba(255,153,0,0.12)",  color: "#ff9900" },
  Azure: { bg: "rgba(0,138,215,0.12)",  color: "#008ad7" },
  GCP:   { bg: "rgba(52,168,83,0.12)",  color: "#34a853" },
};

function InstanceCard({ provider, data, isBest }) {
  const badge = PROVIDER_BADGE[provider];
  return (
    <div
      className="stat-card fade-in"
      style={{
        border: isBest
          ? `1px solid rgba(54,203,114,0.35)`
          : "1px solid var(--border)",
        position: "relative",
      }}
    >
      {isBest && (
        <span
          style={{
            position: "absolute", top: "0.75rem", right: "0.75rem",
            fontSize: "0.6rem", background: "rgba(54,203,114,0.15)",
            color: "var(--success)", border: "1px solid rgba(54,203,114,0.3)",
            padding: "0.15rem 0.5rem", borderRadius: "100px",
          }}
        >
          BEST
        </span>
      )}

      {/* Provider badge */}
      <span
        style={{
          display: "inline-block", padding: "0.2rem 0.6rem",
          borderRadius: "6px", fontSize: "0.65rem", fontWeight: 600,
          letterSpacing: "0.06em", marginBottom: "0.75rem",
          background: badge.bg, color: badge.color,
        }}
      >
        {provider}
      </span>

      {/* Instance name */}
      <div style={{ fontFamily: "var(--font-mono)", fontSize: "1rem", fontWeight: 600, color: "var(--text)", marginBottom: "0.5rem" }}>
        {data.instance_type}
      </div>

      {/* Specs row */}
      <div style={{ display: "flex", gap: "1rem", fontSize: "0.7rem", color: "var(--muted)", marginBottom: "0.75rem" }}>
        <span>{data.vcpu} vCPU</span>
        <span>{data.ram_gb} GB RAM</span>
        <span>{data.storage_gb} GB</span>
      </div>

      {/* Cost */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
        <div>
          <div style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>Monthly</div>
          <div style={{ fontFamily: "var(--font-head)", fontSize: "1.4rem", fontWeight: 800, color: isBest ? "var(--success)" : "var(--accent)" }}>
            ${data.monthly_cost}
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "0.6rem", color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.08em" }}>Per Hour</div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "0.85rem", color: "var(--muted)" }}>
            ${data.predicted_hourly_cost}
          </div>
        </div>
      </div>

      {data.fallback && (
        <div style={{ fontSize: "0.6rem", color: "var(--warning)", marginTop: "0.5rem", opacity: 0.8 }}>
          ⚠ No exact match — closest available instance
        </div>
      )}
    </div>
  );
}

export default function AdvisorPage() {
  const [form, setForm] = useState({
    vcpu: 2, ram_gb: 4, storage_gb: 50, usage_hours: 720,
    region: "us-east", pricing_model: "on-demand",
  });
  const [loading,   setLoading]   = useState(false);
  const [result,    setResult]    = useState(null);
  const [instances, setInstances] = useState(null);

  // Cache: skip API if inputs haven't changed
  const lastInputRef = useRef(null);

  const handleChange = (name, value) => setForm((f) => ({ ...f, [name]: value }));

  const inputKey = () => JSON.stringify(form);

  const handlePredict = async () => {
    if (lastInputRef.current === inputKey()) return; // no change
    setLoading(true);
    setResult(null);
    setInstances(null);
    try {
      // Parallel calls — cost comparison + instance recommendation
      const [costData, instData] = await Promise.all([
        api.predict(form),
        api.recommendInstance(form),
      ]);
      setResult(costData);
      setInstances(instData);
      lastInputRef.current = inputKey();
    } finally {
      setLoading(false);
    }
  };

  const barData = result
    ? Object.entries(result.predicted_costs || {}).map(([name, cost]) => ({
        name, cost, fill: PROVIDER_COLORS[name],
      }))
    : [];

  return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Live Advisor</div>
        <h1>Find the <span>cheapest cloud</span> for your workload</h1>
        <p>
          Configure your requirements. Our ML model predicts hourly costs across
          AWS, Azure, and GCP — then recommends the optimal specific instance.
        </p>
      </div>

      <div className="main">
        <div className="two-col section">

          {/* ── INPUT FORM ── */}
          <div className="card">
            <div className="card-title">Resource Requirements</div>
            <div className="form-grid">
              <Slider label="vCPU Cores"                  name="vcpu"        min={1}  max={64}   step={1}  value={form.vcpu}        unit=""     onChange={handleChange} />
              <Slider label="RAM (GB)"                    name="ram_gb"      min={1}  max={256}  step={1}  value={form.ram_gb}      unit=" GB"  onChange={handleChange} />
              <Slider label="Storage (GB)"                name="storage_gb"  min={10} max={2000} step={10} value={form.storage_gb}  unit=" GB"  onChange={handleChange} />
              <Slider label="Instance Runtime (hrs/month)" name="usage_hours" min={1}  max={744}  step={1}  value={form.usage_hours} unit=" hrs" onChange={handleChange} />
            </div>

            <div className="dropdown-grid">
              <div className="dropdown-group">
                <label className="dropdown-label">Region</label>
                <select
                  className="dropdown"
                  value={form.region}
                  onChange={(e) => handleChange("region", e.target.value)}
                >
                  {REGIONS.map((r) => (
                    <option key={r.value} value={r.value}>{r.label}</option>
                  ))}
                </select>
              </div>
              <div className="dropdown-group">
                <label className="dropdown-label">Pricing Model</label>
                <select
                  className="dropdown"
                  value={form.pricing_model}
                  onChange={(e) => handleChange("pricing_model", e.target.value)}
                >
                  {PRICING_MODELS.map((p) => (
                    <option key={p.value} value={p.value}>{p.label}</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              className={`btn-primary ${loading ? "loading" : ""}`}
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "→  Predict & Compare"}
            </button>
          </div>

          {/* ── PROVIDER COMPARISON ── */}
          <div className="card">
            <div className="card-title">Provider Comparison</div>
            {result ? (
              <div className="fade-in">
                <ProviderBars providers={result.predicted_costs} />
                <div className="rec-box">
                  <span className="rec-icon">✦</span>
                  <div className="rec-text">
                    <strong>{result.recommendation}</strong> is your best match.
                    Switch from the most expensive option and save{" "}
                    <strong>${result.savings_vs_most_expensive}/mo</strong>.
                  </div>
                </div>
              </div>
            ) : (
              <div className="empty">
                <div className="empty-icon">◈</div>
                <p>Configure your workload and run a prediction to see provider costs here.</p>
              </div>
            )}
          </div>
        </div>

        {/* ── INSTANCE RECOMMENDATIONS ── */}
        {instances && (
          <div className="section fade-in">
            <div style={{ marginBottom: "1rem" }}>
              <div className="card-title" style={{ marginBottom: "0.25rem" }}>
                Recommended Instances
              </div>
              <p style={{ fontSize: "0.75rem", color: "var(--muted)" }}>
                ML-ranked: each candidate was predicted individually; the cheapest sufficient instance per provider is shown.
              </p>
            </div>
            <div className="results-grid">
              {Object.entries(instances.recommendations).map(([provider, data]) => (
                <InstanceCard
                  key={provider}
                  provider={provider}
                  data={data}
                  isBest={provider === instances.best_provider}
                />
              ))}
            </div>
          </div>
        )}

        {/* ── STATS + BAR CHART ── */}
        {result && (
          <div className="section fade-in">
            <div className="results-grid">
              <StatCard
                label="Predicted Monthly Cost"
                value={`$${result.predicted_costs[result.recommendation]}`}
                sub="Based on your inputs"
                type="success"
              />
              <StatCard
                label="Recommended Provider"
                value={result.recommendation}
                sub="Lowest cost for your config"
                type="success"
              />
              <StatCard
                label="Potential Savings"
                value={`$${result.savings_vs_most_expensive}`}
                sub="vs. most expensive option"
                type="success"
              />
            </div>

            <div className="card">
              <div className="card-title">Monthly Cost — Provider Breakdown</div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={barData} margin={{ top: 0, right: 0, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                  <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" }} />
                  <YAxis tick={{ fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" }} unit="$" />
                  <Tooltip
                    contentStyle={{
                      ...CHART_TOOLTIP_STYLE,
                      backgroundColor: "#111",
                      border: "1px solid #333",
                    }}
                    labelStyle={{ color: "#fff" }}   // heading text
                    itemStyle={{ color: "#fff" }}    // value text
                    cursor={{ fill: "rgba(255,255,255,0.03)" }}
                    formatter={(v) => [`$${v}`, "Monthly Cost"]}
                  />
                  <Bar dataKey="cost" radius={[6, 6, 0, 0]}>
                    {barData.map((entry) => (
                      <rect key={entry.name} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
