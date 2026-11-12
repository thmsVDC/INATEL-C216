const EVENTS_URL = "/api/v1/events";

function describeError(detail) {
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).filter(Boolean).join(" ");
  }
  return typeof detail === "string" ? detail : null;
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(path, {
      ...options,
      headers: options.body
        ? { "Content-Type": "application/json", ...options.headers }
        : options.headers,
    });
  } catch {
    throw new Error("Não foi possível conectar à API. Tente novamente.");
  }

  const payload = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(
      describeError(payload?.detail) || "Não foi possível concluir a operação.",
    );
  }
  return payload;
}

function eventRegistrationsUrl(eventId) {
  return `${EVENTS_URL}/${eventId}/registrations`;
}

export function listRegistrations(eventId) {
  return request(eventRegistrationsUrl(eventId));
}

export function createRegistration(eventId, registration) {
  return request(eventRegistrationsUrl(eventId), {
    method: "POST",
    body: JSON.stringify(registration),
  });
}

export function cancelRegistration(eventId, registrationId) {
  return request(`${eventRegistrationsUrl(eventId)}/${registrationId}`, {
    method: "DELETE",
  });
}
