from flask import Flask, render_template, request  # Импортируем необходимые модули из Flask
from search_engine import SearchEngineCSV  # Импортируем класс SearchEngineCSV из файла search_engine

# Создаем экземпляр Flask-приложения
app = Flask(__name__)

# Путь к CSV-файлу, содержащему данные корпуса
csv_file = 'corpus_data_with_labels.csv'
# Инициализируем поисковый движок с указанием пути к CSV-файлу
search_engine = SearchEngineCSV(csv_file)


@app.route('/')  # Определяем маршрут для главной страницы
def home():
    # Отправляем шаблон head.html для отображения главной страницы
    return render_template('head.html')


@app.route('/search', methods=['GET', 'POST'])  # Определяем маршрут для страницы поиска
def search():
    query = None  # Переменная для хранения поискового запроса
    results = []  # Список для хранения результатов поиска
    if request.method == 'POST':  # Если метод запроса POST (при отправке формы)
        query = request.form['query']  # Получаем значение поискового запроса из формы
        results = search_engine.search(query)  # Выполняем поиск по запросу с помощью поискового движка

    # Отправляем шаблон search.html с запросом и результатами
    return render_template('search.html', query=query, results=results)


# Проверяем, является ли этот файл основным модулем, и запускаем приложение
if __name__ == "__main__":
    app.run(debug=True, port=50000)  # Запускаем приложение с отладкой на порту 50000
