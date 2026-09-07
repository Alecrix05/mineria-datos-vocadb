from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'raw' / 'vocadb_songs_disperso.csv'

df = pd.read_csv(RUTA_CSV)
df['publishDate'] = pd.to_datetime(df['publishDate'])

print("-- TIPOS DE DATOS --")
print(df.dtypes)

print("\n-- RESUMEN ESTADISTICO GENERAL --")
print(df.describe(include='all'))

print("\n-- DISTRIBUCION DE TIPOS DE CANCION --")
print(df['songType'].value_counts())

print("\n-- RANGO DE FECHAS --")
print(df['publishDate'].describe())

print("\n-- PROMEDIO AGRUPADO POR AÑO --")

df['year'] = df['publishDate'].dt.year

agrupado = df.groupby('year')[['favoritedTimes', 'ratingScore', 'lengthSeconds']].mean()
print(agrupado)