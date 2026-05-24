from flask import Flask, render_template
import requests
import csv
from io import StringIO

app = Flask(__name__, static_folder='static')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1dXqUhakKxRJMn8m-x1WA_9MSdMYu-585C6VZ9Aa9Z_w/export?format=csv&sheet=Лист1"

def get_menu_from_sheet():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200: return {}
        
        f = StringIO(response.text)
        reader = csv.reader(f)
        next(reader, None)
        
        menu_by_categories = {}
        for row in reader:
            if not row or len(row) < 2: continue
            category, name = row[0].strip(), row[1].strip()
            if not category or not name: continue
            desc = row[2].strip() if len(row) > 2 else ""
            price = row[3].strip() if len(row) > 3 and row[3].strip() else "—"
            if price != "—" and not price.endswith("֏"): price = f"{price} ֏"
            
            if category not in menu_by_categories: menu_by_categories[category] = []
            menu_by_categories[category].append({"name": name, "desc": desc, "price": price})
        return menu_by_categories
    except: return {}

@app.route('/')
def home():
    return render_template('index.html', menu=get_menu_from_sheet())

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
