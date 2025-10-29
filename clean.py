# helper to inspect and rename columns interactively (simple script)
import pandas as pd, os, sqlite3

DATA_DIR = 'data'
path = os.path.join(DATA_DIR, 'crop_production.csv')
if not os.path.exists(path):
    print('No crop_production.csv found in data/. Put your file there first.')
    raise SystemExit(1)

df = pd.read_csv(path)
print('Current columns:')
for i,c in enumerate(df.columns):
    print(i, '->', repr(c))

print('\nExample rename mapping:')
print("{'Food grains (cereals) - Rice':'rice', 'Food grains (cereals) - Wheat':'wheat'}")

# Do a simple automated rename for common patterns
new_cols = []
for c in df.columns:
    nc = str(c).strip().lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
    new_cols.append(nc)
df.columns = new_cols
out = os.path.join(DATA_DIR,'crop_production_normalized.csv')
df.to_csv(out, index=False)
print('Wrote normalized example to', out)
