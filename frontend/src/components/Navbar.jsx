export default function Navbar({ page, setPage }) {
  return (
    <nav>
      <div className="nav-logo">
        <img src="/cloudnova_logo.svg" alt="CloudNova" style={{ width: "20px", height: "20px", marginRight: "0.5rem", verticalAlign: "top" }} />
          CloudNova
      </div>
      <div className="nav-tabs">
        {[
          ["advisor", "Advisor"],
          ["pricing", "Pricing"],
          ["trends",  "Trends" ],
        ].map(([id, label]) => (
          <button
            key={id}
            className={`nav-tab ${page === id ? "active" : ""}`}
            onClick={() => setPage(id)}
          >
            {label}
          </button>
        ))}
      </div>
    </nav>
  );
}