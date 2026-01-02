from database import Database
from models import Notification


class NotificationRepository:
    def __init__(self):
        self.db = Database()

    def add_notification(self, notification):
        query = """
        INSERT INTO notification (event_id, sent_at, status)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?)
        """
        return self.db.execute_insert_with_identity(query, notification.to_tuple())

    def update_notification(self, notification):
        query = """
        UPDATE notification 
        SET event_id=?, sent_at=?, status=?
        WHERE id=?
        """
        params = notification.to_tuple() + (notification.id,)
        return self.db.execute_query(query, params, commit=True)

    def delete_notification(self, notification_id):
        query = "DELETE FROM notification WHERE id=?"
        return self.db.execute_query(query, (notification_id,), commit=True)

    def get_notification(self, notification_id):
        query = "SELECT * FROM notification WHERE id=?"
        row = self.db.execute_query(query, (notification_id,), fetchone=True)
        if row:
            return Notification(row.id, row.event_id, row.sent_at, row.status)
        return None

    def get_notifications_by_event(self, event_id):
        query = "SELECT * FROM notification WHERE event_id=? ORDER BY sent_at DESC"
        rows = self.db.execute_query(query, (event_id,), fetch=True)
        return [Notification(r.id, r.event_id, r.sent_at, r.status) for r in rows]

    def get_pending_notifications(self):
        query = "SELECT * FROM notification WHERE status='planned' ORDER BY sent_at"
        rows = self.db.execute_query(query, fetch=True)
        return [Notification(r.id, r.event_id, r.sent_at, r.status) for r in rows]

    def get_all_notifications(self):
        """ДОБАВЬ ЭТОТ МЕТОД - он используется в UI"""
        query = "SELECT * FROM notification ORDER BY sent_at DESC"
        rows = self.db.execute_query(query, fetch=True)
        return [Notification(r.id, r.event_id, r.sent_at, r.status) for r in rows]
