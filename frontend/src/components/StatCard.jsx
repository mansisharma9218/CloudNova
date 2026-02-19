export default function StatCard({ label, value, sub, type = "accent" }) {
  return (
    <div className="stat-card fade-in">
      <div className="stat-label">{label}</div>
      <div className={`stat-value ${type}`}>{value}</div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  );
}
