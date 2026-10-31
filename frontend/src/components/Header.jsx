export default function Header() {
  return (
    <header className="flex items-center justify-between gap-4">
      <a
        aria-label="Quiz das Bandeiras, início"
        className="flex items-center gap-3"
        href="/"
      >
        <span className="grid size-11 place-items-center rounded-2xl bg-cyan-300 text-xl text-slate-950 shadow-lg shadow-cyan-950/40">
          ⚑
        </span>
        <span>
          <span className="block text-sm font-bold tracking-wide text-white">
            MUNDO EM JOGO
          </span>
          <span className="block text-xs text-slate-400">quiz das bandeiras</span>
        </span>
      </a>
    </header>
  );
}
