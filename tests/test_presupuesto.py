# -*- coding: utf-8 -*-
"""Pruebas de las reglas de presupuesto y alertas (presupuesto.py)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from finanzas import GestorFinanzas      # noqa: E402
from presupuesto import Presupuesto      # noqa: E402


class TestPresupuesto(unittest.TestCase):

    def setUp(self):
        self.p = Presupuesto({"Comida": 200.0, "Vivienda": 300.0})

    def test_niveles_de_alerta(self):
        # 0 % → ok ; 60 % → aviso ; 90 % → atención ; 100 % → sobregiro
        self.assertEqual(self.p.evaluar_categoria("Comida", 0)["nivel"], "ok")
        self.assertEqual(self.p.evaluar_categoria("Comida", 120)["nivel"], "aviso")
        self.assertEqual(self.p.evaluar_categoria("Comida", 180)["nivel"], "atencion")
        self.assertEqual(self.p.evaluar_categoria("Comida", 200)["nivel"], "sobregiro")
        self.assertEqual(self.p.evaluar_categoria("Comida", 260)["nivel"], "sobregiro")

    def test_categoria_sin_limite(self):
        self.assertEqual(self.p.evaluar_categoria("Ocio", 50)["nivel"], "sin_limite")

    def test_alerta_por_gasto_grande(self):
        # 70 > 30% de 200 (=60) → debe avisar
        self.assertIsNotNone(self.p.alerta_por_gasto("Comida", 70))
        # 40 < 60 → no avisa
        self.assertIsNone(self.p.alerta_por_gasto("Comida", 40))

    def test_panel_recorre_categorias(self):
        g = GestorFinanzas()
        g.agregar_gasto(300, "Vivienda")
        g.agregar_gasto(120, "Comida")
        panel = self.p.panel(g)
        self.assertEqual(len(panel), 2)              # una entrada por categoría con límite
        niveles = {r["mensaje"].split()[1] for r in panel}
        self.assertTrue(niveles)                     # produjo mensajes


if __name__ == "__main__":
    unittest.main()
