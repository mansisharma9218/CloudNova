export default function LoginPage({ login }) {
  return (
    <div className="login-wrapper">
      <div className="login-card fade-in">
        <div className="login-logo">
          <img src="/cloudnova_logo.svg" alt="CloudNova" />
          <h1>CloudNova</h1>
        </div>

        <p className="login-subtitle">
          Smart Cloud Resource Advisor
        </p>

        <button className="btn-primary login-btn" onClick={login}>
          Sign in with Google
        </button>
      </div>
    </div>
  );
}