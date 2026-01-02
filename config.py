import json
import os


class Config:
    def __init__(self):
        self.config_file = 'config.json'
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = self.get_default()
            self.save(data)

        self.server = data['database']['server']
        self.database = data['database']['database']
        self.driver = data['database']['driver']
        self.trusted_connection = data['database']['trusted_connection']
        self.default_reminder_days = data['settings']['default_reminder_days']

    def get_default(self):
        return {
            'database': {
                'server': '.',
                'database': 'Contact_Event_Reminder_System',
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': True
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
                    'trusted_connection': self.trusted_connection
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
        return conn_str
