"""Vistas basadas en funciones de la tienda de prueba."""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from pedidos import servicios
from pedidos.models import Pedido

TOKEN_VALIDO = "secreto-de-prueba"


@require_GET
def salud(request):
    """Indica que el servicio está activo. Responde 200 con {"estado": "ok"}."""
    return JsonResponse({"estado": "ok"})


@csrf_exempt
@require_POST
def crear_pedido(request):
    """Crea un pedido. Requiere el encabezado X-Token.

    Cuerpo JSON: cliente, items (al menos uno) y descuento_pct (0-100, opcional).

    Responde 201 con el pedido creado, 401 sin token válido y 422 si el cuerpo es inválido.
    """
    if request.headers.get("X-Token", "") != TOKEN_VALIDO:
        return JsonResponse({"detail": "token inválido"}, status=401)
    try:
        datos = json.loads(request.body or b"{}")
        pedido = servicios.crear_pedido(
            datos.get("cliente", ""), datos.get("items") or [], datos.get("descuento_pct", 0.0)
        )
    except (ValueError, TypeError, AttributeError) as exc:
        return JsonResponse({"detail": str(exc)}, status=422)
    obj = Pedido.objects.create(
        cliente=pedido["cliente"],
        items=pedido["items"],
        subtotal=pedido["subtotal"],
        descuento_pct=pedido["descuento_pct"],
        total=pedido["total"],
    )
    return JsonResponse(obj.a_dict(), status=201)


@require_GET
def obtener_pedido(request, pedido_id: int):
    """Devuelve un pedido por id. Responde 200 con el pedido o 404 si no existe."""
    try:
        return JsonResponse(Pedido.objects.get(id=pedido_id).a_dict())
    except Pedido.DoesNotExist:
        return JsonResponse({"detail": "pedido no encontrado"}, status=400)  # BUG-04 sembrado: debería ser 404


@require_GET
def clasificar(request, edad: str):
    """Clasifica una edad en menor, adulto o mayor.

    Responde 200 con {"edad": n, "categoria": texto}. Responde 422 si edad no es un
    entero o es negativa.
    """
    try:
        categoria = servicios.clasificar_edad(int(edad))
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=422)
    return JsonResponse({"edad": int(edad), "categoria": categoria})
