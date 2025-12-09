import sqlite3
import os
from werkzeug.security import generate_password_hash

# Определите путь к файлу БД
dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, "database.db")

print(f"Создаем базу данных по пути: {db_path}")

# Создайте соединение с БД
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row  # Для доступа по имени колонки
cursor = conn.cursor()

# Создайте таблицу users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    real_name TEXT
)
''')

# Создайте таблицу articles
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(50),
    article_text TEXT,
    is_favorite BOOLEAN DEFAULT 0,
    is_public BOOLEAN DEFAULT 0,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# (Опционально) Добавьте тестового пользователя
test_password = generate_password_hash('test123')
cursor.execute(
    "INSERT OR IGNORE INTO users (login, password, real_name) VALUES (?, ?, ?)",
    ('test_user', test_password, 'Тестовый Пользователь')
)

# Сохраните изменения
conn.commit()

# Проверьте созданные таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Созданные таблицы: {[table[0] for table in tables]}")

# Проверьте пользователей
cursor.execute("SELECT login, real_name FROM users;")
users = cursor.fetchall()
print(f"Пользователи в базе: {[dict(user) for user in users]}")

# Закройте соединение
conn.close()

print(f"База данных успешно создана: {db_path}")
print(f"Размер файла: {os.path.getsize(db_path)} байт")