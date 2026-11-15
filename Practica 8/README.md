# Práctica 8: Pronóstico (series de tiempo)

**Scripts:**
- `pronostico.py`: modelos y pronósticos
- `extraer_totales.py`: descarga de la API el total real de canciones publicadas por mes (para la Parte B)

```powershell
pip install statsmodels
python "Practica 8/extraer_totales.py"   # opcional, ~1-2 min, genera data/raw/vocadb_totales_mensuales.csv
python "Practica 8/pronostico.py"
```

## Parte A: % de canciones con favoritos (trimestral)

- **Serie:** % de canciones con al menos 1 favorito por trimestre, de 2008 a 2025 (72 trimestres, ~80 canciones por trimestre). Se excluye 2007 porque solo tiene 2 trimestres.
- **Validación:** se entrena hasta 2023 y se prueba con 2024-2025 (8 trimestres).

| Modelo | MAE | RMSE |
|---|---|---|
| **Promedio móvil (4)** | **4.41** | **5.03** |
| ARIMA(1,1,1) | 4.47 | 5.11 |
| Holt amortiguado | 5.00 | 5.90 |
| Ingenuo (último valor) | 5.03 | 6.01 |
| Tendencia lineal | 10.07 | 11.27 |

(Error en puntos porcentuales. Gráfica: `01_comparacion_modelos.png`.)

- **Pronóstico 2026-2027** (`02_pronostico_pct_favoritos.png`, `pronostico_pct_favoritos.csv`): **~16 %** de canciones con favoritos por trimestre. El intervalo aproximado de 95 % va de 0 % a 36 %.

**Interpretación**
- La tendencia lineal es el peor modelo: proyecta la caída de 2017-2023, pero en 2024-2025 la serie se estabilizó e incluso repuntó (de 5 % a 16-21 %).
- Los modelos que siguen el nivel reciente (promedio móvil y ARIMA) son los mejores y casi empatan.
- El pronóstico es una línea plana: no hay una tendencia clara que proyectar, y el intervalo es amplio porque cada trimestre tiene pocas canciones en la muestra.

## Parte B: total de canciones publicadas por año

La muestra de la Práctica 1 tiene un número fijo de canciones por año (~320), así que **no sirve para medir cuántas canciones se publican**. Para eso, `extraer_totales.py` pide a la API solo el conteo real de cada mes (228 consultas, sin descargar canciones).

Cuando existe `data/raw/vocadb_totales_mensuales.csv`, `pronostico.py` también:
- muestra las canciones publicadas por año,
- compara los mismos 5 modelos (entrenando hasta 2022 y probando con 2023-2025),
- pronostica 2026-2028 y genera `03_pronostico_total_canciones.png` y `pronostico_total_canciones.csv`.

Esta parte responde directamente a la pregunta del proyecto: si la cultura Vocaloid está creciendo o decreciendo en volumen de producción.
