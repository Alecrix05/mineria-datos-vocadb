# Práctica 5: Modelos lineales y correlación

**Script:** `modelos_lineales.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** 3 gráficas en `graficas/`

```powershell
pip install statsmodels
python "Practica 5/modelos_lineales.py"
```

## 1. Correlación (`01_matriz_correlacion.png`)
- `favoritedTimes` y `ratingScore`: Pearson 0.98, Spearman 0.85. Es la única relación fuerte.
- Duración, año y número de vocalistas casi no se relacionan con la popularidad (|r| ≤ 0.10).
- Se usa Spearman en la gráfica porque las variables tienen muchos ceros y valores extremos.

## 2. Regresión simple: `ratingScore ~ favoritedTimes` (`02_regresion_rating_favoritos.png`)
- **ratingScore = −0.05 + 5.49 · favoritedTimes**, R² = 0.962
- ¿Por qué es tan alto? En VocaDB, **ratingScore = 3 × favoritos + 2 × likes**. Se comprobó en los datos: se cumple en el 99.9 % de las canciones. La pendiente sale 5.49 y no 3 porque las canciones con favoritos también suelen tener likes.
- Conclusión: las dos variables miden casi lo mismo, así que en los modelos de las siguientes prácticas no se usan juntas como predictoras.

## 3. Tendencia después del pico (`03_tendencia_favoritos.png`)
- Regresión del % anual de canciones con favoritos, 2017-2025: **−3.07 puntos porcentuales por año**, R² = 0.86 (p < 0.001).
- La caída es constante y clara, aunque parte se debe a que las canciones recientes han tenido menos tiempo de acumular favoritos.

## 4. Regresión múltiple: `log(1 + ratingScore)`
Variables: año, duración (min), tipo de canción (referencia: Original) y número de vocalistas.

| Variable | Coeficiente | p | Interpretación |
|---|---|---|---|
| Cover | −0.35 | < 0.001 | Los Cover tienen ~29 % menos rating que los Original |
| Otro | −0.27 | < 0.001 | También menos rating que los Original |
| Remix | +0.11 | 0.059 | Sin diferencia significativa |
| año | −0.011 | < 0.001 | Cada año más reciente, ~1 % menos rating |
| duración (min) | +0.054 | < 0.001 | Canciones más largas, ligeramente más rating |
| num_vocalistas | +0.070 | 0.020 | Más voces, ligeramente más rating |

**R² = 0.037.** Las variables son significativas, pero explican menos del 4 % de la popularidad. La popularidad depende de factores que no están en el dataset (productor conocido, promoción, la canción en sí).
