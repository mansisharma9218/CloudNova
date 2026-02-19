import { PROVIDER_COLORS } from "../constants/providerColors";

export default function ProviderBars({ providers }) {
  const max  = Math.max(...Object.values(providers));
  const best = Object.entries(providers).sort((a, b) => a[1] - b[1])[0][0];

  return (
    <div className="provider-list">
      {Object.entries(providers).map(([name, cost]) => (
        <div className="provider-row" key={name}>
          <span className="provider-name">{name}</span>
          <div className="provider-bar-wrap">
            <div
              className="provider-bar"
              style={{
                width:      `${(cost / max) * 100}%`,
                background: PROVIDER_COLORS[name],
              }}
            />
          </div>
          <span className="provider-cost">
            ${cost}
            {name === best && <span className="badge-best">BEST</span>}
          </span>
        </div>
      ))}
    </div>
  );
}