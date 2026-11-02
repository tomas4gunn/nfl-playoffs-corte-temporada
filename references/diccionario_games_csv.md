# Diccionario de datos: `data/raw/games.csv`

Fuente de las descripciones: documentación del repositorio nflverse/nfldata (archivo `DATASETS.md`). Las marcadas con **\*** no figuran en esa documentación y se **deducen del nombre de la columna**.

Faltantes calculados sobre las **7.548 filas** del archivo crudo (incluye la temporada 2026 en curso).

| Columna | Tipo | Faltantes | ¿Se usa? | Descripción |
|---|---|---|---|---|
| `game_id` | str | 0 (0.0 %) | No | Identificador legible del partido: temporada, semana, visitante y local (ej. 1999_01_MIN_ATL). |
| `season` | int64 | 0 (0.0 %) | Sí | Año de la temporada. Los partidos de enero y los playoffs cuentan en la temporada del año anterior. |
| `game_type` | str | 0 (0.0 %) | Sí | Tipo de partido: REG (temporada regular), WC, DIV, CON (playoffs) o SB (Super Bowl). |
| `week` | int64 | 0 (0.0 %) | Sí | Semana de la temporada (1 a 17/18 en regular; 18 a 21 en playoffs, según la documentación). |
| `gameday` | str | 0 (0.0 %) | Sí | Fecha del partido. |
| `weekday` | str | 0 (0.0 %) | No | Día de la semana. |
| `gametime` | str | 259 (3.4 %) | No | Hora de inicio (hora del Este, 24 h). |
| `away_team` | str | 0 (0.0 %) | Sí | Equipo visitante. |
| `away_score` | float64 | 152 (2.0 %) | Sí | Puntos del visitante (faltante si el partido no se jugó). |
| `home_team` | str | 0 (0.0 %) | Sí | Equipo local designado. |
| `home_score` | float64 | 152 (2.0 %) | Sí | Puntos del local (faltante si el partido no se jugó). |
| `location` | str | 0 (0.0 %) | No | Home si el local juega en su estadio; Neutral si se juega en cancha neutral. |
| `result` | float64 | 152 (2.0 %) | No | Puntos del local menos puntos del visitante. |
| `total` | float64 | 152 (2.0 %) | No | Suma de los puntos de ambos equipos. |
| `overtime` | float64 | 152 (2.0 %) | No | 1 si el partido llegó a tiempo extra. \* |
| `old_game_id` | int64 | 0 (0.0 %) | No | Identificador antiguo del partido. \* |
| `gsis` | float64 | 151 (2.0 %) | No | Identificador del partido en el sistema GSIS de la NFL. |
| `nfl_detail_id` | str | 7276 (96.4 %) | No | Identificador del partido en otra fuente de la NFL. \* |
| `pfr` | str | 0 (0.0 %) | No | Identificador en Pro Football Reference. |
| `pff` | float64 | 2879 (38.1 %) | No | Identificador en Pro Football Focus. |
| `espn` | int64 | 0 (0.0 %) | No | Identificador en ESPN. |
| `ftn` | float64 | 5602 (74.2 %) | No | Identificador del partido en FTN. \* |
| `away_rest` | int64 | 0 (0.0 %) | No | Días de descanso del visitante. \* |
| `home_rest` | int64 | 0 (0.0 %) | No | Días de descanso del local. \* |
| `away_moneyline` | float64 | 2117 (28.0 %) | No | Cuota moneyline del visitante. \* |
| `home_moneyline` | float64 | 2117 (28.0 %) | No | Cuota moneyline del local. \* |
| `spread_line` | float64 | 136 (1.8 %) | No | Línea de ventaja (spread): positiva si el local era favorito. Coincide en signo con result. |
| `away_spread_odds` | float64 | 2117 (28.0 %) | No | Cuota del spread, visitante. \* |
| `home_spread_odds` | float64 | 2117 (28.0 %) | No | Cuota del spread, local. \* |
| `total_line` | float64 | 136 (1.8 %) | No | Línea de apuestas de puntos totales. |
| `under_odds` | float64 | 2120 (28.1 %) | No | Cuota de "menos de" en puntos totales. \* |
| `over_odds` | float64 | 2120 (28.1 %) | No | Cuota de "más de" en puntos totales. \* |
| `div_game` | int64 | 0 (0.0 %) | No | 1 si es un partido entre equipos de la misma división. \* |
| `roof` | str | 25 (0.3 %) | No | Techo del estadio: outdoors, open, closed o dome. |
| `surface` | str | 99 (1.3 %) | No | Tipo de superficie de juego. |
| `temp` | float64 | 2297 (30.4 %) | No | Temperatura en el estadio (solo outdoors y open). |
| `wind` | float64 | 2297 (30.4 %) | No | Viento en mph (solo outdoors y open). |
| `away_qb_id` | str | 136 (1.8 %) | No | Identificador del mariscal de campo visitante. \* |
| `home_qb_id` | str | 136 (1.8 %) | No | Identificador del mariscal de campo local. \* |
| `away_qb_name` | str | 136 (1.8 %) | No | Mariscal de campo visitante. \* |
| `home_qb_name` | str | 136 (1.8 %) | No | Mariscal de campo local. \* |
| `away_coach` | str | 0 (0.0 %) | No | Entrenador del visitante. |
| `home_coach` | str | 0 (0.0 %) | No | Entrenador del local. |
| `referee` | str | 208 (2.8 %) | No | Árbitro principal. |
| `stadium_id` | str | 0 (0.0 %) | No | Identificador del estadio. \* |
| `stadium` | str | 0 (0.0 %) | No | Nombre del estadio. |
