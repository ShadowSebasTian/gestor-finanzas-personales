# -*- coding: utf-8 -*-
"""
almacenamiento.py — Persistencia simple en un archivo JSON.

Permite que los datos no se pierdan al cerrar el programa. Usa solo la librería
estándar (módulo json), así que no requiere instalar nada extra.
"""
import json
import os


def cargar(ruta):
    """
    Lee movimientos y límites de presupuesto desde un JSON.
    Si el archivo no existe, devuelve estructuras vacías (no es un error).
    """
    if not os.path.exists(ruta):          # condicional: archivo ausente → empezar de cero
        return [], {}
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    movimientos = datos.get("movimientos", [])
    limites = datos.get("limites", {})
    return movimientos, limites


def guardar(ruta, movimientos, limites):
    """Escribe movimientos y límites en el JSON (crea la carpeta si hace falta)."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)
    datos = {"movimientos": movimientos, "limites": limites}
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
