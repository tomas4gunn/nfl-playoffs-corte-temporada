"""Genera los archivos intermedios y procesados a partir de data/raw/games.csv.

Uso desde la raíz del proyecto:  python -m nfl_playoffs.dataset
"""
import pandas as pd

from .config import INTERIM, PROCESSED
from .features import construir_todo


def main():
    INTERIM.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    g, tg, objetivo, tablas = construir_todo()
    tg.to_csv(INTERIM / "partidos_por_equipo.csv", index=False)
    for n, t in tablas.items():
        t.to_csv(PROCESSED / f"variables_corte_{n:02d}.csv", index=False)
    pd.concat(tablas.values(), ignore_index=True).to_csv(PROCESSED / "variables_todos_los_cortes.csv", index=False)
    print("Listo:", {n: t.shape for n, t in tablas.items()})


if __name__ == "__main__":
    main()
