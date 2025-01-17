import os
import time
import webview
import psutil
import threading
import sqlite3
from db import create_db, get_history, clear_history


# Функция для записи данных в SQLite базу данных
def record_data():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_info.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    while recording:
        # Получаем данные о загрузке CPU
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Вставляем данные о CPU в базу данных
        cursor.execute('INSERT INTO cpu_data (cpu_usage, ram, disk) VALUES (?,?,?)', (cpu_usage, ram_usage, disk_usage))
        conn.commit()
        time.sleep(1)  # Обновление данных каждую секунду
    conn.close()

# Функция для получения системной информации и передачи в JavaScript
def get_system_info():
    while True:
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Отправляем данные о системе в JavaScript
        webview.windows[0].evaluate_js(
            f"updateSystemInfo({cpu_usage}, {ram_usage}, {disk_usage})"
        )
        time.sleep(1)

# Функции для начала и остановки записи данных
def toggle_recording():
    global recording
    if not recording:
        recording = True
        
        # Запускаем поток для записи данных в фоновом режиме
        threading.Thread(target=record_data, daemon=True).start()
    else:
        recording = False


class API:
    def toggle_recording(self):
        toggle_recording()
        
    def get_history(self):
        return get_history()  

    def clear_history(self):
        clear_history()  

# Запуск PyWebview окна
if __name__ == '__main__':
    create_db()  # Создаем базу данных
    recording = False  # Флаг для начала записи

    # Запускаем поток для получения системной информации
    threading.Thread(target=get_system_info, daemon=True).start()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'templates', 'index.html')
    
    # Загружаем HTML страницу
    webview.create_window('System Monitor', template_path, js_api=API())
    webview.start()
