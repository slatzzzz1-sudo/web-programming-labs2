from flask import Blueprint, url_for, request, redirect, Response, abort, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'



flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
access_log = []

# Сначала маршрут С параметром
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.lab2end(name)
    return f'''<!doctype html>
    <html>
        <head>
            <title>Цветок добавлен</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {", ".join(flower_list)}</p>
            <p><a href="/lab2/all_flowers/">Посмотреть все цветы</a></p>
        </body>
    </html>'''

# Потом маршрут БЕЗ параметра (должен быть вторым!)
@lab2.route('/lab2/add_flower')
@lab2.route('/lab2/add_flower/')
def no_flower():
    return '''<!doctype html>
    <html>
        <head>
            <title>Ошибка</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>400 Bad Request</h1>
            <p>Вы не задали имя цветка.</p>
            <p><a href="/lab2/all_flowers/">Посмотреть все цветы</a></p>
        </body>
    </html>''', 400

# Остальные ваши маршруты...
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    else:
        flower_name = flower_list[flower_id]
        return f"""<!doctype html>
        <html>
            <head>
                <title>Цветок {flower_id}</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>Цветок: {flower_name}</h1>
                <p>ID цветка: {flower_id}</p>
                <p>
                    <a href="/lab2/all_flowers/">Посмотреть все цветы</a>
                </p>
            </body>
        </html>
        """

@lab2.route('/lab2/all_flowers/')
def all_flowers():
    return f'''<!doctype html>
    <html>
        <head>
            <title>Все цветы</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Информация о цветах</h1>
            <h2>Список всех цветов:</h2>
            <ul>
                {"".join([f'<li>{flower} (ID: {idx})</li>' for idx, flower in enumerate(flower_list)])}
            </ul>
            <p><strong>Общее количество:</strong> {len(flower_list)}</p>
            <p><a href="/lab2/clear_flowers/">Очистить список</a></p>
        </body>
    </html>'''

@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return '''<!doctype html>
    <html>
        <head>
            <title>Список очищен</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Список цветов очищен</h1>
            <p>Все цветы были удалены из списка.</p>
            <p><a href="/lab2/all_flowers/">Вернуться к списку цветов</a></p>
        </body>
    </html>'''


@lab2.route('/lab2/example')
def example():
    name = 'Самойлов Дмитрий'
    lab_number = 2
    group = 'ФБИ-32'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
        ]
    return render_template('example.html', name=name, 
                            lab_number=lab_number, group=group, 
                            course=course, fruits=fruits)
@lab2.route('/lab2/')
def lab2_menu():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:num1>/<int:num2>')
def calc(num1, num2):
    return f'''<h1>Расчёт с параметрами:</h1>
    <p>{num1} + {num2} = {num1 + num2}<br>
    {num1} - {num2} = {num1 + num2}<br>
    {num1} x {num2} = {num1 * num2}<br>
    {num1}/{num2} = {num1/num2}<br>
    {num1}<sup>{num2}</sup> = {num1**num2}</p>'''

@lab2.route('/lab2/calc/')
def calc1():
    return redirect(url_for('calc', num1=1, num2=1))

@lab2.route('/lab2/calc/<int:num1>')
def calc_with_one(num1):
    return redirect(url_for('calc', num1=num1, num2=1))

@lab2.route('/lab2/books/')
def books():
    books_data = [
    {"author": "Айн Рэнд", "title": "Атлант расправил плечи", "genre": "Философский роман", "pages": 1168},
    {"author": "Стивен Кинг", "title": "Оно", "genre": "Ужасы", "pages": 1245},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 574},
    {"author": "Джек Лондон", "title": "Белый Клык", "genre": "Приключения", "pages": 284},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Айзек Азимов", "title": "Я, робот", "genre": "Научная фантастика", "pages": 320},
    {"author": "Джон Р.Р. Толкин", "title": "Властелин Колец", "genre": "Фэнтези", "pages": 1137},
    {"author": "Жюль Верн", "title": "Двадцать тысяч лье под водой", "genre": "Приключения", "pages": 432},
    {"author": "Агата Кристи", "title": "Убийство в Восточном экспрессе", "genre": "Детектив", "pages": 316},
    {"author": "Пауло Коэльо", "title": "Алхимик", "genre": "Роман", "pages": 256},
    {"author": "Клайв С. Льюис", "title": "Хроники Нарнии", "genre": "Фэнтези", "pages": 768}
]
    return render_template('books.html', books=books_data)


@lab2.route('/lab2/gallery/')
def gallery():
    dogs = [
        {"name": "Шарик", "slug": "dog", "desc": "Профессиональный искатель мячиков."},
        {"name": "Барбос", "slug": "dog2", "desc": "Эксперт по охране дивана."},
        {"name": "Рекс", "slug": "dog3", "desc": "Специалист по раскапыванию клумб."},
        {"name": "Дружок", "slug": "dog4", "desc": "Мастер побегов на прогулке."},
        {"name": "Тузик", "slug": "dog5", "desc": "Критик собачьих лакомств."},
        {"name": "Лорд", "slug": "dog6", "desc": "Ночной дегустатор корма."},
        {"name": "Бобик", "slug": "dog7", "desc": "Гуру виляния хвостом."},
        {"name": "Гром", "slug": "dog8", "desc": "Разрушитель тапочек."},
        {"name": "Жучка", "slug": "dog9", "desc": "Охотник за мячами."},
        {"name": "Альма", "slug": "dog10", "desc": "Знаток кошачьего пения."},
        {"name": "Зевс", "slug": "dog11", "desc": "Сомелье собачьих кормов."},
        {"name": "Блэк", "slug": "dog12", "desc": "Маскировщик под ночь."},
        {"name": "Пират", "slug": "dog13", "desc": "Любитель свернуться калачиком."},
        {"name": "Цезарь", "slug": "dog14", "desc": "Повелитель лежанок."},
        {"name": "Солнышко", "slug": "dog15", "desc": "Искатель теплых мест у батареи."},
        {"name": "Боня", "slug": "dog16", "desc": "Профессиональный будильник в 6 утра."},
        {"name": "Марс", "slug": "dog17", "desc": "Исследователь сумок хозяев."},
        {"name": "Луна", "slug": "dog18", "desc": "Лунный зайчик в образе собаки."},
        {"name": "Фил", "slug": "dog19", "desc": "Консультант по утренним пробежкам."},
        {"name": "Молния", "slug": "dog20", "desc": "Мастер внезапных пробежек."}
    ]
    
    for item in dogs:
        item["img_url"] = url_for('static',
                                  filename=f'dogs/{item["slug"]}.jpg')
    return render_template('gallery.html', items=dogs, title="Собачки")