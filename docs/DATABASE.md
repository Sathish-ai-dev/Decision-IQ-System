# Database Schema

All tables live in the `public` schema, have `id uuid PRIMARY KEY`, `created_at`, `updated_at` (where mutable), and Row-Level Security enabled. Explicit `GRANT`s are issued to `authenticated` and `service_role`.

## Enums

- `app_role`: `admin | analyst | organization | community | citizen`
- `entity_status`: `draft | active | archived | processing | failed`

## Core

| Table | Purpose | Notable columns |
| --- | --- | --- |
| `profiles` | User profile, 1:1 with `auth.users` | `full_name`, `avatar_url`, `organization_id`, `bio` |
| `organizations` | Workspace / tenant | `name`, `slug`, `description` |
| `user_roles` | Role assignments (separate table for security) | `user_id`, `role` |
| `permissions` | Role → resource → action reference | `role`, `resource`, `action` |
| `projects` | Group data, docs, and reports | `name`, `organization_id`, `owner_id` |

## Content

| Table | Purpose |
| --- | --- |
| `documents` | Uploaded files (name, path, mime, size) |
| `datasets` | Curated tables ready for analysis |
| `reports` | Authored summaries / exports |
| `automations` | Workflow definitions (trigger + config JSON) |
| `notifications` | Per-user notifications |
| `audit_logs` | Actor, action, entity, entity_id, metadata |

## Data & AI (future-ready)

| Table | Purpose |
| --- | --- |
| `data_sources` | Connected DBs / APIs / storage (type, config JSON, last_synced_at) |
| `models` | AI models available to the platform (provider, version, capabilities) |
| `conversations` | Chat sessions (user_id, model_id) |
| `chat_messages` | Messages within a conversation |
| `ai_responses` | Model output linked to a message (latency, tokens) |
| `insights` | AI-generated observations linked to a source entity |

## Security Model

- **RLS on**: every table
- **Ownership**: `owner_id = auth.uid()` on user-scoped rows
- **Role checks**: `public.has_role(_user_id uuid, _role app_role)` — SECURITY DEFINER, only callable by authenticated users
- **Signup trigger**: creates a `profiles` row and grants `citizen` role automatically
- **Audit log visibility**: admin-only via `has_role(auth.uid(), 'admin')`

## Migrations

All migrations live in `supabase/migrations/`. The foundation migration is authored via Lovable's migration tool and includes:
1. Enum types
2. Helper functions (`set_updated_at`, `has_role`, `handle_new_user`)
3. Core tables + GRANTs + RLS + policies + triggers
4. `on_auth_user_created` trigger on `auth.users`
