import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, "database.db")

print(f"Проверка БД: {db_path}")
print(f"Файл существует: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Проверка таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nТаблицы в базе:")
    for table in tables:
        print(f"  - {table[0]}")
        # Покажем структуру таблицы
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"    {col[1]} ({col[2]})")
    
    # Проверка данных
    print(f"\nДанные в таблице users:")
    cursor.execute("SELECT COUNT(*) as count FROM users;")
    count = cursor.fetchone()[0]
    print(f"  Количество записей: {count}")
    
    if count > 0:
        cursor.execute("SELECT login, real_name FROM users LIMIT 5;")
        users = cursor.fetchall()
        for user in users:
            print(f"  Логин: {user[0]}, Имя: {user[1]}")
    
    conn.close()
else:
    print("\nФайл БД не найден! Создайте его с помощью create_database.py")