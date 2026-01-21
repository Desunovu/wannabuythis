#!/usr/bin/env bash

set -e
set -x

cd backend
uv run python -c "import src.infrastructure.entrypoints.fastapi.app as app; import json; print(json.dumps(app.app.openapi()))" > ../frontend/openapi.json
