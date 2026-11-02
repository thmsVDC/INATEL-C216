import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App.jsx";

const countries = [
  "Brasil",
  "Japão",
  "Canadá",
  "França",
  "Alemanha",
  "Itália",
  "Portugal",
  "Argentina",
  "Estados Unidos",
  "Coreia do Sul",
];

function mockGameApi() {
  let index = 0;
  let score = 0;
  let streak = 0;
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url, options = {}) => {
      if (url === "/api/v1/games") {
        return {
          ok: true,
          json: async () => ({
            id: 7,
            flag_url: "/flags/br.png",
            score,
            streak,
            is_active: true,
            choices: [countries[0], "Japão", "Canadá", "França"],
          }),
        };
      }

      const { answer, finish } = JSON.parse(options.body);
      const isCorrect = answer === countries[index];
      if (isCorrect) {
        score += 1;
        streak += 1;
      } else {
        streak = 0;
      }
      const correctCountry = countries[index];
      index += 1;
      const nextCountry = countries[index] || correctCountry;
      return {
        ok: true,
        json: async () => ({
          is_correct: isCorrect,
          correct_country: isCorrect ? null : correctCountry,
          game: {
            id: 7,
            flag_url: `/flags/${index}.png`,
            score,
            streak,
            is_active: !finish,
            choices: [
              nextCountry,
              ...countries.filter((country) => country !== nextCountry).slice(0, 3),
            ],
          },
        }),
      };
    }),
  );
}

describe("Quiz das Bandeiras", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("persists answers through the games API and completes a round", async () => {
    mockGameApi();
    const user = userEvent.setup();
    render(<App />);

    expect(
      await screen.findByRole("img", { name: "Bandeira do desafio atual" }),
    ).toBeInTheDocument();

    for (let index = 0; index < 10; index += 1) {
      const country = countries[index];
      await user.click(screen.getByRole("button", { name: country, exact: true }));
      expect(await screen.findByRole("status")).toHaveTextContent("Resposta correta");
      if (index < 9) {
        await user.click(screen.getByRole("button", { name: "Próxima bandeira" }));
      }
    }

    await user.click(screen.getByRole("button", { name: "Ver resultado" }));
    expect(await screen.findByRole("heading", { name: "Perfeito!" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Perfeito!" })).toHaveTextContent(
      /Você acertou 10 de 10 bandeiras/,
    );
    expect(fetch).toHaveBeenCalledTimes(11);
    expect(fetch).toHaveBeenLastCalledWith(
      "/api/v1/games/7/guess",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("shows a useful message when the backend cannot be reached", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    render(<App />);

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível conectar",
    );
    expect(screen.getByRole("button", { name: /Tentar novamente/ })).toBeInTheDocument();
  });
});
