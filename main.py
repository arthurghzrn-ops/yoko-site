import csv
import requests
from flask import Flask, render_template

app = Flask(__name__)

# ID твоей Google Таблицы
SPREADSHEET_ID = '1dXqUhakKxRJMn8m-x1WA_9MSdMYu-585C6VZ9Aa9Z_w'
# Ссылка для скачивания первого листа в формате CSV
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=0'

def get_menu_from_sheets():
    menu = []
    try:
        # Делаем запрос к Google Таблице
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # Читаем полученные строки как CSV
            lines = response.text.splitlines()
            reader = csv.DictReader(lines)
            
            for row in reader:
                # Проверяем, чтобы название блюда не было пустым
                if row.get('Название'):
                    menu.append({
                        "name": row.get('Название'),
                        "price": row.get('Цена', ''),
                        "desc": row.get('Описание', '')
                    })
        else:
            print(f"Ошибка получения данных: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при чтении таблицы: {e}")
    
    # Если таблица пустая или произошла ошибка, покажем заглушку, чтобы сайт не падал
    if not menu:
        menu = [
            {"name": "Загрузка меню...", "price": "", "desc": "Пожалуйста, добавьте позиции в Google Таблицу."}
        ]
    return menu

@app.route('/')
def home():
    title = "YOKO | Asian Loft & Kitchen"
    slogan = "Два мира. Одно меню. Идеальный вкус."
    
    # Получаем актуальное меню из Google Таблицы прямо при заходе гостя
    menu_data = get_menu_from_sheets()
    
    return render_template('index.html', title=title, slogan=slogan, menu=menu_data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
