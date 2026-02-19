import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, Legend,
} from "recharts";
import { PROVIDER_COLORS }    from "../constants/providerColors";
import { CHART_TOOLTIP_STYLE } from "../constants/ChartTooltipStyle";

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];

const trendData = MONTHS.map((m, i) => ({
  month: m,
  AWS:   +(28 + Math.sin(i) * 4 + i * 1.2).toFixed(2),
  Azure: +(26 + Math.cos(i) * 3 + i * 1.0).toFixed(2),
  GCP:   +(24 + Math.sin(i + 1) * 2 + i * 0.9).toFixed(2),
}));

const radarData = [
  { metric: "Price",    AWS: 60, Azure: 65, GCP: 75 },
  { metric: "Speed",    AWS: 80, Azure: 75, GCP: 70 },
  { metric: "Regions",  AWS: 90, Azure: 80, GCP: 70 },
  { metric: "Support",  AWS: 75, Azure: 80, GCP: 65 },
  { metric: "Services", AWS: 90, Azure: 80, GCP: 72 },
];

const TICK_STYLE = { fill: "#64748b", fontSize: 11, fontFamily: "'JetBrains Mono'" };
const LEGEND_STYLE = { fontSize: 11, fontFamily: "'JetBrains Mono'" };

export default function TrendsPage() {
  return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Analytics</div>
        <h1>Cost <span>trends &amp; analysis</span></h1>
        <p>
          Visualize estimated cost trajectories and a multi-dimension
          provider comparison radar.
        </p>
      </div>

      <div className="main">
        <div className="two-col section">

          {/* ── LINE CHART ── */}
          <div className="card">
            <div className="card-title">
              6-Month Cost Trend (sample 4 vCPU / 8GB workload)
            </div>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart
                data={trendData}
                margin={{ top: 0, right: 0, left: -10, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="month" tick={TICK_STYLE} />
                <YAxis tick={TICK_STYLE} unit="$" />
                <Tooltip contentStyle={CHART_TOOLTIP_STYLE} />
                <Legend wrapperStyle={LEGEND_STYLE} />
                <Line type="monotone" dataKey="AWS"   stroke={PROVIDER_COLORS.AWS}   strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Azure" stroke={PROVIDER_COLORS.Azure} strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="GCP"   stroke={PROVIDER_COLORS.GCP}   strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* ── RADAR CHART ── */}
          <div className="card">
            <div className="card-title">Provider Capability Radar</div>
            <ResponsiveContainer width="100%" height={240}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.06)" />
                <PolarAngleAxis dataKey="metric" tick={TICK_STYLE} />
                <Radar name="AWS"   dataKey="AWS"   stroke={PROVIDER_COLORS.AWS}   fill={PROVIDER_COLORS.AWS}   fillOpacity={0.1} />
                <Radar name="Azure" dataKey="Azure" stroke={PROVIDER_COLORS.Azure} fill={PROVIDER_COLORS.Azure} fillOpacity={0.1} />
                <Radar name="GCP"   dataKey="GCP"   stroke={PROVIDER_COLORS.GCP}   fill={PROVIDER_COLORS.GCP}   fillOpacity={0.1} />
                <Legend wrapperStyle={LEGEND_STYLE} />
                <Tooltip contentStyle={CHART_TOOLTIP_STYLE} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>
    </div>
  );
}
