import pyodbc

# Параметры подключения
server = 'LOCALHOST\\SQLEXPRESS'  # ВАЖНО: Укажите ваш Server Name из SSMS
database = 'ReminderApp'  # Имя созданной базы данных

server = 'Cronos\\SQLEXPRESS01'
database = 'Contact_Event_Reminder_System'

# Формирование строки подключения
# Driver может отличаться, см. раздел "Как узнать драйвер" ниже
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

try:
    # 1. Подключение
    conn = pyodbc.connect(connection_string)
    print("Успешное подключение к базе данных!")

    # 2. Создание курсора
    cursor = conn.cursor()

    # 3. Пример запроса (вставим тестового пользователя, если таблица пуста)
    cursor.execute("SELECT COUNT(*) FROM [user]")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Добавляем тестового пользователя...")
        insert_query = "INSERT INTO [user] (name, email) VALUES (?, ?)"
        cursor.execute(insert_query, ('Ivan Ivanov', 'ivan@test.com'))
        conn.commit()  # ВАЖНО: сохраняем изменения

    # 4. Чтение данных
    cursor.execute("SELECT * FROM [user]")
    rows = cursor.fetchall()

    print("\nСписок пользователей:")
    for row in rows:
        print(f"ID: {row.id}, Name: {row.name}, Email: {row.email}")

except pyodbc.Error as e:
    print(f"Ошибка подключения: {e}")

finally:
    # 5. Закрытие соединения
    if 'conn' in locals():
        conn.close()
        print("\nСоединение закрыто.")


if __name__ == '__main__':
    print()
