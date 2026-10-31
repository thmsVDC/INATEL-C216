import { expect, test } from "@playwright/test";

const questions = [
  ["Brasil", "br"],
  ["Japão", "jp"],
  ["Canadá", "ca"],
  ["França", "fr"],
  ["Alemanha", "de"],
  ["Itália", "it"],
  ["Portugal", "pt"],
  ["Argentina", "ar"],
  ["Estados Unidos", "us"],
  ["Coreia do Sul", "kr"],
].map(([country, code]) => ({
  country,
  flag_url: `https://example.com/${code}.png`,
  choices: [
    country,
    ...["Canadá", "França", "Japão", "Alemanha", "Portugal"]
      .filter((choice) => choice !== country)
      .slice(0, 3),
  ],
}));

test("the user completes a full flag quiz", async ({ page }) => {
  await page.route("**/api/v1/flags/quiz**", (route) =>
    route.fulfill({ json: questions }),
  );
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "De onde é esta bandeira?" }),
  ).toBeVisible();

  for (let index = 0; index < 10; index += 1) {
    const image = page.getByRole("img", { name: /^Bandeira de / });
    const alt = await image.getAttribute("alt");
    const correctCountry = alt.replace("Bandeira de ", "");

    await page.getByRole("button", { name: correctCountry, exact: true }).click();
    await expect(page.getByRole("status")).toContainText("Resposta correta");

    await page
      .getByRole("button", {
        name: index === 9 ? "Ver resultado" : "Próxima bandeira",
      })
      .click();
  }

  await expect(page.getByRole("heading", { name: "Perfeito!" })).toBeVisible();
  await expect(page.getByText("100%", { exact: true })).toBeVisible();
});
