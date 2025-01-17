import unittest
import os
import sqlite3
from main import create_db, get_history, clear_history

class TestSystemInfoDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'system_info.db')
        create_db()
    
    def test_create_db(self):
        """Тест на создание базы данных"""
        self.assertTrue(os.path.exists(self.db_path), "База данных не была создана")
    
    def test_get_history_empty(self):
        """Тест на получение пустой истории"""
        data = get_history()
        self.assertEqual(data, [], "История должна быть пустой")

    def test_clear_history(self):
        """Тест на очистку истории"""
        clear_history()
        data = get_history()
        self.assertEqual(data, [], "История не была очищена")
    
    def test_insert_data_and_get_history(self):
        """Тест на вставку данных и получение истории"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cpu_data (cpu_usage, ram, disk) VALUES (?, ?, ?)', (45.5, 60.2, 80.1))
        conn.commit()
        conn.close()

        data = get_history()
        self.assertEqual(len(data), 1, "История должна содержать одну запись")
        self.assertEqual(data[0]['cpu_usage'], 45.5, "Неверное значение CPU Usage")
        self.assertEqual(data[0]['ram'], 60.2, "Неверное значение RAM")
        self.assertEqual(data[0]['disk'], 80.1, "Неверное значение Disk")

if __name__ == '__main__':
    unittest.main()
