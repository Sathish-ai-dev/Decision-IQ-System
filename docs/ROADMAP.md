# Roadmap

## Phase 1 — Foundation (current)

**Status:** ✅ In progress

- Marketing site (Home, Features, About, Contact)
- Authentication (email/password + Google OAuth) + password reset
- Dashboard shell (sidebar, top nav, theme toggle, user menu)
- 15+ dashboard pages with polished placeholder UIs
- Reusable component library (`MetricCard`, `ChartCard`, `EmptyState`, `StatusBadge`, `ThemeToggle`, `PageHeader`)
- Light / Dark / System theming
- Full database schema (16 tables) with RLS + GRANTs
- Docs (README, Architecture, Database, API, Roadmap)

## Phase 2 — Data Sources & Ingestion

- Real connectors: PostgreSQL, BigQuery, S3, REST APIs
- Sync scheduling + `last_synced_at` tracking
- Document upload → object storage (Cloud Storage / Supabase Storage)
- Document metadata extraction

## Phase 3 — AI Assistant & RAG

- FastAPI service on Cloud Run
- ChromaDB vector store for `documents` and `datasets`
- Gemini via Vertex AI as the primary LLM
- LangChain-based agent for tool use
- Grounded chat: real `conversations`, `chat_messages`, `ai_responses`
- Model selection via `models` table

## Phase 4 — Insights & Analytics

- Real analytics: KPIs computed from `data_sources` and `datasets`
- Anomaly detection populating `insights`
- Forecasting (Prophet or Vertex AI Forecast)
- Heatmap and geographic map with real regional data

## Phase 5 — Automation Engine

- Trigger types: schedule (pg_cron), event (webhook), AI signal
- Workflow execution runtime
- Retries, failure notifications, audit trail
- Templates library

## Phase 6 — Governance & Enterprise

- SSO (SAML)
- Fine-grained permissions per resource
- Data classification and DLP
- Multi-region deployment
- SOC 2 readiness

## Non-goals (for now)

- Native mobile apps
- In-product billing (subscription management)
- Marketplace / third-party plugins
