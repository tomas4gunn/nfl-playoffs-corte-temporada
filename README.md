# ¿Qué tan pronto se puede saber quién llega a los playoffs de la NFL?

Proyecto del parcial de **Aprendizaje Automático** (Centro Politécnico Superior Malvinas Argentinas).
**Alumno:** Tomás Roa Gunn

**Pregunta:** a partir de cuántos partidos jugados (4, 6, 9 o 12) se puede anticipar, con un rendimiento útil, qué equipos de la NFL van a llegar a playoffs.
**Tipo de problema:** clasificación binaria supervisada (`llega_playoffs` = 1 o 0).
**Modelos previstos:** regresión logística, árbol de decisión, KNN y SVM (scikit-learn), por corte de temporada.

## Estado de las entregas
| Entrega | Contenido | Dónde |
|---|---|---|
| 1 | Descripción y formulación del objetivo | PDF entregado en el campus |
| **2** | **Descripción del dataset y origen** | [`docs/descripcion_dataset_y_origen.md`](docs/descripcion_dataset_y_origen.md) y [`notebooks/`](notebooks/) |
| 3 | Modelos y resultados | Pendiente |

## Estructura (plantilla Cookiecutter Data Science)
```
├── data
│   ├── raw/          games.csv original, sin modificar
│   ├── interim/      un registro por equipo y partido
│   ├── processed/    variables por corte (4, 6, 9, 12) con la variable objetivo
│   └── external/
├── docs/             descripción del dataset y origen
├── models/
├── notebooks/        1.0-trg-carga-y-exploracion-de-datos.ipynb
├── nfl_playoffs/     código (config, features, dataset)
├── references/       diccionario de datos
├── reports/figures/  gráficos
└── requirements.txt
```

## Datos
Resultados de partidos de la NFL del proyecto abierto [nflverse/nfldata](https://github.com/nflverse/nfldata), descargados el 2 de noviembre de 2026. Detalle completo en `docs/descripcion_dataset_y_origen.md`.

## Cómo reproducirlo
```bash
pip install -r requirements.txt
python -m nfl_playoffs.dataset
jupyter notebook notebooks/
```
