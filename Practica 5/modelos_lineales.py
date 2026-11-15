from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)

AZUL, NARANJA, GRIS = '#2a78d6', '#eb6834', '#888888'
plt.rcParams.update({
    'savefig.dpi': 150, 'font.size': 10, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
})

pd.set_option('display.width', 140)
df = pd.read_csv(RUTA_CSV)

variables = ['favoritedTimes', 'ratingScore', 'lengthSeconds', 'year', 'num_vocalistas']
pearson = df[variables].corr(method='pearson')
spearman = df[variables].corr(method='spearman')
print("-- CORRELACION DE PEARSON --")
print(pearson.round(3))
print("\n-- CORRELACION DE SPEARMAN --")
print(spearman.round(3))

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(spearman, cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(range(len(variables)), variables, rotation=45, ha='right')
ax.set_yticks(range(len(variables)), variables)
for i in range(len(variables)):
    for j in range(len(variables)):
        valor = spearman.iloc[i, j]
        ax.text(j, i, f'{valor:.2f}', ha='center', va='center',
                color='white' if abs(valor) > 0.6 else '#222222')
ax.grid(False)
fig.colorbar(im, ax=ax, shrink=0.8, label='Spearman')
ax.set_title('Matriz de correlación (Spearman)')
fig.tight_layout()
fig.savefig(CARPETA / '01_matriz_correlacion.png', bbox_inches='tight')
plt.close(fig)

modelo_simple = smf.ols('ratingScore ~ favoritedTimes', data=df).fit()
print("\n-- REGRESION SIMPLE: ratingScore ~ favoritedTimes --")
print(modelo_simple.summary().tables[1])
print(f"R^2 = {modelo_simple.rsquared:.4f}")

likes = (df['ratingScore'] - 3 * df['favoritedTimes']) / 2
cumple = ((likes >= 0) & (likes == likes.round())).mean() * 100
print(f"Canciones donde ratingScore = 3*favoritos + 2*likes (likes entero >= 0): {cumple:.1f} %")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df['favoritedTimes'], df['ratingScore'], s=12, alpha=0.4, color=AZUL, label='Canciones')
x = np.linspace(0, df['favoritedTimes'].max(), 100)
ax.plot(x, modelo_simple.params['Intercept'] + modelo_simple.params['favoritedTimes'] * x,
        color=NARANJA, linewidth=2,
        label=f"y = {modelo_simple.params['Intercept']:.2f} + "
              f"{modelo_simple.params['favoritedTimes']:.2f}x   (R² = {modelo_simple.rsquared:.3f})")
ax.set_xlabel('favoritedTimes')
ax.set_ylabel('ratingScore')
ax.set_title('Regresión lineal: ratingScore vs favoritedTimes')
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(CARPETA / '02_regresion_rating_favoritos.png', bbox_inches='tight')
plt.close(fig)

anual = (df.groupby('year')['tiene_favoritos'].mean() * 100).rename('pct_fav').reset_index()
tramo = anual[anual['year'] >= 2017]
modelo_tendencia = smf.ols('pct_fav ~ year', data=tramo).fit()
pendiente = modelo_tendencia.params['year']
print("\n-- TENDENCIA % CON FAVORITOS (2017-2025) --")
print(modelo_tendencia.summary().tables[1])
print(f"R^2 = {modelo_tendencia.rsquared:.4f} | cambio por año = {pendiente:.2f} puntos porcentuales")

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(anual['year'], anual['pct_fav'], color=GRIS, marker='o', markersize=5, linewidth=1.5,
        label='% observado')
ax.plot(tramo['year'], modelo_tendencia.fittedvalues, color=NARANJA, linewidth=2,
        label=f'Tendencia 2017-2025: {pendiente:.2f} pts/año (R² = {modelo_tendencia.rsquared:.2f})')
ax.set_xticks(anual['year'])
ax.tick_params(axis='x', rotation=45)
ax.set_ylabel('% de canciones con favoritos')
ax.set_title('Tendencia lineal después del pico de 2017')
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(CARPETA / '03_tendencia_favoritos.png', bbox_inches='tight')
plt.close(fig)

datos = df.dropna(subset=['lengthSeconds']).copy()
datos['log_rating'] = np.log1p(datos['ratingScore'])
datos['duracion_min'] = datos['lengthSeconds'] / 60
modelo_multiple = smf.ols(
    "log_rating ~ year + duracion_min + C(tipo_agrupado, Treatment('Original')) + num_vocalistas",
    data=datos).fit()
print("\n-- REGRESION MULTIPLE: log(1 + ratingScore) --")
print(modelo_multiple.summary().tables[1])
print(f"R^2 = {modelo_multiple.rsquared:.4f} | R^2 ajustado = {modelo_multiple.rsquared_adj:.4f}")
