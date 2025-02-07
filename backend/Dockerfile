# ==== Python-base Stage ====
FROM python:3.12 as python-base
ENV PYTHONBUFFERED=1 \
    PYTHONWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# ==== Builder-base Stage ====
FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main

# ==== Development Stage ====
FROM python-base as development
ENV FASTAPI_ENV=development
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR $PYSETUP_PATH
RUN poetry install
WORKDIR /app
COPY . .
CMD ["uvicorn","src.integration.entrypoints.fastapi_app:app",  "--reload", "--host", "0.0.0.0", "--port", "8000"]

# ==== Production Stage ====
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder-base $VENV_PATH $VENV_PATH
WORKDIR /app
COPY . .
CMD ["uvicorn", "src.integration.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
