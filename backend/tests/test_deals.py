from app.main import app


def test_create_and_list_deals():
    with app.test_client() as client:
        # Create a contact to relate to (optional)
        c_resp = client.post("/contacts/", json={"name": "Grace Hopper"})
        assert c_resp.status_code == 201
        contact_id = c_resp.get_json()["id"]

        # Create a deal
        d_resp = client.post("/deals/", json={
            "title": "Big Contract",
            "amount": 1234.56,
            "stage": "qualified",
            "contact_id": contact_id,
        })
        assert d_resp.status_code == 201, d_resp.data
        deal = d_resp.get_json()
        assert deal["id"] > 0
        assert deal["title"] == "Big Contract"

        # List
        resp = client.get("/deals/")
        assert resp.status_code == 200
        items = resp.get_json()
        assert any(d["title"] == "Big Contract" for d in items)
