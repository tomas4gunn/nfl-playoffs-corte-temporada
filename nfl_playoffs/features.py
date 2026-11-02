"""Carga de datos y construcción de variables por corte de temporada.

Regla central contra la filtración de información (data leakage): las variables de un
corte N se calculan SOLO con los primeros N partidos de temporada regular que jugó
ese equipo en esa temporada. Nada de lo que pasa después entra en las variables.
"""
import pandas as pd

from .config import CORTES, MUDANZAS, RAW, TEMPORADA_MAX, TEMPORADA_MIN


def cargar_partidos(ruta=None):
    """Lee games.csv, filtra temporadas y partidos ya jugados, y unifica nombres de equipos."""
    ruta = ruta or RAW / "games.csv"
    g = pd.read_csv(ruta)
    g = g[(g.season >= TEMPORADA_MIN) & (g.season <= TEMPORADA_MAX)].copy()
    g = g[g.home_score.notna() & g.away_score.notna()]  # solo partidos jugados
    g["home_team"] = g["home_team"].replace(MUDANZAS)
    g["away_team"] = g["away_team"].replace(MUDANZAS)
    g["gameday"] = pd.to_datetime(g["gameday"])
    return g.reset_index(drop=True)


def partidos_por_equipo(g):
    """De una fila por partido a una fila por (equipo, partido) de temporada regular."""
    r = g[g.game_type == "REG"]
    local = pd.DataFrame({
        "season": r.season, "week": r.week, "gameday": r.gameday, "team": r.home_team,
        "rival": r.away_team, "es_local": 1, "puntos_favor": r.home_score,
        "puntos_contra": r.away_score, "div_game": r.div_game})
    visita = pd.DataFrame({
        "season": r.season, "week": r.week, "gameday": r.gameday, "team": r.away_team,
        "rival": r.home_team, "es_local": 0, "puntos_favor": r.away_score,
        "puntos_contra": r.home_score, "div_game": r.div_game})
    tg = pd.concat([local, visita], ignore_index=True)
    # victoria = 1, empate = 0.5, derrota = 0
    tg["resultado"] = 0.5
    tg.loc[tg.puntos_favor > tg.puntos_contra, "resultado"] = 1.0
    tg.loc[tg.puntos_favor < tg.puntos_contra, "resultado"] = 0.0
    tg = tg.sort_values(["season", "team", "gameday", "week"]).reset_index(drop=True)
    tg["n_partido"] = tg.groupby(["season", "team"]).cumcount() + 1
    return tg


def equipos_a_playoffs(g):
    """Conjunto de (temporada, equipo) que jugó al menos un partido de playoffs."""
    p = g[g.game_type != "REG"]
    filas = set(zip(p.season, p.home_team)) | set(zip(p.season, p.away_team))
    return filas


def variables_corte(tg, n):
    """Variables de cada equipo-temporada usando solo sus primeros n partidos."""
    d = tg[tg.n_partido <= n]
    ult = d[d.n_partido > n - min(4, n)]  # últimos 4 partidos DENTRO del corte
    base = d.groupby(["season", "team"]).agg(
        partidos=("n_partido", "max"),
        victorias=("resultado", lambda s: int((s == 1.0).sum())),
        empates=("resultado", lambda s: int((s == 0.5).sum())),
        pct_victorias=("resultado", "mean"),
        puntos_favor_prom=("puntos_favor", "mean"),
        puntos_contra_prom=("puntos_contra", "mean"),
        partidos_local=("es_local", "sum"),
    )
    base["dif_puntos_prom"] = base.puntos_favor_prom - base.puntos_contra_prom
    base["pct_victorias_ult4"] = ult.groupby(["season", "team"]).resultado.mean()
    base["derrotas"] = base.partidos - base.victorias - base.empates
    return base.reset_index()


def tabla_corte(tg, objetivo, n):
    f = variables_corte(tg, n)
    f["corte"] = n
    f["llega_playoffs"] = [int((s, t) in objetivo) for s, t in zip(f.season, f.team)]
    cols = ["season", "team", "corte", "partidos", "victorias", "empates", "derrotas",
            "pct_victorias", "puntos_favor_prom", "puntos_contra_prom", "dif_puntos_prom",
            "pct_victorias_ult4", "partidos_local", "llega_playoffs"]
    return f[cols]


def construir_todo():
    g = cargar_partidos()
    tg = partidos_por_equipo(g)
    objetivo = equipos_a_playoffs(g)
    tablas = {n: tabla_corte(tg, objetivo, n) for n in CORTES}
    return g, tg, objetivo, tablas
