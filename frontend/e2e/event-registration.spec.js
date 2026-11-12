import { expect, test } from "@playwright/test";

let createdEventId;

test.afterEach(async ({ page }) => {
  if (!createdEventId) return;

  await page.evaluate(async (eventId) => {
    await fetch(`/api/v1/events/${eventId}`, { method: "DELETE" });
  }, createdEventId);
  createdEventId = undefined;
});

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
  const eventDialog = page.getByRole("dialog");
  await eventDialog.getByLabel("Nome do evento").fill(title);
  await eventDialog.getByLabel("Categoria").fill("Teste E2E");
  await eventDialog.getByLabel("Local").fill("Auditório de testes");
  await eventDialog.getByLabel("Data e horário").fill(startsAt);
  await eventDialog.getByLabel("Vagas disponíveis").fill("1");
  const createdEventResponse = page.waitForResponse(
    (response) =>
      response.request().method() === "POST" &&
      new URL(response.url()).pathname === "/api/v1/events",
  );
  await eventDialog.getByRole("button", { name: "Criar evento" }).click();
  createdEventId = (await (await createdEventResponse).json()).id;

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
