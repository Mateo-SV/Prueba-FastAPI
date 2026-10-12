H = {"X-Token": "secreto-de-prueba"}


def test_salud(client):
    r = client.get("/salud")
    assert r.status_code == 200 and r.get_json() == {"estado": "ok"}


def test_crear_pedido_201(client):  # falla por BUG-03
    r = client.post("/pedidos", json={"cliente": "Ana", "items": [10, 20]}, headers=H)
    assert r.status_code == 201 and r.get_json()["total"] == 30


def test_crear_pedido_sin_token_401(client):
    assert client.post("/pedidos", json={"cliente": "Ana", "items": [1]}).status_code == 401


def test_crear_pedido_invalido_422(client):
    assert client.post("/pedidos", json={"cliente": "Ana"}, headers=H).status_code == 422


def test_pedido_inexistente_404(client):
    assert client.get("/pedidos/99").status_code == 404


def test_clasificar_negativa_422(client):
    assert client.get("/clasificar/-1").status_code == 422


def test_clasificar_65_es_mayor(client):  # falla por BUG-02
    assert client.get("/clasificar/65").get_json()["categoria"] == "mayor"
