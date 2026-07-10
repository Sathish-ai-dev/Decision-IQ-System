# ARCHITECTURE

## High-Level
Users -> React Frontend -> FastAPI -> Services -> PostgreSQL/Supabase -> Storage.

Future AI: Documents -> Chunking -> Embeddings -> Vector Search -> Gemini.

## Backend
backend/app/modules/{auth,organizations,projects,documents,data_sources,datasets,analytics,ai}

Shared layers: core, database, shared.
