"""Rutas Flask (Blueprint) de la tienda de prueba."""
from functools import wraps

from flask import Blueprint, current_app, jsonify, request

from tienda import servicios

bp = Blueprint("tienda", __name__)
TOKEN_VALIDO = "secreto-de-prueba"


def requiere_token(vista):
    """Decorador: exige el encabezado X-Token. Responde 401 si falta o no coincide."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if request.headers.get("X-Token", "") != TOKEN_VALIDO:
            return jsonify({"detail": "token inválido"}), 401
        return vista(*args, **kwargs)

    return envoltura


@bp.get("/salud")
def salud():
    """Indica que el servicio está activo. Responde 200 con {"estado": "ok"}."""
    return jsonify({"estado": "ok"}), 200


@bp.post("/pedidos")
@requiere_token
def crear_pedido():
    """Crea un pedido. Requiere X-Token.

    Cuerpo JSON: cliente (texto no vacío), items (lista de números, al menos uno)
    y descuento_pct (0-100, opcional).

    Responde 201 con el pedido creado, 401 sin token válido y 422 si el cuerpo es inválido.
    """
    datos = request.get_json(silent=True) or {}
    try:
        pedido = servicios.crear_pedido(
            datos.get("cliente", ""), datos.get("items") or [], datos.get("descuento_pct", 0.0)
        )
    except (ValueError, TypeError, AttributeError) as exc:
        return jsonify({"detail": str(exc)}), 422
    repo = current_app.config["PEDIDOS"]
    pedido["id"] = len(repo) + 1
    repo[pedido["id"]] = pedido
    return jsonify(pedido), 200  # BUG-03 sembrado: debería responder 201


@bp.get("/pedidos/<int:pedido_id>")
def obtener_pedido(pedido_id: int):
    """Devuelve un pedido por id. Responde 200 con el pedido o 404 si no existe."""
    pedido = current_app.config["PEDIDOS"].get(pedido_id)
    if pedido is None:
        return jsonify({"detail": "pedido no encontrado"}), 404
    return jsonify(pedido), 200


@bp.get("/clasificar/<edad>")
def clasificar(edad: str):
    """Clasifica una edad en menor, adulto o mayor.

    Responde 200 con {"edad": n, "categoria": texto}. Responde 422 si edad no es un
    entero o es negativa.
    """
    try:
        categoria = servicios.clasificar_edad(int(edad))
    except ValueError as exc:
        return jsonify({"detail": str(exc)}), 422
    return jsonify({"edad": int(edad), "categoria": categoria}), 200
