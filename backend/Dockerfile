FROM python:3.12 as python-base
# Set environment variables
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
# Add poetry and venv to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` - build deps and create venv
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # for installing poetry
        curl
# Install Poetry (with the usage of the POETRY_HOME and POETRY_VERSION)
RUN curl -sSL https://install.python-poetry.org | python3 -
# Copy project requirement files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
# Install runtime dependencies (uses $POETRY_VIRTUALENVS_IN_PROJECT)
RUN poetry install --no-dev

# `development` image
FROM python-base as development
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH
# copy poetry+venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# quick install all deps
RUN poetry install
# mountpoint of code
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "--reload", "src.integration.entrypoints.fastapi_app:app"]

# `production` image
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/
WORKDIR /app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.integration.entrypoints.fastapi_app::app"]
