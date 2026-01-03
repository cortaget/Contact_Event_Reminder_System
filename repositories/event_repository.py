from database import Database
from models import Event
from datetime import datetime, timedelta


class EventRepository:
    def __init__(self):
        self.db = Database()

    def add_event(self, event):
        query = """
        INSERT INTO event (person_id, event_type_id, event_date, reminder_days_before, reminder_time)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_insert_with_identity(query, event.to_tuple())

    def update_event(self, event):
        query = """
        UPDATE event 
        SET person_id=?, event_type_id=?, event_date=?, reminder_days_before=?, reminder_time=?
        WHERE id=?
        """
        params = event.to_tuple() + (event.id,)
        return self.db.execute_query(query, params, commit=True)

    def delete_event(self, event_id):
        query = "DELETE FROM event WHERE id=?"
        return self.db.execute_query(query, (event_id,), commit=True)

    def get_event(self, event_id):
        query = "SELECT * FROM event WHERE id=?"
        row = self.db.execute_query(query, (event_id,), fetchone=True)
        if row:
            return Event(row.id, row.person_id, row.event_type_id,
                         row.event_date, row.reminder_days_before, row.reminder_time)
        return None

    def get_all_events(self):
        query = "SELECT * FROM event ORDER BY event_date"
        rows = self.db.execute_query(query, fetch=True)
        return [Event(r.id, r.person_id, r.event_type_id, r.event_date,
                      r.reminder_days_before, r.reminder_time) for r in rows]

    def get_upcoming_events(self, days_ahead=30):
        query = """
        SELECT * FROM event 
        WHERE event_date BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(day, ?, CAST(GETDATE() AS DATE))
        ORDER BY event_date
        """
        rows = self.db.execute_query(query, (days_ahead,), fetch=True)
        return [Event(r.id, r.person_id, r.event_type_id, r.event_date,
                      r.reminder_days_before, r.reminder_time) for r in rows]

    def get_events_for_person(self, person_id):
        query = "SELECT * FROM event WHERE person_id=? ORDER BY event_date"
        rows = self.db.execute_query(query, (person_id,), fetch=True)
        return [Event(r.id, r.person_id, r.event_type_id, r.event_date,
                      r.reminder_days_before, r.reminder_time) for r in rows]
