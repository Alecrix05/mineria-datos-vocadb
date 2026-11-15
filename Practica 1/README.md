# Práctica 1: Selección y limpieza de datos

## Scripts
- `extraer_csv_vocadb.py`: extracción desde la API de VocaDB → `data/raw/vocadb_songs_disperso.csv`
- `limpieza_datos.py`: limpieza → `data/processed/vocadb_limpio.csv`

```powershell
python "Practica 1/limpieza_datos.py"
```

## Limpieza aplicada

| Problema | Casos | Decisión |
|---|---|---|
| `lengthSeconds = 0` (duración no registrada) | 292 | Se cambia a `NaN` |
| `lengthSeconds` > 15 min (dramas, mashups, videos largos) | 14 | Se cambia a `NaN` |
| `artistString` nulo | 8 | Se llena con `Desconocido` |
| `publishDate` como texto con zona horaria | todas | Se convierte a datetime sin zona |
| Duplicados por `id` | 0 | Ninguno |

No se eliminan filas: las canciones con duración inválida siguen siendo útiles para el análisis de popularidad.

## Columnas nuevas

| Columna | Descripción |
|---|---|
| `year`, `month` | Año y mes de publicación |
| `etapa` | Periodo: 2007-2012, 2013-2018, 2019-2025 |
| `productor` | Texto antes de `feat.` en `artistString` |
| `vocalista` | Primera voz sintética después de `feat.`, normalizada y romanizada (ej. `初音ミク V4 (English)` → `Hatsune Miku`) |
| `num_vocalistas` | Número de voces en la canción |
| `tipo_agrupado` | Original, Cover, Remix u Otro (los tipos con menos de 120 canciones se agrupan) |
| `tiene_favoritos` | 1 si la canción tiene al menos 1 favorito, 0 si no |
