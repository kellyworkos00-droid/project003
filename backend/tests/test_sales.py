from app.main import app


def test_create_and_list_orders():
    with app.test_client() as client:
        # Create contact
        c_resp = client.post("/contacts/", json={"name": "Test Customer"})
        assert c_resp.status_code == 201
        contact_id = c_resp.get_json()["id"]

        # Create order
        resp = client.post("/sales/", json={
            "order_number": "SO-001",
            "contact_id": contact_id,
            "status": "confirmed",
            "total": 500.00,
        })
        assert resp.status_code == 201, resp.data
        order = resp.get_json()
        assert order["id"] > 0
        assert order["order_number"] == "SO-001"

        resp = client.get("/sales/")
        assert resp.status_code == 200
        items = resp.get_json()
        assert any(s["order_number"] == "SO-001" for s in items)
