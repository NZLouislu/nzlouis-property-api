import pytest
from unittest.mock import Mock, MagicMock

def test_get_properties_no_params(client, mock_db):
    response = client.get("/api/property")
    assert response.status_code == 200
    assert response.json() == []

def test_get_properties_by_city(client, mock_db, sample_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/property?city=Auckland&page=0&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["address"] == "123 Queen Street"

def test_get_properties_by_id(client, mock_db, sample_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get(f"/api/property?id={sample_property['id']}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == sample_property["id"]

def test_get_properties_with_suburbs(client, mock_db, sample_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/property?city=Auckland&suburbs=Auckland Central,Parnell")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_properties_with_search(client, mock_db, sample_property):
    mock_result = Mock()
    mock_result.mappings.return_value.all.return_value = [sample_property]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/property?city=Auckland&search=Queen")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_autocomplete_properties(client, mock_db):
    mock_result = Mock()
    mock_result.all.return_value = [("123 Queen Street",), ("456 Queen Street",)]
    mock_db.execute.return_value = mock_result
    
    response = client.get("/api/property/autocomplete?query=Queen")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_autocomplete_with_city_filter(client, mock_db):
    mock_result = Mock()
    mock_result.all.return_value = [("123 Queen Street",)]
    mock_db.execute.return_value = mock_result
    
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
