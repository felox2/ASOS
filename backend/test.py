import pytest
from httpx import AsyncClient
from app.main import app
from app.config import Settings

@pytest.fixture(scope="module")
def test_settings():
    return Settings(
        JWT_SECRET_KEY="test_secret_key",
        DB_DRIVER="sqlite",
        DB_HOST="test_host",
        ACCESS_KEY_ID="test_access_key_id",
        ACCESS_KEY_SECRET="test_access_key_secret",
        INTERNAL_STORAGE_URL="http://localhost/internal",
        EXTERNAL_STORAGE_URL="http://localhost/external",
        BUCKET="test_bucket"
    )

@pytest.fixture(scope="module")
def test_app(test_settings):
    app.dependency_overrides[Settings] = lambda: test_settings
    yield app
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_read_products_simple(test_app):
    async with AsyncClient(app=test_app, base_url="http://localhost") as client:
        response = await client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)