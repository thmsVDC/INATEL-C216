import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  cancelRegistration,
  createRegistration,
  listRegistrations,
} from "./registrations";

describe("registrations API", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("lists registrations for an event", async () => {
    const registrations = [{ id: 4, participant_name: "Ana Souza" }];
    fetch.mockResolvedValue({ ok: true, json: async () => registrations });

    await expect(listRegistrations(12)).resolves.toEqual(registrations);
    expect(fetch).toHaveBeenCalledWith("/api/v1/events/12/registrations", {
      headers: undefined,
    });
  });

  it("creates a registration with a JSON body", async () => {
    const registration = {
      participant_name: "Ana Souza",
      participant_email: "ana@example.com",
    };
    fetch.mockResolvedValue({ ok: true, json: async () => ({ id: 5, ...registration }) });

    await expect(createRegistration(12, registration)).resolves.toMatchObject({
      id: 5,
      participant_email: "ana@example.com",
    });
    expect(fetch).toHaveBeenCalledWith(
      "/api/v1/events/12/registrations",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registration),
      }),
    );
  });

  it("cancels a registration and reports API conflicts", async () => {
    fetch.mockResolvedValueOnce({ ok: true, status: 204 });
    await expect(cancelRegistration(12, 5)).resolves.toBeNull();
    expect(fetch).toHaveBeenCalledWith(
      "/api/v1/events/12/registrations/5",
      expect.objectContaining({ method: "DELETE" }),
    );

    fetch.mockResolvedValueOnce({
      ok: false,
      status: 409,
      json: async () => ({ detail: "Este evento não tem mais vagas disponíveis." }),
    });
    await expect(
      createRegistration(12, {
        participant_name: "Carla Reis",
        participant_email: "carla@example.com",
      }),
    ).rejects.toThrow("Este evento não tem mais vagas disponíveis.");
  });

  it("reports a connection error when the API cannot be reached", async () => {
    fetch.mockRejectedValue(new TypeError("Network error"));

    await expect(listRegistrations(12)).rejects.toThrow(
      "Não foi possível conectar à API. Tente novamente.",
    );
  });
});
