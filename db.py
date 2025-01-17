import os
import sqlite3

# Функция для создания базы данных SQLite и вставки в нее данных
def create_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_info.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpu_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            cpu_usage REAL,  
            ram REAL,  
            disk REAL,  
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
        )
    ''')
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение с базой данных


# Функция для получения истории записанных данных
def get_history():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_info.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cpu_data ORDER BY timestamp DESC')  # Получаем все данные в порядке убывания времени
    data = cursor.fetchall()  # Получаем все результаты
    conn.close()  # Закрываем соединение с базой данных
    results = []
    for info in data:
        # Добавляем данные в список в виде словаря
        results.append(
             {
            "id": info[0],  # Идентификатор записи
            "cpu_usage": info[1],  # Процент использования CPU
            "ram": info[2],  # Процент использования оперативной памяти
            "disk": info[3],  # Процент использования диска
            "timestamp": info[4]  # Время записи
             }
        )
    return results  # Возвращаем результаты


# Функция для очистки всех записей в базе данных
def clear_history():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_info.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cpu_data')  # Удаляем все записи
    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение с базой данных
    return True  # Возвращаем True, чтобы показать, что очистка прошла успешно
