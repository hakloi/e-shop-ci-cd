import datetime
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    description: str
    created_at: str


app = FastAPI(title="E-Shop-СI-CD")

with open(Path(__file__).parent / "shop.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

@app.get("/products")
async def get_products():
    return PRODUCTS

@app.get("/product/{pid}")
async def get_product(pid: int):
    if 0 <= pid < len(PRODUCTS):
        return PRODUCTS[pid]
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/health")
async def health():
    return {"status": "ok", "products": len(PRODUCTS)}

@app.get("/cart")
async def get_cart_contents():
    total = sum(item["price"] * item["quantity"] for item in cart)
    return {
        "items": cart,
        "total": round(total, 2)
    }


@app.post("/cart/add")
async def add_to_cart(
    pid: int = Query(..., description="Product ID"),
    qty: int = Query(1, ge=1, description="Quantity")
):

    if pid < 0 or pid >= len(PRODUCTS):
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = PRODUCTS[pid]

    for item in cart:
        if item["id"] == pid:
            item["quantity"] += qty
            item["total"] = item["price"] * item["quantity"]
            return {"message": f"Added {qty} more of {product['name']}", "cart": cart}
    
    cart.append({
        "id": pid,
        "name": product["name"],
        "price": product["price"],
        "quantity": qty,
        "total": product["price"] * qty
    })
    
    return {"message": f"Added {product['name']} to cart", "cart": cart}


@app.delete("/cart")
async def clear_cart():
    global cart
    cart = []
    return {"message": "Cart cleared", "cart": cart}


@app.post("/checkout")
async def checkout():
    global cart, orders, order_counter
    
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total = sum(item["price"] * item["quantity"] for item in cart)
    
    order = {
        "id": order_counter,
        "items": cart.copy(),
        "total": round(total, 2),
        "created_at": datetime.now().isoformat(),
        "status": "created"
    }
    
    orders.append(order)
    order_counter += 1
    cart = []  
    
    return {"message": "Order created", "order": order}


@app.get("/orders")
async def get_orders():
    return {"orders": orders}


@app.get("/order/{oid}")
async def get_order(oid: int):
    for order in orders:
        if order["id"] == oid:
            return order
    raise HTTPException(status_code=404, detail="Order not found")