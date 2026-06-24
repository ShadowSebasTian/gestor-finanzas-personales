# -*- coding: utf-8 -*-
"""
main.py — Programa principal del Gestor de Finanzas Personales (consola).

Aquí se "arma" todo: el BUCLE del menú (while) que mantiene el programa vivo y los
CONDICIONALES (if/elif/else) que deciden qué hacer según la opción elegida.
La lógica de cálculo vive en finanzas.py y presupuesto.py; la entrada de datos en util.py.

Uso:
    python src/main.py          # modo interactivo (menú)
    python src/main.py --demo   # demostración automática (sin teclado), para el video
"""
import datetime
import os
import sys

from finanzas import GestorFinanzas, CATEGORIAS_INGRESO, CATEGORIAS_GASTO
from presupuesto import Presupuesto
import almacenamiento
import util

# Rutas de datos (relativas a este archivo, para que funcione desde cualquier carpeta).
BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE, "..", "datos", "finanzas.json")   # datos del usuario
ARCHIVO_EJEMPLO = os.path.join(BASE, "..", "datos", "ejemplo.json")  # semilla de ejemplo


def hoy():
    return datetime.date.today().isoformat()


# ----------------------------------------------------------------- carga inicial
def cargar_estado():
    """Carga los datos del usuario; si no existen, parte del ejemplo incluido."""
    ruta = ARCHIVO_DATOS if os.path.exists(ARCHIVO_DATOS) else ARCHIVO_EJEMPLO
    movimientos, limites = almacenamiento.cargar(ruta)
    return GestorFinanzas(movimientos), Presupuesto(limites)


# ---------------------------------------------------------------- acciones menú
def registrar(gestor, presupuesto, tipo):
    """Registra un ingreso o un gasto pidiendo los datos por teclado."""
    print(f"\n— Registrar {tipo} —")
    monto = util.leer_monto("  Monto: $")
    categorias = CATEGORIAS_INGRESO if tipo == "ingreso" else CATEGORIAS_GASTO
    categoria = util.elegir_opcion("  Categoría:", categorias)
    descripcion = util.leer_texto("  Descripción (opcional): ")
    fecha = util.leer_texto(f"  Fecha [{hoy()}]: ", defecto=hoy())

    if tipo == "ingreso":
        gestor.agregar_ingreso(monto, categoria, descripcion, fecha)
    else:
        gestor.agregar_gasto(monto, categoria, descripcion, fecha)
        # Alerta inmediata si el gasto es grande frente al presupuesto de su categoría.
        aviso = presupuesto.alerta_por_gasto(categoria, monto)
        if aviso:
            print("  " + aviso)

    print(f"  ✓ {tipo.capitalize()} de {util.formato_moneda(monto)} "
          f"registrado en '{categoria}'.")


def ver_resumen(gestor):
    """Muestra saldo, totales y desglose por categoría (recorridos con bucles)."""
    print("\n========== RESUMEN ==========")
    print(f"  Ingresos: {util.formato_moneda(gestor.total_ingresos())}")
    print(f"  Gastos:   {util.formato_moneda(gestor.total_gastos())}")
    print(f"  Saldo:    {util.formato_moneda(gestor.saldo())}")
    print(f"  Movimientos registrados: {gestor.cantidad_movimientos()}")

    gastos_cat = gestor.total_por_categoria("gasto")
    if gastos_cat:                                   # condicional: ¿hay gastos?
        print("\n  Gasto por categoría:")
        for categoria, total in sorted(gastos_cat.items()):   # bucle
            print(f"    - {categoria}: {util.formato_moneda(total)}")
        print(f"  Promedio por gasto: {util.formato_moneda(gestor.promedio_gastos())}")
    else:
        print("  (Aún no hay gastos registrados.)")
    print("=============================")


def gestionar_presupuesto(gestor, presupuesto):
    """Submenú: ver el panel de alertas o definir el límite de una categoría."""
    while True:                                      # bucle del submenú
        print("\n— Presupuesto y alertas —")
        if presupuesto.limites:                      # condicional: ¿hay límites?
            for resultado in presupuesto.panel(gestor):   # bucle sobre el panel
                print("  " + resultado["mensaje"])
        else:
            print("  (No has definido presupuestos todavía.)")

        opcion = util.elegir_opcion(
            "\n  ¿Qué deseas hacer?",
            ["Definir / cambiar un límite", "Volver al menú principal"],
        )
        if opcion == "Volver al menú principal":     # condicional de salida
            break
        categoria = util.elegir_opcion("  ¿Para qué categoría?", CATEGORIAS_GASTO)
        monto = util.leer_monto(f"  Límite mensual para '{categoria}': $")
        presupuesto.definir_limite(categoria, monto)
        print(f"  ✓ Límite de '{categoria}' fijado en {util.formato_moneda(monto)}.")


def guardar(gestor, presupuesto):
    almacenamiento.guardar(ARCHIVO_DATOS, gestor.movimientos, presupuesto.limites)
    print(f"  ✓ Datos guardados en {os.path.relpath(ARCHIVO_DATOS, BASE)}.")


# ----------------------------------------------------------------- bucle de menú
def menu():
    gestor, presupuesto = cargar_estado()
    print("\n*** GESTOR DE FINANZAS PERSONALES — UIDE ***")

    while True:                                      # BUCLE PRINCIPAL del programa
        print(f"\nSaldo actual: {util.formato_moneda(gestor.saldo())}")
        opcion = util.elegir_opcion(
            "MENÚ PRINCIPAL",
            [
                "Registrar ingreso",
                "Registrar gasto",
                "Ver resumen",
                "Presupuesto y alertas",
                "Guardar",
                "Salir",
            ],
        )

        # Despacho de la opción con condicionales encadenados.
        if opcion == "Registrar ingreso":
            registrar(gestor, presupuesto, "ingreso")
        elif opcion == "Registrar gasto":
            registrar(gestor, presupuesto, "gasto")
        elif opcion == "Ver resumen":
            ver_resumen(gestor)
        elif opcion == "Presupuesto y alertas":
            gestionar_presupuesto(gestor, presupuesto)
        elif opcion == "Guardar":
            guardar(gestor, presupuesto)
        elif opcion == "Salir":
            if gestor.cantidad_movimientos() > 0:
                if util.leer_texto("  ¿Guardar antes de salir? (s/n) [s]: ",
                                   defecto="s").lower().startswith("s"):
                    guardar(gestor, presupuesto)
            print("  ¡Hasta luego!")
            break                                    # rompe el bucle → termina


# ----------------------------------------------------------------- modo demo
def demo():
    """Demostración automática (sin teclado): carga el ejemplo y muestra el flujo."""
    movimientos, limites = almacenamiento.cargar(ARCHIVO_EJEMPLO)
    gestor = GestorFinanzas(movimientos)
    presupuesto = Presupuesto(limites)

    print("*** DEMO — GESTOR DE FINANZAS PERSONALES (UIDE) ***")
    print("\nSe cargan movimientos de ejemplo y se registra un gasto nuevo...")
    nuevo = 60.0
    presupuesto_aviso = presupuesto.alerta_por_gasto("Ocio", nuevo)
    gestor.agregar_gasto(nuevo, "Ocio", "Cine y cena", hoy())
    print(f"  + Gasto de {util.formato_moneda(nuevo)} en 'Ocio'.")
    if presupuesto_aviso:
        print("  " + presupuesto_aviso)

    ver_resumen(gestor)

    print("\n— Panel de alertas de presupuesto —")
    for resultado in presupuesto.panel(gestor):
        print("  " + resultado["mensaje"])
    print("\n(Fin de la demo.)")


if __name__ == "__main__":
    # Condicional: elige el modo según el argumento recibido.
    if "--demo" in sys.argv:
        demo()
    else:
        try:
            menu()
        except (KeyboardInterrupt, EOFError):
            print("\n  (Programa interrumpido.)")
