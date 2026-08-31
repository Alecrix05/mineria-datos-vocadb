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
data/raw/ -> dataset crudo, sin procesar
notebooks/ -> notebooks de exploración y análisis
src/ -> scripts reutilizables (extracción, limpieza, etc.)

## Cómo reproducir la extracción

Requiere Python con las librerías `requests` y `pandas`:

```powershell
pip install requests pandas
python src/extraer_cvs_vocadb.py
```

El script generará un archivo CSV en la raíz del proyecto; muévelo manualmente a `data/raw/` si es necesario.

## Avances
- [x] Práctica 1: Limpieza de Datos

## Autor
Christian Alejandro García Sánchez
