# -*- coding: utf-8 -*-
"""
generar_diagramas.py — Renderiza los diagramas de flujo a PNG con matplotlib.

Dibuja con la paleta UIDE las cuatro funcionalidades principales del programa.
Ejecutar:  python docs/diagramas/generar_diagramas.py
Genera:    docs/diagramas/0X-*.png
"""
import os
import matplotlib
matplotlib.use("Agg")  # backend sin ventana (para guardar archivos)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon

AQUI = os.path.dirname(os.path.abspath(__file__))

# Paleta UIDE
GRANATE = "#7a1f3d"
DORADO = "#d6a03a"
ROSA = "#f7eef1"
ORO_CLARO = "#fbf3e0"
TEXTO = "#2b2b2b"

# Tamaños base de cada figura del diagrama
PW, PH = 3.0, 1.0      # proceso / entrada-salida
DHW, DHH = 1.9, 1.0    # semi-ancho / semi-alto del rombo (decisión)
TW, TH = 2.2, 0.9      # terminal (inicio/fin)


def _texto(ax, x, y, t, color=TEXTO, size=9, bold=False):
    ax.text(x, y, t, ha="center", va="center", fontsize=size, color=color,
            weight="bold" if bold else "normal", zorder=5, wrap=True)


def proceso(ax, x, y, t, fill="white", fg=TEXTO, w=PW, h=PH):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fill,
                           edgecolor=GRANATE, linewidth=1.6, zorder=3))
    _texto(ax, x, y, t, color=fg)
    return {"x": x, "y": y, "w": w, "h": h, "kind": "rect"}


def entrada_salida(ax, x, y, t, w=PW, h=PH):
    s = 0.45
    pts = [(x - w / 2 + s, y + h / 2), (x + w / 2 + s, y + h / 2),
           (x + w / 2 - s, y - h / 2), (x - w / 2 - s, y - h / 2)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=ORO_CLARO,
                         edgecolor=DORADO, linewidth=1.6, zorder=3))
    _texto(ax, x, y, t)
    return {"x": x, "y": y, "w": w, "h": h, "kind": "io"}


def decision(ax, x, y, t, hw=DHW, hh=DHH):
    pts = [(x, y + hh), (x + hw, y), (x, y - hh), (x - hw, y)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=ROSA,
                         edgecolor=GRANATE, linewidth=1.6, zorder=3))
    _texto(ax, x, y, t, size=8.5)
    return {"x": x, "y": y, "w": hw * 2, "h": hh * 2, "kind": "diamond"}


def terminal(ax, x, y, t, w=TW, h=TH):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.45",
                                facecolor=GRANATE, edgecolor=GRANATE, zorder=3))
    _texto(ax, x, y, t, color="white", bold=True)
    return {"x": x, "y": y, "w": w, "h": h, "kind": "term"}


def anchor(n, lado):
    """Devuelve el punto (x,y) del borde del nodo en el lado pedido."""
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    if n["kind"] == "diamond":
        return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
                "left": (x - w / 2, y), "right": (x + w / 2, y)}[lado]
    return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
            "left": (x - w / 2, y), "right": (x + w / 2, y)}[lado]


def flecha(ax, p1, p2, label=None, lpos=0.5, ldx=0.0, ldy=0.0):
    """Flecha recta de p1 a p2, con etiqueta opcional (Sí/No)."""
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=2)
    if label:
        lx = p1[0] + (p2[0] - p1[0]) * lpos + ldx
        ly = p1[1] + (p2[1] - p1[1]) * lpos + ldy
        ax.text(lx, ly, label, fontsize=8, color=GRANATE, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"), zorder=4)


def ruta(ax, pts, label=None, lidx=0):
    """Polilínea (codos) por varios puntos; flecha solo en el último tramo."""
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                color="#444", lw=1.6, zorder=2)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=2)
    if label:
        p1, p2 = pts[lidx], pts[lidx + 1]
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.25, label, fontsize=8,
                color=GRANATE, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"), zorder=4)


def linea(ax, p1, p2):
    """Tramo sin flecha (para unir a un bus de salida)."""
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#444", lw=1.6, zorder=2)


def lienzo(xlim, ylim, titulo):
    fig, ax = plt.subplots(figsize=((xlim[1] - xlim[0]) * 0.9,
                                    (ylim[1] - ylim[0]) * 0.55))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(titulo, fontsize=12, color=GRANATE, weight="bold", pad=10)
    return fig, ax


def guardar(fig, nombre):
    ruta_png = os.path.join(AQUI, nombre)
    fig.savefig(ruta_png, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("✓", nombre)


# ============================================================ Diagrama 1
def d1_menu():
    fig, ax = lienzo((-1, 7), (-1.4, 13), "1. Bucle del menú principal")
    A = terminal(ax, 0, 12, "Inicio")
    B = entrada_salida(ax, 0, 10, "Cargar datos\nguardados")
    C = proceso(ax, 0, 8, "Mostrar saldo\ny menú")
    D = entrada_salida(ax, 0, 6, "Leer opción")
    E = decision(ax, 0, 3.8, "¿Opción\n= Salir?")
    F = proceso(ax, 4.2, 3.8, "Ejecutar la\nacción elegida")
    G = entrada_salida(ax, 0, 1.4, "Guardar datos\n(opcional)")
    H = terminal(ax, 0, -0.4, "Fin")
    flecha(ax, anchor(A, "bottom"), anchor(B, "top"))
    flecha(ax, anchor(B, "bottom"), anchor(C, "top"))
    flecha(ax, anchor(C, "bottom"), anchor(D, "top"))
    flecha(ax, anchor(D, "bottom"), anchor(E, "top"))
    flecha(ax, anchor(E, "right"), anchor(F, "left"), label="No")
    flecha(ax, anchor(E, "bottom"), anchor(G, "top"), label="Sí")
    flecha(ax, anchor(G, "bottom"), anchor(H, "top"))
    # Bucle: de F de vuelta a C
    ruta(ax, [anchor(F, "top"), (4.2, 8), anchor(C, "right")])
    guardar(fig, "01-menu-principal.png")


# ============================================================ Diagrama 2
def d2_registrar():
    fig, ax = lienzo((-5, 4), (-4.0, 13), "2. Registrar ingreso o gasto")
    A = terminal(ax, 0, 12, "Inicio")
    B = entrada_salida(ax, 0, 10, "Pedir monto")
    C = decision(ax, 0, 7.7, "¿Monto válido?\n(número y > 0)")
    D = proceso(ax, -3.6, 7.7, "Mostrar error")
    E = entrada_salida(ax, 0, 5.4, "Elegir categoría")
    F = entrada_salida(ax, 0, 3.6, "Pedir descripción\ny fecha")
    G = proceso(ax, 0, 1.8, "Registrar\nmovimiento")
    H = decision(ax, 0, -0.6, "¿Gasto supera\n30% del límite?")
    I = proceso(ax, -3.6, -0.6, "Mostrar alerta")
    Z = terminal(ax, 0, -3.0, "Fin")
    flecha(ax, anchor(A, "bottom"), anchor(B, "top"))
    flecha(ax, anchor(B, "bottom"), anchor(C, "top"))
    flecha(ax, anchor(C, "left"), anchor(D, "right"), label="No")
    ruta(ax, [anchor(D, "top"), (-3.6, 10), anchor(B, "left")])  # error → reintentar
    flecha(ax, anchor(C, "bottom"), anchor(E, "top"), label="Sí")
    flecha(ax, anchor(E, "bottom"), anchor(F, "top"))
    flecha(ax, anchor(F, "bottom"), anchor(G, "top"))
    flecha(ax, anchor(G, "bottom"), anchor(H, "top"))
    flecha(ax, anchor(H, "left"), anchor(I, "right"), label="Sí")
    flecha(ax, anchor(H, "bottom"), anchor(Z, "top"), label="No")
    ruta(ax, [anchor(I, "bottom"), (-3.6, -3.0), anchor(Z, "left")])
    guardar(fig, "02-registrar-movimiento.png")


# ============================================================ Diagrama 3
def d3_resumen():
    fig, ax = lienzo((-6, 5), (-2.0, 13), "3. Ver resumen (bucle por categoría)")
    A = terminal(ax, 0, 12, "Inicio")
    B = proceso(ax, 0, 10, "Calcular ingresos,\ngastos y saldo")
    C = decision(ax, 0, 7.8, "¿Hay gastos?")
    D = proceso(ax, -4.2, 7.8, "Mostrar:\nsin gastos")
    E = decision(ax, 0, 5.3, "¿Quedan\ncategorías?")
    F = proceso(ax, 0, 3.1, "Acumular total\nde la categoría")
    G = proceso(ax, 0, 1.0, "Mostrar desglose\ny promedio")
    Z = terminal(ax, 0, -1.0, "Fin")
    flecha(ax, anchor(A, "bottom"), anchor(B, "top"))
    flecha(ax, anchor(B, "bottom"), anchor(C, "top"))
    flecha(ax, anchor(C, "left"), anchor(D, "right"), label="No")
    flecha(ax, anchor(C, "bottom"), anchor(E, "top"), label="Sí")
    flecha(ax, anchor(E, "bottom"), anchor(F, "top"), label="Sí")
    # Retorno del bucle (ortogonal): F vuelve a E por la izquierda
    ruta(ax, [anchor(F, "left"), (-3.0, 3.1), (-3.0, 5.3), anchor(E, "left")])
    # Salida del bucle: E "No" baja por la derecha hasta G
    ruta(ax, [anchor(E, "right"), (3.6, 5.3), (3.6, 1.0), anchor(G, "right")], label="No")
    flecha(ax, anchor(G, "bottom"), anchor(Z, "top"))
    ruta(ax, [anchor(D, "bottom"), (-4.2, -1.0), anchor(Z, "left")])
    guardar(fig, "03-ver-resumen.png")


# ============================================================ Diagrama 4
def d4_alertas():
    fig, ax = lienzo((-1, 9), (0, 13), "4. Semáforo de alertas (if / elif / else)")
    A = terminal(ax, 0, 12, "Inicio")
    B = proceso(ax, 0, 10, "Calcular %\n= gastado / límite")
    C = decision(ax, 0, 8, "¿% ≥ 100%?")
    D = decision(ax, 0, 6, "¿% ≥ 80%?")
    E = decision(ax, 0, 4, "¿% ≥ 50%?")
    F1 = proceso(ax, 0, 2, "Bajo control", fill="#cfe9cf")
    C1 = proceso(ax, 4.5, 8, "SOBREGIRO", fill="#e9b7b7")
    D1 = proceso(ax, 4.5, 6, "Atención", fill="#f0cda3")
    E1 = proceso(ax, 4.5, 4, "Aviso", fill="#f1e2a3")
    Z = terminal(ax, 4.5, 1.0, "Fin")
    flecha(ax, anchor(A, "bottom"), anchor(B, "top"))
    flecha(ax, anchor(B, "bottom"), anchor(C, "top"))
    flecha(ax, anchor(C, "right"), anchor(C1, "left"), label="Sí")
    flecha(ax, anchor(C, "bottom"), anchor(D, "top"), label="No")
    flecha(ax, anchor(D, "right"), anchor(D1, "left"), label="Sí")
    flecha(ax, anchor(D, "bottom"), anchor(E, "top"), label="No")
    flecha(ax, anchor(E, "right"), anchor(E1, "left"), label="Sí")
    flecha(ax, anchor(E, "bottom"), anchor(F1, "top"), label="No")
    # Bus de salida derecho hacia Fin
    bus = 7.2
    linea(ax, anchor(C1, "right"), (bus, 8))
    linea(ax, anchor(D1, "right"), (bus, 6))
    linea(ax, anchor(E1, "right"), (bus, 4))
    ruta(ax, [(bus, 8), (bus, 1.0), anchor(Z, "right")])
    ruta(ax, [anchor(F1, "bottom"), (0, 1.0), anchor(Z, "left")])
    guardar(fig, "04-alertas-presupuesto.png")


if __name__ == "__main__":
    d1_menu()
    d2_registrar()
    d3_resumen()
    d4_alertas()
    print("Diagramas generados en", AQUI)
