import csv
import json
from datetime import datetime
from database import Database
from models import Person, Event, Group


class ImportService:
    def __init__(self):
        self.db = Database()

    def import_persons_from_csv(self, file_path):
        operations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Парсинг даты
                    birth_date = None
                    if row.get('birth_date'):
                        try:
                            birth_date = datetime.strptime(row['birth_date'], '%Y-%m-%d').date()
                        except:
                            try:
                                birth_date = datetime.strptime(row['birth_date'], '%d.%m.%Y').date()
                            except:
                                birth_date = None

                    # Парсинг is_active
                    is_active = row.get('is_active', '1')
                    is_active = is_active in ['1', 'True', 'true', 'yes']

                    query = """
                    INSERT INTO person (first_name, last_name, birth_date, gender, is_active)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    params = (
                        row['first_name'],
                        row['last_name'],
                        birth_date,
                        row.get('gender'),
                        is_active
                    )
                    operations.append((query, params))

            return self.db.execute_transaction(operations)
        except Exception as e:
            print(f"Import error: {e}")
            raise

    def import_events_from_json(self, file_path):
        operations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                events = json.load(f)
                for event in events:
                    # Парсинг даты
                    event_date = None
                    if event.get('event_date'):
                        try:
                            event_date = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
                        except:
                            try:
                                event_date = datetime.strptime(event['event_date'], '%d.%m.%Y').date()
                            except:
                                event_date = None

                    query = """
                    INSERT INTO event (person_id, event_type, event_date, reminder_days_before)
                    VALUES (?, ?, ?, ?)
                    """
                    params = (
                        event['person_id'],
                        event['event_type'],
                        event_date,
                        event.get('reminder_days_before', 7)
                    )
                    operations.append((query, params))

            return self.db.execute_transaction(operations)
        except Exception as e:
            print(f"Import error: {e}")
            raise

    def import_groups_from_json(self, file_path):
        operations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for group in data['groups']:
                    query = "INSERT INTO [group] (name) VALUES (?)"
                    operations.append((query, (group['name'],)))

            return self.db.execute_transaction(operations)
        except Exception as e:
            print(f"Import error: {e}")
            raise
