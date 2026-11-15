from collections import Counter
from pathlib import Path
import re
import matplotlib.pyplot as plt
import pandas as pd
from janome.tokenizer import Tokenizer

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)

AZUL, NARANJA, AQUA, AMARILLO, GRIS = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#bbbbbb'
plt.rcParams.update({
    'savefig.dpi': 150, 'font.size': 10, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
    'font.family': ['Yu Gothic', 'MS Gothic', 'Noto Sans CJK JP', 'DejaVu Sans'],
})
pd.set_option('display.width', 140)
pd.set_option('display.max_columns', 10)

df = pd.read_csv(RUTA_CSV)
df['name'] = df['name'].astype(str)


def escritura(titulo):
    if re.search(r'[぀-ヿ]', titulo):
        return 'Japonés (kana)'
    if re.search(r'[一-鿿]', titulo):
        return 'Solo kanji/hanzi'
    if re.search(r'[A-Za-z]', titulo):
        return 'Alfabeto latino'
    return 'Otro (coreano, símbolos)'

df['escritura'] = df['name'].apply(escritura)
orden = ['Japonés (kana)', 'Solo kanji/hanzi', 'Alfabeto latino', 'Otro (coreano, símbolos)']
colores = [AZUL, AQUA, NARANJA, GRIS]
tabla = pd.crosstab(df['etapa'], df['escritura'], normalize='index')[orden] * 100
print("-- ESCRITURA DEL TITULO POR ETAPA (%) --")
print(tabla.round(1))

fig, ax = plt.subplots(figsize=(9, 3.8))
izquierda = pd.Series(0.0, index=tabla.index)
for categoria, color in zip(orden, colores):
    ax.barh(tabla.index, tabla[categoria], left=izquierda, color=color, label=categoria,
            height=0.6, edgecolor='white', linewidth=1)
    for y, (inicio, valor) in enumerate(zip(izquierda, tabla[categoria])):
        if valor > 6:
            ax.text(inicio + valor / 2, y, f'{valor:.0f} %', ha='center', va='center',
                    color='white', fontweight='bold')
    izquierda += tabla[categoria]
ax.set_xlim(0, 100)
ax.invert_yaxis()
ax.set_xlabel('% de títulos')
ax.set_title('Sistema de escritura de los títulos por etapa')
ax.grid(axis='y', visible=False)
ax.legend(ncol=4, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.2))
fig.tight_layout()
fig.savefig(CARPETA / '01_escritura_por_etapa.png', bbox_inches='tight')
plt.close(fig)

STOPWORDS = {'the', 'and', 'for', 'you', 'your', 'are', 'not', 'all', 'with', 'from', 'that',
             'this', 'its', "it's", "don't", 'just', 'feat', 'ver', 'version', 'mix', 'remix',
             'edit', 'original', 'cover', 'one', 'new', 'off', 'out', 'can', 'have', 'into'}
palabras = Counter(
    p for titulo in df.loc[df['escritura'] == 'Alfabeto latino', 'name']
    for p in re.findall(r"[a-z']+", titulo.lower())
    if len(p) > 2 and p not in STOPWORDS)
top_en = pd.Series(dict(palabras.most_common(15)))
print("\n-- PALABRAS MAS FRECUENTES (titulos en alfabeto latino) --")
print(top_en.to_string())

TRADUCCION = {
    'ミク': 'Miku', 'うた': 'canción', '世界': 'mundo', '初音': 'Hatsune', '少女': 'chica',
    'ガール': 'girl', 'あなた': 'tú', '好き': 'me gusta', 'クリスマス': 'Navidad',
    '今日': 'hoy', '明日': 'mañana', 'ゲーム': 'juego', '天使': 'ángel', '魔法': 'magia',
    'ゴースト': 'fantasma', '最後': 'final', 'いつか': 'algún día', 'テーマ': 'tema',
    '恋': 'amor', '夜': 'noche', '君': 'tú', '花': 'flor', '夢': 'sueño', '空': 'cielo',
    'リン': 'Rin', 'ルカ': 'Luka', 'レン': 'Len', '世': 'mundo', '僕': 'yo', '歌': 'canción',
    'ラブ': 'love', 'ワールド': 'world', 'プリンセス': 'princesa', 'セカイ': 'mundo',
}
NO_SUSTANTIVOS = {'こと', 'もの', 'よう', 'さん', 'ちゃん', 'たち', 'ここ', 'これ', 'それ', 'の', 'ん'}
tokenizador = Tokenizer()
sustantivos = Counter()
for titulo in df.loc[df['escritura'] == 'Japonés (kana)', 'name']:
    for token in tokenizador.tokenize(titulo):
        texto = token.surface
        if (token.part_of_speech.startswith('名詞') and len(texto) > 1
                and texto not in NO_SUSTANTIVOS
                and not re.fullmatch(r'[\W\d_A-Za-z]+', texto)):
            sustantivos[texto] += 1
top_jp = pd.Series(dict(sustantivos.most_common(15)))
etiquetas_jp = [f"{p} ({TRADUCCION[p]})" if p in TRADUCCION else p for p in top_jp.index]
print("\n-- SUSTANTIVOS MAS FRECUENTES (titulos en japones) --")
print(pd.Series(top_jp.values, index=etiquetas_jp).to_string())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
ax1.barh(top_en.index[::-1], top_en.values[::-1], color=NARANJA, height=0.7)
ax1.set_title('Palabras más frecuentes\n(títulos en alfabeto latino)')
ax1.set_xlabel('Apariciones')
ax1.grid(axis='y', visible=False)
ax2.barh(etiquetas_jp[::-1], top_jp.values[::-1], color=AZUL, height=0.7)
ax2.set_title('Sustantivos más frecuentes\n(títulos en japonés)')
ax2.set_xlabel('Apariciones')
ax2.grid(axis='y', visible=False)
fig.tight_layout()
fig.savefig(CARPETA / '02_palabras_frecuentes.png', bbox_inches='tight')
plt.close(fig)

CLAVES = {
    'remix / mix / arrange': r'remix|\bmix\b|arrange|アレンジ',
    'ver. / version': r'\bver\b|ver\.|version|バージョン',
    'cover / 歌ってみた': r'cover|カバー|歌ってみた',
    'instrumental / off vocal': r'inst|off ?vocal|オフボーカル|カラオケ|karaoke',
}
titulos = df['name'].str.lower()
filas = []
for etiqueta, patron in CLAVES.items():
    contiene = titulos.str.contains(patron, regex=True)
    pct_por_tipo = df[contiene]['songType'].value_counts(normalize=True) * 100
    filas.append({'palabra_clave': etiqueta, 'titulos': int(contiene.sum()),
                  'tipo_mas_comun': pct_por_tipo.index[0] if len(pct_por_tipo) else '-',
                  '%_de_ese_tipo': round(pct_por_tipo.iloc[0], 1) if len(pct_por_tipo) else 0})
claves = pd.DataFrame(filas)
print("\n-- PALABRAS CLAVE DEL TITULO VS TIPO DE CANCION --")
print(claves.to_string(index=False))
claves.to_csv(Path(__file__).resolve().parent / 'palabras_clave_vs_tipo.csv', index=False, encoding='utf-8-sig')

partes = df['artistString'].str.split(' feat. ', n=1, regex=False)
df['voz_original'] = partes.str[1].fillna('').str.split(', ').str[0].str.strip()
diversidad = df.groupby('year').agg(
    canciones=('id', 'count'),
    productores_distintos=('productor', 'nunique'),
    voces_distintas=('voz_original', lambda s: s[s != ''].nunique()),
)
print("\n-- DIVERSIDAD POR AÑO --")
print(diversidad.to_string())

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(diversidad.index, diversidad['voces_distintas'], color=AZUL, marker='o', markersize=5,
        linewidth=2, label='Voces sintéticas distintas')
ax.set_xticks(diversidad.index)
ax.tick_params(axis='x', rotation=45)
ax.set_ylabel('Voces distintas (en ~320 canciones)')
ax.set_title('Diversidad de voces sintéticas por año')
ax.set_ylim(0, diversidad['voces_distintas'].max() * 1.15)
fig.tight_layout()
fig.savefig(CARPETA / '03_diversidad_voces.png', bbox_inches='tight')
plt.close(fig)
