import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, Legend
} from "recharts";

import api from "../api/cloudApi";
import { PROVIDER_COLORS } from "../constants/providerColors";
import { CHART_TOOLTIP_STYLE } from "../constants/ChartTooltipStyle";

const radarData = [
  { metric: "Price", AWS: 60, Azure: 65, GCP: 75 },
  { metric: "Speed", AWS: 80, Azure: 75, GCP: 70 },
  { metric: "Regions", AWS: 90, Azure: 80, GCP: 70 },
  { metric: "Support", AWS: 75, Azure: 80, GCP: 65 },
  { metric: "Services", AWS: 90, Azure: 80, GCP: 72 },
];

const TICK_STYLE = {
  fill: "#64748b",
  fontSize: 11,
  fontFamily: "'JetBrains Mono'"
};

const LEGEND_STYLE = {
  fontSize: 11,
  fontFamily: "'JetBrains Mono'"
};

export default function TrendsPage() {

  const [trendData, setTrendData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.trends().then(data => {
      setTrendData(data);
      setLoading(false);
    });
  }, []);

  return (
    <div>

      <div className="hero">
        <div className="hero-tag"><span className="dot" />Analytics</div>
        <h1>Cost <span>trends & analysis</span></h1>
        <p>
          ML predicted cost trajectory across AWS, Azure and GCP.
        </p>
      </div>

      <div className="main">
        <div className="two-col section">

          {/* LINE CHART */}
          <div className="card">

            <div className="card-title">
              6-Month Predicted Cost Trend
            </div>

            {loading ? (
              <div className="empty">
                <div className="empty-icon">⟳</div>
                <p>Loading trend data...</p>
              </div>
            ) : (

              <ResponsiveContainer width="100%" height={260}>
                <LineChart
                  data={trendData}
                  margin={{ top: 20, right: 10, left: -25, bottom: -10 }}
                >

                  <defs>
                    <linearGradient id="awsGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={PROVIDER_COLORS.AWS} stopOpacity={0.6}/>
                      <stop offset="100%" stopColor={PROVIDER_COLORS.AWS} stopOpacity={0}/>
                    </linearGradient>

                    <linearGradient id="azureGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={PROVIDER_COLORS.Azure} stopOpacity={0.6}/>
                      <stop offset="100%" stopColor={PROVIDER_COLORS.Azure} stopOpacity={0}/>
                    </linearGradient>

                    <linearGradient id="gcpGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={PROVIDER_COLORS.GCP} stopOpacity={0.6}/>
                      <stop offset="100%" stopColor={PROVIDER_COLORS.GCP} stopOpacity={0}/>
                    </linearGradient>
                  </defs>

                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="rgba(255,255,255,0.04)"
                  />

                  <XAxis dataKey="month" tick={TICK_STYLE} />
                  <YAxis tick={TICK_STYLE} unit="$" />

                  <Tooltip
                    contentStyle={CHART_TOOLTIP_STYLE}
                    formatter={(v)=>[`$${v}`, "Cost"]}
                  />

                  <Legend wrapperStyle={LEGEND_STYLE} />

                  <Line
                    type="monotone"
                    dataKey="AWS"
                    stroke={PROVIDER_COLORS.AWS}
                    strokeWidth={3}
                    dot={{ r: 3 }}
                    activeDot={{ r: 6 }}
                  />

                  <Line
                    type="monotone"
                    dataKey="Azure"
                    stroke={PROVIDER_COLORS.Azure}
                    strokeWidth={3}
                    dot={{ r: 3 }}
                    activeDot={{ r: 6 }}
                  />

                  <Line
                    type="monotone"
                    dataKey="GCP"
                    stroke={PROVIDER_COLORS.GCP}
                    strokeWidth={3}
                    dot={{ r: 3 }}
                    activeDot={{ r: 6 }}
                  />

                </LineChart>
              </ResponsiveContainer>

            )}
          </div>

          {/* RADAR */}
          <div className="card">

            <div className="card-title">
              Provider Capability Radar
            </div>

            <ResponsiveContainer width="100%" height={250}>
              <RadarChart data={radarData}>

                <PolarGrid stroke="rgba(255,255,255,0.06)" />

                <PolarAngleAxis
                  dataKey="metric"
                  tick={TICK_STYLE}
                />

                <Radar
                  name="AWS"
                  dataKey="AWS"
                  stroke={PROVIDER_COLORS.AWS}
                  fill={PROVIDER_COLORS.AWS}
                  fillOpacity={0.15}
                />

                <Radar
                  name="Azure"
                  dataKey="Azure"
                  stroke={PROVIDER_COLORS.Azure}
                  fill={PROVIDER_COLORS.Azure}
                  fillOpacity={0.15}
                />

                <Radar
                  name="GCP"
                  dataKey="GCP"
                  stroke={PROVIDER_COLORS.GCP}
                  fill={PROVIDER_COLORS.GCP}
                  fillOpacity={0.15}
                />

                <Legend wrapperStyle={LEGEND_STYLE}/>
                <Tooltip contentStyle={CHART_TOOLTIP_STYLE}/>

              </RadarChart>
            </ResponsiveContainer>

          </div>

        </div>
      </div>
    </div>
  );
}