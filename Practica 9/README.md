# Práctica 9: Análisis de texto

**Script:** `analisis_texto.py` (lee `data/processed/vocadb_limpio.csv`)
**Salida:** 3 gráficas en `graficas/` y `palabras_clave_vs_tipo.csv`

```powershell
pip install janome
python "Practica 9/analisis_texto.py"
```

Se analizan dos campos de texto: el título (`name`) y los créditos (`artistString`). Como el 65 % de los títulos está en japonés o kanji, se usa **Janome**, un tokenizador morfológico de japonés escrito en Python puro, para separar palabras y quedarse con los sustantivos.

## 1. Sistema de escritura del título (`01_escritura_por_etapa.png`)

| Etapa | Japonés (kana) | Solo kanji | Alfabeto latino |
|---|---|---|---|
| 2007-2012 | 59 % | 10 % | 30 % |
| 2013-2018 | 49 % | 10 % | **39 %** |
| 2019-2025 | 53 % | 13 % | 33 % |

Los títulos en alfabeto latino (inglés sobre todo) crecieron en 2013-2018. Esto coincide con la etapa de mayor popularidad y con la llegada de bancos de voz en inglés, lo que sugiere una escena más internacional.

## 2. Palabras más frecuentes (`02_palabras_frecuentes.png`)
- **Títulos en alfabeto latino** (sin palabras vacías como "the" o "and"): *love, world, night, song, last, heart, blue, star, time, moon*.
- **Títulos en japonés** (sustantivos): ミク (Miku), うた (canción), 世界 (mundo), 初音 (Hatsune), 少女 (chica), ガール (girl), あなた (tú), 好き (me gusta).
- En ambos idiomas se repiten los mismos temas: **amor, mundo, noche/cielo y la propia Miku**. Que "Miku" sea el sustantivo más común confirma su papel de personaje, no solo de voz.

## 3. Palabras clave vs tipo de canción

| Palabra en el título | Títulos | Tipo más común |
|---|---|---|
| remix / mix / arrange | 122 | Remix (83 %) |
| instrumental / off vocal | 23 | Instrumental (87 %) |
| ver. / version | 93 | Remix (36 %) |
| cover / 歌ってみた | 3 | Cover (67 %) |

Algunas palabras del título predicen bien el tipo de canción. Esto confirma lo que se propuso en la Práctica 6: agregar características de texto podría mejorar el clasificador. Los Cover casi nunca lo dicen en el título, y por eso son difíciles de detectar.

## 4. Diversidad de voces sintéticas (`03_diversidad_voces.png`)
En cada año (~320 canciones por año), el número de voces distintas pasó de **6 en 2007 a 154 en 2025**. Junto con la caída de Hatsune Miku de 93 % a 18 % (Práctica 3), muestra que la escena se diversificó mucho: hay más bancos de voz, más versiones y más idiomas. Este conteo trata cada versión como una voz distinta (por ejemplo, "初音ミク V4 (English)" cuenta aparte de "初音ミク").

El número de productores distintos se mantiene estable (82-91 % de las canciones de cada año son de productores diferentes): la producción está muy repartida entre muchos creadores.
