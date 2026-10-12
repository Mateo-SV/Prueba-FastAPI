import json

import pytest

from tienda import servicios as s


def test_calcular_total_vacio():
    assert s.calcular_total([]) == 0


def test_calcular_total_suma():
    assert s.calcular_total([10, 20]) == 30


def test_calcular_total_none():
    with pytest.raises(TypeError):
        s.calcular_total(None)


def test_calcular_total_negativo():
    with pytest.raises(ValueError):
        s.calcular_total([-1])


def test_descuento_normal():
    assert s.aplicar_descuento(200, 10) == 180


def test_descuento_100_es_valido():  # falla por BUG-01
    assert s.aplicar_descuento(50, 100) == 0


def test_clasificar_65_es_mayor():  # falla por BUG-02
    assert s.clasificar_edad(65) == "mayor"


def test_clasificar_limites():
    assert s.clasificar_edad(17) == "menor"
    assert s.clasificar_edad(18) == "adulto"


def test_email_sin_arroba():
    with pytest.raises(ValueError):
        s.normalizar_email("sin-arroba")


def test_leer_config_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        s.leer_config(tmp_path / "no.json")


def test_leer_config_ok(tmp_path):
    ruta = tmp_path / "c.json"
    ruta.write_text(json.dumps({"a": 1}))
    assert s.leer_config(ruta) == {"a": 1}


def test_crear_pedido_integra_calculos():
    p = s.crear_pedido("Ana", [10, 20], 50)
    assert p["total"] == 15
