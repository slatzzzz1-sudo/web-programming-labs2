import sqlite3
import os

# Проверка подключения
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(dir_path, "database.db")
    
    print(f"Путь к БД: {db_path}")
    print(f"Файл существует: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверка таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Таблицы: {tables}")
        
        conn.close()
        print("Подключение успешно!")
    else:
        print("Файл БД не найден!")
        
except Exception as e:
    print(f"Ошибка: {e}")