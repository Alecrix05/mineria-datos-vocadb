# Práctica 3: Visualización de datos

**Script:** `visualizacion.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** 6 gráficas en `graficas/`

```powershell
python "Practica 3/visualizacion.py"
```

## Gráficas y hallazgos

| Gráfica | Qué muestra | Hallazgo |
|---|---|---|
| `01_tipos_por_anio.png` | Proporción de Original / Cover / Remix / Otro por año | 2007 es casi todo Cover (72 %), porque Miku salió en agosto de 2007 y lo primero fueron covers. Desde 2008 las canciones originales dominan (55-70 %). |
| `02_pct_favoritos_por_anio.png` | % de canciones con al menos 1 favorito | Sube hasta su pico en 2017 (39 %) y baja hasta 12 % en 2024. |
| `03_hist_duracion.png` | Distribución de la duración | Forma de campana con mediana de 3.7 min, el formato típico de canción pop. |
| `04_box_duracion_tipo.png` | Duración por tipo | Original y Cover tienen duraciones muy parecidas; Remix y Otro varían más. |
| `05_top_vocalistas.png` | Las 10 voces sintéticas más usadas | Hatsune Miku aparece en 2,039 canciones, casi 7 veces más que la segunda (Kagamine Rin). |
| `06_pct_miku_por_anio.png` | % de canciones con Miku como voz principal | Baja de 93 % en 2007 a ~18 % en 2024-2025: hay mucha más variedad de voces. |

## Nota sobre la caída de favoritos
Las canciones recientes han tenido menos tiempo para que los usuarios las marquen como favoritas, así que parte de la caída después de 2017 se debe a la antigüedad de la canción y no solo a la pérdida de popularidad.

## Decisión
Se usa **% de canciones con al menos 1 favorito** en lugar del promedio de `favoritedTimes`, porque el 76 % de las canciones tiene 0 favoritos y el promedio queda dominado por unas cuantas canciones muy populares.
