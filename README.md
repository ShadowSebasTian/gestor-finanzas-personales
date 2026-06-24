# Gestor de Finanzas Personales

Programa de consola en **Python** para registrar ingresos y gastos, ver un resumen de las
finanzas y recibir **alertas de presupuesto** por categoría. Desarrollado para la actividad
**Aprendizaje Autónomo 2** de *Lógica de Programación 1* (UIDE).

> Su objetivo didáctico es aplicar de forma clara las **estructuras de control** del curso:
> **condicionales** (`if / elif / else`) y **bucles** (`while`, `for`).

## ¿Qué hace?

- **Registrar ingreso / gasto** con monto, categoría, descripción y fecha.
- **Ver resumen**: saldo, total de ingresos y gastos, desglose por categoría y promedio por gasto.
- **Presupuesto y alertas**: define un límite por categoría y el programa avisa con semáforo
  (🟢 ok, 🟡 aviso, 🟠 atención, 🔴 sobregiro) según el porcentaje usado.
- **Persistencia** en un archivo JSON (los datos no se pierden al cerrar).

## Cómo ejecutarlo

Requiere solo Python 3 (sin librerías externas: usa la librería estándar).

```bash
# Modo interactivo (menú)
python src/main.py

# Demostración automática (sin teclado), útil para el video
python src/main.py --demo
```

## Cómo correr las pruebas

```bash
python -m unittest discover -s tests -v
```

## Estructura del proyecto

```
proyecto/
├─ src/
│  ├─ main.py            # Bucle de menú (while) y despacho de opciones (if/elif)
│  ├─ finanzas.py        # Lógica pura: registrar, saldo, totales, promedios
│  ├─ presupuesto.py     # Reglas de umbrales y alertas (condicionales escalonados)
│  ├─ almacenamiento.py  # Guardar/cargar en JSON
│  └─ util.py            # Validación de entradas (bucles de reintento) y formato
├─ tests/                # Pruebas automáticas (unittest)
├─ datos/ejemplo.json    # Datos de muestra para la demo
└─ diagramas/            # Diagramas de flujo (fuente .mmd y .png)
```

## Relación con los diagramas de flujo

Cada funcionalidad principal tiene su **diagrama de flujo** en `diagramas/`:

| Diagrama | Funcionalidad | Estructura de control que ilustra |
|---|---|---|
| `01-menu-principal` | Bucle del menú | `while` + `if/elif` |
| `02-registrar-movimiento` | Registrar ingreso/gasto | validación con `while` |
| `03-ver-resumen` | Resumen por categoría | `for` que acumula |
| `04-alertas-presupuesto` | Semáforo de presupuesto | `if/elif/else` escalonado |

## Autor

Sebastian Cumba — Ingeniería en Inteligencia Artificial, UIDE.
