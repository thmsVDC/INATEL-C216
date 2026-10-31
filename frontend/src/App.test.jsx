import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import App from "./App.jsx";

describe("Quiz das Bandeiras", () => {
  it("shows the first flag and advances after a correct answer", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByRole("img", { name: "Bandeira de Brasil" })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Brasil" }));

    expect(screen.getByRole("status")).toHaveTextContent("Resposta correta");
    expect(screen.getByText("Acertos")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Próxima bandeira" }));

    expect(screen.getByRole("img", { name: "Bandeira de Japão" })).toBeInTheDocument();
  });

  it("reveals the correct answer and resets the streak after a wrong answer", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "Japão" }));

    expect(screen.getByRole("status")).toHaveTextContent("A resposta era Brasil");
    expect(screen.getByText("Sequência").parentElement).toHaveTextContent("0");
    expect(screen.getByRole("button", { name: "Brasil" })).toBeDisabled();
  });

  it("completes the quiz and can start a new round", async () => {
    const user = userEvent.setup();
    render(<App />);

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
    expect(screen.getByRole("img", { name: "Bandeira de Brasil" })).toBeInTheDocument();
  });
});
