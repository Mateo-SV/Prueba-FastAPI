"""Aplicación FastAPI de prueba para QAgent (EP-09)."""
from fastapi import Depends, FastAPI, HTTPException

from app import servicios
from app.dependencias import obtener_repositorio, verificar_token
from app.modelos import ClasificacionOut, PedidoIn, PedidoOut, SaludOut

app = FastAPI(title="Prueba-FastAPI")


@app.get("/salud", response_model=SaludOut)
def salud() -> SaludOut:
    """Indica que el servicio está activo. Responde 200."""
    return SaludOut(estado="ok")


@app.post("/pedidos", response_model=PedidoOut, status_code=201)
def crear_pedido(
    datos: PedidoIn,
    repo: dict = Depends(obtener_repositorio),
    _token: str = Depends(verificar_token),
) -> PedidoOut:
    """Crea un pedido. Requiere X-Token.

    Responde 201 con el pedido, 401 sin token válido, 422 si el cuerpo es inválido.
    """
    try:
        pedido = servicios.crear_pedido(datos.cliente, datos.items, datos.descuento_pct)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    nuevo_id = len(repo) + 1
    repo[nuevo_id] = {"id": nuevo_id, **pedido}
    return PedidoOut(**repo[nuevo_id])


@app.get("/pedidos/{pedido_id}", response_model=PedidoOut)
def obtener_pedido(pedido_id: int, repo: dict = Depends(obtener_repositorio)) -> PedidoOut:
    """Devuelve un pedido por id. Responde 404 si no existe."""
    if pedido_id not in repo:
        raise HTTPException(status_code=404, detail="pedido no encontrado")
    return PedidoOut(**repo[pedido_id])


@app.get("/clasificar/{edad}", response_model=ClasificacionOut)
def clasificar(edad: int) -> ClasificacionOut:
    """Clasifica una edad en menor, adulto o mayor. Responde 422 si edad es negativa."""
    try:
        categoria = servicios.clasificar_edad(edad)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ClasificacionOut(edad=edad, categoria=categoria)
