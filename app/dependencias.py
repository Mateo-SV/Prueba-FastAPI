"""Dependencias (Depends) de la API."""
from fastapi import Header, HTTPException

TOKEN_VALIDO = "secreto-de-prueba"
_PEDIDOS: dict[int, dict] = {}


def verificar_token(x_token: str = Header(default="")) -> str:
    """Valida el encabezado X-Token.

    Raises:
        HTTPException: 401 si el token falta o no coincide.
    """
    if x_token != TOKEN_VALIDO:
        raise HTTPException(status_code=401, detail="token inválido")
    return x_token


def obtener_repositorio() -> dict[int, dict]:
    """Devuelve el almacén en memoria de pedidos (reemplazable en pruebas)."""
    return _PEDIDOS
