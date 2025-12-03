from flask import Flask, url_for, request
import datetime

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)


@app.route('/')
@app.route('/index')
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
                    <li><a href="/lab3/">Лабораторная работа 3</a></li>
                    <li><a href="/lab4">Лабораторная работа 4</a></li>
                </ul>
                <hr>
                <footer>
                    Самойлов Дмитрий Алексеевич, ФБИ-32, 3 курс, 2025
                </footer>
            </body>
        </html>'''

@app.errorhandler(500)
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
                <img src="''' + e500 + '''" alt="500 error cat">
            </body>
        </html>
        ''', 500


# Журнал посещений
access_log = []

@app.errorhandler(404)
def not_found(err):
    ip = request.remote_addr
    date = datetime.datetime.now()
    url = request.url

    # Добавляем запись в журнал
    access_log.append(f"[{date}] пользователь {ip} зашел на адрес: {url}")

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