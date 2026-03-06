import { useState, useEffect } from "react";
import api from "../api/cloudApi";

export default function PricingPage() {
  const [data,    setData]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState("All");

  useEffect(() => {
    api.pricing().then(d => { setData(d); setLoading(false); });
  }, []);

  let filtered = filter === "All"
  ? data
  : data.filter(r => r.provider === filter);

// limit rows per provider
  const providerCounts = {};
  filtered = filtered.filter(row => {
   const p = row.provider;
    providerCounts[p] = (providerCounts[p] || 0) + 1;
    return providerCounts[p] <= 40;
  });

  return (
    <div>
      <div className="hero">
        <div className="hero-tag"><span className="dot" />Live Pricing</div>
        <h1>Cloud <span>pricing table</span></h1>
        <p>
          Browse and compare instance types across AWS, Azure, and GCP.
          Data is fetched live from the backend.
        </p>
      </div>

      <div className="main">
        <div className="card section">

          {/* ── HEADER + FILTER TABS ── */}
          <div className="card-title" style={{ justifyContent: "space-between" }}>
            <span>Instance Pricing</span>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              {["All", "AWS", "Azure", "GCP"].map(p => (
                <button
                  key={p}
                  onClick={() => setFilter(p)}
                  className={`nav-tab ${filter === p ? "active" : ""}`}
                  style={{ padding: "0.3rem 0.75rem" }}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* ── TABLE ── */}
          {loading ? (
            <div className="empty">
              <div className="empty-icon">⟳</div>
              <p>Loading pricing data...</p>
            </div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Provider</th>
                    <th>Instance</th>
                    <th>vCPU</th>
                    <th>RAM (GB)</th>
                    <th>$/Hour</th>
                    <th>$/Month (est.)</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((row, i) => (
                    <tr key={i}>
                      <td>
                        <span className={`badge badge-${row.provider.toLowerCase()}`}>
                          {row.provider}
                        </span>
                      </td>
                      <td>{row.instance}</td>
                      <td>{row.vcpu}</td>
                      <td>{row.ram}</td>
                      <td>${row.price.toFixed(4)}</td>
                      <td>${(row.price * 720).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}