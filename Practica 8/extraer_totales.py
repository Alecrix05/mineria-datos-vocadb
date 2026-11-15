from pathlib import Path
import calendar
import time
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_SALIDA = BASE_DIR / 'data' / 'raw' / 'vocadb_totales_mensuales.csv'
BASE_URL = 'https://vocadb.net/api/songs'
START_YEAR, END_YEAR = 2007, 2025

filas = []
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        ultimo_dia = calendar.monthrange(year, month)[1]
        params = {
            'afterDate': f'{year}-{month:02d}-01T00:00:00Z',
            'beforeDate': f'{year}-{month:02d}-{ultimo_dia}T23:59:59Z',
            'getTotalCount': 'true',
            'maxResults': 1,
        }
        for intento in range(3):
            try:
                resp = requests.get(BASE_URL, params=params, timeout=30)
                resp.raise_for_status()
                total = resp.json().get('totalCount', 0)
                break
            except requests.RequestException as error:
                print(f"  Reintentando {year}-{month:02d} ({error})")
                time.sleep(2)
        else:
            raise SystemExit(f"No se pudo obtener {year}-{month:02d}")
        filas.append({'mes': f'{year}-{month:02d}-01', 'total_canciones': total})
        time.sleep(0.2)
    print(f"Año {year}: {sum(f['total_canciones'] for f in filas[-12:]):,} canciones")

RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(filas).to_csv(RUTA_SALIDA, index=False)
print(f"\nGuardado en {RUTA_SALIDA}")
