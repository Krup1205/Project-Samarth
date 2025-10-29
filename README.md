# Project Samarth Prototype

Drop your data CSV files into the `data/` folder:
- `data/rainfall_data.csv` (year-wise rainfall; columns like YEAR, ANNUAL or monthly columns)
- `data/crop_production.csv` (year-wise crop production; first column Year and other crop columns)

Then run:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt

# load CSVs into SQLite
python load_to_db.py

# run demo
python app.py
```

Open http://127.0.0.1:5000 in your browser.
