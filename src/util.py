# -*- coding: utf-8 -*-
"""
util.py — Utilidades de entrada/salida por consola.

Concentra la lectura de datos por teclado con VALIDACIÓN mediante bucles:
si el usuario escribe algo inválido, se le vuelve a preguntar (no se cae el programa).
"""


def formato_moneda(valor):
    """Devuelve el valor como texto de dinero, p. ej. 1234.5 → '$1,234.50'."""
    return f"${valor:,.2f}"


def leer_texto(mensaje, defecto=""):
    """Lee texto; si se deja vacío, usa el valor por defecto."""
    respuesta = input(mensaje).strip()
    return respuesta if respuesta else defecto


def leer_monto(mensaje):
    """
    Pide un número positivo y NO se rinde hasta obtenerlo.
    Bucle 'while True' + manejo de error: patrón clásico de validación de entrada.
    """
    while True:                                  # bucle de reintento
        entrada = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            print("  ✗ Escribe un número (ej. 25.50).")
            continue
        if valor <= 0:                           # condicional: rechazar 0 o negativos
            print("  ✗ El monto debe ser mayor que cero.")
            continue
        return round(valor, 2)


def elegir_opcion(mensaje, opciones):
    """
    Muestra una lista numerada y devuelve la opción elegida (texto).
    'opciones' es una lista de strings. Repite hasta que la elección sea válida.
    """
    while True:                                  # bucle de reintento
        print(mensaje)
        for i, opcion in enumerate(opciones, start=1):   # bucle para numerar
            print(f"  {i}) {opcion}")
        eleccion = input("  Elige una opción: ").strip()
        if eleccion.isdigit():                   # condicional: ¿es número?
            indice = int(eleccion)
            if 1 <= indice <= len(opciones):     # condicional: ¿está en rango?
                return opciones[indice - 1]
        print("  ✗ Opción no válida, intenta de nuevo.\n")
