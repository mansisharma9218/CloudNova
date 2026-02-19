import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import api from "../api/cloudApi";
import { PROVIDER_COLORS } from "../constants/providerColors";
import { CHART_TOOLTIP_STYLE } from "../constants/ChartTooltipStyle";
import Slider from "../components/Slider";
import StatCard from "../components/StatCard";
import ProviderBars from "../components/ProviderBars";

export default function AdvisorPage() {
  const [form, setForm] = useState({
    vcpu: 2, ram_gb: 4, storage_gb: 50, usage_hours: 720,
  });
  const [loading, setLoading] = useState(false);
  const [result,  setResult]  = useState(null);

  const handleChange = (name, value) => setForm(f => ({ ...f, [name]: value }));

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const data = await api.predict(form);
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  const barData = result
    ? Object.entries(result.providers).map(([name, cost]) => ({
        name,
        cost,
        fill: PROVIDER_COLORS[name],
      }))
    : [];

  return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Live Advisor</div>
        <h1>Find the <span>cheapest cloud</span> for your workload</h1>
        <p>
          Configure your requirements below. Our ML model predicts monthly costs
          across AWS, Azure, and GCP — then recommends the optimal choice.
        </p>
      </div>

      <div className="main">
        {/* ── INPUT + COMPARISON ── */}
        <div className="two-col section">

          {/* INPUT FORM */}
          <div className="card">
            <div className="card-title">Resource Requirements</div>
            <div className="form-grid">
              <Slider label="vCPU Cores"        name="vcpu"        min={1}  max={64}   step={1}  value={form.vcpu}        unit=""     onChange={handleChange} />
              <Slider label="RAM (GB)"           name="ram_gb"      min={1}  max={256}  step={1}  value={form.ram_gb}      unit=" GB"  onChange={handleChange} />
              <Slider label="Storage (GB)"       name="storage_gb"  min={10} max={2000} step={10} value={form.storage_gb}  unit=" GB"  onChange={handleChange} />
              <Slider label="Usage Hours/Month"  name="usage_hours" min={1}  max={744}  step={1}  value={form.usage_hours} unit=" hrs" onChange={handleChange} />
            </div>
            <button
              className={`btn-primary ${loading ? "loading" : ""}`}
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "→  Predict & Compare"}
            </button>
          </div>

          {/* PROVIDER COMPARISON */}
          <div className="card">
            <div className="card-title">Provider Comparison</div>
            {result ? (
              <div className="fade-in">
                <ProviderBars providers={result.providers} />
                <div className="rec-box">
                  <span className="rec-icon">✦</span>
                  <div className="rec-text">
                    <strong>{result.recommendation}</strong> is your best match for this workload.
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

        {/* ── STATS + CHART ── */}
        {result && (
          <div className="section fade-in">
            <div className="results-grid">
              <StatCard label="Predicted Monthly Cost" value={`$${result.predicted_monthly_cost_usd}`} sub="Based on your inputs"          type="success"  />
              <StatCard label="Recommended Provider"   value={result.recommendation}                  sub="Lowest cost for your config"    type="success" />
              <StatCard label="Potential Savings"      value={`$${result.savings_vs_most_expensive}`} sub="vs. most expensive option"      type="success" />
            </div>

            <div className="card">
              <div className="card-title">Monthly Cost — Provider Breakdown</div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={barData} margin={{ top: 0, right: 0, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                  <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" }} />
                  <YAxis tick={{ fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" }} unit="$" />
                  <Tooltip
                    contentStyle={CHART_TOOLTIP_STYLE}
                    cursor={{ fill: "rgba(255,255,255,0.03)" }}
                    formatter={(v) => [`$${v}`, "Monthly Cost"]}
                  />
                  <Bar dataKey="cost" radius={[6, 6, 0, 0]}
                    fill={barData[0]?.fill}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}