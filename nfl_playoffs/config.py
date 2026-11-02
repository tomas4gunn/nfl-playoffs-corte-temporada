"""Parámetros del proyecto."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
INTERIM = RAIZ / "data" / "interim"
PROCESSED = RAIZ / "data" / "processed"
FIGURAS = RAIZ / "reports" / "figures"

# Temporadas con 32 equipos (desde 2002) y ya terminadas (la 2026 está en curso)
TEMPORADA_MIN = 2002
TEMPORADA_MAX = 2025

# Cortes de la temporada: cantidad de partidos YA jugados por el equipo
CORTES = (4, 6, 9, 12)

# Equipos que cambiaron de ciudad: se unifican bajo el nombre actual
MUDANZAS = {"OAK": "LV", "SD": "LAC", "STL": "LA"}
