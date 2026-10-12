# Bugs sembrados (verdad del banco de pruebas)

QAgent debe detectarlos como `bug_detectado` (sin relajar aserciones). Cada uno está
marcado en el código con `# BUG-0X sembrado`.

| ID | Framework | Archivo | Función / ruta | Docstring dice | Código hace | Valor límite |
|---|---|---|---|---|---|---|
| BUG-01 | todos | `*/servicios.py` | `aplicar_descuento` | porcentaje 0–100 incluidos | rechaza 100 (`>=`) | `porcentaje=100` |
| BUG-02 | todos | `*/servicios.py` | `clasificar_edad` | 65 o más es "mayor" | 65 da "adulto" (`<=`) | `edad=65` |
| BUG-03 | Flask | `flask_demo/tienda/rutas.py` | `POST /pedidos` | responde 201 | responde 200 | pedido válido |
| BUG-04 | Django | `django_demo/pedidos/views.py` | `GET /pedidos/<id>` | 404 si no existe | responde 400 | id inexistente |

## Fallos esperados por carpeta

| Carpeta | Tests | Fallan a propósito |
|---|---|---|
| `.` (FastAPI) | 18 | 2 (BUG-01, BUG-02) |
| `flask_demo/` | 19 | 4 (BUG-01, BUG-02 en servicios; BUG-02 y BUG-03 en rutas) |
| `django_demo/` | 19 | 4 (BUG-01, BUG-02 en servicios; BUG-02 y BUG-04 en vistas) |

Al correr QAgent anota por bug: ¿lo detectó?, ¿en qué intento?, ¿hubo laundering?
