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
    

def test_cart():
    client.delete("/cart")
    
    response = client.get("/cart")
    assert response.status_code == 200
    cart_data = response.json()
    assert "items" in cart_data
    assert "total" in cart_data
    assert cart_data["total"] == 0
    
    response = client.post("/cart/add?pid=0&qty=2")
    assert response.status_code == 200
    
    response = client.get("/cart")
    cart_data = response.json()
    assert len(cart_data["items"]) > 0
    assert cart_data["total"] > 0


def test_clear_cart():
    client.post("/cart/add?pid=0&qty=1")
    response = client.delete("/cart")
    assert response.status_code == 200
    
    response = client.get("/cart")
    cart_data = response.json()
    assert len(cart_data["items"]) == 0
    assert cart_data["total"] == 0


def test_cart_add_invalid_product():
    response = client.post("/cart/add?pid=999&qty=1")
    assert response.status_code == 404


def test_cart_add_invalid_quantity():
    response = client.post("/cart/add?pid=0&qty=0")
    assert response.status_code == 422