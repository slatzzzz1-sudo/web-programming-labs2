from flask import Blueprint, render_template, request, redirect
from db import db
from sqlalchemy import or_, and_, func
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка имя пользователя не должно быть пустым
    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Имя пользователя не может быть пустым')

    # Проверка пароль не должен быть пустым
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('/lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # 2. Автоматический логин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember')  # 3. Галочка "запомнить меня"

    # Проверка, что логин и пароль не пустые
    if not login_form or login_form.strip() == '':
        return render_template('/lab8/login.html',
                               error='Логин не может быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('/lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            # 3. Используем remember для длительной сессии
            login_user(user, remember=(remember == 'on'))
            return redirect('/lab8/')

    return render_template('/lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles')
def article_list():
    q = (request.args.get('q') or '').strip().lower()

    # 1. Получаем статьи по доступу
    if current_user.is_authenticated:
        articles_list = articles.query.filter(
            or_(
                articles.is_public.is_(True),
                and_(
                    articles.is_public.is_(False),
                    articles.user_id == current_user.id
                )
            )
        ).order_by(articles.created_at.desc()).all()
    else:
        articles_list = articles.query.filter(
            articles.is_public.is_(True)
        ).order_by(articles.created_at.desc()).all()

    # 2. Поиск по Python (регистронезависимый, кириллица работает)
    if q:
        articles_list = [
            a for a in articles_list
            if q in a.title.lower() or q in a.article_text.lower()
        ]

    return render_template(
        'lab8/articles.html',
        articles=articles_list,
        q=q
    )


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    # 4. Создание статьи
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not title or not article_text:
        return render_template('lab8/create.html', 
                               error='Заполните все поля')

    new_article = articles(
        title=title,
        article_text=article_text,
        is_public=is_public,
        user_id=current_user.id
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # 5. Редактирование статьи
    article = articles.query.get_or_404(article_id)

    # Проверяем, что статья принадлежит текущему пользователю
    if article.user_id != current_user.id:
        return "Ошибка: нет доступа к этой статье", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'

    if not title or not article_text:
        return render_template('lab8/edit.html', 
                               article=article,
                               error='Заполните все поля')

    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.updated_at = datetime.utcnow()

    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    # 6. Удаление статьи
    article = articles.query.get_or_404(article_id)

    # Проверяем, что статья принадлежит текущему пользователю
    if article.user_id != current_user.id:
        return "Ошибка: нет доступа к этой статье", 403

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')