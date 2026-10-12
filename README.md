# Prueba-FastAPI

Repositorio de apoyo para el SPK de QAgent: software FastAPI con docstrings claros,
endpoints con `response_model`, `Depends`, validación 422 y bugs sembrados.

## Instalar y ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate        # Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload # http://127.0.0.1:8000/docs
pytest                        # 2 fallos esperados (BUG-01, BUG-02)
```

## Endpoints

| Método | Ruta | Qué cubre |
|---|---|---|
| GET | `/salud` | T1 humo (200) |
| POST | `/pedidos` | T3 funcional (201), T4 límite (422), T8 errores (401 `Depends`) |
| GET | `/pedidos/{id}` | T8 (404) |
| GET | `/clasificar/{edad}` | T4 límite (422, bordes 17/18/64/65) |

Token de prueba: encabezado `X-Token: secreto-de-prueba`.

## Funciones (app/servicios.py)

`calcular_total`, `aplicar_descuento`, `calcular_iva`, `clasificar_edad`,
`normalizar_email`, `leer_config` (E/S), `crear_pedido` (integración, `llama_a`).
Ver `BUGS.md` para los bugs sembrados.
