import pytest
from fastapi.testclient import TestClient

from app.dependencias import TOKEN_VALIDO, obtener_repositorio
from app.main import app

H = {"X-Token": TOKEN_VALIDO}


@pytest.fixture
def client():
    repo: dict = {}
    app.dependency_overrides[obtener_repositorio] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_salud(client):
    r = client.get("/salud")
    assert r.status_code == 200 and r.json() == {"estado": "ok"}


def test_crear_pedido_201(client):
    r = client.post("/pedidos", json={"cliente": "Ana", "items": [10, 20]}, headers=H)
    assert r.status_code == 201 and r.json()["total"] == 30


def test_crear_pedido_sin_token_401(client):
    assert client.post("/pedidos", json={"cliente": "Ana", "items": [1]}).status_code == 401


def test_crear_pedido_invalido_422(client):
    assert client.post("/pedidos", json={"cliente": "Ana"}, headers=H).status_code == 422


def test_pedido_inexistente_404(client):
    assert client.get("/pedidos/99").status_code == 404


def test_clasificar_negativa_422(client):
    assert client.get("/clasificar/-1").status_code == 422
