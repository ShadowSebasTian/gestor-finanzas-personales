# -*- coding: utf-8 -*-
"""
presupuesto.py — Reglas de presupuesto y alertas.

Esta es la parte "inteligente" del programa: compara lo gastado en cada categoría
contra un límite y decide, mediante CONDICIONALES escalonados, qué alerta mostrar.
También recorre todas las categorías con un BUCLE para construir un panel de alertas.
"""

# Umbrales (porcentaje del límite de la categoría) que disparan cada nivel.
UMBRAL_AVISO = 0.50      # 50 %  → conviene vigilar
UMBRAL_ATENCION = 0.80   # 80 %  → atención
UMBRAL_SOBREGIRO = 1.00  # 100 % → presupuesto superado


class Presupuesto:
    """Guarda un límite de gasto por categoría y evalúa el estado de cada una."""

    def __init__(self, limites=None):
        # limites: dict {categoria: monto_maximo_mensual}
        self.limites = dict(limites) if limites else {}

    def definir_limite(self, categoria, monto):
        """Asigna (o cambia) el límite de una categoría."""
        if monto <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        self.limites[categoria] = round(float(monto), 2)

    def evaluar_categoria(self, categoria, gastado):
        """
        Decide el nivel de alerta de UNA categoría según el gasto acumulado.
        Devuelve un dict con nivel, mensaje y porcentaje usado.

        Aquí se ve el condicional escalonado (if / elif / else): el orden importa,
        porque se evalúa de la condición más grave a la más leve.
        """
        limite = self.limites.get(categoria)
        if limite is None:
            return {"nivel": "sin_limite", "porcentaje": 0.0,
                    "mensaje": f"'{categoria}' no tiene presupuesto definido."}

        porcentaje = (gastado / limite) if limite else 0.0

        if porcentaje >= UMBRAL_SOBREGIRO:
            nivel = "sobregiro"
            mensaje = (f"🔴 SOBREGIRO en {categoria}: gastaste "
                       f"{porcentaje*100:.0f}% del presupuesto.")
        elif porcentaje >= UMBRAL_ATENCION:
            nivel = "atencion"
            mensaje = (f"🟠 Atención en {categoria}: vas al "
                       f"{porcentaje*100:.0f}% del presupuesto.")
        elif porcentaje >= UMBRAL_AVISO:
            nivel = "aviso"
            mensaje = (f"🟡 Aviso en {categoria}: llevas el "
                       f"{porcentaje*100:.0f}% del presupuesto.")
        else:
            nivel = "ok"
            mensaje = (f"🟢 {categoria} bajo control: "
                       f"{porcentaje*100:.0f}% del presupuesto.")

        return {"nivel": nivel, "porcentaje": round(porcentaje, 4), "mensaje": mensaje}

    def alerta_por_gasto(self, categoria, monto_gasto):
        """
        Alerta inmediata cuando UN solo gasto es muy grande respecto al límite
        de su categoría (más del 30 %). Devuelve un mensaje o None.
        """
        limite = self.limites.get(categoria)
        if limite and monto_gasto > 0.30 * limite:
            return (f"⚠ Ese gasto representa el {monto_gasto/limite*100:.0f}% "
                    f"del presupuesto de {categoria}.")
        return None

    def panel(self, gestor):
        """
        Recorre TODAS las categorías con límite y arma la lista de evaluaciones.
        Ejemplo de bucle que produce una colección de resultados.
        """
        resultados = []
        for categoria in sorted(self.limites):       # bucle sobre las categorías
            gastado = gestor.gasto_en_categoria(categoria)
            resultados.append(self.evaluar_categoria(categoria, gastado))
        return resultados
