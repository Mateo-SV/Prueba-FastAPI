"""Aplicación Flask de prueba para QAgent (fábrica create_app)."""
from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    """Crea y configura la aplicación Flask.

    Args:
        config: valores opcionales que reemplazan la configuración por defecto.

    Returns:
        La aplicación lista, con el blueprint registrado y un almacén de pedidos vacío.
    """
    app = Flask(__name__)
    app.config["PEDIDOS"] = {}
    app.config.update(config or {})

    from tienda.rutas import bp

    app.register_blueprint(bp)
    return app
