import pytest
from unittest.mock import Mock

def test_get_forecast_properties(client, mock_db, sample_forecast_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_forecast_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/forecast?city=Wellington&page=0&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["confidence_score"] == 0.85
    assert data[0]["predicted_status"] == "Likely to sell"

def test_get_forecast_with_suburbs(client, mock_db, sample_forecast_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_forecast_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/forecast?city=Wellington&suburbs=Te Aro,Kelburn")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_forecast_fallback_to_properties(client, mock_db, sample_property):
    mock_result_empty = Mock()
    mock_result_empty.mappings.return_value.all.return_value = []
    
    mock_result_fallback = Mock()
    mock_result_fallback.mappings.return_value.all.return_value = [sample_property]
    
    mock_db.execute.side_effect = [mock_result_empty, mock_result_fallback]
    
    response = client.get("/api/forecast?city=Auckland")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_forecast_autocomplete(client, mock_db):
    mock_result = Mock()
    mock_result.all.return_value = [("123 Cuba Street",), ("456 Cuba Mall",)]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/forecast/autocomplete?query=Cuba")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_forecast_missing_city():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    
    response = client.get("/api/forecast")
    assert response.status_code == 422

def test_forecast_confidence_score_validation():
    from app.models.property import ForecastProperty
    import pytest
    
    with pytest.raises(ValueError):
        ForecastProperty(
            id="test",
            property_url="http://test.com",
            address="Test",
            suburb="Test",
            city="Test",
            region="Test",
            confidence_score=1.5,
            predicted_status="Test"
        )
