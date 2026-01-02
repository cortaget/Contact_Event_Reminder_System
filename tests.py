from repositories.person_repository import PersonRepository
from repositories.event_repository import EventRepository
from repositories.group_repository import GroupRepository
from repositories.person_group_repository import PersonGroupRepository
from repositories.report_repository import ReportRepository
from models import Person, Event, Group
from datetime import date

from repositories.person_repository import PersonRepository
from repositories.event_repository import EventRepository
from repositories.group_repository import GroupRepository
from repositories.notification_repository import NotificationRepository


class AllRepository:
    def __init__(self):
        self.person_repo = PersonRepository()
        self.event_repo = EventRepository()
        self.group_repo = GroupRepository()
        self.notification_repo = NotificationRepository()

    def get_all_data(self):
        return {
            'persons': self.person_repo.get_all_persons(),
            'events': self.event_repo.get_all_events(),
            'groups': self.group_repo.get_all_groups(),
            'notifications': self.notification_repo.get_all_notifications()
        }

    def del_all_data(self):
        try:
            operations = [
                ("DELETE FROM notification", ()),
                ("DELETE FROM event", ()),
                ("DELETE FROM person_group", ()),
                ("DELETE FROM person", ()),
                ("DELETE FROM [group]", ()),
                ("DELETE FROM [user]", ())
            ]
            self.person_repo.db.execute_transaction(operations)
            print("✅ Все данные успешно удалены")
            return True
        except Exception as e:
            print(f"❌ Ошибка при удалении: {e}")
            return False

    def verify_all_deleted(self):
        """Проверяет что все таблицы пустые"""
        tables = ['notification', 'event', 'person_group', 'person', '[group]', '[user]']

        print("\n🔍 Проверка таблиц:")
        all_empty = True

        for table in tables:
            query = f"SELECT COUNT(*) as count FROM {table}"
            result = self.person_repo.db.execute_query(query, fetchone=True)
            count = result[0] if result else 0

            status = "✅ Пусто" if count == 0 else f"❌ Осталось {count} записей"
            print(f"{table:20s}: {status}")

            if count > 0:
                all_empty = False

        if all_empty:
            print("\n✅ ВСЕ ТАБЛИЦЫ ПУСТЫЕ")
        else:
            print("\n⚠️ НЕ ВСЕ ДАННЫЕ УДАЛЕНЫ!")

        return all_empty


def main():
    all_repo = AllRepository()
    data = all_repo.get_all_data()

    all_repo.del_all_data()
    all_repo.verify_all_deleted()










if __name__ == '__main__':
    main()
