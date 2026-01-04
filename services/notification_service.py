import pyodbc
from config import Config
from datetime import datetime, timedelta


class NotificationService:
    def __init__(self):
        self.config = Config()

    def get_connection(self):
        """Получить подключение к БД"""
        conn_str = self.config.get_connection_string()
        return pyodbc.connect(conn_str)

    def check_pending_reminders(self):
        """
        Проверить события, требующие напоминания
        Возвращает список событий, по которым нужно напомнить СЕГОДНЯ
        """
        query = """
        SELECT 
            e.id AS event_id,
            e.event_date,
            e.reminder_days_before,
            e.reminder_time,
            et.name AS event_type,
            p.first_name,
            p.last_name,
            p.id AS person_id,
            DATEDIFF(day, GETDATE(), e.event_date) AS days_until
        FROM event e
        INNER JOIN person p ON e.person_id = p.id
        INNER JOIN event_type et ON e.event_type_id = et.id
        WHERE 
            -- Событие в будущем или сегодня
            e.event_date >= CAST(GETDATE() AS DATE)
            -- Нужно напомнить сегодня или раньше
            AND DATEDIFF(day, GETDATE(), e.event_date) <= e.reminder_days_before
            -- Уведомление ещё не отправлено
            AND NOT EXISTS (
                SELECT 1 FROM notification n 
                WHERE n.event_id = e.id 
                AND n.status = 'sent'
                AND CAST(n.sent_at AS DATE) = CAST(GETDATE() AS DATE)
            )
        ORDER BY e.event_date
        """

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()

            # Преобразовать в список словарей
            reminders = []
            for row in results:
                reminders.append({
                    'event_id': row.event_id,
                    'event_date': row.event_date,
                    'reminder_days_before': row.reminder_days_before,
                    'reminder_time': row.reminder_time,
                    'event_type': row.event_type,
                    'first_name': row.first_name,
                    'last_name': row.last_name,
                    'person_id': row.person_id,
                    'days_until': row.days_until
                })

            return reminders

        except Exception as e:
            print(f"❌ Ошибка проверки напоминаний: {e}")
            return []

    def mark_notification_sent(self, event_id):
        """Отметить уведомление как отправленное"""
        query = """
        INSERT INTO notification (event_id, sent_at, status)
        VALUES (?, GETDATE(), 'sent')
        """

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (event_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения уведомления: {e}")
            return False

    def get_reminder_text(self, reminder):
        """Сформировать текст напоминания"""
        full_name = f"{reminder['first_name']} {reminder['last_name']}"
        event_type = reminder['event_type']
        days_until = reminder['days_until']
        event_date = reminder['event_date'].strftime('%d.%m.%Y')

        if days_until == 0:
            return f"🎉 DNES je {event_type}: {full_name}!"
        elif days_until == 1:
            return f"⏰ ZÍTRA je {event_type}: {full_name} ({event_date})"
        else:
            return f"📅 Za {days_until} dní ({event_date}) je {event_type}: {full_name}"
