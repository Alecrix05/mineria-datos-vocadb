# Práctica 7: Clustering con K-Means

**Script:** `clustering_kmeans.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** 3 gráficas en `graficas/` y `canciones_con_cluster.csv` (cada canción con su cluster)

```powershell
python "Practica 7/clustering_kmeans.py"
```

## Planteamiento
- **Datos:** 5,736 canciones con duración válida.
- **Variables:** log(1 + favoritos), log(1 + likes), duración (min) y año, estandarizadas con `StandardScaler`. Se usa logaritmo porque la mayoría de las canciones tiene 0 favoritos y unas pocas tienen más de 100.

## Elección de k (`01_codo_silueta.png`)

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| Silueta | **0.479** | 0.292 | 0.273 | 0.285 | 0.256 | 0.278 | 0.295 |

- k = 2 tiene la mejor silueta, pero solo separa "con favoritos" de "sin favoritos", algo que ya se sabía.
- El codo empieza a suavizarse entre k = 3 y k = 4. **Se eligió k = 4** porque da grupos interpretables y la silueta casi no cambia entre k = 3 y k = 8.

## Perfiles (k = 4)

| Cluster | Canciones | % con favoritos | Duración mediana | Año mediano | % Original | % Miku |
|---|---|---|---|---|---|---|
| 0: Recientes sin favoritos | 2,259 | 17.7 % | 3.4 min | 2022 | 58 % | 26 % |
| 1: **Populares** | 403 | **99.5 %** | 3.9 min | 2015 | **79 %** | 36 % |
| 2: Largas (4+ min) | 1,874 | 24.7 % | 4.6 min | 2013 | 59 % | 34 % |
| 3: Cortas 2007-2017 | 1,200 | 14.3 % | 2.7 min | 2010 | 54 % | **49 %** |

Gráficas: `02_clusters_pca.png` (proyección PCA; 69 % de la varianza en 2 componentes) y `03_clusters_anio_duracion.png`.

## Interpretación
- **Populares (7 % de las canciones):** casi todas son originales y su año mediano es 2015, en plena etapa de mayor popularidad que se vio en las Prácticas 3 y 4.
- **Cortas 2007-2017:** canciones de la primera etapa, con muchas piezas cortas (covers y demos) y la mayor presencia de Miku (49 %), lo que coincide con su dominio inicial.
- **Recientes sin favoritos:** el grupo más grande, con año mediano 2022 y poca interacción. Refuerza la caída de favoritos en años recientes.
- **Largas (4+ min):** canciones de duración larga de cualquier año, con popularidad baja o media.
- El año y la popularidad son lo que más separa los grupos. La duración separa sobre todo a las canciones cortas de las largas.
