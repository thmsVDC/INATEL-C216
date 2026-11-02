export default function App() {
  return (
    <main className="page-shell">
      <header className="site-header">
        <a aria-label="OrganizaJá, início" className="brand" href="/">
          <span aria-hidden="true" className="brand-mark">
            OJ
          </span>
          <span>OrganizaJá</span>
        </a>
      </header>

      <section aria-labelledby="welcome-title" className="welcome-card">
        <p className="eyebrow">Eventos acadêmicos em um só lugar</p>
        <h1 id="welcome-title">Organize, participe, aproveite.</h1>
        <p className="intro">
          Encontre eventos da comunidade acadêmica e acompanhe suas inscrições.
        </p>
        <p className="setup-note">A plataforma está sendo preparada.</p>
      </section>
    </main>
  );
}
