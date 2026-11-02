const GAMES_URL = "/api/v1/games";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(path, {
      ...options,
      headers: { "Content-Type": "application/json", ...options.headers },
    });
  } catch {
    throw new Error(
      "Não foi possível conectar ao servidor. Verifique se a aplicação está ativa.",
    );
  }

  const payload =
    response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(payload?.detail || "Não foi possível concluir a operação.");
  }
  return payload;
}

export const listGames = (limit = 50) => request(`${GAMES_URL}?limit=${limit}`);
export const getGame = (id) => request(`${GAMES_URL}/${id}`);
export const createGame = () => request(GAMES_URL, { method: "POST" });
export const replaceGame = (id, game) =>
  request(`${GAMES_URL}/${id}`, {
    method: "PUT",
    body: JSON.stringify(game),
  });
export const updateGame = (id, changes) =>
  request(`${GAMES_URL}/${id}`, {
    method: "PATCH",
    body: JSON.stringify(changes),
  });
export const submitGuess = (id, answer, finish = false) =>
  request(`${GAMES_URL}/${id}/guess`, {
    method: "POST",
    body: JSON.stringify({ answer, finish }),
  });
export const deleteGame = (id) => request(`${GAMES_URL}/${id}`, { method: "DELETE" });
