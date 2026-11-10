import { expect, test } from "@playwright/test";

test("cria evento, persiste inscrição após recarregar e libera vaga ao cancelar", async ({
  page,
}) => {
  const title = `Evento E2E ${Date.now()}`;
  const participantName = "Participante de teste";
  const participantEmail = `e2e-${Date.now()}@example.com`;
  const startsAt = new Date(Date.now() + 24 * 60 * 60 * 1000)
    .toISOString()
    .slice(0, 16);

  await page.goto("/");
  await page.getByRole("button", { name: "Criar evento", exact: true }).click();
  await page.getByLabel("Nome do evento").fill(title);
  await page.getByLabel("Categoria").fill("Teste E2E");
  await page.getByLabel("Local").fill("Auditório de testes");
  await page.getByLabel("Data e horário").fill(startsAt);
  await page.getByLabel("Vagas disponíveis").fill("1");
  await page.getByRole("button", { name: "Criar evento", exact: true }).last().click();

  const eventCard = page.locator(".event-card").filter({ hasText: title });
  await expect(eventCard).toBeVisible();
  await eventCard.getByRole("button", { name: "Inscrições e vagas" }).click();

  const registrationDialog = page.getByRole("dialog");
  await registrationDialog.getByLabel("Nome").fill(participantName);
  await registrationDialog.getByLabel("E-mail").fill(participantEmail);
  await registrationDialog
    .getByRole("button", { name: "Confirmar inscrição" })
    .click();
  await expect(registrationDialog.getByText(participantEmail)).toBeVisible();
  await expect(registrationDialog.getByText("0 vagas disponíveis")).toBeVisible();

  await page.reload();
  const persistedEvent = page.locator(".event-card").filter({ hasText: title });
  await expect(persistedEvent).toBeVisible();
  await persistedEvent.getByRole("button", { name: "Inscrições e vagas" }).click();

  const persistedDialog = page.getByRole("dialog");
  await expect(persistedDialog.getByText(participantEmail)).toBeVisible();
  await persistedDialog
    .getByRole("button", { name: `Cancelar inscrição de ${participantName}` })
    .click();
  await expect(persistedDialog.getByText(participantEmail)).toHaveCount(0);
  await expect(persistedDialog.getByText("1 vaga disponível")).toBeVisible();
});
