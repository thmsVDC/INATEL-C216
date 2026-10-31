import { expect, test } from "@playwright/test";

test("the user completes a full flag quiz", async ({ page }) => {
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
