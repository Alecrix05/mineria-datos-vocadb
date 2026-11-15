# Práctica 4: Pruebas estadísticas

**Script:** `pruebas_estadisticas.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** `resultados_pruebas.csv` con estadístico, p-valor y decisión de cada prueba
**Nivel de significancia:** α = 0.05

```powershell
python "Practica 4/pruebas_estadisticas.py"
```

## Resultados

| Prueba | H0 | p-valor | Decisión |
|---|---|---|---|
| D'Agostino-Pearson (normalidad) | La duración es normal | < 0.001 | Se rechaza |
| Levene | Varianzas de duración iguales entre tipos | < 0.001 | Se rechaza |
| ANOVA de un factor | Duración media igual por tipo | < 0.001 | Se rechaza |
| Kruskal-Wallis | Duración igual por tipo | 0.002 | Se rechaza |
| Chi-cuadrada | Tipo de canción independiente de la etapa | < 0.001 | Se rechaza |
| Chi-cuadrada | Tener favoritos independiente de la etapa | < 0.001 | Se rechaza |
| Kruskal-Wallis | `ratingScore` igual en las 3 etapas | < 0.001 | Se rechaza |

## Interpretación

1. **¿ANOVA o Kruskal-Wallis?** La duración no es normal y las varianzas no son iguales, así que no se cumplen los supuestos del ANOVA. Se reporta como referencia, pero la prueba válida es **Kruskal-Wallis**.
2. **Duración por tipo:** Kruskal-Wallis indica diferencias. El post-hoc (Mann-Whitney con corrección de Bonferroni) muestra que **solo los Remix son distintos**: duran más (mediana 237 s) que los Original (221 s) y los Cover (220 s). Original y Cover duran prácticamente lo mismo.
3. **Tipo de canción vs etapa:** la proporción de tipos cambia con el tiempo. En 2013-2018 hubo más Originales (61.7 %) que en 2007-2012 (55.5 %), aunque la diferencia es moderada.
4. **Favoritos vs etapa:** es la diferencia más fuerte. El % de canciones con al menos 1 favorito es 22.7 % (2007-2012), **31.4 % (2013-2018)** y 19.9 % (2019-2025). Confirma estadísticamente el pico que se vio en la Práctica 3.
5. **Precaución:** con más de 6,000 canciones, diferencias pequeñas salen significativas. Por eso se reportan también las medianas y porcentajes, que muestran el tamaño real de cada diferencia.
