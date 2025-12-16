from flask import Blueprint, render_template, request, abort, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        'title': 'Inception',
        'title_ru': 'Начало',
        'year': 2010,
        'description': 'Профессиональный вор идей Кобб использует \
        технологию проникновения в сны, чтобы внедрить в подсознание \
        человека чужую мысль. Ему предстоит выполнить почти невозможное \
        задание — не украсть, а внедрить идею. Фильм исследует природу \
        реальности, памяти и человеческого сознания через многослойные \
        сновидческие миры.'
    },
    {
        'title': 'The Matrix',
        'title_ru': 'Матрица',
        'year': 1999,
        'description': 'Хакер по кличке Нео узнает, что его мир — \
        лишь компьютерная симуляция, созданная машинами для порабощения \
        человечества. Вместе с группой повстанцев он вступает в борьбу \
        против системы. Фильм стал культурным феноменом, повлиявшим на \
        кинематограф и поп-культуру, исследуя темы свободы воли, реальности \
        и технологического контроля.'
    },
    {
        'title': 'Parasite',
        'title_ru': 'Паразиты',
        'year': 2019,
        'description': 'Бедная семья Ки-тхэка хитростью устраивается на работу \
        в богатый дом семьи Пак. Однако их планам мешает неожиданное открытие — \
        в доме уже живут другие «паразиты». Острая социальная сатира о классовом \
        неравенстве, которая мастерски сочетает черную комедию, триллер и драму, \
        став первым неанглоязычным фильмом, получившим «Оскар» за лучший фильм.'
    },
    {
        'title': 'Pulp Fiction',
        'title_ru': 'Криминальное чтиво',
        'year': 1994,
        'description': 'Несколько переплетающихся историй о бандитах, \
        боксере, гангстерах и их неожиданных приключениях в Лос-Анджелесе. \
        Фильм с нелинейным повествованием, запоминающимися диалогами и \
        культовыми сценами, переопределивший независимое кино 1990-х и \
        ставший визитной карточкой Квентина Тарантино.'
    },
    {
        'title': 'The Dark Knight',
        'title_ru': 'Темный рыцарь',
        'year': 2008,
        'description': 'Бэтмен, комиссар Гордон и прокурор Харви Дент \
        объединяются против криминала Готэма, но их планы нарушает \
        хаотичный и непредсказуемый Джокер. Фильм поднимает вопросы \
        морали, жертвенности и природы героизма, с культовой ролью \
        Хита Леджера в роли антагониста.'
    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        if film['description'] == '':
            return {'description': 'Заполните описание'}, 400
        films[id] = film
        return films[id], 200
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400
    films.append(film)
    new_index = len(films) - 1
    return {"id": new_index, "film": film}, 201