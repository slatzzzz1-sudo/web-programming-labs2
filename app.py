from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!doctype html>
<html>
<body>
<h1>web-cepsep на flask</h1>
<a href="/author">author</a>
</body>
</html>""", 200, {
    "X-Server": "sample",
    "Content-Type": "text/html; charset=utf-8"
}

@app.route('/lab1/image')
def author():
    name = 'Самойлов Дмитрий Алекссевич'
    group = 'ФБИ-32'
    faculty = 'ФБ'
    return '''<!doctype html>
        <html>
           <body>
               <p>Студент: ''' + name + '''</p>
               <p>Группа: ''' + group + '''</p>
               <p>Факультет: ''' + faculty + '''</p>
               <a href="/web">web</a>
           </body>
        </html>'''

@app.route('/lab1/counter')
def image():
    path = url_for('static', filename='oak.jpg')
    css = url_for('static', filename='lab1.css')
    return '''<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
           <body>
               <h1>Дуб</h1>
               <img src="''' + path + '''">
           </body>
        </html>'''

count = 0

@app.route('/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''<!doctype html>
        <html>
           <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''<br>
               <a href="/lab1/cleencounter">Очистка счётчика</a>
               <hr>
               Дата и время: ''' + str(time) + '''<br>
               Запрошенный адрес: ''' + url + '''<br>
               Ваш IP-адрес: ''' + client_ip + '''<br> 
           </body>
        </html>'''

@app.route('/lab1/cleencounter')
def cleencounter():
    global count
    count = 0
    return '''<!doctype html>
        <html>
           <body>
               Счётчик очищен! <br>
               Сколько раз вы сюда заходили: ''' + str(count) + '''<br>
               <a href="/lab1/counter">Вернуться на счётчик</a>
           </body>
        </html>'''


@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''<!doctype html>
        <html>
           <body>
               <h1>Создано успешно</h1>
               <div><i>что-то создано...</i></div>
           </body>
        </html>''', 201

@app.errorhandler(404)
def not_found(err):
        return 'нет такой страницы', 404


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
                    <li><a href="/lab1">Первая лабораторная</a></li>
                </ul>
                <hr>
                <footer>
                    Самойлов Дмитрий Алексеевич, ФБИ-32, 3 курс, 2025
                </footer>
            </body>
                </html>'''


@app.route('/lab1')
def lab1():
    return '''<!doctype html>
        <html>
            <head>
                <title>Лабораторная 1</title>
            </head>
            <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Корень сайта</a>
            </body>
        </html>'''
