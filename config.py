import json
import os
import sys


class Config:
    def __init__(self):
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
            data = self.get_default()
            self.save(data)

        db = data.get('database', {})
        self.server = db.get('server', 'localhost')
        self.database = db.get('database', 'Contact_Event_Reminder_System')
        self.driver = db.get('driver', 'ODBC Driver 17 for SQL Server')
        self.trusted_connection = db.get('trusted_connection', False)

        # НОВОЕ: SQL Server Authentication
        self.username = db.get('username', 'sa')
        self.password = db.get('password', '')

        settings = data.get('settings', {})
        self.default_reminder_days = settings.get('default_reminder_days', 7)

    def get_default(self):
        return {
            'database': {
                'server': 'localhost',
                'database': 'Contact_Event_Reminder_System',
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': False,
                'username': 'sa',
                'password': ''
            },
            'settings': {
                'default_reminder_days': 7
            }
        }

    def save(self, data=None):
        if data is None:
            data = {
                'database': {
                    'server': self.server,
                    'database': self.database,
                    'driver': self.driver,
                    'trusted_connection': self.trusted_connection,
                    'username': self.username,
                    'password': self.password
                },
                'settings': {
                    'default_reminder_days': self.default_reminder_days
                }
            }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_connection_string(self):
        conn_str = f'DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};'
        if self.trusted_connection:
            conn_str += 'Trusted_Connection=yes;'
        else:
            conn_str += f'UID={self.username};PWD={self.password};'
        return conn_str
