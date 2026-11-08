const EVENTS_URL = "/api/v1/events";

function getErrorMessage(detail) {
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
    throw new Error(
      "Não foi possível conectar à API. Confira se o backend está em execução.",
    );
  }

  const payload = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(
      getErrorMessage(payload?.detail) || "Não foi possível concluir a operação.",
    );
  }
  return payload;
}

export function listEvents(filters = {}) {
  const params = new URLSearchParams({ limit: "100" });
  if (filters.q) params.set("q", filters.q);
  if (filters.category) params.set("category", filters.category);
  if (filters.starts_after) {
    params.set("starts_after", new Date(filters.starts_after).toISOString());
  }
  if (filters.starts_before) {
    params.set("starts_before", new Date(filters.starts_before).toISOString());
  }
  return request(`${EVENTS_URL}?${params.toString()}`);
}

export function createEvent(event) {
  return request(EVENTS_URL, { method: "POST", body: JSON.stringify(event) });
}

export function updateEvent(id, event) {
  return request(`${EVENTS_URL}/${id}`, {
    method: "PUT",
    body: JSON.stringify(event),
  });
}

export function deleteEvent(id) {
  return request(`${EVENTS_URL}/${id}`, { method: "DELETE" });
}
