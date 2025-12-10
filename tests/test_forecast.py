import pytest
from unittest.mock import Mock

def test_get_forecast_properties(client, mock_supabase, sample_forecast_property):
    mock_response = Mock()
    mock_response.data = [sample_forecast_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/forecast?city=Wellington&page=0&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["confidence_score"] == 0.85
    assert data[0]["predicted_status"] == "Likely to sell"

def test_get_forecast_with_suburbs(client, mock_supabase, sample_forecast_property):
    mock_response = Mock()
    mock_response.data = [sample_forecast_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.in_.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/forecast?city=Wellington&suburbs=Te Aro,Kelburn")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_forecast_fallback_to_properties(client, mock_supabase, sample_property):
    mock_forecast_response = Mock()
    mock_forecast_response.data = []
    
    mock_property_response = Mock()
    mock_property_response.data = [sample_property]
    
    mock_query = Mock()
    
    def execute_side_effect():
        if mock_query.call_count == 1:
            return mock_forecast_response
        return mock_property_response
    
    mock_query.execute.side_effect = [mock_forecast_response, mock_property_response]
    mock_query.eq.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/forecast?city=Auckland")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_forecast_autocomplete(client, mock_supabase):
    mock_response = Mock()
    mock_response.data = [
        {"address": "123 Cuba Street"},
        {"address": "456 Cuba Mall"}
    ]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.ilike.return_value = mock_query
    mock_query.limit.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
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
