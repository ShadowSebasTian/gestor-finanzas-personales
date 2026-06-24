# -*- coding: utf-8 -*-
"""Pruebas de la lógica pura de finanzas.py (no requieren teclado)."""
import os
import sys
import unittest

# Hace visible la carpeta src/ para poder importar los módulos.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from finanzas import GestorFinanzas  # noqa: E402


class TestGestorFinanzas(unittest.TestCase):

    def setUp(self):
        self.g = GestorFinanzas()
        self.g.agregar_ingreso(1000, "Sueldo")
        self.g.agregar_gasto(300, "Vivienda")
        self.g.agregar_gasto(100, "Comida")
        self.g.agregar_gasto(50, "Comida")

    def test_totales(self):
        self.assertEqual(self.g.total_ingresos(), 1000.0)
        self.assertEqual(self.g.total_gastos(), 450.0)
        self.assertEqual(self.g.saldo(), 550.0)

    def test_total_por_categoria(self):
        gastos = self.g.total_por_categoria("gasto")
        self.assertEqual(gastos["Comida"], 150.0)
        self.assertEqual(gastos["Vivienda"], 300.0)

    def test_promedio_gastos(self):
        # (300 + 100 + 50) / 3 = 150
        self.assertEqual(self.g.promedio_gastos(), 150.0)

    def test_promedio_sin_gastos(self):
        vacio = GestorFinanzas()
        self.assertEqual(vacio.promedio_gastos(), 0.0)

    def test_monto_invalido(self):
        with self.assertRaises(ValueError):
            self.g.agregar_gasto(0, "Comida")
        with self.assertRaises(ValueError):
            self.g.agregar_ingreso(-5, "Sueldo")


if __name__ == "__main__":
    unittest.main()
