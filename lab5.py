from flask import (Blueprint, render_template, request, session, redirect,
                   current_app)
import psycopg2
import sqlite3
from os import path
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/err')
def err():
    return render_template('lab5/errr.html')

def db_connect():
    # Пытаемся использовать PostgreSQL, если недоступен - переключаемся на SQLite
    db_type = current_app.config.get('DB_TYPE', 'postgres')

    if db_type == 'postgres':
        try:
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='samoylov_dima_knowledge_base',
                user='samoylov_dima_knowledge_base',
                password='123'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            current_app.config['ACTIVE_DB_TYPE'] = 'postgres'
            return conn, cur
        except psycopg2.OperationalError:
            # Если PostgreSQL недоступен, автоматически переключаемся на SQLite
            print("PostgreSQL недоступен, используется SQLite")
            db_type = 'sqlite'

    # Используем SQLite
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
   if request.method == 'GET':
        return render_template('lab5/register.html')
   login = request.form.get('login').strip()
   password = request.form.get('password').strip()
   real_name = request.form.get('real_name')
   
   if not (login and password):
       return render_template('lab5/register.html', error='Заполните логин и пароль')

   conn, cur = db_connect()

   db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

   if db_type == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
   else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

   if cur.fetchone():
       db_close(conn, cur)
       return render_template('lab5/register.html', error='Такой пользователь уже существует')

   password_hash = generate_password_hash(password)
   if db_type == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash, real_name))
   else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, password_hash, real_name))
   db_close(conn, cur)
   return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/log2')
def log2():
    login = session.get('login')
    if login:
       return render_template('lab5/login.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    if db_type == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    session['login'] = login
    session['user_id'] = user['id']

    user_dict = dict(user)
    session['real_name'] = user_dict.get('real_name', '')

    db_close(conn, cur)
    return render_template('lab5/success_login.html',
                           login=login)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('real_name', None)
    return redirect('/lab5')


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_articles.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # True/False
    is_favorite = request.form.get('is_favorite') == 'on'

    # Валидация - проверка на пустые поля
    if not title or not article_text:
        return render_template('lab5/create_articles.html',
                               error='Заполните название и текст статьи')

    conn, cur = db_connect()

    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    if db_type == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    login_id = user["id"]

    if db_type == 'postgres':
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_public,"
            "is_favorite) VALUES (%s, %s, %s, %s, %s)",
            (login_id, title, article_text, is_public, is_favorite)
            )
    else:
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_public,"
            "is_favorite) VALUES (?, ?, ?, ?, ?)",
            (login_id, title, article_text, is_public, is_favorite)
            )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    if db_type == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    login_id = user["id"]

    # Сначала избранные, потом остальные
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC;",
                    (login_id, ))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;",
                    (login_id, ))
    articles = cur.fetchall()

    db_close(conn, cur)

    # Проверка на отсутствие статей
    if not articles:
        return render_template('/lab5/articles.html', articles=articles,
                               no_articles=True)

    return render_template('/lab5/articles.html', articles=articles,
                           no_articles=False)


@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    # Получаем публичные статьи с именами авторов
    if db_type == 'postgres':
        cur.execute("""
            SELECT a.*, u.login, u.real_name
            FROM articles a
            JOIN users u ON a.user_id = u.id
            WHERE a.is_public = true
            ORDER BY a.is_favorite DESC, a.id DESC
        """)
    else:
        cur.execute("""
            SELECT a.*, u.login, u.real_name
            FROM articles a
            JOIN users u ON a.user_id = u.id
            WHERE a.is_public = 1
            ORDER BY a.is_favorite DESC, a.id DESC
        """)

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('/lab5/public_articles.html', articles=articles,
                           login=session.get('login'))


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    # Проверяем, принадлежит ли статья текущему пользователю
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;",
                    (article_id, session.get('user_id')))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;",
                    (article_id, session.get('user_id')))

    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    # Обработка формы редактирования
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'

    # Валидация - проверка на пустые поля
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html',
                               article=article,
                               error='Заполните название и текст статьи')

    # Обновление статьи
    if db_type == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_public=%s, is_favorite=%s WHERE id=%s;",
                    (title, article_text, is_public, is_favorite, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_public=?, is_favorite=? WHERE id=?;",
                    (title, article_text, is_public, is_favorite, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    # Проверяем, принадлежит ли статья текущему пользователю
    if db_type == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;",
                    (article_id, session.get('user_id')))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;",
                    (article_id, session.get('user_id')))

    article = cur.fetchone()

    if article:
        # Удаляем статью
        if db_type == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    if db_type == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('/lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    db_type = current_app.config.get('ACTIVE_DB_TYPE', 'sqlite')

    if request.method == 'GET':
        if db_type == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE id=%s;",
                        (session.get('user_id'),))
        else:
            cur.execute("SELECT real_name FROM users WHERE id=?;",
                        (session.get('user_id'),))

        user = cur.fetchone()
        db_close(conn, cur)

        if user and user['real_name']:
            user_data = {'real_name': user['real_name']}
        else:
            user_data = {'real_name': ''}
        return render_template('lab5/profile.html', user=user_data)

    # Обработка изменения профиля
    real_name = request.form.get('real_name')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Проверка подтверждения пароля
    if new_password and new_password != confirm_password:
        db_close(conn, cur)
        return render_template('lab5/profile.html',
                               user={'real_name': real_name},
                               error='Пароли не совпадают')

    # Обновление данных
    if new_password:
        password_hash = generate_password_hash(new_password)
        if db_type == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE id=%s;",
                        (real_name, password_hash, session.get('user_id')))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE id=?;",
                        (real_name, password_hash, session.get('user_id')))
    else:
        if db_type == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE id=%s;",
                        (real_name, session.get('user_id')))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE id=?;",
                        (real_name, session.get('user_id')))

    # Обновляем сессию
    session['real_name'] = real_name

    db_close(conn, cur)
    return redirect('/lab5/list')