import pytest

def test_get_regions(client):
    response = client.get("/api/regions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    region = data[0]
    assert "id" in region
    assert "name" in region
    assert "cities" in region
    assert isinstance(region["cities"], list)

def test_regions_structure(client):
    response = client.get("/api/regions")
    data = response.json()
    
    for region in data:
        assert "id" in region
        assert "name" in region
        assert "cities" in region
        
        for city in region["cities"]:
            assert "id" in city
            assert "name" in city
            assert "suburbs" in city
            
            for suburb in city["suburbs"]:
                assert "id" in suburb
                assert "name" in suburb

def test_wellington_region_exists(client):
    response = client.get("/api/regions")
    data = response.json()
    
    wellington = next((r for r in data if r["id"] == "wellington"), None)
    assert wellington is not None
    assert wellington["name"] == "Wellington"
    assert len(wellington["cities"]) > 0

def test_auckland_region_exists(client):
    response = client.get("/api/regions")
    data = response.json()
    
    auckland = next((r for r in data if r["id"] == "auckland"), None)
    assert auckland is not None
    assert auckland["name"] == "Auckland"
    assert len(auckland["cities"]) > 0

def test_wellington_has_expected_cities(client):
    response = client.get("/api/regions")
    data = response.json()
    
    wellington = next((r for r in data if r["id"] == "wellington"), None)
    city_names = [c["name"] for c in wellington["cities"]]
    
    assert "Wellington City" in city_names
    assert "Lower Hutt" in city_names
    assert "Upper Hutt" in city_names
    assert "Porirua" in city_names

def test_auckland_has_expected_cities(client):
    response = client.get("/api/regions")
    data = response.json()
    
    auckland = next((r for r in data if r["id"] == "auckland"), None)
    city_names = [c["name"] for c in auckland["cities"]]
    
    assert "Auckland - City" in city_names
    assert "Auckland - North Shore" in city_names

def test_wellington_city_has_suburbs(client):
    response = client.get("/api/regions")
    data = response.json()
    
    wellington = next((r for r in data if r["id"] == "wellington"), None)
    wellington_city = next((c for c in wellington["cities"] if c["id"] == "wellington-city"), None)
    
    assert wellington_city is not None
    assert len(wellington_city["suburbs"]) > 0
    
    suburb_names = [s["name"] for s in wellington_city["suburbs"]]
    assert "Te Aro" in suburb_names
    assert "Kelburn" in suburb_names
