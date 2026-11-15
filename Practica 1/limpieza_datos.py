from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_RAW = BASE_DIR / 'data' / 'raw' / 'vocadb_songs_disperso.csv'
RUTA_LIMPIO = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'

DURACION_MAXIMA = 900

VOCALISTAS = [
    ('初音ミク', 'Hatsune Miku'), ('Miku', 'Hatsune Miku'),
    ('鏡音リン', 'Kagamine Rin'), ('鏡音レン', 'Kagamine Len'),
    ('巡音ルカ', 'Megurine Luka'), ('GUMI', 'GUMI'), ('Megpoid', 'GUMI'),
    ('重音テト', 'Kasane Teto'), ('KAITO', 'KAITO'), ('MEIKO', 'MEIKO'),
    ('結月ゆかり', 'Yuzuki Yukari'), ('flower', 'v flower'),
    ('唄音ウタ', 'Utane Uta'), ('可不', 'KAFU'), ('洛天依', 'Luo Tianyi'),
    ('神威がくぽ', 'Kamui Gakupo'), ('東北きりたん', 'Tohoku Kiritan'),
    ('Fukase', 'Fukase'), ('闇音レンリ', 'Yamine Renri'),
    ('猫村いろは', 'Nekomura Iroha'), ('various', 'Varios'),
]


def normalizar_vocalista(texto):
    if not isinstance(texto, str) or texto == '':
        return 'Sin dato'
    if texto == 'IA' or texto.startswith('IA ') or texto.endswith(' IA'):
        return 'IA'
    for clave, nombre in VOCALISTAS:
        if clave in texto:
            return nombre
    return 'Otro'

df = pd.read_csv(RUTA_RAW)
filas_iniciales = len(df)
print(f"Filas iniciales: {filas_iniciales}")

df = df.drop_duplicates(subset='id')
print(f"Duplicados eliminados: {filas_iniciales - len(df)}")

df['publishDate'] = pd.to_datetime(df['publishDate'], utc=True).dt.tz_localize(None)

print(f"artistString nulos: {df['artistString'].isna().sum()} -> 'Desconocido'")
df['artistString'] = df['artistString'].fillna('Desconocido')

ceros = (df['lengthSeconds'] == 0).sum()
largos = (df['lengthSeconds'] > DURACION_MAXIMA).sum()
df['lengthSeconds'] = df['lengthSeconds'].astype(float)
df.loc[df['lengthSeconds'] == 0, 'lengthSeconds'] = np.nan
df.loc[df['lengthSeconds'] > DURACION_MAXIMA, 'lengthSeconds'] = np.nan
print(f"Duracion = 0 -> NaN: {ceros}")
print(f"Duracion > {DURACION_MAXIMA} s -> NaN: {largos}")

df['year'] = df['publishDate'].dt.year
df['month'] = df['publishDate'].dt.month
df['etapa'] = pd.cut(df['year'], bins=[2006, 2012, 2018, 2025],
                     labels=['2007-2012', '2013-2018', '2019-2025'])

partes = df['artistString'].str.split(' feat. ', n=1, regex=False)
df['productor'] = partes.str[0].str.strip()
voces = partes.str[1].fillna('')
df['num_vocalistas'] = voces.apply(lambda v: len(v.split(', ')) if v else 0)
df['vocalista'] = voces.str.split(', ').str[0].apply(normalizar_vocalista)

principales = ['Original', 'Cover', 'Remix']
df['tipo_agrupado'] = np.where(df['songType'].isin(principales), df['songType'], 'Otro')

df['tiene_favoritos'] = (df['favoritedTimes'] > 0).astype(int)

RUTA_LIMPIO.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(RUTA_LIMPIO, index=False, encoding='utf-8-sig')

print(f"\nFilas finales: {len(df)}")
print(f"Duracion valida: {df['lengthSeconds'].notna().sum()} canciones")
print("\nVocalistas principales:")
print(df['vocalista'].value_counts().head(10))
print("\nTipo agrupado:")
print(df['tipo_agrupado'].value_counts())
print(f"\nGuardado en {RUTA_LIMPIO}")
