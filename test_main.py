from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_health():
    """Проверка endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_products():
    """Проверка endpoint /products"""
    response = client.get("/products")
    
    products = response.json() 
    assert response.status_code == 200
    assert isinstance(products, list)
    assert len(products) > 0