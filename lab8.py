from flask import Blueprint, render_template, request, redirect, session, flash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    login = current_user.login if current_user.is_authenticated else 'Anonymous'
    # Получаем статьи для отображения на главной
    public_articles = articles.query.filter_by(is_public=True).order_by(articles.likes.desc()).all()
    return render_template('lab8/index.html', login=login, articles=public_articles)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form:
        return render_template('lab8/register.html',
                               error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html',
                               error='Пароль не должен быть пустым')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический логин после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'
    
    if not login_form:
        return render_template('lab8/login.html',
                               error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html',
                               error='Пароль не должен быть пустым')
    
    user = users.query.filter_by(login=login_form).first()
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)
            return redirect('/lab8/')
    
    return render_template('/lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/article', methods=['GET', 'POST'])
@login_required
def list_articles():
    status_message = None
    
    if request.method == 'POST':
        article_id = request.form.get('article_id')
        is_public = request.form.get('is_public') == 'on'
        is_favorite = request.form.get('is_favorite') == 'on'
        
        # ИСПРАВЛЕНО: используем login_id вместо user_id
        article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
        
        if article:
            # Обновляем оба статуса
            article.is_public = is_public
            article.is_favorite = is_favorite
            db.session.commit()
            status_message = f"Статус статьи «{article.title}» обновлен."
        else:
            status_message = "Ошибка: статья не найдена или недоступна."
    
    # ИСПРАВЛЕНО: используем login_id вместо user_id
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/list_articles.html', 
                         articles=user_articles, 
                         status_message=status_message)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/article/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create_article.html', 
                             error='Название и текст статьи обязательны!')
    
    # ИСПРАВЛЕНО: используем login_id вместо user_id, добавляем is_favorite
    new_article = articles(
        login_id=current_user.id,  # ← ВАЖНОЕ ИСПРАВЛЕНИЕ
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,   # ← Добавлено
        is_public=is_public,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/article')

@lab8.route('/lab8/article/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # ИСПРАВЛЕНО: используем login_id вместо user_id
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/article')
    
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        is_public = request.form.get('is_public') == 'on'
        is_favorite = request.form.get('is_favorite') == 'on'
        
        if not title or not text:
            return render_template(
                'lab8/edit_article.html',
                article=article,
                error="Название и текст статьи не могут быть пустыми."
            )
        
        # Обновляем статью
        article.title = title
        article.article_text = text
        article.is_public = is_public
        article.is_favorite = is_favorite
        db.session.commit()
        
        return redirect('/lab8/article')
    
    return render_template('lab8/edit_article.html', article=article)

@lab8.route('/lab8/article/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # ИСПРАВЛЕНО: используем login_id вместо user_id
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/article')
    
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/article')

# ДОБАВЛЕНО: Обработка лайков для публичных статей
@lab8.route('/lab8/article/like/<int:article_id>', methods=['POST'])
def like_article(article_id):
    article = articles.query.get(article_id)
    
    if article and article.is_public:
        article.likes = (article.likes or 0) + 1
        db.session.commit()
        flash(f'Лайк добавлен к статье "{article.title}"!', 'success')
    else:
        flash('Статья не найдена или не является публичной', 'error')
    
    return redirect('/lab8/')

# ДОБАВЛЕНО: Отдельный маршрут для избранных статей
@lab8.route('/lab8/article/favorites')
@login_required
def favorite_articles():
    # ИСПРАВЛЕНО: используем login_id вместо user_id
    favorite_articles_list = articles.query.filter_by(
        login_id=current_user.id, 
        is_favorite=True
    ).all()
    
    return render_template('lab8/favorite_articles.html', 
                         articles=favorite_articles_list)

# ДОБАВЛЕНО: Все публичные статьи
@lab8.route('/lab8/article/public')
def public_articles():
    public_articles_list = articles.query.filter_by(is_public=True)\
        .order_by(articles.likes.desc())\
        .all()
    
    return render_template('lab8/public_articles.html', 
                         articles=public_articles_list)