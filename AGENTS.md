# AGENTS.md

## Project

Monorepo with a wishlist application, consisting of a backend and a frontend.

## Stack

**Application**

- **Frontend**: Nuxt.js (Vue-based framework)
- **Backend**: FastAPI with SQLAlchemy
- **Database**: PostgreSQL 16
- **Cache**: Redis
- **Proxy**: Traefik v3
- **Deployment**: Docker

**Backend**

- **Workdir**: `backend/`
- **Language**: Python 3.12
- **DI container**: dishka
- **Auth**: pyjwt, passlib (argon2)
- **Package manager**: uv

## Backend folder structure

- `/src/config.py` — application settings loaded from environment variables.
- `/src/shared` — shared kernel: DDD building blocks, mediator + UnitOfWork, abstract ports, utils, logger.
- `/src/modules` — isolated business modules (`users`, `wishlists`, ...), one per aggregate, each a vertical slice: `domain`, `application`, `infrastructure`, `queries`, `entrypoints`.
- `/src/infrastructure` — concrete adapters and app assembly: SQLAlchemy ORM, Redis, dishka container, FastAPI app. Modules are wired in centrally here: command and event handlers in `di/providers/mediator.py`, routers in `entrypoints/fastapi/app.py`.
- `/alembic` — migrations for the schema declared in `infrastructure/database/sqlalchemy/orm.py`.
- `/tests` — pytest by levels: `unit`, `integration`, plus test DI wiring in `di`.

## Architecture principles

Built on **onion/hexagonal architecture + DDD + CQRS**.

- **Domain layer is storage-agnostic**: domain models are plain dataclasses with no ORM imports; mapping is done imperatively.
- **Read side is storage-aware**: `queries/` functions take a SQLAlchemy `Session` directly instead of going through repositories.
- **Ports and adapters**: external dependencies (database, cache, mail) sit behind an abstract port, with a concrete adapter and an in-memory fake for tests.
- **Mediator**: commands and domain events flow through registered handlers, with a queue that chains newly raised events.
- **Unit of Work**: commits or rolls back a transaction and collects new domain events.
- **CQRS**: write side uses commands + handlers; read side uses dedicated query functions.
- **Dependency Injection**: environment-aware containers for production, development, and tests.
- **Unit tests** reach handlers only through the mediator, covering all negative and boundary cases of the application layer and the domain beneath it.
- **Integration tests** cover endpoint happy paths and the boundary cases unit tests cannot reach.

## Backend commands

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

- Lint code:
  ```bash
  uv run ruff check .
  ```

- After changing any HTTP endpoint, regenerate the OpenAPI spec
  ```bash
  ./scripts/generate-openapi-specs.sh
  ```

## Commit conventions

Conventional Commits: `<type>(<scope>): <description>`.

Types: `feat`, `fix`, `refactor`, `style`, `chore`, `test`, `docs`, `build`, `ci`, `perf`.

Scopes: `backend`, `frontend`.
