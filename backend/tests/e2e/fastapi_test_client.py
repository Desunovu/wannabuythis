from fastapi.testclient import TestClient

from src.integration.entrypoints.fastapi_app import create_app

fastapi_app = create_app(test_mode=True)

client = TestClient(fastapi_app)
