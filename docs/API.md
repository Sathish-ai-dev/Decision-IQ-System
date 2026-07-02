# API Design

Two API surfaces are planned:

## 1. TanStack Server Functions (in-app)

Used by the React frontend for authenticated, RLS-scoped reads and writes. Implemented via `createServerFn` from `@tanstack/react-start` and the `requireSupabaseAuth` middleware.

Not exposed as public HTTP endpoints — invoked directly by the client through TanStack's typed RPC layer.

Example (planned):

```ts
export const listDocuments = createServerFn({ method: 'GET' })
  .middleware([requireSupabaseAuth])
  .handler(async ({ context }) =>
    context.supabase.from('documents').select('*').order('created_at', { ascending: false }),
  );
```

## 2. FastAPI Service (planned)

A separate service on Google Cloud Run for AI, orchestration, and long-running work. Called by the frontend via authenticated HTTP requests.

### Auth

Bearer token = Supabase JWT. FastAPI verifies the token against Supabase JWKS.

### Planned endpoints

```
POST   /v1/auth/exchange              Exchange Supabase JWT → FastAPI session token (optional)

GET    /v1/data-sources               List connected sources
POST   /v1/data-sources               Connect a new source
POST   /v1/data-sources/{id}/sync     Trigger a manual sync

GET    /v1/documents                  List documents
POST   /v1/documents                  Upload metadata (file → object storage)
POST   /v1/documents/{id}/embed       Trigger RAG embedding

POST   /v1/chat/conversations         Create conversation
POST   /v1/chat/conversations/{id}/messages   Post a user message → streamed AI response
GET    /v1/chat/conversations/{id}    Fetch history

POST   /v1/insights/scan              Trigger insight generation
GET    /v1/insights                   List insights

GET    /v1/automations                List automations
POST   /v1/automations                Create automation
POST   /v1/automations/{id}/run       Trigger manual run
GET    /v1/automations/{id}/runs      Run history

GET    /v1/analytics/kpis             Compute KPIs
GET    /v1/analytics/forecast         Time-series forecast
```

### Conventions

- All responses use `application/json`.
- Errors use RFC 7807-style bodies: `{ "type", "title", "status", "detail" }`.
- Rate limits enforced per-user via Redis.
- Streaming endpoints (chat) use SSE.

## 3. Webhooks / Public Endpoints (planned)

TanStack server routes under `src/routes/api/public/*` for external callers (cron, webhooks). Every handler validates a signature before doing any privileged work.

## Status

All API endpoints listed above are **planned only**. The current build ships schema, authentication, and UI foundation. No API endpoints are implemented yet.
