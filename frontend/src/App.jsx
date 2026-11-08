import { useCallback, useEffect, useState } from "react";

import { createEvent, deleteEvent, listEvents, updateEvent } from "./api/events.js";

const EMPTY_FILTERS = { q: "", category: "", starts_after: "", starts_before: "" };

function formatDate(value) {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "full",
    timeStyle: "short",
  }).format(new Date(value));
}

function toDateTimeInput(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return new Date(date.getTime() - date.getTimezoneOffset() * 60_000)
    .toISOString()
    .slice(0, 16);
}

function EventDialog({ event, error, saving, onClose, onSave }) {
  const [form, setForm] = useState(() => ({
    title: event?.title ?? "",
    description: event?.description ?? "",
    category: event?.category ?? "",
    location: event?.location ?? "",
    starts_at: event ? toDateTimeInput(event.starts_at) : "",
    capacity: event?.capacity ?? 30,
  }));

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function submit(eventObject) {
    eventObject.preventDefault();
    onSave({
      ...form,
      description: form.description.trim() || null,
      starts_at: new Date(form.starts_at).toISOString(),
      capacity: Number(form.capacity),
    });
  }

  return (
    <div className="modal-backdrop">
      <section
        aria-labelledby="event-dialog-title"
        aria-modal="true"
        className="event-dialog"
        role="dialog"
      >
        <div className="dialog-heading">
          <div>
            <p className="eyebrow">OrganizaJá · eventos</p>
            <h2 id="event-dialog-title">
              {event ? "Editar evento" : "Criar evento"}
            </h2>
          </div>
          <button
            aria-label="Fechar formulário"
            className="icon-button"
            onClick={onClose}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="event-form" onSubmit={submit}>
          <label className="field field-wide">
            <span>Nome do evento</span>
            <input
              maxLength={120}
              minLength={3}
              onChange={(eventObject) => updateField("title", eventObject.target.value)}
              placeholder="Ex.: Semana de Tecnologia"
              required
              value={form.title}
            />
          </label>

          <label className="field">
            <span>Categoria</span>
            <input
              maxLength={60}
              onChange={(eventObject) => updateField("category", eventObject.target.value)}
              placeholder="Palestra, workshop..."
              required
              value={form.category}
            />
          </label>

          <label className="field">
            <span>Local</span>
            <input
              maxLength={150}
              onChange={(eventObject) => updateField("location", eventObject.target.value)}
              placeholder="Bloco, sala ou endereço"
              required
              value={form.location}
            />
          </label>

          <label className="field">
            <span>Data e horário</span>
            <input
              onChange={(eventObject) => updateField("starts_at", eventObject.target.value)}
              required
              type="datetime-local"
              value={form.starts_at}
            />
          </label>

          <label className="field">
            <span>Vagas disponíveis</span>
            <input
              max={10000}
              min={1}
              onChange={(eventObject) => updateField("capacity", eventObject.target.value)}
              required
              type="number"
              value={form.capacity}
            />
          </label>

          <label className="field field-wide">
            <span>Descrição <small>(opcional)</small></span>
            <textarea
              maxLength={3000}
              onChange={(eventObject) => updateField("description", eventObject.target.value)}
              placeholder="Conte o que os participantes podem esperar."
              rows={4}
              value={form.description}
            />
          </label>

          {error && <p className="form-error field-wide" role="alert">{error}</p>}

          <div className="form-actions field-wide">
            <button className="button button-secondary" onClick={onClose} type="button">
              Cancelar
            </button>
            <button className="button button-primary" disabled={saving} type="submit">
              {saving ? "Salvando..." : event ? "Salvar alterações" : "Criar evento"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

function EventCard({ event, deleting, onDelete, onEdit }) {
  return (
    <article className="event-card">
      <div className="event-card-topline">
        <span className="category-pill">{event.category}</span>
        <span className="event-id">#{String(event.id).padStart(3, "0")}</span>
      </div>
      <h3>{event.title}</h3>
      <p className="event-description">
        {event.description || "Um encontro para aprender e compartilhar com a comunidade."}
      </p>
      <dl className="event-details">
        <div>
          <dt>Quando</dt>
          <dd>{formatDate(event.starts_at)}</dd>
        </div>
        <div>
          <dt>Onde</dt>
          <dd>{event.location}</dd>
        </div>
        <div>
          <dt>Capacidade</dt>
          <dd>{event.capacity} participantes</dd>
        </div>
      </dl>
      <div className="event-card-actions">
        <button className="button button-secondary" onClick={() => onEdit(event)} type="button">
          Editar
        </button>
        <button
          className="button button-danger"
          disabled={deleting}
          onClick={() => onDelete(event)}
          type="button"
        >
          {deleting ? "Excluindo..." : "Excluir"}
        </button>
      </div>
    </article>
  );
}

export default function App() {
  const [events, setEvents] = useState([]);
  const [draftFilters, setDraftFilters] = useState(EMPTY_FILTERS);
  const [appliedFilters, setAppliedFilters] = useState(EMPTY_FILTERS);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const loadEvents = useCallback(async () => {
    setIsLoading(true);
    setLoadError("");
    try {
      const result = await listEvents(appliedFilters);
      setEvents(result);
    } catch (error) {
      setLoadError(error.message);
    } finally {
      setIsLoading(false);
    }
  }, [appliedFilters]);

  useEffect(() => {
    loadEvents();
  }, [loadEvents]);

  function updateFilter(field, value) {
    setDraftFilters((current) => ({ ...current, [field]: value }));
  }

  function applyFilters(event) {
    event.preventDefault();
    setAppliedFilters({ ...draftFilters, q: draftFilters.q.trim() });
    setSuccessMessage("");
  }

  function clearFilters() {
    setDraftFilters(EMPTY_FILTERS);
    setAppliedFilters(EMPTY_FILTERS);
    setSuccessMessage("");
  }

  function openCreateDialog() {
    setEditingEvent(null);
    setActionError("");
    setDialogOpen(true);
  }

  function openEditDialog(event) {
    setEditingEvent(event);
    setActionError("");
    setDialogOpen(true);
  }

  async function saveEvent(data) {
    setIsSaving(true);
    setActionError("");
    setSuccessMessage("");
    try {
      if (editingEvent) {
        await updateEvent(editingEvent.id, data);
        setSuccessMessage("Evento atualizado com sucesso.");
      } else {
        await createEvent(data);
        setSuccessMessage("Evento criado com sucesso.");
      }
      setDialogOpen(false);
      setEditingEvent(null);
      await loadEvents();
    } catch (error) {
      setActionError(error.message);
    } finally {
      setIsSaving(false);
    }
  }

  async function removeEvent(event) {
    const confirmed = window.confirm(`Excluir o evento “${event.title}”?`);
    if (!confirmed) return;

    setDeletingId(event.id);
    setSuccessMessage("");
    setLoadError("");
    try {
      await deleteEvent(event.id);
      setSuccessMessage("Evento excluído.");
      await loadEvents();
    } catch (error) {
      setLoadError(error.message);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <main className="app-shell">
      <header className="site-header">
        <a aria-label="OrganizaJá, início" className="brand" href="/">
          <span aria-hidden="true" className="brand-mark">OJ</span>
          <span>OrganizaJá</span>
        </a>
        <span className="header-note">Comunidade acadêmica</span>
      </header>

      <section aria-labelledby="welcome-title" className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Ideias que aproximam pessoas</p>
          <h1 id="welcome-title">Seu próximo encontro começa aqui.</h1>
          <p className="hero-description">
            Descubra o que está acontecendo na comunidade acadêmica ou organize um evento para reunir todo mundo.
          </p>
          <button className="button button-primary hero-button" onClick={openCreateDialog} type="button">
            <span aria-hidden="true">＋</span> Criar evento
          </button>
        </div>
        <div aria-hidden="true" className="hero-art">
          <div className="art-orbit orbit-one" />
          <div className="art-orbit orbit-two" />
          <div className="art-center">OJ</div>
          <span className="art-note note-one">ideias</span>
          <span className="art-note note-two">encontros</span>
          <span className="art-note note-three">comunidade</span>
        </div>
      </section>

      <section aria-labelledby="events-title" className="events-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Agenda da comunidade</p>
            <h2 id="events-title">Eventos</h2>
          </div>
          <p className="result-count" aria-live="polite">
            {isLoading ? "Buscando eventos..." : `${events.length} ${events.length === 1 ? "evento" : "eventos"}`}
          </p>
        </div>

        <form aria-label="Filtros de eventos" className="filter-panel" onSubmit={applyFilters}>
          <label className="field search-field">
            <span>Buscar por nome</span>
            <input
              onChange={(event) => updateFilter("q", event.target.value)}
              placeholder="Ex.: semana acadêmica"
              value={draftFilters.q}
            />
          </label>
          <label className="field">
            <span>Categoria</span>
            <input
              maxLength={60}
              onChange={(event) => updateFilter("category", event.target.value)}
              placeholder="Todas as categorias"
              value={draftFilters.category}
            />
          </label>
          <label className="field date-field">
            <span>A partir de</span>
            <input
              onChange={(event) => updateFilter("starts_after", event.target.value)}
              type="datetime-local"
              value={draftFilters.starts_after}
            />
          </label>
          <label className="field date-field">
            <span>Até</span>
            <input
              onChange={(event) => updateFilter("starts_before", event.target.value)}
              type="datetime-local"
              value={draftFilters.starts_before}
            />
          </label>
          <div className="filter-actions">
            <button className="button button-secondary" type="submit">Aplicar filtros</button>
            <button className="text-button" onClick={clearFilters} type="button">Limpar</button>
          </div>
        </form>

        {successMessage && <p className="success-message" role="status">{successMessage}</p>}
        {loadError && (
          <div className="error-panel" role="alert">
            <div>
              <strong>Não foi possível carregar os eventos.</strong>
              <p>{loadError}</p>
            </div>
            <button className="button button-secondary" onClick={loadEvents} type="button">Tentar novamente</button>
          </div>
        )}

        {isLoading && events.length === 0 ? (
          <div aria-live="polite" className="loading-state" role="status">
            <span className="loading-dot" /> Carregando a agenda...
          </div>
        ) : events.length > 0 ? (
          <div aria-busy={isLoading} className="event-grid">
            {events.map((event) => (
              <EventCard
                deleting={deletingId === event.id}
                event={event}
                key={event.id}
                onDelete={removeEvent}
                onEdit={openEditDialog}
              />
            ))}
          </div>
        ) : !loadError ? (
          <div className="empty-state">
            <span aria-hidden="true" className="empty-icon">✳</span>
            <h3>{Object.values(appliedFilters).some(Boolean) ? "Nenhum evento encontrado" : "Sua agenda começa aqui"}</h3>
            <p>
              {Object.values(appliedFilters).some(Boolean)
                ? "Experimente ajustar os filtros ou limpe a busca para ver todos os eventos."
                : "Ainda não há eventos cadastrados. Que tal criar o primeiro?"}
            </p>
            {Object.values(appliedFilters).some(Boolean) ? (
              <button className="button button-secondary" onClick={clearFilters} type="button">Limpar filtros</button>
            ) : (
              <button className="button button-primary" onClick={openCreateDialog} type="button">Criar primeiro evento</button>
            )}
          </div>
        ) : null}
      </section>

      <footer className="site-footer">
        <span>OrganizaJá</span>
        <span>Feito para encontros que fazem a diferença.</span>
      </footer>

      {dialogOpen && (
        <EventDialog
          error={actionError}
          event={editingEvent}
          onClose={() => setDialogOpen(false)}
          onSave={saveEvent}
          saving={isSaving}
        />
      )}
    </main>
  );
}
