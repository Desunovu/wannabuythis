FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder-base
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app

# Dev builder
FROM builder-base AS builder-dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Prod builder
FROM builder-base AS builder-prod
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Development
FROM python:3.12-slim-bookworm AS development
COPY --from=builder-dev /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
CMD ["uvicorn","src.infrastructure.entrypoints.fastapi.app:app",  "--reload", "--host", "0.0.0.0", "--port", "8000", "--root-path", "/api"]

# Production
FROM python:3.12-slim-bookworm AS production
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot
COPY --from=builder-prod --chown=nonroot:nonroot /app /app
ENV PATH="/app/.venv/bin:$PATH"
USER nonroot
WORKDIR /app
CMD ["uvicorn", "src.infrastructure.entrypoints.fastapi.app:app", "--host", "0.0.0.0", "--port", "8000", "--root-path", "/api"]
