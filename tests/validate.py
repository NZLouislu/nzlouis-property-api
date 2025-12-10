import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    try:
        from app.main import app
        from app.config import get_settings
        from app.models.property import PropertyBase, ForecastProperty
        from app.models.region import Region, City, Suburb
        from app.routers import properties, forecast, regions
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    try:
        from app.main import app
        assert app is not None
        assert app.title == "NZ Louis Property API"
        print("✅ App creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_config():
    try:
        from app.config import get_settings
        settings = get_settings()
        assert settings.api_title == "NZ Louis Property API"
        assert settings.api_version == "1.0.0"
        assert settings.max_page_size == 50
        print("✅ Config validation successful")
        return True
    except Exception as e:
        print(f"❌ Config validation failed: {e}")
        return False

def test_models():
    try:
        from app.models.property import PropertyBase
        from app.models.region import Region, City, Suburb
        
        suburb = Suburb(id="test", name="Test Suburb")
        city = City(id="test", name="Test City", suburbs=[suburb])
        region = Region(id="test", name="Test Region", cities=[city])
        
        assert suburb.name == "Test Suburb"
        assert city.suburbs[0].name == "Test Suburb"
        assert region.cities[0].name == "Test City"
        
        print("✅ Model validation successful")
        return True
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

def test_routes_registered():
    try:
        from app.main import app
        routes = [route.path for route in app.routes]
        
        assert "/health" in routes
        assert "/api/property" in routes
        assert "/api/forecast" in routes
        assert "/api/regions" in routes
        
        print("✅ Routes registration successful")
        return True
    except Exception as e:
        print(f"❌ Routes registration failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Running Basic Validation Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_config,
        test_models,
        test_routes_registered,
    ]
    
    results = []
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        results.append(test())
    
    print("\n" + "=" * 50)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 50)
    
    if all(results):
        print("\n✅ All validation tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
