import { useCallback, useEffect, useState } from "react";

import { createGame, submitGuess } from "./api/games.js";
import Header from "./components/Header.jsx";
import ResultScreen from "./components/ResultScreen.jsx";

export default function App() {
  const [game, setGame] = useState(null);
  const [displayQuestion, setDisplayQuestion] = useState(null);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [guessResult, setGuessResult] = useState(null);
  const [isFinished, setIsFinished] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [actionError, setActionError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const loadQuestions = useCallback(async () => {
    setIsLoading(true);
    setLoadError("");
    try {
      const nextGame = await createGame();
      setGame(nextGame);
      setDisplayQuestion({ flag_url: nextGame.flag_url, choices: nextGame.choices });
      setQuestionIndex(0);
      setSelectedAnswer(null);
      setGuessResult(null);
      setIsFinished(false);
      setActionError("");
    } catch (error) {
      setLoadError(error.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  const question = displayQuestion
    ? {
        image: displayQuestion.flag_url,
        choices: displayQuestion.choices,
      }
    : null;
  const isCorrect = guessResult?.is_correct;
  const progress = isFinished ? 100 : game ? ((questionIndex + 1) / 10) * 100 : 0;

  async function chooseAnswer(answer) {
    if (selectedAnswer !== null || !question || !game?.is_active || isSubmitting) return;
    setSelectedAnswer(answer);
    await saveGuess(answer);
  }

  async function saveGuess(answer = selectedAnswer) {
    if (!game || answer === null || isSubmitting) return;
    const finish = questionIndex === 9;
    setIsSubmitting(true);
    setActionError("");
    try {
      const result = await submitGuess(game.id, answer, finish);
      setGame(result.game);
      setGuessResult(result);
    } catch (error) {
      setActionError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function goToNextQuestion() {
    if (!game || !guessResult) return;
    if (questionIndex === 9) {
      setIsFinished(true);
      return;
    }
    setDisplayQuestion({ flag_url: game.flag_url, choices: game.choices });
    setQuestionIndex((currentIndex) => currentIndex + 1);
    setSelectedAnswer(null);
    setGuessResult(null);
    setActionError("");
  }

  return (
    <main className="min-h-screen overflow-hidden px-4 py-6 text-slate-100 sm:px-8 sm:py-10">
      <div aria-hidden="true" className="ambient ambient-one" />
      <div aria-hidden="true" className="ambient ambient-two" />
      <div className="relative mx-auto flex min-h-[calc(100vh-3rem)] max-w-6xl flex-col">
        <Header />

        <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col justify-center py-12">
          {isLoading ? (
            <p aria-live="polite" className="text-center text-slate-300" role="status">
              Carregando bandeiras...
            </p>
          ) : loadError ? (
            <section className="text-center" role="alert">
              <h1 className="text-3xl font-black text-white">
                Não foi possível iniciar o quiz
              </h1>
              <p className="mt-4 text-slate-300">{loadError}</p>
              <button
                className="button-primary mt-6"
                onClick={loadQuestions}
                type="button"
              >
                Tentar novamente <span aria-hidden="true">↻</span>
              </button>
            </section>
          ) : isFinished ? (
            <ResultScreen onRestart={loadQuestions} score={game?.score ?? 0} total={10} />
          ) : question ? (
            <>
              <div className="mb-7 text-center">
                <p className="mb-3 text-sm font-bold uppercase tracking-[0.25em] text-cyan-300">
                  Uma volta pelo mundo
                </p>
                <h1 className="text-4xl font-black tracking-tight text-white sm:text-5xl">
                  De onde é esta bandeira?
                </h1>
                <p className="mx-auto mt-4 max-w-lg text-base leading-7 text-slate-400">
                  Escolha o país correspondente. São 10 desafios para testar seu
                  conhecimento.
                </p>
              </div>

              <div className="mb-5 flex items-center justify-between text-sm">
                <span className="font-semibold text-slate-300">
                  Bandeira <span className="text-white">{questionIndex + 1}</span> de 10
                </span>
                <div className="flex gap-5 text-slate-400">
                  <span>
                    Acertos <strong className="ml-1 text-white">{game.score}</strong>
                  </span>
                  <span>
                    Sequência <strong className="ml-1 text-white">{game.streak}</strong>
                  </span>
                </div>
              </div>

              <div
                aria-label={["Progresso: ", questionIndex + 1, " de ", 10].join("")}
                className="mb-7 h-2 overflow-hidden rounded-full bg-white/10"
                role="progressbar"
                aria-valuemax={10}
                aria-valuemin={0}
                aria-valuenow={questionIndex + 1}
              >
                <div
                  className="h-full rounded-full bg-cyan-300 transition-all duration-500"
                  style={{ width: [progress, "%"].join("") }}
                />
              </div>

              <section
                aria-label={["Desafio ", questionIndex + 1].join("")}
                className="rounded-[2rem] border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-black/30 backdrop-blur sm:p-8"
              >
                <div className="grid min-h-48 place-items-center rounded-3xl border border-white/5 bg-slate-950/70 p-6 sm:min-h-60">
                  <img
                    alt="Bandeira do desafio atual"
                    className="max-h-40 w-full max-w-sm object-contain drop-shadow-2xl sm:max-h-48"
                    src={question.image}
                  />
                </div>

                <div className="mt-6 grid gap-3 sm:grid-cols-2">
                  {question.choices.map((choice, index) => {
                    const isSelected = selectedAnswer === choice;
                    const isAnswer = guessResult?.correct_country === choice;
                    const stateClass =
                      selectedAnswer === null
                        ? "answer-idle"
                        : isAnswer
                          ? "answer-correct"
                          : isSelected
                            ? "answer-wrong"
                            : "answer-muted";

                    return (
                      <button
                        aria-label={choice}
                        aria-pressed={isSelected}
                        className={["answer-button", stateClass].join(" ")}
                        disabled={selectedAnswer !== null}
                        key={choice}
                        onClick={() => chooseAnswer(choice)}
                        type="button"
                      >
                        <span className="mr-3 text-xs font-bold text-slate-500">
                          0{index + 1}
                        </span>
                        {choice}
                        {isAnswer && <span className="ml-auto">✓</span>}
                        {isSelected && !isCorrect && <span className="ml-auto">×</span>}
                      </button>
                    );
                  })}
                </div>

                {actionError && (
                  <p className="mt-4 text-center text-rose-300" role="alert">
                    {actionError}
                  </p>
                )}
                {selectedAnswer !== null && actionError && !guessResult && (
                  <button
                    className="button-primary mt-4 w-full"
                    onClick={() => saveGuess()}
                    type="button"
                  >
                    Tentar salvar resposta novamente
                  </button>
                )}
                {selectedAnswer !== null && guessResult && (
                  <div aria-live="polite" className="mt-5" role="status">
                    <p
                      className={
                        "text-center text-sm font-bold " +
                        (isCorrect ? "text-emerald-300" : "text-rose-300")
                      }
                    >
                      {isCorrect
                        ? "Resposta correta! Mandou bem."
                        : [
                            "Quase! A resposta era ",
                            guessResult.correct_country,
                            ".",
                          ].join("")}
                    </p>
                    <button
                      className="button-primary mt-4 w-full"
                      onClick={goToNextQuestion}
                      type="button"
                    >
                      {isSubmitting
                        ? "Salvando..."
                        : questionIndex === 9
                          ? "Ver resultado"
                          : "Próxima bandeira"}
                      <span aria-hidden="true">→</span>
                    </button>
                  </div>
                )}
              </section>
            </>
          ) : null}
        </div>

        <footer className="flex flex-col items-center justify-between gap-2 border-t border-white/10 pt-5 text-xs text-slate-500 sm:flex-row">
          <span>Quiz das Bandeiras</span>
        </footer>
      </div>
    </main>
  );
}
