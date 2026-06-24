# -*- coding: utf-8 -*-
"""
finanzas.py — Lógica pura del Gestor de Finanzas Personales.

Aquí vive el "qué hace" el programa, SIN pedir datos por teclado ni imprimir menús
(eso es trabajo de main.py). Mantener esta capa separada permite probarla con
pruebas automáticas y razonar la lógica con claridad.

Estructuras de Lógica de Programación que se usan y se ven aquí:
  - Bucles (for) para recorrer y acumular movimientos.
  - Condicionales (if/elif/else) para clasificar ingresos vs. gastos.
"""

# Categorías sugeridas para clasificar los movimientos.
CATEGORIAS_INGRESO = ["Sueldo", "Beca", "Venta", "Otro"]
CATEGORIAS_GASTO = ["Comida", "Transporte", "Vivienda", "Educación", "Ocio", "Otro"]


class GestorFinanzas:
    """Mantiene la lista de movimientos y calcula totales a partir de ella."""

    def __init__(self, movimientos=None):
        # Cada movimiento es un dict: {tipo, categoria, monto, descripcion, fecha}.
        self.movimientos = list(movimientos) if movimientos else []

    # ---------------------------------------------------------------- registrar
    def _agregar(self, tipo, monto, categoria, descripcion, fecha):
        """Valida y agrega un movimiento. Devuelve el dict creado."""
        # Condicional de validación: el monto debe ser un número positivo.
        if monto is None or monto <= 0:
            raise ValueError("El monto debe ser un número mayor que cero.")
        movimiento = {
            "tipo": tipo,
            "categoria": categoria or "Otro",
            "monto": round(float(monto), 2),
            "descripcion": (descripcion or "").strip(),
            "fecha": fecha or "",
        }
        self.movimientos.append(movimiento)
        return movimiento

    def agregar_ingreso(self, monto, categoria="Otro", descripcion="", fecha=""):
        return self._agregar("ingreso", monto, categoria, descripcion, fecha)

    def agregar_gasto(self, monto, categoria="Otro", descripcion="", fecha=""):
        return self._agregar("gasto", monto, categoria, descripcion, fecha)

    # ------------------------------------------------------------------ totales
    def total_ingresos(self):
        """Suma todos los ingresos recorriendo la lista con un bucle for."""
        total = 0.0
        for m in self.movimientos:           # bucle
            if m["tipo"] == "ingreso":       # condicional
                total += m["monto"]
        return round(total, 2)

    def total_gastos(self):
        """Suma todos los gastos."""
        total = 0.0
        for m in self.movimientos:           # bucle
            if m["tipo"] == "gasto":         # condicional
                total += m["monto"]
        return round(total, 2)

    def saldo(self):
        """Saldo disponible = ingresos − gastos."""
        return round(self.total_ingresos() - self.total_gastos(), 2)

    def total_por_categoria(self, tipo="gasto"):
        """
        Devuelve un dict {categoria: total} para el tipo pedido.
        Ejemplo de acumulación dentro de un bucle, decidiendo con condicionales.
        """
        acumulado = {}
        for m in self.movimientos:               # bucle
            if m["tipo"] != tipo:                # condicional: ignora el otro tipo
                continue
            categoria = m["categoria"]
            # Si la categoría no existe aún en el dict, se inicia en 0.
            if categoria not in acumulado:
                acumulado[categoria] = 0.0
            acumulado[categoria] += m["monto"]
        # Redondeo final de cada total.
        for categoria in acumulado:
            acumulado[categoria] = round(acumulado[categoria], 2)
        return acumulado

    def gasto_en_categoria(self, categoria):
        """Total gastado en UNA categoría concreta (se usa en las alertas)."""
        return self.total_por_categoria("gasto").get(categoria, 0.0)

    def promedio_gastos(self):
        """Promedio por gasto. Evita dividir entre cero con un condicional."""
        gastos = [m["monto"] for m in self.movimientos if m["tipo"] == "gasto"]
        if not gastos:                       # condicional: sin gastos no hay promedio
            return 0.0
        return round(sum(gastos) / len(gastos), 2)

    def cantidad_movimientos(self):
        return len(self.movimientos)
