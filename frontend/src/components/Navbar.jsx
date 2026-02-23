export default function Navbar({ page, setPage, logout }) {
  return (
    <nav className="navbar">
      
      <div className="nav-logo">
        <img
          src="/cloudnova_logo.svg"
          alt="CloudNova"
          className="nav-logo-img"
        />
        <span>CloudNova</span>
      </div>

      <div className="nav-tabs">
        {["advisor", "pricing", "trends"].map((id) => (
          <button
            key={id}
            className={`nav-tab ${page === id ? "active" : ""}`}
            onClick={() => setPage(id)}
          >
            {id}
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