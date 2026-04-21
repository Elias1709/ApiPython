
def test_create_lead(client):
    response = client.post("/leads", json={
        "nombre": "Test User4",
        "email": "test4@example.com",
        "telefono": "3876666666",
        "fuente": "instagram",
        "producto_interes": "vestido de baño",
        "presupuesto": 150.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Lead registrado exitosamente"


def test_get_leads(client):
    response = client.get("/leads")
    assert response.status_code == 200
    data = response.json()
    assert "leads" in data
    assert isinstance(data["leads"], list)
    assert len(data["leads"]) >= 1
    assert "email" in data["leads"][0]


def test_get_lead_by_email(client):
    payload = {
        "nombre": "Lead Consulta",
        "email": "consulta@example.com",
        "fuente": "facebook"
    }
    client.post("/leads", json=payload)

    response = client.get(f"/leads/{payload['email']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["nombre"] == payload["nombre"]


def test_update_lead(client):
    payload = {
        "nombre": "Lead Update",
        "email": "update@example.com",
        "fuente": "instagram"
    }
    client.post("/leads", json=payload)

    updated = {
        "nombre": "Lead Actualizado",
        "email": "update@example.com",
        "fuente": "instagram"
    }
    response = client.put(f"/leads/{payload['email']}", json=updated)
    assert response.status_code == 200
    assert response.json()["message"] == "Lead actualizado exitosamente"


def test_delete_lead(client):
    payload = {
        "nombre": "Lead Delete",
        "email": "delete@example.com",
        "fuente": "facebook"
    }
    client.post("/leads", json=payload)

    response = client.delete(f"/leads/{payload['email']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Lead eliminado exitosamente"
