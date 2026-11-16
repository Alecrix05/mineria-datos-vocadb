# Proyecto de Minería de Datos — VocaDB

## Descripción
El objetivo de este proyecto es analizar la influencia y evolución de la cultura musical Vocaloid a lo largo de los años, desde su primera aparición hasta la actualidad, usando datos obtenidos de la API pública de VocaDB.

## Motivación
Elegí este tema por un interés personal en Vocaloid, y también para analizar la popularidad y el crecimiento o decrecimiento de esta cultura musical a través del tiempo. Elegí la API de VocaDB porque cuenta con datos históricos de canciones desde los inicios de Vocaloid hasta la actualidad.

## Fuente de datos

- **API:** https://vocadb.net/api
- **Documentación:** https://vocadb.net/swagger

Se verificó que no existe un análisis público (notebook, artículo o proyecto de minería de datos) que use este dataset o uno equivalente extraído de VocaDB.

## Metodología de extracción
La extracción se realizó cubriendo el rango histórico completo, desde el primer año de Vocaloid hasta la actualidad. Por cada año se tomó una muestra aleatoria mediante varios puntos de arranque independientes dentro del catálogo de ese año, buscando que las canciones quedaran dispersas a lo largo de los distintos meses en vez de concentradas en una sola fecha. Se buscó una cantidad similar de canciones por año (no exactamente igual en todos los casos, según la disponibilidad real de cada año).

## Estructura del dataset

| Columna | Tipo | Descripción |
|---|---|---|
| id | numérico | Identificador único de la canción en VocaDB |
| name | texto | Nombre/título de la canción |
| artistString | texto | Productor(es) y voz sintética (Vocaloid/UTAU) usada en la canción |
| songType | categórico | Tipo de canción (ej. Original, Remix, Cover) |
| publishDate | fecha | Fecha de publicación original de la canción |
| lengthSeconds | numérico | Duración de la canción en segundos |
| favoritedTimes | numérico | Número de veces que la canción fue marcada como favorita en VocaDB |
| ratingScore | numérico | Puntaje de calificación acumulado en VocaDB |
| status | categórico | Estado de la ficha en VocaDB (ej. Finished, Draft, Approved) |

## Estructura del repositorio
```
data/raw/            # dataset crudo (extraído de la API)
data/processed/      # dataset limpio (lo usan las prácticas 3 a 9)
Practica 1/          # extracción y limpieza de datos
Practica 2/          # estadística descriptiva, diagrama de entidades, métricas agrupadas
Practica 3/          # visualización de datos
Practica 4/          # pruebas estadísticas
Practica 5/          # correlación y modelos lineales
Practica 6/          # clasificación con KNN
Practica 7/          # clustering con K-Means
Practica 8/          # pronóstico con series de tiempo
Practica 9/          # análisis de texto
requirements.txt     # librerías necesarias
```
Cada carpeta de práctica tiene su propio `README.md` con la metodología, los resultados y la interpretación.

## Cómo ejecutar

```powershell
pip install -r requirements.txt

# 1. Limpieza (genera data/processed/vocadb_limpio.csv)
python "Practica 1/limpieza_datos.py"

# 2. Cada práctica (en cualquier orden después de la limpieza)
python "Practica 2/estadistica_descriptiva.py"
python "Practica 3/visualizacion.py"
python "Practica 4/pruebas_estadisticas.py"
python "Practica 5/modelos_lineales.py"
python "Practica 6/clasificacion_knn.py"
python "Practica 7/clustering_kmeans.py"
python "Practica 8/pronostico.py"
python "Practica 9/analisis_texto.py"
```

La extracción (`Practica 1/extraer_csv_vocadb.py`) guarda directo en `data/raw/`. **Ojo:** al volver a ejecutarla se descarga una muestra nueva y se reemplaza el CSV actual, por lo que todos los resultados cambiarían. Solo es necesaria para reproducir la metodología.

## Historial de cambios

**Ajuste posterior a la extracción de datos:** el script de extracción original incluía el parámetro `songTypes: "Original"` en las llamadas a la API, por lo que el primer dataset entregado contenía únicamente canciones de tipo Original, sin variabilidad en esa columna. Al iniciar la Práctica 2 se identificó esta limitante (útil para análisis futuros como comparaciones por tipo o pruebas ANOVA), por lo que se eliminó dicho filtro y se volvió a ejecutar la extracción con la misma metodología de muestreo. El dataset actualizado incluye 10 tipos distintos de canción (Original, Cover, Remix, Remaster, Instrumental, entre otros).

**Limpieza y ajustes al script de extracción:** se agregó `Practica 1/limpieza_datos.py`, que genera `data/processed/vocadb_limpio.csv` con las correcciones descritas en `Practica 1/README.md`. Al script de extracción se le agregó una semilla aleatoria (`random.seed(42)`) y ahora guarda directo en `data/raw/`.

## Avances
- [x] Práctica 1: Selección y limpieza de datos
- [x] Práctica 2: Estadística descriptiva, diagrama de entidades y relaciones, métricas agrupadas por año
- [x] Práctica 3: Visualización de datos
- [x] Práctica 4: Pruebas estadísticas
- [x] Práctica 5: Modelos lineales y correlación
- [x] Práctica 6: Clasificación (KNN)
- [x] Práctica 7: Clustering (K-Means)
- [x] Práctica 8: Pronóstico (series de tiempo)
- [x] Práctica 9: Análisis de texto
- [ ] PIA: Video de reporte final

## Hallazgos principales
- **Popularidad:** el % de canciones con al menos 1 favorito subió hasta un pico en 2017 (39 %) y luego bajó (12-17 % en 2023-2025). La diferencia entre etapas es estadísticamente significativa (P3, P4, P5).
- **Diversidad:** Hatsune Miku pasó de ser la voz del 93 % de las canciones en 2007 al 18 % en 2025, mientras que las voces distintas por año pasaron de 6 a 154 (P3, P9).
- **Popularidad y rating:** en VocaDB, `ratingScore = 3 × favoritos + 2 × likes` (se cumple en el 99.9 % de las canciones) (P5).
- **Perfiles:** K-Means encontró un grupo de canciones populares (7 %, 79 % originales, año mediano 2015) frente a grupos con poca interacción (P7).
- **Clasificación:** KNN distingue Original de Cover con una exactitud balanceada de 0.63; las palabras del título podrían mejorarlo (P6, P9).

## Autor
Christian Alejandro García Sánchez
