from pathlib import Path
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_CSV = BASE_DIR / 'data' / 'processed' / 'vocadb_limpio.csv'
RUTA_TOTALES = BASE_DIR / 'data' / 'raw' / 'vocadb_totales_mensuales.csv'
CARPETA = Path(__file__).resolve().parent / 'graficas'
CARPETA.mkdir(exist_ok=True)

AZUL, NARANJA, AQUA, GRIS = '#2a78d6', '#eb6834', '#1baf7a', '#888888'
plt.rcParams.update({
    'savefig.dpi': 150, 'font.size': 10, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e6e6e6',
    'axes.axisbelow': True, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
})


def evaluar_modelos(train, test, estacional=None):
    h = len(test)
    preds = {
        'Ingenuo (último valor)': np.repeat(train.iloc[-1], h),
        'Promedio móvil (4)': np.repeat(train.iloc[-4:].mean(), h),
    }
    t = np.arange(len(train))
    coef = np.polyfit(t, train.values, 1)
    preds['Tendencia lineal'] = np.polyval(coef, np.arange(len(train), len(train) + h))
    preds['Holt amortiguado'] = ExponentialSmoothing(
        train, trend='add', damped_trend=True, seasonal=estacional,
        seasonal_periods=4 if estacional else None).fit().forecast(h).values
    preds['ARIMA(1,1,1)'] = ARIMA(train, order=(1, 1, 1)).fit().forecast(h).values
    return {nombre: pd.Series(p, index=test.index) for nombre, p in preds.items()}


def tabla_errores(preds, test):
    filas = []
    for nombre, p in preds.items():
        error = test - p
        filas.append({'modelo': nombre, 'MAE': np.abs(error).mean(),
                      'RMSE': np.sqrt((error ** 2).mean())})
    return pd.DataFrame(filas).sort_values('MAE').reset_index(drop=True)


def ajustar_final(serie, nombre, h):
    if nombre == 'ARIMA(1,1,1)':
        res = ARIMA(serie, order=(1, 1, 1)).fit().get_forecast(h)
        ic = res.conf_int(alpha=0.05)
        return res.predicted_mean, ic.iloc[:, 0], ic.iloc[:, 1]
    if nombre == 'Holt amortiguado':
        modelo = ExponentialSmoothing(serie, trend='add', damped_trend=True).fit()
        pred = modelo.forecast(h)
    elif nombre == 'Tendencia lineal':
        coef = np.polyfit(np.arange(len(serie)), serie.values, 1)
        pred = pd.Series(np.polyval(coef, np.arange(len(serie), len(serie) + h)))
    elif nombre == 'Promedio móvil (4)':
        pred = pd.Series(np.repeat(serie.iloc[-4:].mean(), h))
    else:
        pred = pd.Series(np.repeat(serie.iloc[-1], h))
    margen = 1.96 * serie.diff().dropna().std()
    return np.asarray(pred), np.asarray(pred) - margen, np.asarray(pred) + margen

df = pd.read_csv(RUTA_CSV, parse_dates=['publishDate'])
serie = (df.set_index('publishDate').resample('QS')['tiene_favoritos'].mean() * 100)
serie = serie['2008-01-01':]
serie.index.freq = 'QS'
print(f"Serie trimestral: {len(serie)} trimestres ({serie.index[0].date()} a {serie.index[-1].date()})")

train, test = serie[:'2023-12-31'], serie['2024-01-01':]
preds = evaluar_modelos(train, test)
errores = tabla_errores(preds, test)
print("\n-- PARTE A: ERRORES EN 2024-2025 (puntos porcentuales) --")
print(errores.round(2).to_string(index=False))
mejor = errores.loc[0, 'modelo']
print(f"Mejor modelo: {mejor}")

H = 8
fechas_futuras = pd.date_range(serie.index[-1] + pd.offsets.QuarterBegin(startingMonth=1), periods=H, freq='QS')
pred, inf, sup = ajustar_final(serie, mejor, H)
pronostico_a = pd.DataFrame({'trimestre': fechas_futuras.date, 'pronostico_pct': np.round(pred, 2),
                             'limite_inferior': np.round(np.clip(inf, 0, 100), 2),
                             'limite_superior': np.round(np.clip(sup, 0, 100), 2)})
print("\nPronostico 2026-2027:")
print(pronostico_a.to_string(index=False))
pronostico_a.to_csv(Path(__file__).resolve().parent / 'pronostico_pct_favoritos.csv', index=False)

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(serie['2019-01-01':].index, serie['2019-01-01':].values, color=GRIS, marker='o',
        markersize=4, linewidth=1.5, label='Observado')
colores = [AZUL, NARANJA, AQUA, '#eda100', '#6250d6']
for (nombre, p), color in zip(preds.items(), colores):
    ax.plot(p.index, p.values, color=color, linewidth=2, label=nombre,
            linestyle='--' if 'ARIMA' in nombre else '-')
ax.axvline(test.index[0], color='#555555', linestyle='--', linewidth=1)
ax.text(test.index[0], ax.get_ylim()[1] * 0.97, '  prueba', va='top')
ax.set_ylabel('% con favoritos')
ax.set_title('Comparación de modelos en el periodo de prueba (2024-2025)')
ax.legend(frameon=False, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.1))
fig.tight_layout()
fig.savefig(CARPETA / '01_comparacion_modelos.png', bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(serie.index, serie.values, color=AZUL, linewidth=1.5, label='Observado (trimestral)')
ax.plot(serie.index, serie.rolling(4).mean(), color=GRIS, linewidth=1.5, linestyle='--',
        label='Promedio móvil 4 trimestres')
ax.plot(fechas_futuras, pred, color=NARANJA, linewidth=2, marker='o', markersize=4,
        label=f'Pronóstico ({mejor})')
ax.fill_between(fechas_futuras, np.clip(inf, 0, 100), np.clip(sup, 0, 100), color=NARANJA,
                alpha=0.15, label='Intervalo 95 %')
ax.set_ylabel('% con favoritos')
ax.set_title('% de canciones con favoritos: histórico y pronóstico 2026-2027')
ax.legend(frameon=False, ncol=2, loc='upper left')
fig.tight_layout()
fig.savefig(CARPETA / '02_pronostico_pct_favoritos.png', bbox_inches='tight')
plt.close(fig)

if not RUTA_TOTALES.exists():
    print(f"\n[Parte B omitida] No existe {RUTA_TOTALES.name}. Corre primero:"
          f"\n  python \"Practica 8/extraer_totales.py\"")
else:
    mensual = pd.read_csv(RUTA_TOTALES, parse_dates=['mes']).set_index('mes')['total_canciones']
    anual = mensual.resample('YS').sum()
    anual.index.freq = 'YS'
    print("\n-- PARTE B: CANCIONES PUBLICADAS POR AÑO (VocaDB) --")
    print(anual.rename(lambda d: d.year).to_string())
    pico_b = anual.idxmax().year
    print(f"Año con mas canciones: {pico_b}")

    train_b, test_b = anual[:'2022-12-31'], anual['2023-01-01':]
    preds_b = evaluar_modelos(train_b, test_b)
    errores_b = tabla_errores(preds_b, test_b)
    print("\nErrores en 2023-2025 (canciones):")
    print(errores_b.round(0).to_string(index=False))
    mejor_b = errores_b.loc[0, 'modelo']
    print(f"Mejor modelo: {mejor_b}")

    H_B = 3
    fechas_b = pd.date_range(anual.index[-1] + pd.DateOffset(years=1), periods=H_B, freq='YS')
    pred_b, inf_b, sup_b = ajustar_final(anual, mejor_b, H_B)
    pronostico_b = pd.DataFrame({'anio': fechas_b.year, 'pronostico': np.round(pred_b),
                                 'limite_inferior': np.round(np.clip(inf_b, 0, None)),
                                 'limite_superior': np.round(sup_b)})
    print("\nPronostico 2026-2028:")
    print(pronostico_b.to_string(index=False))
    pronostico_b.to_csv(Path(__file__).resolve().parent / 'pronostico_total_canciones.csv', index=False)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(anual.index.year, anual.values, color=AZUL, width=0.7, label='Canciones publicadas')
    ax.plot(fechas_b.year, pred_b, color=NARANJA, marker='o', linewidth=2,
            label=f'Pronóstico ({mejor_b})')
    ax.fill_between(fechas_b.year, np.clip(inf_b, 0, None), sup_b, color=NARANJA, alpha=0.15,
                    label='Intervalo 95 %')
    ax.set_xticks(list(anual.index.year) + list(fechas_b.year))
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel('Canciones publicadas')
    ax.set_title('Canciones Vocaloid publicadas por año en VocaDB y pronóstico')
    ax.legend(frameon=False, loc='upper left')
    ax.grid(axis='x', visible=False)
    fig.tight_layout()
    fig.savefig(CARPETA / '03_pronostico_total_canciones.png', bbox_inches='tight')
    plt.close(fig)
