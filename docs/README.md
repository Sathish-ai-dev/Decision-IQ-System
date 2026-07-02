# Decision Intelligence Platform

Enterprise AI-powered decision intelligence for citizens, organizations, analysts, and government teams.

## Stack

- **Frontend:** React 19, TypeScript, TanStack Start (Router + Query), Vite, Tailwind CSS v4, shadcn/ui, Recharts, Lucide
- **Forms/Validation:** React Hook Form + Zod
- **Backend (current):** Lovable Cloud (Postgres + Auth) via Supabase
- **Backend (planned):** FastAPI, Google Cloud (Vertex AI, Gemini), LangChain, ChromaDB
- **Deployment:** Cloudflare Worker (edge SSR)

## Getting Started

```bash
bun install
bun run dev
```

The app runs on `http://localhost:8080`.

## Project Structure

```
src/
  components/
    common/       # shared building blocks (MetricCard, EmptyState, StatusBadge, ThemeToggle)
    layouts/      # AppSidebar, TopNav, MarketingShell
    ui/           # shadcn primitives
  routes/         # TanStack file-based routes
    _authenticated/  # protected dashboard shell
  hooks/          # useAuth
  contexts/       # ThemeProvider (light / dark / system)
  constants/      # navigation config
  lib/            # utilities
  integrations/   # supabase client (managed) + lovable OAuth
docs/             # architecture, database, roadmap, API
supabase/         # migrations
```

## Documentation

- [System Architecture](./SYSTEM_ARCHITECTURE.md)
- [Database Schema](./DATABASE.md)
- [API Design](./API.md)
- [Roadmap](./ROADMAP.md)

## Roles

The platform supports five primary user roles: `admin`, `analyst`, `organization`, `community`, and `citizen`. Roles are stored in a separate `user_roles` table and checked with a `SECURITY DEFINER` `has_role()` function to keep RLS policies safe from recursion.

## Status

Foundation phase — UI, authentication, navigation, reusable components, and database schema. AI/ML/RAG/workflow execution are intentionally deferred.
