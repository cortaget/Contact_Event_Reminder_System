from database import Database
from models import EventType

class EventTypeRepository:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        """Получить все типы событий"""
        rows = self.db.execute_query("SELECT id, name FROM event_type ORDER BY name", fetch=True)
        return [EventType(r.id, r.name) for r in rows]

    def get_by_id(self, id_):
        """Получить тип по ID"""
        row = self.db.execute_query("SELECT id, name FROM event_type WHERE id=?", (id_,), fetchone=True)
        return EventType(row.id, row.name) if row else None

    def add(self, name):
        """Добавить новый тип"""
        query = "INSERT INTO event_type (name) OUTPUT INSERTED.id VALUES (?)"
        return self.db.execute_insert_with_identity(query, (name,))
