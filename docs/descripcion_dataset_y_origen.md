# Entrega 2: Descripción del dataset y origen

**Proyecto:** ¿Qué tan pronto se puede saber quién llega a los playoffs de la NFL?
**Materia:** Aprendizaje Automático, Centro Politécnico Superior Malvinas Argentinas
**Alumno:** Tomás Roa Gunn

Este documento resume lo que está en el notebook `notebooks/1.0-trg-carga-y-exploracion-de-datos.ipynb`, donde se pueden ver el código y los resultados completos.

## 1. Origen de los datos

| | |
|---|---|
| **Dataset** | `games.csv` del repositorio **nflverse/nfldata** (resultados de todos los partidos de la NFL) |
| **Dónde está** | https://github.com/nflverse/nfldata (carpeta `data`) |
| **Cómo lo obtuve** | Descarga directa del archivo `games.csv` desde el repositorio |
| **Fecha de adquisición** | 2 de noviembre de 2026 |
| **Verificación** | SHA-256 del archivo crudo: `ab502863ef21813a6ceb2f650b9ad1bed95667a27c6d6a996d8c3ea4b9016a06` |
| **Tipo de fuente** | Proyecto abierto con datos públicos de la NFL. No es un dataset de un organismo oficial argentino |
| **Documentación** | `DATASETS.md` del mismo repositorio, que además referencia el origen histórico del archivo (`leesharpe/nfldata` y habitatring.com) |
| **Licencia** | No la verifiqué en esta entrega; la voy a revisar en el repositorio antes de la Entrega 3 |

El archivo crudo está **sin modificar** en `data/raw/games.csv`. Todo lo demás se genera a partir de él con el código del proyecto (`python -m nfl_playoffs.dataset`).

**Por qué este dataset:** es público, está documentado, tiene la información para armar la variable objetivo (quién jugó playoffs) y permite calcular las variables en cualquier punto de la temporada, que es lo que necesita la pregunta del proyecto.

## 2. Descripción del dataset crudo

- **Filas:** 7.548 (un partido por fila) · **Columnas:** 46
- **Temporadas:** 1999 a 2026
- **Tipos de partido:** temporada regular `REG` 7.239 · playoffs: `WC` 120, `DIV` 108, `CON` 54, `SB` 27
- **Tipos de dato:** 21 de texto, 18 numéricas decimales, 7 enteras
- El **diccionario completo de las 46 columnas** (tipo, faltantes y descripción) está en `references/diccionario_games_csv.md`.

**Columnas que uso:** `season`, `game_type`, `week`, `gameday`, `away_team`, `home_team`, `away_score`, `home_score`.

**Columnas que no uso:** identificadores de otras fuentes, cuotas de apuestas, clima, estadio, árbitro, entrenadores y mariscales de campo. Varias tienen muchos faltantes (por ejemplo, `ftn` 74,2 % y `pff` 38,1 %), y además `result`, `total` y las cuotas son datos del partido mismo o externos, que no aportan a las variables de rendimiento que quiero construir.

### Hallazgos al revisar los datos
1. **El archivo incluye la temporada 2026, que está en curso.** Trae el calendario completo (272 partidos) pero solo 120 tienen puntaje. Como todavía no se sabe quién llega a playoffs, **se excluye**.
2. **En 2022 hay 271 partidos de temporada regular en lugar de 272:** el Bills–Bengals de la semana 17 se canceló. Buffalo y Cincinnati jugaron 16.
3. **Las temporadas tienen 16 partidos hasta 2020 y 17 desde 2021.**
4. **Tres equipos cambiaron de ciudad** (OAK a LV, SD a LAC, STL a LA). Se unificaron bajo el nombre actual para tener 32 equipos.
5. **El formato de playoffs cambió en 2020:** de 12 a 14 equipos.

## 3. Preprocesamiento realizado

1. **Alcance:** temporadas **2002 a 2025** (desde que la liga tiene 32 equipos) y solo partidos **ya jugados**. Quedan 6.499 partidos (6.223 de temporada regular y 276 de playoffs).
2. **Unificación de nombres** de los equipos que se mudaron.
3. **Variable objetivo `llega_playoffs`:** vale 1 si el equipo jugó al menos un partido `WC`, `DIV`, `CON` o `SB` esa temporada. En total son 300 equipo-temporadas con valor 1.
4. **Tabla por equipo y partido** (12.446 filas, `data/interim/partidos_por_equipo.csv`): cada partido se divide en dos filas, una por equipo, con `n_partido` = número de partido de **ese equipo** en la temporada, ordenado por fecha. Así "los primeros 9 partidos" son los 9 que jugó, no la semana 9, ya que hay semana de descanso.
5. **Variables por corte** (4, 6, 9 y 12 partidos) calculadas **solo con los primeros N partidos** del equipo.

## 4. Dataset final

Un archivo por corte en `data/processed/` (`variables_corte_04.csv`, `_06`, `_09`, `_12`) y uno que los reúne (`variables_todos_los_cortes.csv`).

| | |
|---|---|
| **Filas por corte** | 768 (32 equipos × 24 temporadas) |
| **Filas del archivo combinado** | 3.072 (768 × 4 cortes) |
| **Valores faltantes** | 0 |
| **Equipos en playoffs** | 300 de 768 (**39,1 %**). 37,5 % hasta 2019 (12 de 32) y 43,8 % desde 2020 (14 de 32) |

| Variable | Tipo | Descripción |
|---|---|---|
| `season`, `team` | entero, texto | Temporada y equipo (identifican la fila; **no** son variables del modelo) |
| `corte` | entero | Cantidad de partidos usados: 4, 6, 9 o 12 |
| `partidos`, `victorias`, `empates`, `derrotas` | entero | Récord del equipo hasta el corte |
| `pct_victorias` | decimal | Victorias sobre partidos (el empate cuenta 0,5) |
| `puntos_favor_prom`, `puntos_contra_prom`, `dif_puntos_prom` | decimal | Promedios por partido y diferencia |
| `pct_victorias_ult4` | decimal | Rendimiento en los últimos 4 partidos del corte |
| `partidos_local` | entero | Cuántos de esos partidos jugó de local |
| `llega_playoffs` | entero (0/1) | **Variable objetivo** |

### Control de calidad y de filtración de información
- Cada fila usa **exactamente N partidos** (verificado en los 4 cortes).
- **200 casos al azar** se recalcularon a mano desde el dato crudo y coinciden.
- Cada temporada tiene 32 equipos y 12 o 14 en playoffs, según corresponde.
- **No se usan** `season` ni datos del partido mismo (`result`, `total`, cuotas) como variables.
- En el corte de 4 partidos, `pct_victorias_ult4` es igual a `pct_victorias` y se descarta en ese corte. `victorias` y `pct_victorias` son equivalentes dentro de cada corte.

## 5. Exploración (descriptiva)
- Los equipos que llegan a playoffs tienen, con 9 partidos, un `pct_victorias` promedio de 0,68 contra 0,39 de los que no llegan, y una diferencia de puntos de +5,3 contra -3,4 por partido.
- La diferencia entre promedios casi no cambia según el corte (0,29 a 0,30), pero la dispersión dentro de cada grupo baja y los grupos se solapan menos: la separación estandarizada pasa de 1,26 (4 partidos) a 2,14 (12 partidos).
- Esto es una hipótesis para la Entrega 3: se calculó con todas las temporadas y **no se usa para elegir modelos ni cortes**.

## 6. Validación prevista (respuesta a los comentarios de la Entrega 1)
- **Prueba no independiente:** las temporadas 2019 a 2025 ya se usaron como prueba en la Semana 6. Por eso uso validación **walk-forward**: para cada temporada `y` entre 2010 y 2025 se entrena con 2002 hasta `y-1` y se valida en `y`. Hay 9 tramos anteriores a 2019 que nunca se usaron como prueba, y los de 2019 a 2025 se reportan **aparte y declarados como ya vistos**.
- **Cuatro cortes:** un modelo por corte, con el mismo esquema, para comparar de forma justa.
- **Orden temporal:** los hiperparámetros se eligen con validación cruzada temporal dentro del entrenamiento, y el escalado se ajusta solo con el entrenamiento, dentro de un `Pipeline`.
- **Referencias para comparar:** (1) el modelo que siempre predice "no llega", y (2) una regla simple por `pct_victorias` con umbral elegido solo con el entrenamiento.
- **"Predicción confiable" (propuesta):** se prioriza el F1 de la clase "llega a playoffs". Un corte será suficiente si en promedio supera a la regla por % de victorias. El umbral numérico se fijará en la Entrega 3 con los datos de entrenamiento, antes de mirar 2019 a 2025.

## 7. Antecedentes
Hice una búsqueda inicial (2 de noviembre de 2026) de trabajos relacionados. **No es una revisión exhaustiva** y la voy a ampliar antes de la Entrega 3.

| Trabajo | Qué hace | En qué se diferencia de este proyecto |
|---|---|---|
| [A Machine Learning Analysis of the NFL: Predicting New Playoff Contenders](https://harvardsportsanalysis.org/2018/09/a-machine-learning-analysis-of-the-nfl-predicting-new-playoff-contenders/) (Harvard Sports Analysis Collective, 2018) | Usa 1.280 partidos de 2012 a 2016, PCA y K-Means (modelo **no supervisado**) para detectar equipos con mal récord que podrían ser contendientes la temporada siguiente | Es no supervisado y mira la **temporada siguiente**. Acá se hace **clasificación supervisada dentro de la misma temporada**, por cortes |
| [Multiple Machine Learning Algorithms-based NBA Team Playoffs Prediction](https://www.itm-conferences.org/10.1051/itmconf/20257004024) (Yeung, 2025) | Predice si un equipo de la **NBA** clasifica a playoffs usando estadísticas de 1947 a 2024 y cuatro modelos; el mejor fue Random Forest (AUC 0,841) | Es otro deporte y usa estadísticas de **temporada completa**. No estudia cuánto antes se puede anticipar |
| [Advancing NFL win prediction: from Pythagorean formulas to machine learning algorithms](https://doi.org/10.3389/fspor.2025.1638446) (Weirich et al., 2025) | **Regresión** del porcentaje de victorias de equipos de la NFL con datos de 2003 a 2023; la red neuronal fue la mejor | Predice el porcentaje de victorias (regresión), no la clasificación a playoffs, y con la temporada completa |

**Aporte de este proyecto:** responder **a partir de cuántos partidos** se puede anticipar la clasificación con un rendimiento útil, con validación que respeta el orden temporal y comparando contra una regla simple.

## 8. Limitaciones
- Las variables salen solo de resultados de partidos: no incluyen lesiones, calidad del mariscal de campo ni dificultad del calendario restante.
- Son 24 temporadas: un dataset chico. Los cuatro cortes de una misma temporada están correlacionados entre sí.
- El cambio de formato de playoffs en 2020 altera la proporción de equipos clasificados.
- El dataset es público pero **no argentino**; la consigna lo recomienda sin exigirlo.

## 9. Cómo reproducirlo
```bash
pip install -r requirements.txt
python -m nfl_playoffs.dataset        # regenera data/interim y data/processed
jupyter notebook notebooks/            # abrir 1.0-trg-carga-y-exploracion-de-datos.ipynb
```
