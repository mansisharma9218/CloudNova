import { useState, useEffect } from "react";
import {
  ScatterChart, Scatter, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer, ReferenceLine,
  BarChart, Bar, Cell,
} from "recharts";

import api from "../api/cloudApi";
import { CHART_TOOLTIP_STYLE } from "../constants/ChartTooltipStyle";

const TICK = { fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" };

// Colour scale for feature importance bars
const FI_COLORS = [
  "#5ba6fb", "#64abfd", "#7bbdfe", "#36cb72",
  "#4ade80", "#fbbf24", "#f87171", "#a78bfa",
];

function MetricCard({ label, value, sub, color = "var(--accent)" }) {
  return (
    <div className="stat-card fade-in">
      <div className="stat-label">{label}</div>
      <div style={{ fontFamily: "var(--font-head)", fontSize: "1.9rem", fontWeight: 800, color }}>
        {value}
      </div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  );
}

function SectionTitle({ children }) {
  return (
    <div className="card-title" style={{ marginBottom: "1.25rem" }}>
      {children}
    </div>
  );
}

// Perfect-prediction reference line tooltip
const ScatterTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const { actual, predicted } = payload[0].payload;
  const err = Math.abs(actual - predicted).toFixed(4);
  return (
    <div style={{ ...CHART_TOOLTIP_STYLE, padding: "0.6rem 0.9rem" }}>
      <div style={{ color: "#e2e8f0", fontSize: 11 }}>Actual:    <strong>${actual}/hr</strong></div>
      <div style={{ color: "#e2e8f0", fontSize: 11 }}>Predicted: <strong>${predicted}/hr</strong></div>
      <div style={{ color: "#64748b", fontSize: 10 }}>Error: ${err}</div>
    </div>
  );
};

export default function InsightsPage() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    api.insights()
      .then(setData)
      .catch(() => setError("Failed to load model insights."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Model Insights</div>
        <h1>Model <span>performance & analysis</span></h1>
      </div>
      <div className="main">
        <div className="empty"><div className="empty-icon">⟳</div><p>Loading insights...</p></div>
      </div>
    </div>
  );

  if (error) return (
    <div className="main" style={{ paddingTop: "3rem" }}>
      <div className="empty"><p style={{ color: "var(--danger)" }}>{error}</p></div>
    </div>
  );

  const { metrics, pred_vs_actual, feature_importance, model_info } = data;

  // Scatter data: convert to {x, y} for recharts Scatter
  const scatterData = pred_vs_actual.map((p) => ({
    actual:    p.actual,
    predicted: p.predicted,
    x: p.actual,
    y: p.predicted,
  }));

  // Perfect prediction line extent
  const maxVal = Math.max(...pred_vs_actual.map((p) => Math.max(p.actual, p.predicted)));

  // Prediction → Recommendation flow steps (corrected 6-step version)
  const flowSteps = [
    {
      step: "01",
      title: "Input",
      desc: "User specifies vCPU, RAM, storage, instance runtime, region and pricing model.",
    },
    {
      step: "02",
      title: "Cost Prediction (ML)",
      desc: "Random Forest predicts price_per_hour from input features. Monthly cost = price_per_hour × usage_hours.",
    },
    {
      step: "03",
      title: "Candidate Generation",
      desc: "All valid configurations across providers, regions, and pricing models are generated. Constraint: vcpu ≥ required AND ram ≥ required.",
    },
    {
      step: "04",
      title: "Cost Estimation for Candidates",
      desc: "For each candidate: use exact pricing lookup if available; otherwise use ML model prediction to estimate price_per_hour.",
    },
    {
      step: "05",
      title: "Ranking & Selection",
      desc: "Monthly cost is computed for all candidates. Results are sorted ascending and the top-N cheapest options are selected.",
    },
    {
      step: "06",
      title: "Output",
      desc: "Returns provider, region, pricing model, price_per_hour, monthly_cost, and source (exact / ML) per recommendation. Cheapest option is highlighted.",
    },
  ];

  return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Model Insights</div>
        <h1>ML Model <span>performance & explainability</span></h1>
        <p>
          Live metrics, predicted vs actual accuracy, and feature importance
          from the Random Forest model powering CloudNova's cost predictions.
        </p>
      </div>

      <div className="main">

        {/* ── METRIC CARDS ── */}
        <div className="results-grid section">
          <MetricCard
            label="Mean Absolute Error"
            value={`$${metrics.mae}/hr`}
            sub="Average hourly prediction error"
            color="var(--success)"
          />
          <MetricCard
            label="RMSE"
            value={`$${metrics.rmse}/hr`}
            sub="Root mean squared error"
            color="var(--accent)"
          />
          <MetricCard
            label="R² Score"
            value={metrics.r2}
            sub={`${metrics.n_train.toLocaleString()} train · ${metrics.n_test.toLocaleString()} test samples`}
            color="var(--accent2)"
          />
        </div>

        <div className="two-col section">

          {/* ── PREDICTED VS ACTUAL SCATTER ── */}
          <div className="card">
            <SectionTitle>Predicted vs Actual ($/hr)</SectionTitle>
            <p style={{ fontSize: "0.72rem", color: "var(--muted)", marginBottom: "1.25rem", lineHeight: 1.6 }}>
              Each dot is one test-set instance. Points on the diagonal line are perfect predictions.
              Tighter clustering = higher accuracy.
            </p>
            <ResponsiveContainer width="100%" height={280}>
              <ScatterChart margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis
                  type="number" dataKey="x" name="Actual"
                  tick={TICK} label={{ value: "Actual ($/hr)", position: "insideBottom", offset: 2, fill: "#64748b", fontSize: 10 }}
                  domain={[0, maxVal + 0.05]}
                  tickFormatter={(v) => `$${v.toFixed(2)}`}
                />
                <YAxis
                  type="number" dataKey="y" name="Predicted"
                  tick={TICK}
                  domain={[0, maxVal + 0.05]}
                  tickFormatter={(v) => `$${v.toFixed(2)}`}
                />
                <Tooltip content={<ScatterTooltip />} cursor={{ strokeDasharray: "3 3" }} />
                {/* Perfect prediction diagonal */}
                <ReferenceLine
                  segment={[{ x: 0, y: 0 }, { x: maxVal, y: maxVal }]}
                  stroke="rgba(54,203,114,0.35)"
                  strokeDasharray="5 3"
                  label={{ value: "Perfect", fill: "rgba(54,203,114,0.5)", fontSize: 10, position: "insideTopLeft" }}
                />
                <Scatter
                  data={scatterData}
                  fill="var(--accent)"
                  fillOpacity={0.55}
                  r={3}
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {/* ── FEATURE IMPORTANCE ── */}
          <div className="card">
            <SectionTitle>Feature Importance (%)</SectionTitle>
            <p style={{ fontSize: "0.72rem", color: "var(--muted)", marginBottom: "1.25rem", lineHeight: 1.6 }}>
              How much each feature contributes to the model's predictions.
              Higher = stronger predictor of hourly cost.
            </p>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart
                data={feature_importance}
                layout="vertical"
                margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" horizontal={false} />
                <XAxis
                  type="number" dataKey="importance"
                  tick={TICK} tickFormatter={(v) => `${v}%`}
                  domain={[0, Math.ceil(feature_importance[0]?.importance * 1.1)]}
                />
                <YAxis
                  type="category" dataKey="label" width={110}
                  tick={{ ...TICK, fontSize: 10 }}
                />
                <Tooltip
                  contentStyle={{
                    ...CHART_TOOLTIP_STYLE,
                    color: "#ffffff",
                  }}
                  labelStyle={{ color: "#ffffff" }}
                  itemStyle={{ color: "#ffffff" }}
                  formatter={(v) => [`${v}%`, "Importance"]}
                  cursor={{ fill: "rgba(255,255,255,0.03)" }}
                />
                <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                  {feature_importance.map((_, i) => (
                    <Cell key={i} fill={FI_COLORS[i % FI_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* ── HOW THE MODEL WORKS ── */}
        <div className="card section">
          <SectionTitle>How the Model Works</SectionTitle>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem" }}>

            {/* Left: algorithm + features */}
            <div>
              <div style={{ fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "var(--muted)", marginBottom: "0.6rem" }}>
                Algorithm
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1.5rem" }}>
                <span style={{
                  background: "rgba(91,166,251,0.1)", border: "1px solid rgba(91,166,251,0.25)",
                  color: "var(--accent)", padding: "0.35rem 0.9rem", borderRadius: "8px",
                  fontFamily: "var(--font-mono)", fontSize: "0.8rem",
                }}>
                  {model_info.algorithm}
                </span>
                <span style={{ fontSize: "0.75rem", color: "var(--muted)" }}>
                  {model_info.n_estimators} trees · max depth {model_info.max_depth}
                </span>
              </div>

              <div style={{ fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "var(--muted)", marginBottom: "0.75rem" }}>
                Input Features
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {model_info.features.map((f, i) => (
                  <div key={i} style={{ display: "flex", gap: "0.75rem", alignItems: "flex-start" }}>
                    <span style={{
                      background: `${FI_COLORS[i % FI_COLORS.length]}18`,
                      border: `1px solid ${FI_COLORS[i % FI_COLORS.length]}33`,
                      color: FI_COLORS[i % FI_COLORS.length],
                      padding: "0.15rem 0.5rem", borderRadius: "5px",
                      fontFamily: "var(--font-mono)", fontSize: "0.7rem",
                      whiteSpace: "nowrap", flexShrink: 0,
                    }}>
                      {f.name}
                    </span>
                    <span style={{ fontSize: "0.72rem", color: "var(--muted)", lineHeight: 1.5 }}>
                      {f.description}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: corrected 6-step prediction flow */}
            <div>
              <div style={{ fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "var(--muted)", marginBottom: "0.75rem" }}>
                Prediction → Recommendation Flow
              </div>

              {flowSteps.map(({ step, title, desc }) => (
                <div key={step} style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
                  <div style={{
                    flexShrink: 0, width: "28px", height: "28px", borderRadius: "50%",
                    background: "rgba(91,166,251,0.1)", border: "1px solid rgba(91,166,251,0.25)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontFamily: "var(--font-mono)", fontSize: "0.6rem", color: "var(--accent)",
                  }}>
                    {step}
                  </div>
                  <div>
                    <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text)", marginBottom: "0.2rem" }}>
                      {title}
                    </div>
                    <div style={{ fontSize: "0.7rem", color: "var(--muted)", lineHeight: 1.55 }}>
                      {desc}
                    </div>
                  </div>
                </div>
              ))}

              <div style={{
                marginTop: "1rem",
                background: "rgba(54,203,114,0.06)", border: "1px solid rgba(54,203,114,0.2)",
                borderRadius: "8px", padding: "0.85rem",
                fontSize: "0.72rem", color: "var(--muted)", lineHeight: 1.6,
              }}>
                <strong style={{ color: "var(--success)" }}>Key constraint: </strong>
                The ML model performs regression, not classification. It always predicts a
                continuous cost value. Recommendations are generated by ranking all valid
                candidates based on their predicted (or exact) cost and selecting the cheapest.
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}