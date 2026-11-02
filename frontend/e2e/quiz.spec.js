import { expect, test } from "@playwright/test";

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

test("the user completes a flag quiz with answers persisted by the API", async ({
  page,
}) => {
  let index = 0;
  let score = 0;
  let streak = 0;
  await page.route("**/api/v1/games**", async (route) => {
    if (
      route.request().method() === "POST" &&
      !route.request().url().endsWith("/guess")
    ) {
      await route.fulfill({
        json: {
          id: 1,
          flag_url: "https://example.com/0.png",
          score,
          streak,
          is_active: true,
          choices: [countries[0], "Canadá", "França", "Japão"],
        },
      });
      return;
    }

    const { answer, finish } = route.request().postDataJSON();
    const correctCountry = countries[index];
    const isCorrect = answer === correctCountry;
    if (isCorrect) {
      score += 1;
      streak += 1;
    } else {
      streak = 0;
    }
    index += 1;
    await route.fulfill({
      json: {
        is_correct: isCorrect,
        correct_country: isCorrect ? null : correctCountry,
        game: {
          id: 1,
          flag_url: `https://example.com/${index}.png`,
          score,
          streak,
          is_active: !finish,
          choices: [
            countries[index] || correctCountry,
            ...countries
              .filter((name) => name !== (countries[index] || correctCountry))
              .slice(0, 3),
          ],
        },
      },
    });
  });

  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "De onde é esta bandeira?" }),
  ).toBeVisible();

  for (let round = 0; round < 10; round += 1) {
    await page.getByRole("button", { name: countries[round], exact: true }).click();
    await expect(page.getByRole("status")).toContainText("Resposta correta");
    if (round < 9) {
      await page.getByRole("button", { name: "Próxima bandeira" }).click();
    }
  }

  await page.getByRole("button", { name: "Ver resultado" }).click();
  await expect(page.getByRole("heading", { name: "Perfeito!" })).toBeVisible();
  await expect(page.getByText("100%", { exact: true })).toBeVisible();
});
