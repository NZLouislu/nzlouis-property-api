import pytest
from unittest.mock import Mock, MagicMock

def test_get_properties_no_params(client, mock_supabase):
    mock_response = Mock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.limit.return_value.execute.return_value = mock_response
    
    response = client.get("/api/property")
    assert response.status_code == 200
    assert response.json() == []

def test_get_properties_by_city(client, mock_supabase, sample_property):
    mock_response = Mock()
    mock_response.data = [sample_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/property?city=Auckland&page=0&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["address"] == "123 Queen Street"

def test_get_properties_by_id(client, mock_supabase, sample_property):
    mock_response = Mock()
    mock_response.data = [sample_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get(f"/api/property?id={sample_property['id']}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_property["id"]

def test_get_properties_with_suburbs(client, mock_supabase, sample_property):
    mock_response = Mock()
    mock_response.data = [sample_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.in_.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/property?city=Auckland&suburbs=Auckland Central,Parnell")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_properties_with_search(client, mock_supabase, sample_property):
    mock_response = Mock()
    mock_response.data = [sample_property]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.ilike.return_value = mock_query
    mock_query.order.return_value = mock_query
    mock_query.range.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/property?city=Auckland&search=Queen")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_autocomplete_properties(client, mock_supabase):
    mock_response = Mock()
    mock_response.data = [
        {"address": "123 Queen Street"},
        {"address": "456 Queen Street"}
    ]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.ilike.return_value = mock_query
    mock_query.limit.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/property/autocomplete?query=Queen")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_autocomplete_with_city_filter(client, mock_supabase):
    mock_response = Mock()
    mock_response.data = [{"address": "123 Queen Street"}]
    
    mock_query = Mock()
    mock_query.execute.return_value = mock_response
    mock_query.eq.return_value = mock_query
    mock_query.ilike.return_value = mock_query
    mock_query.limit.return_value = mock_query
    
    mock_table = Mock()
    mock_table.select.return_value = mock_query
    mock_supabase.table.return_value = mock_table
    
    response = client.get("/api/property/autocomplete?query=Queen&city=Auckland")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_autocomplete_missing_query():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    
    response = client.get("/api/property/autocomplete")
    assert response.status_code == 422

def test_property_validation_page_size_too_large():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    
    response = client.get("/api/property?city=Auckland&page_size=100")
    assert response.status_code == 422
