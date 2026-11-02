const QUIZ_SIZE = 10;

export async function fetchQuizQuestions() {
  const response = await fetch(`/api/v1/flags/quiz?count=${QUIZ_SIZE}`);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(payload?.detail || "Não foi possível carregar as bandeiras agora.");
  }

  if (!Array.isArray(payload) || payload.length === 0) {
    throw new Error("A API não retornou perguntas para o quiz.");
  }

  return payload.map(({ country, flag_url, choices }) => ({
    country,
    image: flag_url,
    choices,
  }));
}
