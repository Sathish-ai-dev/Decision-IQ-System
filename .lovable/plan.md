
# Decision Intelligence Platform — Foundation Plan (v2)

Scope: UI foundation, navigation, auth, reusable components, DB schema, docs. **No** AI/ML/RAG/workflow logic.

## Stack alignment note

Project runs on **TanStack Start + TanStack Router** (not React Router DOM) — this is the required template stack. It satisfies the same routing/protected-route need. All other libraries match your request (Tailwind, shadcn, React Query, RHF, Zod, Lucide, Recharts, Supabase).

## 1. Design system (`src/styles.css`)

- Google Cloud / Material 3-inspired palette in oklch: neutral surfaces, blue primary, soft accents, chart tokens
- Semantic tokens (background, foreground, primary, muted, accent, border, sidebar, chart-1..5)
- Rounded-xl cards, soft elevation shadows, generous spacing
- Inter typography loaded via `<link>` in `__root.tsx`

## 2. Theme system

`ThemeProvider` context supporting **Light / Dark / System**:
- `system` follows `prefers-color-scheme` with live listener
- Persisted in `localStorage`
- Toggle in top nav (dropdown: Light / Dark / System)

## 3. Enable Lovable Cloud (Supabase)

Provides auth + Postgres. Adds managed `_authenticated/route.tsx` gate + bearer middleware.

## 4. Database schema (single migration)

All tables: `id uuid pk`, `created_at`, `updated_at`, `status` where relevant. RLS on. GRANTs to `authenticated` + `service_role`. Policies via `auth.uid()` or `has_role()`. `updated_at` trigger. Signup trigger auto-creates profile + default `citizen` role.

Core tables:
- `profiles` (linked to `auth.users`, full_name, avatar_url, organization_id)
- `organizations` (name, slug, description)
- `app_role` enum: `admin | analyst | organization | community | citizen`
- `user_roles` (user_id, role) — separate table (security requirement)
- `permissions` (role, resource, action) — reference
- `projects`, `documents`, `datasets`, `reports`
- `automations` (renamed from workflows: name, project_id, owner_id, config jsonb, trigger_type)
- `notifications`, `audit_logs`

Future-ready tables (schema only, no logic):
- `data_sources` (name, type, config jsonb, org_id, owner_id, status, last_synced_at)
- `conversations` (title, user_id, model_id)
- `chat_messages` (conversation_id, role, content, tokens)
- `ai_responses` (message_id, response, latency_ms, tokens_in, tokens_out, model_id)
- `models` (name, provider, version, capabilities jsonb, is_active)
- `insights` (title, summary, source_type, source_id, project_id, owner_id, confidence)

## 5. Routes (TanStack file-based)

**Public** (top-level, SSR):
- `index.tsx` — Home (hero, overview, features, benefits, how it works, tech, testimonials, CTA, footer)
- `features.tsx`, `about.tsx`, `contact.tsx`
- `auth.tsx` — Login + Register + Forgot Password (tabs), Google OAuth via `lovable.auth`
- `reset-password.tsx`

**Protected** (`_authenticated/*`, managed gate → `/auth`):
- `dashboard.tsx`
- `ai-assistant.tsx` (UI only)
- `insights.tsx` (new)
- `data-sources.tsx` (new)
- `documents.tsx`, `datasets.tsx`
- `analytics.tsx`, `reports.tsx`
- `automation.tsx` (renamed from workflow)
- `organizations.tsx`, `users.tsx`, `notifications.tsx`
- `profile.tsx`, `settings.tsx`, `admin.tsx`

Root `notFoundComponent` = 404.

## 6. Dashboard shell (`_authenticated/route.tsx`)

Sidebar grouped as requested:

```
Overview        → Dashboard
AI              → AI Assistant, Insights
Data            → Data Sources, Documents, Datasets
Analytics       → Analytics, Reports
Automation      → Automation
Administration  → Organizations, Users, Notifications, Settings, Admin
```

Top nav: search box, theme toggle (Light/Dark/System), notifications bell, user dropdown (profile/settings/sign-out).

## 7. Dashboard widgets (placeholders)

Metric cards + panels for:
- Connected Data Sources
- Uploaded Documents
- Generated Insights
- Active Automations
- Organizations
- Recent Activity (list)
- AI Recommendations (placeholder card)
- Analytics Overview (recharts area chart placeholder)

## 8. Analytics page placeholders

- KPI card row
- Line / Bar / Pie / Area charts (recharts with static demo data)
- Heatmap placeholder (CSS grid)
- Geographic Map placeholder (SVG/placeholder block)
- Forecast placeholder (dashed-projection chart)
- Timeline placeholder

## 9. Other pages

- **AI Assistant**: conversation list + chat window + input + suggested prompts (no logic)
- **Insights**: card grid of placeholder AI insights with confidence badges
- **Data Sources**: table + "Connect Source" button + type filter + status badges
- **Documents**: DataTable + upload button + empty state
- **Datasets**: grid/table toggle, category filter, status badges
- **Reports**: card grid + export button + preview placeholder
- **Automation**: timeline + automation cards + trigger cards + table
- **Settings**: tabs (Profile, Security, Appearance, Notifications, Organization, API Keys)
- **Admin**: tabs (Users, Roles, Orgs, Audit Log)

## 10. Reusable components (`src/components/common/`)

`MetricCard`, `ChartCard`, `EmptyState`, `ErrorState`, `LoadingSpinner`, `PageHeader`, `SearchBox`, `FileUpload`, `DataTable`, `StatusBadge`, `SectionHeader`.

## 11. Folder structure

```
src/
  components/
    common/       # shared building blocks
    layouts/      # AppSidebar, TopNav, DashboardShell
    ui/           # shadcn
  routes/         # TanStack file-based
  hooks/          # useTheme, useAuth
  lib/            # utils, validators
  contexts/       # ThemeProvider
  types/          # shared TS types
  constants/      # nav config, roles
docs/
  README.md
  SYSTEM_ARCHITECTURE.md
  DATABASE.md
  ROADMAP.md
  API.md
```

## 12. Documentation (initial placeholders)

- **README.md** — project overview, stack, setup, structure
- **SYSTEM_ARCHITECTURE.md** — layers (frontend, auth, DB, future FastAPI/Vertex AI/RAG), diagram (ASCII)
- **DATABASE.md** — table list, relationships, RLS notes
- **ROADMAP.md** — phased plan: Phase 1 (foundation ✅), Phase 2 (Data sources + ingestion), Phase 3 (RAG + Chat), Phase 4 (Insights + Analytics), Phase 5 (Automation engine)
- **API.md** — planned FastAPI endpoints (auth, data sources, chat, insights, automations) — placeholders only

## Out of scope (explicit)

- AI/LLM/RAG/embeddings/vector DB
- Real file processing
- Automation execution
- Analytics pipelines / real KPIs
- Realtime data

## Deliverable

Polished enterprise-SaaS foundation: marketing site → auth → dashboard shell with all sections navigable and visually complete. Schema + docs ready to extend with FastAPI, Vertex AI, Gemini, RAG, ChromaDB later.
