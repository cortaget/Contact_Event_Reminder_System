import json
import os
import sys


class Config:
    def __init__(self):
<<<<<<< HEAD
        # Определить правильный путь к config.json
        if getattr(sys, 'frozen', False):
            # Запущено из EXE - config.json рядом с EXE
            self.app_path = os.path.dirname(sys.executable)
        else:
            # Запущено из Python - config.json рядом с config.py
            self.app_path = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(self.app_path, 'config.json')
        print(f"📂 Путь к config.json: {self.config_file}")  # Для отладки
        self.load()

    def load(self):
        """Загрузить конфигурацию из файла"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ Конфигурация загружена из {self.config_file}")
            except Exception as e:
                print(f"⚠️ Ошибка чтения конфига: {e}")
                data = self.get_default()
                self.save(data)
        else:
            print(f"⚠️ Файл config.json не найден, создаю новый...")
=======
        self.config_file = self._get_config_path()
        self.load()

    def _get_config_path(self):
        """Получить путь к config.json"""
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), 'config.json')
        else:
            return os.path.join(os.path.dirname(__file__), 'config.json')

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
>>>>>>> 4113ecb (fix)
            data = self.get_default()
            self.save(data)

        self.server = data['database']['server']
        self.database = data['database']['database']
        self.driver = data['database']['driver']
<<<<<<< HEAD
        self.trusted_connection = data['database']['trusted_connection']
        self.default_reminder_days = data['settings']['default_reminder_days']

    def get_default(self):
        """Получить настройки по умолчанию"""
        return {
            'database': {
                'server': '.',
                'database': 'Contact_Event_Reminder_System',
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': True
=======
        self.trusted_connection = data['database'].get('trusted_connection', False)

        # НОВОЕ: SQL Server Authentication
        self.username = data['database'].get('username', 'sa')
        self.password = data['database'].get('password', '')

        self.default_reminder_days = data['settings']['default_reminder_days']

    def get_default(self):
        return {
            'database': {
                'server': 'localhost',
                'database': 'Contact_Event_Reminder_System',
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': False,  # По умолчанию SQL Auth
                'username': 'sa',
                'password': ''
>>>>>>> 4113ecb (fix)
            },
            'settings': {
                'default_reminder_days': 7
            }
        }

    def save(self, data=None):
<<<<<<< HEAD
        """Сохранить конфигурацию в файл"""
=======
>>>>>>> 4113ecb (fix)
        if data is None:
            data = {
                'database': {
                    'server': self.server,
                    'database': self.database,
                    'driver': self.driver,
<<<<<<< HEAD
                    'trusted_connection': self.trusted_connection
=======
                    'trusted_connection': self.trusted_connection,
                    'username': self.username,
                    'password': self.password
>>>>>>> 4113ecb (fix)
                },
                'settings': {
                    'default_reminder_days': self.default_reminder_days
                }
            }
<<<<<<< HEAD

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✅ Конфигурация сохранена в {self.config_file}")
        except Exception as e:
            print(f"❌ Ошибка сохранения конфига: {e}")

    def get_connection_string(self):
        """Получить строку подключения к БД"""
        conn_str = f'DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};'
        if self.trusted_connection:
            conn_str += 'Trusted_Connection=yes;'
=======
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_connection_string(self):
        conn_str = f'DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};'
        if self.trusted_connection:
            conn_str += 'Trusted_Connection=yes;'
        else:
            conn_str += f'UID={self.username};PWD={self.password};'
>>>>>>> 4113ecb (fix)
        return conn_str
