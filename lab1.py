from flask import Blueprint, url_for, request, redirect, Response
import datetime
lab1 = Blueprint('lab1', __name__)


# -------------------- LAB1 WEB --------------------
@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-cepsep на flask</h1>
<a href="/lab1/author">author</a>
</body>
</html>""", 200, {
        "X-Server": "sample",
        "Content-Type": "text/html; charset=utf-8"
    }


# -------------------- LAB1 AUTHOR --------------------
@lab1.route('/lab1/author')
def author():
    name = 'Самойлов Дмитрий Алекссевич'
    group = 'ФБИ-32'
    faculty = 'ФБ'
    return f'''<!doctype html>
<html>
   <body>
       <p>Студент: {name}</p>
       <p>Группа: {group}</p>
       <p>Факультет: {faculty}</p>
       <a href="/lab1/web">web</a>
   </body>
</html>'''


# -------------------- LAB1 IMAGE --------------------
@lab1.route('/lab1/image')
def image():
    path = url_for('static', filename='oak.jpg')
    css = url_for('static', filename='lab1.css')

    html = f'''<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="{css}">
        <title>Дуб</title>
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}">
    </body>
</html>'''

    response = Response(html)
    response.headers['Content-Language'] = 'ru'
    response.headers['X-Developer'] = 'Samoylov Dima'
    response.headers['X-Lab-Work'] = 'Lab1'
    return response


# -------------------- COUNTER --------------------
count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return f'''<!doctype html>
<html>
   <body>
        Сколько раз вы сюда заходили: {count}<br>
       <a href="/lab1/cleencounter">Очистка счётчика</a>
       <hr>
       Дата и время: {time}<br>
       Запрошенный адрес: {url}<br>
       Ваш IP-адрес: {client_ip}<br>
   </body>
</html>'''


@lab1.route('/lab1/cleencounter')
def cleencounter():
    global count
    count = 0
    return f'''<!doctype html>
<html>
   <body>
       Счётчик очищен! <br>
       Сколько раз вы сюда заходили: {count}<br>
       <a href="/lab1/counter">Вернуться на счётчик</a>
   </body>
</html>'''


# -------------------- INFO REDIRECT --------------------
@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')


# -------------------- CREATED 201 --------------------
@lab1.route('/lab1/created')
def created():
    return '''<!doctype html>
<html>
   <body>
       <h1>Создано успешно</h1>
       <div><i>что-то создано...</i></div>
   </body>
</html>''', 201


# -------------------- 404 CUSTOM --------------------
@lab1.route('/404')
def error404():
    dog = url_for('static', filename='404.jpg')
    return f'''<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f9fafc;
                color: #333;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                font-size: 48px;
                margin-bottom: 20px;
                color: #d9534f;
            }}
            p {{
                font-size: 20px;
                margin-bottom: 30px;
            }}
            a {{
                color: #0275d8;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            img {{
                width: 250px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>404 — Ой! Страница потерялась...</h1>
        <p>Похоже, такой страницы у нас нет.<br>
           Но вы всегда можете вернуться <a href="/">на главную</a>.
        </p>
        <br>
        <img src="{dog}" alt="404 dog">
    </body>
</html>
''', 404


# -------------------- INDEX --------------------
@lab1.route('/')
@lab1.route('/index')
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <meta charset="utf-8">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <ul>
            <li><a href="/lab1">Лабораторная работа 1</a></li>
            <li><a href="/lab2">Лабораторная работа 2</a></li>
        </ul>
        <hr>
        <footer>
            Самойлов Дмитрий Алексеевич, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>'''


# -------------------- LAB1 MENU --------------------
@lab1.route('/lab1')
def lab1_menu():
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке Python.
        </p>
        <a href="/">Корень сайта</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главное меню</a></li>
            <li><a href="/lab1/web">Страница с HTML</a></li>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/image">Страница с картинкой</a></li>
            <li><a href="/lab1/counter">Счётчик</a></li>
            <li><a href="/lab1/cleencounter">Очистка счётчика</a></li>
            <li><a href="/lab1/info">Info (redirect)</a></li>
            <li><a href="/lab1/created">Создано (201)</a></li>
            <li><a href="/404">Ошибка 404</a></li>
        </ul>
    </body>
</html>'''

@lab1.route('/400')
def error400():
    return "<h1>400 Bad Request</h1><p>Запрос не может быть понят сервером из-за некорректного синтаксиса.</p>", 400

@lab1.route('/401')
def error401():
    return "<h1>401 Unauthorized</h1><p>Для доступа требуется аутентификация.</p>", 401

@lab1.route('/402')
def error402():
    return "<h1>402 Payment Required</h1><p>Необходима оплата для продолжения.</p>", 402

@lab1.route('/403')
def error403():
    return "<h1>403 Forbidden</h1><p>У вас нет прав для доступа к этому ресурсу.</p>", 403

@lab1.route('/405')
def error405():
    return "<h1>405 Method Not Allowed</h1><p>Метод запроса не поддерживается для данного ресурса.</p>", 405

@lab1.route('/418')
def error418():
    return "<h1>418 I'm a teapot</h1><p>Я — чайник. Сервер отказывается заваривать кофе в чайнике.</p>", 418

    return "<h1>418 I'm a teapot</h1><p>Я — чайник. Сервер отказывается заваривать кофе в чайнике.</p>", 418


@lab1.route('/error')
def error():
    return 1 / 0

@lab1.errorhandler(500)
def internal_error(err):
    e500 = url_for('static', filename='500.webp')
    return '''<!doctype html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Ошибка 500 — Внутренняя ошибка сервера</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #fff5f5;
                        color: #333;
                        text-align: center;
                        padding: 60px;
                    }
                    h1 {
                        font-size: 42px;
                        color: #c00;
                    }
                    p {
                        font-size: 20px;
                        margin: 20px 0;
                    }
                    a {
                        color: #0066cc;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    img {
                        hieght: 500px;
                        width: 500px;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <h1>500 — Упс! Что-то пошло не так...</h1>
                <p>
                    На сервере произошла внутренняя ошибка.<br>
                    Пожалуйста, попробуйте позже или вернитесь <a href="/">на главную</a>.
                </p>
                <img src="''' + e500 + '''" alt="500 error">
            </body>
        </html>
        ''', 500


# Журнал посещений
access_log = []

@lab1.errorhandler(404)
def not_found(err):
    ip = request.remote_addr
    date = datetime.datetime.now()
    url = request.url

    # Добавляем запись в журнал
    access_log.lab1end(f"[{date}] пользователь {ip} зашел на адрес: {url}")

    # Создаём HTML для журнала
    log_html = "<ul>"
    for entry in access_log:
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"

    return f'''<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>404 — Страница не найдена</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f0f8ff;
                    color: #333;
                    text-align: center;
                    padding: 40px;
                }}
                h1 {{
                    font-size: 48px;
                    color: #d9534f;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 20px;
                    margin-bottom: 20px;
                }}
                a {{
                    color: #0275d8;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                ul {{
                    text-align: left;
                    display: inline-block;
                    margin-top: 20px;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>404 — Страница не найдена</h1>
            <p>Ваш IP: {ip}<br>
            Дата: {date}<br>
            <a href="/">Вернуться на главную</a></p>
            <h2>Журнал посещений</h2>
            {log_html}
        </body>
    </html>
        ''', 404
