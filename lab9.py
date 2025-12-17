from flask import Blueprint, render_template, jsonify, session
from flask_login import current_user, login_required
from db import db
from db.models import GiftBox
import random

lab9 = Blueprint('lab9', __name__)

# 10 уникальных поздравлений
CONGRATULATIONS = {
    1: {"text": "С Новым годом! Пусть сбудутся все мечты!", "gift": "gift1.jpg"},
    2: {"text": "Желаю здоровья, счастья и благополучия!", "gift": "gift2.jpg"},
    3: {"text": "Пусть новый год принесет много радости!", "gift": "gift3.jpg"},
    4: {"text": "Удачи во всех начинаниях и новых свершений!", "gift": "gift4.jpg"},
    5: {"text": "Пусть каждый день будет наполнен счастьем!", "gift": "gift5.jpg"},
    6: {"text": "Желаю финансового благополучия и успеха!", "gift": "gift6.jpg"},
    7: {"text": "Пусть в доме всегда царят мир и гармония!", "gift": "gift7.jpg"},
    8: {"text": "Желаю крепкого здоровья и долгих лет жизни!", "gift": "gift8.jpg"},
    9: {"text": "Пусть все плохое останется в старом году!", "gift": "gift9.jpg"},
    10: {"text": "Счастья, любви и исполнения всех желаний!", "gift": "gift10.jpg"}
}

@lab9.route('/lab9/')
def index():
    # Проверяем, есть ли коробки в БД
    boxes = GiftBox.query.order_by(GiftBox.id).all()
    
    # Если коробок нет, создаем 10 штук с случайными позициями
    if not boxes:
        boxes = []
        for i in range(1, 11):
            box = GiftBox(
                id=i,
                is_opened=False,
                position_x=random.randint(50, 900),
                position_y=random.randint(50, 500)
            )
            boxes.append(box)
            db.session.add(box)
        db.session.commit()
    
    # Считаем сколько коробок еще не открыто
    opened_count = sum(1 for box in boxes if box.is_opened)
    
    return render_template(
        'lab9/index.html',
        boxes=boxes,
        opened_left=10 - opened_count,
        user=current_user
    )


@lab9.route('/lab9/open/<int:box_id>', methods=['POST'])
def open_box(box_id):
    # Получаем коробку из БД
    box = GiftBox.query.get_or_404(box_id)
    
    # Проверяем, открыта ли уже коробка глобально
    if box.is_opened:
        return jsonify({
            'status': 'empty',
            'message': 'Эта коробка уже пуста!'
        })
    
    # Получаем список открытых коробок для текущего пользователя
    user_key = f"opened_boxes_{current_user.get_id() if current_user.is_authenticated else 'guest'}"
    opened_boxes = session.get(user_key, [])
    
    # Проверяем лимит в 3 коробки
    if len(opened_boxes) >= 3:
        return jsonify({
            'status': 'limit_reached',
            'message': 'Вы уже открыли 3 коробки! Больше нельзя.'
        })
    
    # Проверяем, открывал ли пользователь эту коробку ранее
    if box_id in opened_boxes:
        return jsonify({
            'status': 'already_opened',
            'message': 'Вы уже открывали эту коробку!'
        })
    
    # Добавляем коробку в список открытых для пользователя
    opened_boxes.append(box_id)
    session[user_key] = opened_boxes
    
    # Помечаем коробку как открытую в БД
    box.is_opened = True
    db.session.commit()
    
    # Возвращаем поздравление и подарок
    congrat = CONGRATULATIONS.get(box_id, {"text": "Поздравляем!", "gift": "gift.jpg"})
    
    return jsonify({
        'status': 'success',
        'text': congrat['text'],
        'gift': congrat['gift'],
        'box_id': box_id
    })


@lab9.route('/lab9/reset_all', methods=['POST'])
@login_required
def reset_all():
    # Сброс всех коробок (только для админа/авторизованных)
    GiftBox.query.update({GiftBox.is_opened: False})
    db.session.commit()
    
    # Очищаем сессии всех пользователей
    for key in list(session.keys()):
        if key.startswith('opened_boxes_'):
            session.pop(key)
    
    return jsonify({'status': 'reset'})


@lab9.route('/lab9/my_boxes', methods=['GET'])
def my_boxes():
    # Получить список открытых коробок текущим пользователем
    user_key = f"opened_boxes_{current_user.get_id() if current_user.is_authenticated else 'guest'}"
    opened_boxes = session.get(user_key, [])
    
    return jsonify({
        'opened': opened_boxes,
        'count': len(opened_boxes)
    })