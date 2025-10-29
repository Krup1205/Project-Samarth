import sqlite3
import pandas as pd
from tabulate import tabulate
from fuzzywuzzy import process
import re

DB = 'db.sqlite3'

def sql_query(q):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(q, conn)
    conn.close()
    return df

def get_crop_columns():
    """Return all column names from crop_production and crop-like ones only."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(crop_production);")
    cols = [r[1] for r in cur.fetchall()]
    conn.close()
    # exclude non-crop columns
    candidates = [c for c in cols if c.lower() not in ('year', 'region', 'index')]
    return cols, candidates

def find_column_for_crop(crop_name, candidates):
    """Match crop name to DB column (exact, substring, or fuzzy)."""
    crop = crop_name.lower()
    for c in candidates:
        if crop in c.lower():
            return c
    if candidates:
        match, score = process.extractOne(crop, candidates)
        if score >= 70:
            return match
    return None

def answer_question(text):
    text_lower = (text or '').lower().strip()
    if not text_lower:
        return {'text': 'Please ask a question.', 'sources': []}

    # --- 🔹 CASE 1: Average rainfall ---
    if 'average annual rainfall' in text_lower or 'average rainfall' in text_lower:
        try:
            n = 5
            m = re.search(r'(?:last\s*)(\d+)\s*years?', text_lower)
            if m:
                n = int(m.group(1))
            q = f"SELECT year, annual as annual_rainfall FROM climate_timeseries ORDER BY year DESC LIMIT {n}"
            df = sql_query(q)
            if df.empty:
                q = f"SELECT year, annual_rainfall FROM climate_timeseries ORDER BY year DESC LIMIT {n}"
                df = sql_query(q)
                if df.empty:
                    return {'text': 'No rainfall data found in DB.', 'sources': []}
            avg = df.iloc[:, 1].mean()
            txt = f"☔ Average annual rainfall for the last {n} years: {avg:.2f} mm\n\nRecent Data:\n" + tabulate(df, headers='keys', tablefmt='pretty', showindex=False)
            return {'text': txt, 'table': df.to_dict(orient='records'), 'sources': ['climate_timeseries']}
        except Exception as e:
            return {'text': f'Error computing rainfall: {e}', 'sources': []}

    # --- 🔹 CASE 2: Compare production of crops (dynamic) ---
    if 'compare' in text_lower and 'and' in text_lower:
        try:
            # Extract crop names dynamically
            crops = re.findall(r'compare(?: production of)?\s*(.*?)\s*and\s*(.*)', text_lower)
            if not crops:
                return {'text': 'Please use format like: Compare Rice and Wheat', 'sources': []}
            crop1, crop2 = [c.strip() for c in crops[0]]

            _, candidates = get_crop_columns()
            col1 = find_column_for_crop(crop1, candidates)
            col2 = find_column_for_crop(crop2, candidates)

            if not col1 or not col2:
                return {'text': f'Could not find crop columns for {crop1} or {crop2}. Available crops: {", ".join(candidates)}', 'sources': []}

            q = f"SELECT year, `{col1}` AS `{crop1}`, `{col2}` AS `{crop2}` FROM crop_production ORDER BY year DESC LIMIT 10"
            df = sql_query(q)

            avg1 = df[crop1].mean()
            avg2 = df[crop2].mean()
            txt = f"🌾 Comparison of {crop1.title()} and {crop2.title()}:\nAverage {crop1.title()}: {avg1:.2f}\nAverage {crop2.title()}: {avg2:.2f}\n\nRecent Data:\n" + tabulate(df, headers='keys', tablefmt='pretty', showindex=False)
            return {'text': txt, 'table': df.to_dict(orient='records'), 'sources': ['crop_production']}
        except Exception as e:
            return {'text': f'Error comparing crops: {e}', 'sources': []}

    # --- 🔹 CASE 3: Trend of a crop ---
    if 'trend' in text_lower or 'show' in text_lower:
        try:
            crop_match = re.search(r'(?:trend of|show trend of|show)\s*(.*)', text_lower)
            if not crop_match:
                return {'text': 'Please specify a crop name (e.g., Show trend of Tea).', 'sources': []}
            crop = crop_match.group(1).strip()

            _, candidates = get_crop_columns()
            col = find_column_for_crop(crop, candidates)
            if not col:
                return {'text': f'Could not match crop "{crop}" to any column. Available: {", ".join(candidates)}', 'sources': []}

            q = f"SELECT year, `{col}` AS production FROM crop_production ORDER BY year ASC"
            df = sql_query(q)
            if df.empty:
                return {'text': f'No data found for crop {crop}.', 'sources': []}

            txt = f"📈 Production trend for {crop.title()}:\n" + tabulate(df.tail(10), headers='keys', tablefmt='pretty', showindex=False)
            return {'text': txt, 'table': df.to_dict(orient='records'), 'sources': ['crop_production']}
        except Exception as e:
            return {'text': f'Error fetching trend: {e}', 'sources': []}

    # --- 🔹 CASE 4: General fallback ---
    return {
        'text': (
            'Question not supported.\n\n'
            'Try examples like:\n'
            '- Compare Rice and Wheat\n'
            '- Show trend of Tea\n'
            '- Average annual rainfall for last 5 years'
        ),
        'sources': []
    }