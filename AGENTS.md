# AGENTS.md

## Project

Monorepo with a shopping list management system, consisting of backend and frontend applications.

## Backend app Stack

- Workdir: `/backend`
- Language: Python 3.12
- Framework: FastAPI, SQLAlchemy
- Database: PostgreSQL
- Cache: Redis
- DI container: dishka
- Auth: pyjwt, passlib (argon2)
- Package manager: uv

### Backend folder structure

Built on **onion/hexagonal architecture + DDD + CQRS**. Detailed tree and principles: [README](../README.md#architecture).

- `/src/shared` — shared kernel: DDD building blocks, mediator + UnitOfWork, abstract ports, utils, logger.
- `/src/modules` — isolated business modules (`users`, `wishlists`, ...), one per aggregate, each a vertical slice: `domain`, `application` (handlers), `infrastructure` (repo), `queries` (read side), `entrypoints/fastapi` (routers, schemas).
- `/src/infrastructure` — concrete adapters and app assembly: SQLAlchemy ORM, Redis, dishka container, FastAPI app.
- `/tests` — pytest by levels: `unit`, `integration`, plus test DI wiring in `di`.

### Backend app commands

- Install dependencies:
  ```bash
  uv sync
  ```

- Run tests:
  ```bash
  uv run pytest
  ```

- Format code:
  ```bash
  uv run ruff format
  ```

## Commit conventions

Conventional Commits: `<type>(<scope>): <description>`.

Types: `feat`, `fix`, `refactor`, `style`, `chore`, `test`, `docs`, `build`, `ci`, `perf`.

Scopes: `backend`, `frontend`.
