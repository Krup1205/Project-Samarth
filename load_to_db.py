import pandas as pd
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

os.makedirs(DATA_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

def normalize_columns(df):
    # make column names simple: lowercase, underscores, remove special chars
    cols = df.columns
    new = []
    for c in cols:
        nc = str(c).strip()
        nc = nc.replace('\n',' ').replace('\r',' ')
        nc = nc.replace(' ', '_').lower()
        nc = nc.replace('(', '').replace(')', '').replace('.', '').replace('-', '_').replace('/', '_').replace('&','_at_').replace('@','_')
        # collapse repeated underscores
        while '__' in nc:
            nc = nc.replace('__','_')
        new.append(nc)
    df.columns = new
    return df

def load_csv(file_name, table_name):
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        print(f'[WARN] File not found: {path}')
        return False
    print(f'[INFO] Loading {path} into table {table_name} ...')
    # try Excel fallback
    try:
        if path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
    except Exception as e:
        print(f'[ERROR] Failed to read {path}: {e}')
        return False

    df = normalize_columns(df)

    # if climate table has monthly columns, try to compute annual if missing
    if table_name == 'climate_timeseries':
        # common names: year, annual, annual_rainfall, etc.
        if 'year' not in df.columns:
            # try find any column with year in name
            poss = [c for c in df.columns if 'year' in c]
            if poss:
                df.rename(columns={poss[0]:'year'}, inplace=True)
        if 'annual' not in df.columns and 'annual_rainfall' not in df.columns:
            months = [m for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'] if m in df.columns]
            if months:
                df['annual'] = df[months].sum(axis=1)

    # write to sqlite
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f'[OK] Wrote {len(df)} rows to {table_name}')
        return True
    except Exception as e:
        print(f'[ERROR] writing to {table_name}: {e}')
        return False

if __name__ == '__main__':
    t0 = datetime.utcnow().isoformat()
    results = {}
    results['rainfall'] = load_csv('rainfall_data.csv', 'climate_timeseries')
    results['crop'] = load_csv('crop_production.csv', 'crop_production')
    conn.close()
    print('\nSummary:')
    for k,v in results.items():
        print(k, 'loaded' if v else 'missing/failed')
