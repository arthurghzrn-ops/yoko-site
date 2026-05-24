from flask import Flask, render_template
import requests
import csv
from io import StringIO

app = Flask(__name__)

# Ссылка на экспорт твоей Google Таблицы в формате CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1dXqUhakKxRJMn8m-x1WA_9MSdMYu-585C6VZ9Aa9Z_w/export?format=csv&gid=0"

def get_menu_from_sheet():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return {}
        
        f = StringIO(response.text)
        reader = csv.reader(f)
        
        # Пропускаем шапку таблицы (Категория, Название, Описание, Цена)
        next(reader, None)
        
        menu_by_categories = {}
        
        for row in reader:
            # Проверяем, что в строке есть хотя бы категория и название
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                category = row[0].strip()
                name = row[1].strip()
                desc = row[2].strip() if len(row) > 2 else ""
                
                # Проверяем цену, если её нет или забыли указать — ставим 0
                price = row[3].strip() if len(row) > 3 else "0"
                if price and not price.endswith("֏") and price != "0":
                    price = f"{price} ֏"
                
                item = {"name": name, "desc": desc, "price": price}
                
                if category not in menu_by_categories:
                    menu_by_categories[category] = []
                menu_by_categories[category].append(item)
                
        return menu_by_categories
    except Exception as e:
        print(f"Ошибка при чтении таблицы: {e}")
        return {}

@app.route('/')
def home():
    title = "YOKO | Asian Loft & Kitchen"
    slogan = "Два мира. Одно меню. Идеальный вкус."
    
    menu_data = get_menu_from_sheet()
    
    return render_template('index.html', title=title, slogan=slogan, menu=menu_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
