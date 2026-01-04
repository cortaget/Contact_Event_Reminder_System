import pyodbc
import os
from config import Config


class DatabaseInitializer:
    def __init__(self):
        self.config = Config()

    def check_database_exists(self):
        """Проверить существует ли база данных"""
        try:
            # Подключение к master для проверки существования БД
            conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE=master;'
            if self.config.trusted_connection:
                conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()

            # Проверка существования БД
            cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{self.config.database}'")
            result = cursor.fetchone()

            conn.close()
            return result is not None

        except Exception as e:
            print(f"❌ Ошибка проверки БД: {e}")
            return False

    def create_database(self):
        """Создать базу данных"""
        try:
            # Подключение к master
            conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE=master;'
            if self.config.trusted_connection:
                conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(conn_str, timeout=10)
            conn.autocommit = True
            cursor = conn.cursor()

            # Создание БД
            print(f"  🔨 Создание базы данных [{self.config.database}]...")
            cursor.execute(f"CREATE DATABASE [{self.config.database}]")
            print(f"  ✅ База данных [{self.config.database}] создана!")

            conn.close()
            return True

        except Exception as e:
            print(f"  ❌ Ошибка создания БД: {e}")
            return False

    def initialize_schema(self):
        """Инициализировать схему БД из SQL файла"""
        try:
            # Чтение SQL скрипта
            script_path = os.path.join(os.path.dirname(__file__), 'init_database.sql')

            if not os.path.exists(script_path):
                print(f"  ❌ SQL скрипт не найден: {script_path}")
                return False

            with open(script_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            # Подключение к созданной БД
            conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE={self.config.database};'
            if self.config.trusted_connection:
                conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(conn_str, timeout=30)
            cursor = conn.cursor()

            print("  🔨 Создание таблиц и представлений...")

            # Разделение скрипта на батчи (по GO)
            batches = sql_script.split('GO')
            batch_count = 0

            for batch in batches:
                batch = batch.strip()
                if batch and not batch.startswith('--'):
                    try:
                        cursor.execute(batch)
                        conn.commit()
                        batch_count += 1
                    except Exception as e:
                        error_msg = str(e).lower()
                        # Игнорируем только "уже существует"
                        if 'already exists' not in error_msg and 'there is already' not in error_msg:
                            print(f"  ⚠️  Предупреждение: {e}")

            print(f"  ✅ Выполнено {batch_count} SQL команд")
            print("  ✅ Схема базы данных готова!")
            conn.close()
            return True

        except Exception as e:
            print(f"  ❌ Ошибка инициализации схемы: {e}")
            import traceback
            traceback.print_exc()
            return False
