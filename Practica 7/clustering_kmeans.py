from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)
RUTA_SALIDA = Path(__file__).resolve().parent / 'canciones_con_cluster.csv'
SEMILLA = 42

COLORES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
plt.rcParams.update({
    'savefig.dpi': 150, 'font.size': 10, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
})

df = pd.read_csv(RUTA_CSV).dropna(subset=['lengthSeconds']).copy()
df['duracion_min'] = df['lengthSeconds'] / 60
df['log_favoritos'] = np.log1p(df['favoritedTimes'])
df['log_likes'] = np.log1p(((df['ratingScore'] - 3 * df['favoritedTimes']) / 2).clip(lower=0))

caracteristicas = ['log_favoritos', 'log_likes', 'duracion_min', 'year']
X = StandardScaler().fit_transform(df[caracteristicas])
print(f"Canciones: {len(df)} | caracteristicas: {caracteristicas}")

rango_k = range(2, 9)
inercias, siluetas = [], []
for k in rango_k:
    km = KMeans(n_clusters=k, n_init=10, random_state=SEMILLA).fit(X)
    inercias.append(km.inertia_)
    siluetas.append(silhouette_score(X, km.labels_, sample_size=3000, random_state=SEMILLA))
    print(f"k = {k}: inercia = {km.inertia_:9.1f} | silueta = {siluetas[-1]:.3f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(list(rango_k), inercias, marker='o', color=COLORES[0], linewidth=2)
ax1.set_title('Método del codo')
ax1.set_xlabel('k')
ax1.set_ylabel('Inercia')
ax2.plot(list(rango_k), siluetas, marker='o', color=COLORES[1], linewidth=2)
ax2.set_title('Coeficiente de silueta')
ax2.set_xlabel('k')
ax2.set_ylabel('Silueta promedio')
fig.tight_layout()
fig.savefig(CARPETA / '01_codo_silueta.png', bbox_inches='tight')
plt.close(fig)

K = 4
modelo = KMeans(n_clusters=K, n_init=10, random_state=SEMILLA).fit(X)
df['cluster'] = modelo.labels_


def nombrar(fila):
    if fila['pct_con_favoritos'] > 80:
        return 'Populares'
    if fila['anio_mediano'] >= 2019:
        return 'Recientes sin favoritos'
    if fila['duracion_mediana_min'] >= 4:
        return 'Largas (4+ min)'
    return 'Cortas 2007-2017'

perfil = df.groupby('cluster').agg(
    canciones=('id', 'count'),
    favoritos_prom=('favoritedTimes', 'mean'),
    pct_con_favoritos=('tiene_favoritos', lambda s: s.mean() * 100),
    duracion_mediana_min=('duracion_min', 'median'),
    anio_mediano=('year', 'median'),
    pct_original=('songType', lambda s: (s == 'Original').mean() * 100),
    pct_miku=('vocalista', lambda s: (s == 'Hatsune Miku').mean() * 100),
).round(2)
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)
perfil['nombre'] = perfil.apply(nombrar, axis=1)
NOMBRES = perfil['nombre'].to_dict()
print(f"\n-- PERFIL DE CADA CLUSTER (k = {K}) --")
print(perfil)

pca = PCA(n_components=2, random_state=SEMILLA)
coords = pca.fit_transform(X)
var = pca.explained_variance_ratio_ * 100
fig, ax = plt.subplots(figsize=(8, 6))
for c in range(K):
    mascara = df['cluster'].values == c
    ax.scatter(coords[mascara, 0], coords[mascara, 1], s=10, alpha=0.6, color=COLORES[c],
               label=f'{c}: {NOMBRES[c]} ({mascara.sum()})')
ax.set_xlabel(f'Componente 1 ({var[0]:.0f} % de la varianza)')
ax.set_ylabel(f'Componente 2 ({var[1]:.0f} % de la varianza)')
ax.set_title(f'Clusters K-Means (k = {K}) proyectados con PCA')
ax.legend(frameon=False, markerscale=2)
fig.tight_layout()
fig.savefig(CARPETA / '02_clusters_pca.png', bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5))
for c in range(K):
    sub = df[df['cluster'] == c]
    ax.scatter(sub['year'] + np.random.default_rng(c).uniform(-0.35, 0.35, len(sub)),
               sub['duracion_min'], s=6 + sub['favoritedTimes'] * 2, alpha=0.5,
               color=COLORES[c])
    ax.scatter([], [], s=30, color=COLORES[c], label=f'{c}: {NOMBRES[c]}')
ax.set_xticks(range(2007, 2026, 2))
ax.set_xlabel('Año de publicación')
ax.set_ylabel('Duración (min)')
ax.set_title('Clusters por año y duración (tamaño = favoritos)')
ax.legend(frameon=False, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.12))
fig.tight_layout()
fig.savefig(CARPETA / '03_clusters_anio_duracion.png', bbox_inches='tight')
plt.close(fig)

df[['id', 'name', 'artistString', 'songType', 'year', 'duracion_min',
    'favoritedTimes', 'ratingScore', 'cluster']].assign(nombre_cluster=df['cluster'].map(NOMBRES)).to_csv(RUTA_SALIDA, index=False, encoding='utf-8-sig')
print(f"\nAsignacion de clusters guardada en {RUTA_SALIDA.name}")
