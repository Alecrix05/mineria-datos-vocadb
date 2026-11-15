# Práctica 6: Clasificación con KNN

**Script:** `clasificacion_knn.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** 2 gráficas en `graficas/`

```powershell
pip install scikit-learn
python "Practica 6/clasificacion_knn.py"
```

## Planteamiento
- **Objetivo:** predecir si una canción es **Original o Cover**.
- **Datos:** 5,110 canciones (3,392 Original y 1,718 Cover) con duración válida.
- **Características:** duración (min), año, log(1 + favoritos), log(1 + likes), número de vocalistas y si la voz principal es Hatsune Miku. Los likes se calculan como `(ratingScore − 3 × favoritos) / 2`, según lo que se encontró en la Práctica 5.
- **Preprocesamiento:** `StandardScaler`, necesario porque KNN usa distancias y las variables tienen escalas muy distintas (año ≈ 2000, duración ≈ 4).
- **División:** 70 % entrenamiento y 30 % prueba, estratificada y con semilla 42.
- **Selección de k:** búsqueda de k entre 1 y 41 (impares) con pesos uniformes o por distancia, usando validación cruzada de 5 pliegues y **exactitud balanceada** como métrica, porque las clases están desbalanceadas (2:1).

## Resultados
- **Mejor modelo:** k = 27 con pesos por distancia (`01_seleccion_k.png`).

| Métrica (conjunto de prueba) | KNN | Línea base (siempre "Original") |
|---|---|---|
| Exactitud | 0.688 | 0.664 |
| Exactitud balanceada | **0.626** | 0.500 |
| Recall Original | 0.815 | 1.000 |
| Recall Cover | 0.437 | 0.000 |

Matriz de confusión: `02_matriz_confusion.png`.

## Interpretación
- El modelo supera a la línea base: detecta el 44 % de los Cover, mientras que la línea base no detecta ninguno.
- El desempeño es moderado porque Original y Cover se parecen mucho en estas variables. En la Práctica 4 se vio que tienen casi la misma duración (mediana de 221 s contra 220 s). Según la importancia por permutación, las variables que más ayudan son **si la voz es Miku** y el **año**. Después vienen likes, número de vocalistas, duración y favoritos. Los Cover tienen menos favoritos en promedio (19 % tiene al menos uno, contra 28 % de los Original), pero esa diferencia sola no basta para separarlos.
- Para mejorar haría falta información que el dataset no tiene, como tags, el texto del título ("cover", "歌ってみた") o los datos del productor.
