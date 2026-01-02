from datetime import date, datetime


class Person:
    def __init__(self, id=None, first_name='', last_name='', birth_date=None, gender=None, is_active=True):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.is_active = is_active

    def to_tuple(self):
        return (self.first_name, self.last_name, self.birth_date, self.gender, self.is_active)

    def __str__(self):
        status = "✓" if self.is_active else "✗"
        birth = self.birth_date.strftime('%d.%m.%Y') if self.birth_date else 'N/A'
        return f"[{self.id}] {self.first_name} {self.last_name} | {birth} | {self.gender or 'N/A'} {status}"

    def __repr__(self):
        return self.__str__()


class Event:
    def __init__(self, id=None, person_id=None, event_type='birthday', event_date=None, reminder_days_before=7):
        self.id = id
        self.person_id = person_id
        self.event_type = event_type
        self.event_date = event_date
        self.reminder_days_before = reminder_days_before

    def to_tuple(self):
        return (self.person_id, self.event_type, self.event_date, self.reminder_days_before)

    def __str__(self):
        event_date_str = self.event_date.strftime('%d.%m.%Y') if self.event_date else 'N/A'
        return f"[{self.id}] {self.event_type} | {event_date_str} | Person ID: {self.person_id} | Напоминание за {self.reminder_days_before} дней"

    def __repr__(self):
        return self.__str__()


class Notification:
    def __init__(self, id=None, event_id=None, sent_at=None, status='planned'):
        self.id = id
        self.event_id = event_id
        self.sent_at = sent_at or datetime.now()
        self.status = status

    def to_tuple(self):
        return (self.event_id, self.sent_at, self.status)

    def __str__(self):
        sent_time = self.sent_at.strftime('%d.%m.%Y %H:%M') if self.sent_at else 'N/A'
        status_icon = {'planned': '⏳', 'sent': '✓', 'failed': '✗'}.get(self.status, '?')
        return f"[{self.id}] Event ID: {self.event_id} | {sent_time} | {status_icon} {self.status}"

    def __repr__(self):
        return self.__str__()


class Group:
    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name

    def to_tuple(self):
        return (self.name,)

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def __repr__(self):
        return self.__str__()


class User:
    def __init__(self, id=None, name='', email='', notifications_enabled=True):
        self.id = id
        self.name = name
        self.email = email
        self.notifications_enabled = notifications_enabled

    def __str__(self):
        notif = "✓" if self.notifications_enabled else "✗"
        return f"[{self.id}] {self.name} | {self.email} | Уведомления: {notif}"

    def __repr__(self):
        return self.__str__()
