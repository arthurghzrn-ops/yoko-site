from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    title = "YOKO | Asian Loft & Kitchen"
    slogan = "Два мира. Одно меню. Идеальный вкус."
    
    # Меню ресторана
    menu_data = [
        {"name": "Ролл с тунцом", "price": "3,200 ֏", "desc": "Свежий тунец, сливочный сыр, авокадо, рис, нори."},
        {"name": "Стейк Рибай", "price": "7,500 ֏", "desc": "Сочный стейк из говядины с европейской классикой подачи."}
    ]
    
    return render_template('index.html', title=title, slogan=slogan, menu=menu_data)

if __name__ == '__main__':
    # На Render сервер запускается через импорт, но этот блок нужен для тестов
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
