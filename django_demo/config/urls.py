"""Rutas del proyecto."""
from django.urls import path

from pedidos import views

urlpatterns = [
    path("salud", views.salud),
    path("pedidos", views.crear_pedido),
    path("pedidos/<int:pedido_id>", views.obtener_pedido),
    path("clasificar/<str:edad>", views.clasificar),
]
