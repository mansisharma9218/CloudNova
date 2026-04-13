const NAV_TABS = [
  { id: "advisor",  label: "Advisor" },
  { id: "pricing",  label: "Pricing" },
  { id: "insights", label: "Insights" },
];

export default function Navbar({ page, setPage, logout }) {
  return (
    <nav className="navbar">
      <div className="nav-logo">
        <img src="/cloudnova_logo.svg" alt="CloudNova" className="nav-logo-img" />
        <span>CloudNova</span>
      </div>

      <div className="nav-tabs">
        {NAV_TABS.map(({ id, label }) => (
          <button
            key={id}
            className={`nav-tab ${page === id ? "active" : ""}`}
            onClick={() => setPage(id)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="nav-actions">
        <button className="nav-tab logout-btn" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}
