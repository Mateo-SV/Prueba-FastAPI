"""Lógica de negocio pura de Prueba-FastAPI.

Funciones sin FastAPI, pensadas como objetivo de prueba para QAgent (T1-T5, T8).
"""
import json
from pathlib import Path


def calcular_total(items: list[float]) -> float:
    """Suma los precios de la lista.

    Args:
        items: precios de los productos.

    Returns:
        La suma de los precios. Una lista vacía devuelve 0.0.

    Raises:
        TypeError: si items es None.
        ValueError: si algún precio es negativo.
    """
    if items is None:
        raise TypeError("items no puede ser None")
    if any(precio < 0 for precio in items):
        raise ValueError("los precios no pueden ser negativos")
    return float(sum(items))


def aplicar_descuento(total: float, porcentaje: float) -> float:
    """Aplica un descuento porcentual al total.

    Args:
        total: monto original, mayor o igual a 0.
        porcentaje: descuento entre 0 y 100, ambos incluidos.

    Returns:
        El total con el descuento aplicado, redondeado a 2 decimales.

    Raises:
        ValueError: si total es negativo o porcentaje está fuera de 0-100.
    """
    if total < 0:
        raise ValueError("total negativo")
    if porcentaje < 0 or porcentaje >= 100:  # BUG-01 sembrado: 100 debería ser válido
        raise ValueError("porcentaje fuera de rango")
    return round(total * (1 - porcentaje / 100), 2)


def calcular_iva(subtotal: float, tasa: float = 0.18) -> float:
    """Calcula el IVA de un subtotal.

    Args:
        subtotal: monto sin impuesto, mayor o igual a 0.
        tasa: tasa del impuesto entre 0 y 1 (por defecto 0.18).

    Returns:
        El monto del IVA redondeado a 2 decimales.

    Raises:
        ValueError: si subtotal es negativo o tasa está fuera de 0-1.
    """
    if subtotal < 0:
        raise ValueError("subtotal negativo")
    if not 0 <= tasa <= 1:
        raise ValueError("tasa fuera de rango")
    return round(subtotal * tasa, 2)


def clasificar_edad(edad: int) -> str:
    """Clasifica a una persona por su edad.

    Args:
        edad: edad en años, entera y mayor o igual a 0.

    Returns:
        "menor" si edad < 18, "adulto" si 18 <= edad <= 64, "mayor" si edad >= 65.

    Raises:
        ValueError: si edad es negativa.
    """
    if edad < 0:
        raise ValueError("edad negativa")
    if edad < 18:
        return "menor"
    if edad <= 65:  # BUG-02 sembrado: 65 debería ser "mayor"
        return "adulto"
    return "mayor"


def normalizar_email(email: str) -> str:
    """Normaliza un correo: quita espacios y pasa a minúsculas.

    Args:
        email: correo escrito por el usuario.

    Returns:
        El correo sin espacios en los extremos y en minúsculas.

    Raises:
        ValueError: si el texto no contiene "@".
    """
    limpio = email.strip().lower()
    if "@" not in limpio:
        raise ValueError("correo inválido")
    return limpio


def leer_config(ruta: Path) -> dict:
    """Lee un archivo de configuración en formato JSON.

    Args:
        ruta: ruta del archivo.

    Returns:
        El contenido del archivo como diccionario.

    Raises:
        FileNotFoundError: si el archivo no existe.
        ValueError: si el contenido no es JSON válido o no es un objeto.
    """
    texto = Path(ruta).read_text(encoding="utf-8")
    datos = json.loads(texto)
    if not isinstance(datos, dict):
        raise ValueError("la configuración debe ser un objeto JSON")
    return datos


def crear_pedido(cliente: str, items: list[float], descuento_pct: float = 0.0) -> dict:
    """Crea un pedido calculando su total con descuento.

    Args:
        cliente: nombre del cliente, no vacío.
        items: precios de los productos, al menos uno.
        descuento_pct: descuento entre 0 y 100.

    Returns:
        Diccionario con cliente, items, subtotal, descuento_pct y total.

    Raises:
        ValueError: si cliente está vacío, items está vacío o los datos son inválidos.
    """
    if not cliente.strip():
        raise ValueError("cliente vacío")
    if not items:
        raise ValueError("el pedido necesita al menos un item")
    subtotal = calcular_total(items)
    total = aplicar_descuento(subtotal, descuento_pct)
    return {
        "cliente": cliente.strip(),
        "items": list(items),
        "subtotal": subtotal,
        "descuento_pct": descuento_pct,
        "total": total,
    }
