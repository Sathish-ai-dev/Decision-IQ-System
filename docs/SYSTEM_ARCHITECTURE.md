# System Architecture

## Overview

The Decision Intelligence Platform is built as a modular full-stack application with a clear separation between presentation, authentication, data, and (planned) AI layers.

```text
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (React)                       │
│  Marketing site · Auth · Dashboard shell · 15+ pages        │
│  TanStack Router · React Query · shadcn/ui · Tailwind v4    │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       │                               │
┌──────▼──────────┐          ┌─────────▼──────────┐
│  Lovable Cloud  │          │  FastAPI (planned) │
│  (Supabase)     │          │  Google Cloud Run  │
│  · Auth         │          │  · Business logic  │
│  · Postgres     │          │  · Data pipelines  │
│  · RLS          │          │  · Vertex AI       │
│  · Storage      │          │  · Gemini          │
└──────┬──────────┘          │  · LangChain       │
       │                     │  · ChromaDB (RAG)  │
       │                     └────────────────────┘
       │
┌──────▼───────────────────────────────────────────────────┐
│                  PostgreSQL (managed)                     │
│  profiles · organizations · user_roles · permissions      │
│  projects · documents · datasets · reports · automations  │
│  notifications · audit_logs · data_sources                │
│  conversations · chat_messages · ai_responses · models    │
│  insights                                                 │
└───────────────────────────────────────────────────────────┘
```

## Layers

### Presentation

- **Marketing site** (`/`, `/features`, `/about`, `/contact`): public, SSR-friendly, SEO-optimized.
- **Auth** (`/auth`, `/reset-password`): email/password + Google OAuth.
- **Dashboard** (`/_authenticated/*`): sidebar shell, top nav, protected by an integration-managed route gate (`ssr: false` + `getUser()` redirect to `/auth`).

### Auth

Managed by Lovable Cloud (Supabase Auth):
- Email/password sign-up and sign-in
- Google OAuth via `lovable.auth.signInWithOAuth('google', ...)`
- Password reset via `resetPasswordForEmail` + `/reset-password` route

### Data

- Postgres with Row-Level Security on every user-facing table
- `user_roles` is a separate table checked by a `SECURITY DEFINER` `has_role()` function to avoid RLS recursion
- `updated_at` triggers on every mutable table

### Planned AI Layer

A separate FastAPI service will orchestrate:
- **RAG** over `documents` and `datasets` using ChromaDB embeddings
- **Chat** grounded on organization-scoped context (Gemini via Vertex AI)
- **Insights** generation (anomaly detection, trend surfacing) writing to `insights`
- **Automation** execution engine driving `automations`

## Theming

- Light / Dark / System modes
- CSS variables in oklch, mapped into Tailwind v4's `@theme inline`
- Google Cloud-inspired palette with soft elevation shadows

## Governance

- RBAC via `app_role` enum + `user_roles` + `permissions`
- `audit_logs` records privileged actions
- Every server-owned mutation must pass through RLS or a security-checked server function
