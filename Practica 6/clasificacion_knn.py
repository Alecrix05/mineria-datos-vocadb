from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (ConfusionMatrixDisplay, balanced_accuracy_score,
                             classification_report, confusion_matrix)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)
SEMILLA = 42

AZUL, NARANJA = '#2a78d6', '#eb6834'
plt.rcParams.update({
    'savefig.dpi': 150, 'font.size': 10, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
})

df = pd.read_csv(RUTA_CSV)
df = df[df['songType'].isin(['Original', 'Cover'])].dropna(subset=['lengthSeconds']).copy()

df['duracion_min'] = df['lengthSeconds'] / 60
df['log_favoritos'] = np.log1p(df['favoritedTimes'])
df['log_likes'] = np.log1p(((df['ratingScore'] - 3 * df['favoritedTimes']) / 2).clip(lower=0))
df['es_miku'] = (df['vocalista'] == 'Hatsune Miku').astype(int)

caracteristicas = ['duracion_min', 'year', 'log_favoritos', 'log_likes', 'num_vocalistas', 'es_miku']
X = df[caracteristicas]
y = df['songType']
print(f"Canciones: {len(df)}")
print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=SEMILLA)

pipeline = Pipeline([('escalar', StandardScaler()), ('knn', KNeighborsClassifier())])
parametros = {'knn__n_neighbors': list(range(1, 42, 2)), 'knn__weights': ['uniform', 'distance']}
busqueda = GridSearchCV(pipeline, parametros, scoring='balanced_accuracy',
                        cv=StratifiedKFold(5, shuffle=True, random_state=SEMILLA))
busqueda.fit(X_train, y_train)
mejor_k = busqueda.best_params_['knn__n_neighbors']
print(f"\nMejores parametros: {busqueda.best_params_}")
print(f"Exactitud balanceada (validacion cruzada): {busqueda.best_score_:.3f}")

resultados = pd.DataFrame(busqueda.cv_results_)
fig, ax = plt.subplots(figsize=(9, 4.5))
for peso, color, etiqueta in [('uniform', AZUL, 'Pesos uniformes'), ('distance', NARANJA, 'Pesos por distancia')]:
    sub = resultados[resultados['param_knn__weights'] == peso]
    ax.plot(sub['param_knn__n_neighbors'], sub['mean_test_score'], marker='o', markersize=5,
            linewidth=2, color=color, label=etiqueta)
ax.axvline(mejor_k, color='#555555', linestyle='--', linewidth=1)
ax.set_xlabel('k (número de vecinos)')
ax.set_ylabel('Exactitud balanceada (CV)')
ax.set_title('Selección de k con validación cruzada')
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(CARPETA / '01_seleccion_k.png', bbox_inches='tight')
plt.close(fig)

modelo = busqueda.best_estimator_
y_pred = modelo.predict(X_test)
print("\n-- REPORTE EN CONJUNTO DE PRUEBA --")
print(classification_report(y_test, y_pred, digits=3))
print(f"Exactitud balanceada (prueba): {balanced_accuracy_score(y_test, y_pred):.3f}")

base = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
print(f"Linea base (siempre 'Original'): exactitud = {base.score(X_test, y_test):.3f}, "
      f"exactitud balanceada = {balanced_accuracy_score(y_test, base.predict(X_test)):.3f}")

matriz = confusion_matrix(y_test, y_pred, labels=['Original', 'Cover'])
fig, ax = plt.subplots(figsize=(5, 4.5))
ConfusionMatrixDisplay(matriz, display_labels=['Original', 'Cover']).plot(
    ax=ax, cmap='Blues', colorbar=False, values_format='d')
ax.grid(False)
ax.set_xlabel('Predicción')
ax.set_ylabel('Valor real')
ax.set_title(f'Matriz de confusión (k = {mejor_k})')
fig.tight_layout()
fig.savefig(CARPETA / '02_matriz_confusion.png', bbox_inches='tight')
plt.close(fig)

nueva = pd.DataFrame([{'duracion_min': 4.0, 'year': 2024, 'log_favoritos': 0,
                       'log_likes': 0, 'num_vocalistas': 1, 'es_miku': 1}])
print(f"\nEjemplo (4 min, 2024, sin favoritos, Miku): {modelo.predict(nueva)[0]}")
