from flask import Blueprint, render_template, request, session
import sqlite3

from lab5 import db_connect, db_close

lab6 = Blueprint('lab6', __name__)


def init_offices_table():
    """Создаём таблицу offices и заполняем её, если пустая."""
    conn, cur = db_connect()
    try:
        # Одинаковый SQL для Postgres и SQLite
        cur.execute('''
            CREATE TABLE IF NOT EXISTS offices (
                number INTEGER PRIMARY KEY,
                tenant TEXT NOT NULL DEFAULT '',
                price  INTEGER NOT NULL
            )
        ''')

        # Проверяем, есть ли уже записи
        cur.execute('SELECT COUNT(*) AS cnt FROM offices')
        row = cur.fetchone()
        # в RealDictCursor row['cnt'], в sqlite3.Row тоже работает row['cnt']
        count = row['cnt'] if isinstance(row, dict) or hasattr(row, 'keys') else row[0]

        # Если таблица пустая — создаём 10 офисов
        if count == 0:
            use_sqlite = isinstance(conn, sqlite3.Connection)
            for i in range(1, 11):
                if use_sqlite:
                    cur.execute(
                        'INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)',
                        (i, '', 1000)
                    )
                else:
                    cur.execute(
                        'INSERT INTO offices (number, tenant, price) VALUES (%s, %s, %s)',
                        (i, '', 1000)
                    )
    finally:
        db_close(conn, cur)


@lab6.route('/lab6/')
def main():
    init_offices_table()       
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    init_offices_table()       
    data = request.json
    id_ = data.get('id')
    method = data.get('method')

    # ---------- метод info (без авторизации) ----------
    if method == 'info':
        conn, cur = db_connect()
        try:
            cur.execute('SELECT number, tenant, price FROM offices ORDER BY number')
            rows = cur.fetchall()

            offices = []
            for row in rows:
                # и RealDictCursor, и sqlite3.Row поддерживают доступ по имени колонки
                offices.append({
                    'number': row['number'],
                    'tenant': row['tenant'],
                    'price': row['price']
                })

            return {
                'jsonrpc': '2.0',
                'result': offices,
                'id': id_
            }
        finally:
            db_close(conn, cur)

    # все остальные методы требуют логина
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id_
        }

    # определяем тип БД, чтобы правильно использовать плейсхолдеры
    conn, cur = db_connect()
    use_sqlite = isinstance(conn, sqlite3.Connection)
    ph = '?' if use_sqlite else '%s'   # placeholder

    # ---------- booking ----------
    if method == 'booking':
        try:
            office_number = int(data['params'])
        except (ValueError, TypeError, KeyError):
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params'
                },
                'id': id_
            }

        try:
            # Проверяем, существует ли офис и занят ли он
            cur.execute(f'SELECT tenant FROM offices WHERE number = {ph}', (office_number,))
            row = cur.fetchone()

            if not row:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id_
                }

            tenant = row['tenant']

            if tenant != '':
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id_
                }

            # Бронируем
            cur.execute(
                f'UPDATE offices SET tenant = {ph} WHERE number = {ph}',
                (login, office_number)
            )

            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id_
            }
        finally:
            db_close(conn, cur)

    # ---------- cancellation ----------
    if method == 'cancellation':
        try:
            office_number = int(data['params'])
        except (ValueError, TypeError, KeyError):
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params'
                },
                'id': id_
            }

        try:
            cur.execute(f'SELECT tenant FROM offices WHERE number = {ph}', (office_number,))
            row = cur.fetchone()

            if not row:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': id_
                }

            tenant = row['tenant']

            # Офис не арендован
            if tenant == '':
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office is not booked'
                    },
                    'id': id_
                }

            # Офис арендован другим пользователем
            if tenant != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Cannot cancel someone else\'s booking'
                    },
                    'id': id_
                }

            # Снимаем аренду
            empty_tenant = '' if not use_sqlite else ''
            cur.execute(
                f'UPDATE offices SET tenant = {ph} WHERE number = {ph}',
                (empty_tenant, office_number)
            )

            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id_
            }
        finally:
            db_close(conn, cur)

    # ---------- неизвестный метод ----------
    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id_
    }