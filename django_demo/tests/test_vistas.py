import json

import pytest

H = {"HTTP_X_TOKEN": "secreto-de-prueba"}


def post(client, cuerpo, **extra):
    return client.post("/pedidos", data=json.dumps(cuerpo), content_type="application/json", **extra)


def test_salud(client):
    r = client.get("/salud")
    assert r.status_code == 200 and r.json() == {"estado": "ok"}


@pytest.mark.django_db
def test_crear_pedido_201(client):
    r = post(client, {"cliente": "Ana", "items": [10, 20]}, **H)
    assert r.status_code == 201 and r.json()["total"] == 30


def test_crear_pedido_sin_token_401(client):
    assert post(client, {"cliente": "Ana", "items": [1]}).status_code == 401


def test_crear_pedido_invalido_422(client):
    assert post(client, {"cliente": "Ana"}, **H).status_code == 422


@pytest.mark.django_db
def test_pedido_inexistente_404(client):  # falla por BUG-04
    assert client.get("/pedidos/99").status_code == 404


def test_clasificar_negativa_422(client):
    assert client.get("/clasificar/-1").status_code == 422


def test_clasificar_65_es_mayor(client):  # falla por BUG-02
    assert client.get("/clasificar/65").json()["categoria"] == "mayor"
