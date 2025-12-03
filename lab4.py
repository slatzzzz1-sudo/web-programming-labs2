from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')



@lab4.route('/lab4/div', methods=['POST'])

def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html',
                               error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')



@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
        
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('/lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multiplication-form')
def multiplication_form():
    return render_template('lab4/multiplication-form.html')


@lab4.route('/lab4/multiplication', methods=['POST'])
def multiplication():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('/lab4/multiplication.html', x1=x1, x2=x2,
                           result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html',
                               error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods=['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html',
                               error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('/lab4/exp.html',
                               error = 'Не может быть так, что оба поля равны нулю!')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)



tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    operation = request.form.get('operation')
    if operation == 'cut':
        tree_count -= 1
        if tree_count < 0:
            tree_count = 0
    elif operation == 'plant':
        tree_count += 1
    return redirect('/lab4/tree')


users = [

    {'login': 'alex', 'password': '123', 'name': 'Алекс Иванов'},
    {'login': 'pasha', 'password': '111', 'name': 'Паша Траваманов'},
    {'login': 'sasha', 'password': '222', 'name': 'Саша Булкин'},
    {'login': 'dima', 'password': '333', 'name': 'Дима Медведев'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login_from_session = session['login']
            # находим пользователя по логину, чтобы взять имя
            user_name = ''
            for u in users:
                if u['login'] == login_from_session:
                    user_name = u['name']
                    break
            return render_template(
                '/lab4/login.html',
                authorized=authorized,
                login=login_from_session,
                user_name=user_name,
                error=''
            )
        else:
            return render_template(
                '/lab4/login.html',
                authorized=False,
                login='',
                user_name='',
                error=''
            )
    # если POST
    login_form = request.form.get('login', '')
    password_form = request.form.get('password', '')
    # проверка на пустые
    if login_form == '' and password_form == '':
        return render_template(
            '/lab4/login.html',
            authorized=False,
            login=login_form,   # чтобы осталось то, что ввёл
            user_name='',
            error='Не введён логин и пароль'
        )
    if login_form == '':
        return render_template(
            '/lab4/login.html',
            authorized=False,
            login=login_form,   # чтобы осталось то, что ввёл
            user_name='',
            error='Не введён логин'
        )
    if password_form == '':
        return render_template(
            '/lab4/login.html',
            authorized=False,
            login=login_form,
            user_name='',
            error='Не введён пароль'
        )
    for user in users:
        if login_form == user['login'] and password_form == user['password']:
            session['login'] = login_form
            return redirect('/lab4/login')
    # если не нашли
    return render_template(
        '/lab4/login.html',
        authorized=False,
        login=login_form,   # сохраняем введённый логин
        user_name='',
        error='Неверные логин и/или пароль'
    )


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ''
    snowflakes = 0
    temperature = ''
    if request.method == 'POST':
        temperature = request.form.get('temperature', '').strip()

        if temperature == '':
            message = 'Ошибка: не задана температура'
        else:
            try:
                t = int(temperature)

                if t < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif t > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                else:
                    # диапазоны
                    if -12 <= t <= -9:
                        message = f'Установлена температура: {t}°C'
                        snowflakes = 3
                    elif -8 <= t <= -5:
                        message = f'Установлена температура: {t}°C'
                        snowflakes = 2
                    elif -4 <= t <= -1:
                        message = f'Установлена температура: {t}°C'
                        snowflakes = 1
            except ValueError:
                message = 'Ошибка: температура должна быть числом'
    return render_template(
        '/lab4/fridge.html',
        message=message,
        snowflakes=snowflakes,
        temperature=temperature
    )



@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain_order():
    grains = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    message = ''
    error = ''
    selected_grain = 'ячмень'  # по умолчанию
    weight = ''
    discount_text = ''

    if request.method == 'POST':
        selected_grain = request.form.get('grain', 'ячмень')
        weight = request.form.get('weight', '').strip()

        # проверки
        if weight == '':
            error = 'Ошибка: не указан вес'
        else:
            try:
                w = float(weight)

                if w <= 0:
                    error = 'Ошибка: вес должен быть больше 0'
                elif w > 100:
                    error = 'Ошибка: такого объёма сейчас нет в наличии'
                else:
                    price_per_ton = grains.get(selected_grain, 0)
                    total = w * price_per_ton
                    discount = 0

                    if w > 10:
                        discount = total * 0.10
                        total = total - discount
                        discount_text = f'Применена скидка за большой объём: 10% ({int(discount)} руб.)'

                    message = (
                        f'Заказ успешно сформирован. '
                        f'Вы заказали {selected_grain}. '
                        f'Вес: {w} т. '
                        f'Сумма к оплате: {int(total)} руб.'
                    )
            except ValueError:
                error = 'Ошибка: вес должен быть числом'

    return render_template(
        '/lab4/grain.html',
        grains=grains,
        message=message,
        error=error,
        selected_grain=selected_grain,
        weight=weight,
        discount_text=discount_text
    )

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        login_form = request.form.get('login', '').strip()
        name_form = request.form.get('name', '').strip()
        password_form = request.form.get('password', '')
        confirm_form = request.form.get('confirm', '')

        # проверки на пустые
        if login_form == '':
            error = 'Не введён логин'
        elif name_form == '':
            error = 'Не введено имя'
        elif password_form == '':
            error = 'Не введён пароль'
        elif password_form != confirm_form:
            error = 'Пароль и подтверждение не совпадают'
        else:
            # проверка, что такого логина ещё нет
            exists = False
            for u in users:
                if u['login'] == login_form:
                    exists = True
                    break
            if exists:
                error = 'Такой логин уже существует'
            else:
                # добавляем пользователя
                users.append({
                    'login': login_form,
                    'password': password_form,
                    'name': name_form
                })
                # сразу логиним
                session['login'] = login_form
                return redirect('/lab4/login')

    return render_template('/lab4/register.html', error=error)


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']
    return render_template('/lab4/users.html',
                           users=users,
                           current_login=current_login)


@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']

    # ищем текущего пользователя
    current_user = None
    for u in users:
        if u['login'] == current_login:
            current_user = u
            break

    if current_user is None:
        # на всякий случай
        return redirect('/lab4/login')

    error = ''

    if request.method == 'POST':
        new_login = request.form.get('login', '').strip()
        new_name = request.form.get('name', '').strip()
        new_password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if new_login == '':
            error = 'Не введён логин'
        elif new_name == '':
            error = 'Не введено имя'
        else:
            # проверяем, что логин не занят другим
            taken = False
            for u in users:
                if u['login'] == new_login and u is not current_user:
                    taken = True
                    break
            if taken:
                error = 'Такой логин уже используется другим пользователем'
            else:
                # пароль меняем только если оба поля не пустые
                if new_password == '' and confirm == '':
                    # оставить старый пароль
                    current_user['login'] = new_login
                    current_user['name'] = new_name
                    # если логин поменяли — обновим в сессии
                    session['login'] = new_login
                    return redirect('/lab4/users')
                else:
                    if new_password != confirm:
                        error = 'Пароль и подтверждение не совпадают'
                    else:
                        current_user['login'] = new_login
                        current_user['name'] = new_name
                        current_user['password'] = new_password
                        session['login'] = new_login
                        return redirect('/lab4/users')

    return render_template('/lab4/edit_user.html',
                           user=current_user,
                           error=error)


@lab4.route('/lab4/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']

    # удаляем из списка
    for i, u in enumerate(users):
        if u['login'] == current_login:
            users.pop(i)
            break

    # выходим из системы
    session.pop('login', None)
    return redirect('/lab4/login')