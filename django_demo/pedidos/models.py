"""Modelos de la app pedidos."""
from django.db import models


class Pedido(models.Model):
    """Pedido de un cliente con su total ya calculado."""

    cliente = models.CharField(max_length=100)
    items = models.JSONField()
    subtotal = models.FloatField()
    descuento_pct = models.FloatField(default=0)
    total = models.FloatField()

    def a_dict(self) -> dict:
        """Devuelve el pedido como diccionario serializable."""
        return {
            "id": self.id,
            "cliente": self.cliente,
            "items": self.items,
            "subtotal": self.subtotal,
            "descuento_pct": self.descuento_pct,
            "total": self.total,
        }
