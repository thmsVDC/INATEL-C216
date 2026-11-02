import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App.jsx";

const questions = [
  {
    country: "Brasil",
    flag_url: "/br.png",
    choices: ["Brasil", "Japão", "Canadá", "França"],
  },
  {
    country: "Japão",
    flag_url: "/jp.png",
    choices: ["Japão", "Portugal", "Argentina", "Itália"],
  },
  {
    country: "Canadá",
    flag_url: "/ca.png",
    choices: ["Canadá", "Alemanha", "Brasil", "Estados Unidos"],
  },
  {
    country: "França",
    flag_url: "/fr.png",
    choices: ["França", "Itália", "Portugal", "Argentina"],
  },
  {
    country: "Alemanha",
    flag_url: "/de.png",
    choices: ["Alemanha", "Japão", "Coreia do Sul", "Canadá"],
  },
  {
    country: "Itália",
    flag_url: "/it.png",
    choices: ["Itália", "Brasil", "Estados Unidos", "Alemanha"],
  },
  {
    country: "Portugal",
    flag_url: "/pt.png",
    choices: ["Portugal", "França", "Japão", "Coreia do Sul"],
  },
  {
    country: "Argentina",
    flag_url: "/ar.png",
    choices: ["Argentina", "Canadá", "Itália", "Portugal"],
  },
  {
    country: "Estados Unidos",
    flag_url: "/us.png",
    choices: ["Estados Unidos", "Alemanha", "França", "Brasil"],
  },
  {
    country: "Coreia do Sul",
    flag_url: "/kr.png",
    choices: ["Coreia do Sul", "Japão", "Argentina", "Canadá"],
  },
];

describe("Quiz das Bandeiras", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => questions,
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the first flag and advances after a correct answer", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      await screen.findByRole("img", { name: "Bandeira de Brasil" }),
    ).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Brasil" }));

    expect(screen.getByRole("status")).toHaveTextContent("Resposta correta");
    expect(screen.getByText("Acertos")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Próxima bandeira" }));

    expect(screen.getByRole("img", { name: "Bandeira de Japão" })).toBeInTheDocument();
  });

  it("reveals the correct answer and resets the streak after a wrong answer", async () => {
    const user = userEvent.setup();
    render(<App />);

    await screen.findByRole("img", { name: "Bandeira de Brasil" });
    await user.click(screen.getByRole("button", { name: "Japão" }));

    expect(screen.getByRole("status")).toHaveTextContent("A resposta era Brasil");
    expect(screen.getByText("Sequência").parentElement).toHaveTextContent("0");
    expect(screen.getByRole("button", { name: "Brasil" })).toBeDisabled();
  });

  it("completes the quiz and can start a new round", async () => {
    const user = userEvent.setup();
    render(<App />);

    await screen.findByRole("img", { name: "Bandeira de Brasil" });
    for (const country of [
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
    ]) {
      await user.click(screen.getByRole("button", { name: country }));
      const nextLabel =
        country === "Coreia do Sul" ? "Ver resultado" : "Próxima bandeira";
      await user.click(screen.getByRole("button", { name: nextLabel }));
    }

    expect(screen.getByRole("heading", { name: "Perfeito!" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Perfeito!" })).toHaveTextContent(
      /Você acertou 10 de 10/,
    );

    await user.click(screen.getByRole("button", { name: /Jogar novamente/ }));
    expect(
      await screen.findByRole("img", { name: "Bandeira de Brasil" }),
    ).toBeInTheDocument();
  });
});
