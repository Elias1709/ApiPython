import uuid

def test_create_lead(test_client, auth_headers):
    response = test_client.post("/leads", json={
        "nombre": "Test User",
        "email": f"test_{uuid.uuid4().hex}@example.com",
        "telefono": "3876666666",
        "fuente": "instagram",
        "producto_interes": "vestido de baño",
        "presupuesto": 150.0
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Lead registrado exitosamente"


def test_get_leads(test_client, auth_headers):
    response = test_client.get("/leads?page=1&limit=5", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "leads" in data
    assert isinstance(data["leads"], list)
    assert len(data["leads"]) >= 1
    assert "email" in data["leads"][0]


def test_get_lead_by_id(test_client, auth_headers):
    payload = {
        "nombre": "Lead Consulta",
        "email": f"consulta_{uuid.uuid4().hex}@example.com",
        "fuente": "facebook"
    }
    create_response = test_client.post("/leads", json=payload, headers=auth_headers)
    assert create_response.status_code == 200
    lead_id = create_response.json()["id"]

    response = test_client.get(f"/leads/{lead_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["nombre"] == payload["nombre"]


def test_update_lead(test_client, auth_headers):
    payload = {
        "nombre": "Lead Update",
        "email": f"update_{uuid.uuid4().hex}@example.com",
        "fuente": "instagram"
    }
    create_response = test_client.post("/leads", json=payload, headers=auth_headers)
    assert create_response.status_code == 200
    lead_id = create_response.json()["id"]

    updated = {
        "nombre": "Lead Actualizado",
        "fuente": "instagram"
    }
    response = test_client.patch(f"/leads/{lead_id}", json=updated, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Lead actualizado exitosamente"


def test_delete_lead(test_client, auth_headers):
    payload = {
        "nombre": "Lead Delete",
        "email": f"delete_{uuid.uuid4().hex}@example.com",
        "fuente": "facebook"
    }
    create_response = test_client.post("/leads", json=payload, headers=auth_headers)
    assert create_response.status_code == 200
    lead_id = create_response.json()["id"]

    response = test_client.delete(f"/leads/{lead_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Lead eliminado (soft delete)"
