from flask import Flask, render_template
import requests
import csv
from io import StringIO

app = Flask(__name__)

# Железобетонная ссылка: запрашиваем у Google Таблицы именно "Лист1" в формате CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1dXqUhakKxRJMn8m-x1WA_9MSdMYu-585C6VZ9Aa9Z_w/gviz/tq?tqx=out:csv&sheet=Лист1"

def get_menu_from_sheet():
    try:
        # Делаем запрос к таблице
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(nt(f"Ошибка доступа к Google Таблице: статус {response.status_code}"))
            return {}
        
        f = StringIO(response.text)
        reader = csv.reader(f)
        
        # Пропускаем самую первую строчку с заголовками (Категория, Название, Описание, Цена)
        next(reader, None)
        
        menu_by_categories = {}
        
        for row in reader:
            # Защита: если строка пустая или в ней меньше 2-х заполненных колонок — пропускаем её
            if not row or len(row) < 2:
                continue
                
            category = row[0].strip()
            name = row[1].strip()
            
            # Если критически важные поля (категория или название) пустые — идём дальше
            if not category or not name:
                continue
                
            # Беру описание из столбца C (если оно есть)
            desc = row[2].strip() if len(row) > 2 else ""
            
            # Беру цену из столбца D
            price_val = row[3].strip() if len(row) > 3 else ""
            
            # Форматируем красивый вывод цены со знаком драма ֏
            if price_val:
                # Если вдруг в таблице уже написан знак драмы, не дублируем его
                if not price_val.endswith("֏"):
                    price = f"{price_val} ֏"
                else:
                    price = price_val
            else:
                price = "—" # Если цену для блюда забыли указать в таблице
                
            item = {"name": name, "desc": desc, "price": price}
            
            # Сортируем блюда по их категориям
            if category not in menu_by_categories:
                menu_by_categories[category] = []
            menu_by_categories[category].append(item)
                
        return menu_by_categories
        
    except Exception as e:
        print(f"Системная ошибка при чтении таблицы: {e}")
        return {}

@app.route('/')
def home():
    title = "YOKO | Asian Loft & Kitchen"
    slogan = "Два мира. Одно меню. Идеальный вкус."
    
    # Получаем свежие данные из таблицы при каждом обновлении страницы
    menu_data = get_menu_from_sheet()
    
    return render_template('index.html', title=title, slogan=slogan, menu=menu_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
