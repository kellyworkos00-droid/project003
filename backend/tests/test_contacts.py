from app.main import app


def test_create_and_list_contacts():
    with app.test_client() as client:
        resp = client.post("/contacts/", json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "phone": "+1-555-0100",
            "company": "Analytical Engines",
        })
        assert resp.status_code == 201, resp.data
        created = resp.get_json()
        assert created["id"] > 0
        assert created["name"] == "Ada Lovelace"

        resp = client.get("/contacts/")
        assert resp.status_code == 200
        items = resp.get_json()
        assert any(c["name"] == "Ada Lovelace" for c in items)
