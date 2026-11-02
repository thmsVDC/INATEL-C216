export default function ResultScreen({ score, total, onRestart }) {
  const perfect = score === total;

  return (
    <section aria-labelledby="result-title" className="mx-auto max-w-xl text-center">
      <div className="mx-auto mb-6 grid size-20 place-items-center rounded-3xl border border-cyan-300/20 bg-cyan-300/10 text-4xl">
        {perfect ? "🏆" : score >= total * 0.6 ? "🌍" : "🧭"}
      </div>
      <p className="mb-2 text-sm font-bold uppercase tracking-[0.24em] text-cyan-300">
        rodada concluída
      </p>
      <h1 className="text-4xl font-black tracking-tight text-white" id="result-title">
        {perfect ? "Perfeito!" : "Boa viagem!"}
      </h1>
      <p className="mt-4 text-lg text-slate-300">
        Você acertou <strong className="text-white">{score}</strong> de {total} bandeiras.
      </p>
      <div className="my-8 rounded-3xl border border-white/10 bg-white/5 p-6">
        <p className="text-sm text-slate-400">Sua pontuação</p>
        <p className="mt-1 text-5xl font-black text-cyan-300">
          {Math.round((score / total) * 100)}%
        </p>
      </div>
      <button className="button-primary" onClick={onRestart} type="button">
        Jogar novamente <span aria-hidden="true">↻</span>
      </button>
    </section>
  );
}
