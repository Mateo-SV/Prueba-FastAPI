"""Modelos Pydantic de entrada y salida de la API."""
from pydantic import BaseModel, Field


class PedidoIn(BaseModel):
    """Cuerpo para crear un pedido."""

    cliente: str = Field(min_length=1)
    items: list[float] = Field(min_length=1)
    descuento_pct: float = Field(default=0.0, ge=0, le=100)


class PedidoOut(BaseModel):
    """Pedido creado."""

    id: int
    cliente: str
    items: list[float]
    subtotal: float
    descuento_pct: float
    total: float


class ClasificacionOut(BaseModel):
    """Resultado de clasificar una edad."""

    edad: int
    categoria: str


class SaludOut(BaseModel):
    """Estado del servicio."""

    estado: str
