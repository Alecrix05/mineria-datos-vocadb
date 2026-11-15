from itertools import combinations
from pathlib import Path
import pandas as pd
from scipy import stats

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
RUTA_SALIDA = Path(__file__).resolve().parent / 'resultados_pruebas.csv'
ALPHA = 0.05

df = pd.read_csv(RUTA_CSV)
resultados = []


def registrar(prueba, hipotesis_nula, estadistico, p):
    decision = 'Se rechaza H0' if p < ALPHA else 'No se rechaza H0'
    resultados.append({'prueba': prueba, 'H0': hipotesis_nula,
                       'estadistico': round(estadistico, 4), 'p_valor': p, 'decision': decision})
    print(f"\n[{prueba}]\n  H0: {hipotesis_nula}\n  estadistico = {estadistico:.4f}, p = {p:.3e} -> {decision}")

tipos = ['Original', 'Cover', 'Remix', 'Otro']
grupos_duracion = [df.loc[df['tipo_agrupado'] == t, 'lengthSeconds'].dropna() for t in tipos]

est, p = stats.normaltest(df['lengthSeconds'].dropna())
registrar('Normalidad (D\'Agostino) - duracion', 'La duracion sigue una distribucion normal', est, p)

est, p = stats.levene(*grupos_duracion)
registrar('Levene - duracion por tipo', 'Las varianzas de duracion son iguales entre tipos', est, p)

est, p = stats.f_oneway(*grupos_duracion)
registrar('ANOVA - duracion por tipo', 'La duracion media es igual en todos los tipos', est, p)

est, p = stats.kruskal(*grupos_duracion)
registrar('Kruskal-Wallis - duracion por tipo', 'La distribucion de duracion es igual en todos los tipos', est, p)

print("\n[Post-hoc Mann-Whitney con Bonferroni]")
pares = list(combinations(tipos, 2))
for a, b in pares:
    x = df.loc[df['tipo_agrupado'] == a, 'lengthSeconds'].dropna()
    y = df.loc[df['tipo_agrupado'] == b, 'lengthSeconds'].dropna()
    est, p = stats.mannwhitneyu(x, y)
    p_ajustado = min(p * len(pares), 1.0)
    marca = 'diferentes' if p_ajustado < ALPHA else 'sin diferencia'
    print(f"  {a:8s} vs {b:8s}: medianas {x.median():.0f} s vs {y.median():.0f} s, "
          f"p ajustado = {p_ajustado:.3e} -> {marca}")
    resultados.append({'prueba': f'Mann-Whitney {a} vs {b} (Bonferroni)',
                       'H0': f'Duracion igual entre {a} y {b}', 'estadistico': round(est, 4),
                       'p_valor': p_ajustado,
                       'decision': 'Se rechaza H0' if p_ajustado < ALPHA else 'No se rechaza H0'})

tabla = pd.crosstab(df['tipo_agrupado'], df['etapa'])
est, p, gl, _ = stats.chi2_contingency(tabla)
print("\nTabla tipo x etapa:\n", tabla)
registrar('Chi-cuadrada - tipo vs etapa', 'El tipo de cancion es independiente de la etapa', est, p)

tabla = pd.crosstab(df['tiene_favoritos'], df['etapa'])
est, p, gl, _ = stats.chi2_contingency(tabla)
print("\n% con favoritos por etapa:\n", (df.groupby('etapa')['tiene_favoritos'].mean() * 100).round(1))
registrar('Chi-cuadrada - favoritos vs etapa', 'Tener favoritos es independiente de la etapa', est, p)

grupos_rating = [g['ratingScore'] for _, g in df.groupby('etapa')]
est, p = stats.kruskal(*grupos_rating)
registrar('Kruskal-Wallis - ratingScore por etapa', 'El ratingScore se distribuye igual en las 3 etapas', est, p)

pd.DataFrame(resultados).to_csv(RUTA_SALIDA, index=False, encoding='utf-8-sig')
print(f"\nResultados guardados en {RUTA_SALIDA}")
