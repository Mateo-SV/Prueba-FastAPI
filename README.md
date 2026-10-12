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

## Frameworks de prueba (SPK de alcance)

El mismo dominio (pedidos, descuento, clasificación de edad) en tres frameworks:

| Carpeta | Framework | Cliente de pruebas | Ejecutar |
|---|---|---|---|
| `.` (`app/`) | FastAPI | `TestClient` | `pip install -r requirements.txt && pytest` |
| `flask_demo/` | Flask | `app.test_client()` | `cd flask_demo && pip install -r requirements.txt && pytest` |
| `django_demo/` | Django | `Client` + `pytest-django` | `cd django_demo && pip install -r requirements.txt && pytest` |

Cada carpeta tiene sus propias dependencias y su `pytest.ini`; se prueban por separado.
Los bugs sembrados están en `BUGS.md`. Los fallos de pytest son esperados.
