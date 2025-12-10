import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

@pytest.fixture
def mock_supabase():
    mock = Mock()
    return mock

@pytest.fixture
def client(mock_supabase):
    from app.services.supabase_client import get_supabase_client
    app.dependency_overrides[get_supabase_client] = lambda: mock_supabase
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_property():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "property_url": "https://homes.co.nz/address/auckland/test",
        "address": "123 Queen Street",
        "suburb": "Auckland Central",
        "city": "Auckland",
        "region": "Auckland",
        "bedrooms": 3,
        "bathrooms": 2,
        "car_spaces": 1,
        "land_area": 350.5,
        "last_sold_price": 850000,
        "last_sold_date": "2023-06-15",
        "cover_image_url": "https://example.com/image.jpg"
    }

@pytest.fixture
def sample_forecast_property():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "property_url": "https://homes.co.nz/address/wellington/test",
        "address": "456 Cuba Street",
        "suburb": "Te Aro",
        "city": "Wellington",
        "region": "Wellington",
        "bedrooms": 2,
        "bathrooms": 1,
        "car_spaces": 0,
        "land_area": 200.0,
        "last_sold_price": 650000,
        "last_sold_date": "2023-05-10",
        "cover_image_url": "https://example.com/image2.jpg",
        "confidence_score": 0.85,
        "predicted_status": "Likely to sell",
        "predicted_price": 700000
    }
