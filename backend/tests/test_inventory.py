from app.main import app


def test_create_and_list_products():
    with app.test_client() as client:
        resp = client.post("/inventory/", json={
            "name": "Widget A",
            "sku": "WGT-001",
            "description": "Premium widget",
            "price": 29.99,
            "stock": 100,
        })
        assert resp.status_code == 201, resp.data
        product = resp.get_json()
        assert product["id"] > 0
        assert product["sku"] == "WGT-001"

        resp = client.get("/inventory/")
        assert resp.status_code == 200
        items = resp.get_json()
        assert any(p["sku"] == "WGT-001" for p in items)
