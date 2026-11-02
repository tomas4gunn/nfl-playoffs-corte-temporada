# Entrega 2, Descripción del dataset y origen

**Proyecto** ¿Qué tan pronto se puede saber quién llega a los playoffs de la NFL?
**Materia** Aprendizaje Automático, Centro Politécnico Superior Malvinas Argentinas
**Alumno** Tomás Roa Gunn

Acá cuento qué datos elegí, de dónde salen y qué hice con ellos antes de modelar. El código y los resultados completos están en el notebook `notebooks/1.0-trg-carga-y-exploracion-de-datos.ipynb`.

## 1. Origen de los datos

| | |
|---|---|
| **Dataset** | `games.csv` del repositorio **nflverse/nfldata**, con los resultados de todos los partidos de la NFL |
| **Dónde está** | https://github.com/nflverse/nfldata (carpeta `data`) |
| **Cómo lo obtuve** | Bajé el archivo `games.csv` directo del repositorio |
| **Fecha de adquisición** | 2 de noviembre de 2026 |
| **Verificación** | SHA-256 del archivo crudo, `ab502863ef21813a6ceb2f650b9ad1bed95667a27c6d6a996d8c3ea4b9016a06` |
| **Tipo de fuente** | Proyecto abierto con datos públicos de la NFL. No es de un organismo oficial argentino |
| **Documentación** | `DATASETS.md` del mismo repositorio, que cita el origen histórico del archivo (`leesharpe/nfldata` y habitatring.com) |
| **Licencia** | Lo revisé el 2 de noviembre de 2026 y el repositorio **no declara ninguna licencia** (GitHub no muestra una y no hay archivo LICENSE). No es un dataset de dominio público declarado. Lo uso solo con fines académicos, sin redistribuirlo como propio, y cito la fuente y al autor original, Lee Sharpe |

El archivo crudo está **sin modificar** en `data/raw/games.csv`. Todo lo demás se genera a partir de ahí con el código del proyecto (`python -m nfl_playoffs.dataset`).

**Por qué lo elegí.** Es público, está documentado, tiene lo que necesito para armar la variable objetivo (quién jugó playoffs) y me deja calcular las variables en cualquier punto de la temporada, que es justo lo que pide la pregunta del proyecto.

## 2. Descripción del dataset crudo

- **Filas** 7.548 (un partido por fila), **columnas** 46
- **Temporadas** de 1999 a 2026
- **Tipos de partido** temporada regular `REG` 7.239, playoffs `WC` 120, `DIV` 108, `CON` 54 y `SB` 27
- **Tipos de dato** 21 de texto, 18 numéricas decimales y 7 enteras
- El **diccionario de las 46 columnas** (tipo, faltantes y descripción) está en `references/diccionario_games_csv.md`

**Columnas que use** `season`, `game_type`, `week`, `gameday`, `away_team`, `home_team`, `away_score` y `home_score`.

**Columnas que no use** identificadores de otras fuentes, cuotas de apuestas, clima, estadio, árbitro, entrenadores y mariscales de campo. Varias tienen muchos faltantes. Además `result`, `total` y las cuotas son datos del partido mismo o externos, y no aportan a las variables de rendimiento que quiero construir.

### Cosas que encontré al revisar los datos
1. **El archivo incluye la temporada 2026, que está en curso.** Trae el calendario completo (272 partidos) pero solo 120 tienen puntaje. Como todavía no se sabe quién llega a playoffs, la dejé afuera.
2. **En 2022 hay 271 partidos de temporada regular en vez de 272**, porque se canceló el Bills–Bengals de la semana 17. Buffalo y Cincinnati jugaron 16.
3. **Las temporadas tienen 16 partidos hasta 2020 y 17 desde 2021.**
4. **Tres equipos se mudaron de ciudad** (OAK a LV, SD a LAC, STL a LA). Los unifiqué bajo el nombre actual para tener siempre 32 equipos.
5. **El formato de playoffs cambió en 2020**, de 12 a 14 equipos.

## 3. Qué le hice a los datos

1. **Alcance.** Me quedé con las temporadas **2002 a 2025** (desde que la liga tiene 32 equipos) y solo con partidos **ya jugados**. Quedan 6.499 partidos, 6.223 de temporada regular y 276 de playoffs.
2. **Nombres.** Unifiqué los equipos que se mudaron.
3. **Variable objetivo `llega_playoffs`.** Vale 1 si el equipo jugó al menos un partido `WC`, `DIV`, `CON` o `SB` esa temporada. En total son 300 equipo-temporadas con valor 1.
4. **Tabla por equipo y partido** (12.446 filas, en `data/interim/partidos_por_equipo.csv`). Cada partido se divide en dos filas, una por equipo, y `n_partido` es el número de partido **de ese equipo** en la temporada, ordenado por fecha. Así "los primeros 9 partidos" son los 9 que jugó el equipo y no la semana 9, porque hay semana de descanso.
5. **Variables por corte** (4, 6, 9 y 12 partidos), calculadas **solo con los primeros N partidos** del equipo, para no filtrar información del futuro.

## 4. Dataset final

Hay un archivo por corte en `data/processed/` (`variables_corte_04.csv`, `_06`, `_09`, `_12`) y uno que los junta a todos (`variables_todos_los_cortes.csv`).

| | |
|---|---|
| **Filas por corte** | 768 (32 equipos por 24 temporadas) |
| **Filas del archivo combinado** | 3.072 (768 por 4 cortes) |
| **Valores faltantes** | 0 |
| **Equipos en playoffs** | 300 de 768 (**39,1 %**), 37,5 % hasta 2019 (12 de 32) y 43,8 % desde 2020 (14 de 32) |

| Variable | Tipo | Descripción |
|---|---|---|
| `season`, `team` | entero, texto | Temporada y equipo. Identifican la fila y **no** son variables del modelo |
| `corte` | entero | Cantidad de partidos usados, 4, 6, 9 o 12 |
| `partidos`, `victorias`, `empates`, `derrotas` | entero | Récord del equipo hasta el corte |
| `pct_victorias` | decimal | Victorias sobre partidos (el empate cuenta 0,5) |
| `puntos_favor_prom`, `puntos_contra_prom`, `dif_puntos_prom` | decimal | Promedios por partido y diferencia |
| `pct_victorias_ult4` | decimal | Rendimiento en los últimos 4 partidos del corte |
| `partidos_local` | entero | Cuántos de esos partidos jugó de local |
| `llega_playoffs` | entero (0/1) | **Variable objetivo** |

### Control de calidad y de filtración de información
- Cada fila usa **exactamente N partidos** (lo verifiqué en los 4 cortes).
- **200 casos al azar** los recalculé desde el dato crudo y coinciden.
- Cada temporada tiene 32 equipos y 12 o 14 en playoffs, según corresponda.
- **No uso** `season` ni datos del partido mismo (`result`, `total`, cuotas) como variables.
- En el corte de 4 partidos, `pct_victorias_ult4` es igual a `pct_victorias`, así que la descarto en ese corte. Además `victorias` y `pct_victorias` son equivalentes dentro de cada corte.

## 5. Exploración (solo descriptiva)
- Con 9 partidos, los equipos que llegan a playoffs tienen un `pct_victorias` promedio de 0,68 contra 0,39 de los que no llegan, y una diferencia de puntos de +5,3 contra -3,4 por partido.
- La diferencia entre promedios casi no cambia según el corte (0,29 a 0,30), pero la dispersión dentro de cada grupo baja y los grupos se solapan menos. La separación estandarizada pasa de 1,26 (4 partidos) a 2,14 (12 partidos).
- Esto lo tomo como hipótesis para la Entrega 3. Se calculó con todas las temporadas, así que **no lo uso para elegir modelos ni cortes**.

## 6. Cómo voy a validar (respuesta a los comentarios de la Entrega 1)
- **Prueba que ya vi.** Las temporadas 2019 a 2025 ya las usé como prueba en la Semana 6. Por eso voy a usar validación **walk-forward**, o sea que para cada temporada `y` entre 2010 y 2025 entreno con 2002 hasta `y-1` y valido en `y`. Hay 9 tramos anteriores a 2019 que nunca usé como prueba, y los de 2019 a 2025 los voy a reportar **aparte y avisando que ya estaban vistos**.
- **Cuatro cortes.** Un modelo por corte, con el mismo esquema, para comparar de forma justa.
- **Orden temporal.** Los hiperparámetros se eligen con validación cruzada temporal dentro del entrenamiento, y el escalado se ajusta solo con el entrenamiento, dentro de un `Pipeline`.
- **Referencias para comparar.** Una es el modelo que siempre predice "no llega" y la otra es una regla simple por `pct_victorias`, con el umbral elegido solo con el entrenamiento.
- **Qué es una "predicción confiable" (propuesta).** Me voy a fijar en el F1 de la clase "llega a playoffs". Un corte va a ser suficiente si en promedio le gana a la regla por % de victorias. El umbral numérico lo fijo en la Entrega 3 con datos de entrenamiento, antes de mirar 2019 a 2025.

## 7. Antecedentes
Hice una búsqueda inicial el 2 de noviembre de 2026. **No es una revisión exhaustiva** y la voy a ampliar antes de la Entrega 3.

| Trabajo | Qué hace | En qué se diferencia de este proyecto |
|---|---|---|
| [A Machine Learning Analysis of the NFL, Predicting New Playoff Contenders](https://harvardsportsanalysis.org/2018/09/a-machine-learning-analysis-of-the-nfl-predicting-new-playoff-contenders/) (Harvard Sports Analysis Collective, 2018) | Usa 1.280 partidos de 2012 a 2016, PCA y K-Means (modelo **no supervisado**) para detectar equipos con mal récord que podrían ser contendientes la temporada siguiente | Es no supervisado y mira la **temporada siguiente**. Acá hago **clasificación supervisada dentro de la misma temporada**, por cortes |
| [Multiple Machine Learning Algorithms-based NBA Team Playoffs Prediction](https://www.itm-conferences.org/10.1051/itmconf/20257004024) (Yeung, 2025) | Predice si un equipo de la **NBA** clasifica a playoffs con estadísticas de 1947 a 2024 y cuatro modelos. El mejor fue Random Forest (AUC 0,841) | Es otro deporte y usa estadísticas de **temporada completa**. No estudia cuánto antes se puede anticipar |
| [Advancing NFL win prediction, from Pythagorean formulas to machine learning algorithms](https://doi.org/10.3389/fspor.2025.1638446) (Weirich et al., 2025) | Hace **regresión** del porcentaje de victorias de equipos de la NFL con datos de 2003 a 2023, y la red neuronal fue la mejor | Predice el porcentaje de victorias (regresión) y no la clasificación a playoffs, y con la temporada completa |

**Mi aporte** es responder **a partir de cuántos partidos** se puede anticipar la clasificación con un rendimiento útil, con una validación que respeta el orden temporal y comparando contra una regla simple.

## 8. Limitaciones
- Las variables salen solo de resultados de partidos. No tienen lesiones, calidad del mariscal de campo ni dificultad del calendario que falta.
- Son 24 temporadas, un dataset chico, y los cuatro cortes de una misma temporada están correlacionados entre sí.
- El cambio de formato de playoffs en 2020 altera la proporción de equipos clasificados.
- El dataset es público pero **no argentino**. La consigna lo recomienda sin exigirlo.
- No tiene licencia declarada, por eso lo uso solo con fines académicos y cito la fuente.

## 9. Cómo reproducirlo
```bash
pip install -r requirements.txt
python -m nfl_playoffs.dataset        # regenera data/interim y data/processed
jupyter notebook notebooks/            # abrir 1.0-trg-carga-y-exploracion-de-datos.ipynb
```
