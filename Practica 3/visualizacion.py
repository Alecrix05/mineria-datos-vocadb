from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)

AZUL, NARANJA, AQUA, AMARILLO = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
COLOR_TIPO = {'Original': AZUL, 'Cover': NARANJA, 'Remix': AQUA, 'Otro': AMARILLO}
plt.rcParams.update({
    'figure.dpi': 120, 'savefig.dpi': 150, 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#999999', 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
})

df = pd.read_csv(RUTA_CSV, parse_dates=['publishDate'])


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(CARPETA / nombre, bbox_inches='tight')
    plt.close(fig)
    print(f"Guardada: graficas/{nombre}")

tipos = ['Original', 'Cover', 'Remix', 'Otro']
proporcion = pd.crosstab(df['year'], df['tipo_agrupado'], normalize='index')[tipos] * 100
fig, ax = plt.subplots(figsize=(10, 5))
abajo = pd.Series(0.0, index=proporcion.index)
for tipo in tipos:
    ax.bar(proporcion.index, proporcion[tipo], bottom=abajo, color=COLOR_TIPO[tipo],
           label=tipo, width=0.8, edgecolor='white', linewidth=1)
    abajo += proporcion[tipo]
ax.set_title('Composición de tipos de canción por año')
ax.set_ylabel('% de canciones del año')
ax.set_xticks(proporcion.index)
ax.tick_params(axis='x', rotation=45)
ax.set_ylim(0, 100)
ax.grid(axis='x', visible=False)
ax.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=False)
guardar(fig, '01_tipos_por_anio.png')

pct_fav = df.groupby('year')['tiene_favoritos'].mean() * 100
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(pct_fav.index, pct_fav.values, color=AZUL, linewidth=2, marker='o', markersize=6)
pico = pct_fav.idxmax()
ax.annotate(f'Pico: {pct_fav[pico]:.0f} % ({pico})', (pico, pct_fav[pico]),
            textcoords='offset points', xytext=(0, 10), ha='center')
ax.set_title('% de canciones con al menos 1 favorito en VocaDB')
ax.set_ylabel('% de canciones')
ax.set_xticks(pct_fav.index)
ax.tick_params(axis='x', rotation=45)
ax.set_ylim(0, pct_fav.max() * 1.25)
guardar(fig, '02_pct_favoritos_por_anio.png')

duracion_min = df['lengthSeconds'].dropna() / 60
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(duracion_min[duracion_min <= 10], bins=50, color=AZUL, edgecolor='white', linewidth=0.5)
mediana = duracion_min.median()
ax.axvline(mediana, color='#333333', linestyle='--', linewidth=1)
ax.text(mediana + 0.2, ax.get_ylim()[1] * 0.9, f'Mediana: {mediana:.1f} min')
ax.set_title('Distribución de la duración de las canciones (hasta 10 min)')
ax.set_xlabel('Duración (minutos)')
ax.set_ylabel('Número de canciones')
guardar(fig, '03_hist_duracion.png')

fig, ax = plt.subplots(figsize=(8, 4.5))
datos = [df.loc[df['tipo_agrupado'] == t, 'lengthSeconds'].dropna() / 60 for t in tipos]
caja = ax.boxplot(datos, tick_labels=tipos, patch_artist=True, showfliers=False, widths=0.5)
for parche, tipo in zip(caja['boxes'], tipos):
    parche.set_facecolor(COLOR_TIPO[tipo])
    parche.set_alpha(0.85)
for mediana_linea in caja['medians']:
    mediana_linea.set_color('#222222')
ax.set_title('Duración por tipo de canción (sin valores atípicos)')
ax.set_ylabel('Duración (minutos)')
ax.grid(axis='x', visible=False)
guardar(fig, '04_box_duracion_tipo.png')

top_voc = (df[~df['vocalista'].isin(['Otro', 'Sin dato', 'Varios'])]['vocalista']
           .value_counts().head(10).sort_values())
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top_voc.index, top_voc.values, color=AZUL, height=0.7)
for y, valor in enumerate(top_voc.values):
    ax.text(valor + 15, y, str(valor), va='center')
ax.set_title('Top 10 voces sintéticas en la muestra')
ax.set_xlabel('Número de canciones')
ax.grid(axis='y', visible=False)
guardar(fig, '05_top_vocalistas.png')

pct_miku = df.groupby('year')['vocalista'].apply(lambda s: (s == 'Hatsune Miku').mean() * 100)
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(pct_miku.index, pct_miku.values, color=NARANJA, linewidth=2, marker='o', markersize=6)
ax.set_title('% de canciones con Hatsune Miku como voz principal')
ax.set_ylabel('% de canciones del año')
ax.set_xticks(pct_miku.index)
ax.tick_params(axis='x', rotation=45)
ax.set_ylim(0, 100)
guardar(fig, '06_pct_miku_por_anio.png')

print("\n% con favoritos por año:")
print(pct_fav.round(1).to_string())
print("\n% Hatsune Miku por año:")
print(pct_miku.round(1).to_string())
