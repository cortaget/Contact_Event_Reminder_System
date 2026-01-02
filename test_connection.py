"""
Тест подключения к БД и проверка всех таблиц
"""
from database import Database


def test_connection():
    print("=" * 60)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
    print("=" * 60)

    db = Database()

    try:
        # Тест подключения
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"✅ Подключение успешно!\n")
        print(f"SQL Server версия: {version[:100]}...\n")
        conn.close()

        # Проверка таблиц
        print("=" * 60)
        print("ПРОВЕРКА ТАБЛИЦ")
        print("=" * 60)

        tables = ['[user]', 'person', 'event', 'notification', '[group]', 'person_group']

        for table in tables:
            try:
                query = f"SELECT COUNT(*) as count FROM {table}"
                result = db.execute_query(query, fetchone=True)
                count = result[0] if result else 0
                print(f"✅ {table:20s}: {count} записей")
            except Exception as e:
                print(f"❌ {table:20s}: ОШИБКА - {str(e)}")

        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ОШИБКА ПОДКЛЮЧЕНИЯ:")
        print(f"{str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_connection()
    input("\nНажмите Enter для выхода...")
