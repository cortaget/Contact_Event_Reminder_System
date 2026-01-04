import pyodbc
from config import Config


class Database:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.get_connection_string()
        self._ensure_views_exist()  # Проверяем views при инициализации

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def execute_query(self, query, params=None, fetch=False, fetchone=False, commit=False):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())

            if commit:
                conn.commit()
                return cursor.rowcount

            if fetchone:
                return cursor.fetchone()

            if fetch:
                return cursor.fetchall()

            return None

    def execute_insert_with_identity(self, query, params=None):
        """Выполняет INSERT и возвращает ID новой записи через OUTPUT INSERTED.id"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Добавляем OUTPUT INSERTED.id в запрос
            # Ищем ключевое слово VALUES и вставляем перед ним OUTPUT
            if 'OUTPUT' not in query.upper():
                query = query.replace('VALUES', 'OUTPUT INSERTED.id VALUES')

            cursor.execute(query, params or ())
            result = cursor.fetchone()

            if result and result[0] is not None:
                new_id = int(result[0])
                conn.commit()
                return new_id
            else:
                conn.rollback()
                raise Exception("Не удалось получить ID новой записи")

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_transaction(self, operations):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for query, params in operations:
                cursor.execute(query, params or ())
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _ensure_views_exist(self):
        """Проверяет и создает необходимые views, если они не существуют"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Проверяем существование v_upcoming_events
            cursor.execute("""
                SELECT COUNT(*) FROM sys.views 
                WHERE name = 'v_upcoming_events'
            """)

            if cursor.fetchone()[0] == 0:
                # Создаем view
                cursor.execute("""
                    CREATE VIEW [dbo].[v_upcoming_events] AS
                    SELECT
                        e.id AS event_id,
                        e.event_date,
                        e.reminder_days_before,
                        e.reminder_time,
                        et.name AS event_type,
                        p.id AS person_id,
                        p.first_name,
                        p.last_name,
                        g.name AS group_name,
                        DATEDIFF(day, GETDATE(), e.event_date) AS days_until_event
                    FROM event e
                    INNER JOIN person p ON e.person_id = p.id
                    INNER JOIN event_type et ON e.event_type_id = et.id
                    LEFT JOIN person_group pg ON p.id = pg.person_id
                    LEFT JOIN [group] g ON pg.group_id = g.id
                    WHERE e.event_date >= CAST(GETDATE() AS DATE)
                """)
                conn.commit()

            # Проверяем v_event_summary
            cursor.execute("""
                SELECT COUNT(*) FROM sys.views 
                WHERE name = 'v_event_summary'
            """)

            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    CREATE VIEW [dbo].[v_event_summary] AS
                    SELECT
                        e.id AS event_id,
                        e.event_date,
                        e.reminder_days_before,
                        e.reminder_time,
                        et.name AS event_type,
                        p.first_name + ' ' + p.last_name AS person_name,
                        DATEDIFF(day, GETDATE(), e.event_date) AS days_until,
                        CASE
                            WHEN DATEDIFF(day, GETDATE(), e.event_date) < 0 THEN 'prošlé'
                            WHEN DATEDIFF(day, GETDATE(), e.event_date) = 0 THEN 'dnes'
                            WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 7 THEN 'tento týden'
                            WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 30 THEN 'tento měsíc'
                            ELSE 'budoucí'
                        END AS time_category
                    FROM event e
                    INNER JOIN person p ON e.person_id = p.id
                    INNER JOIN event_type et ON e.event_type_id = et.id
                """)
                conn.commit()

            # Проверяем v_group_statistics
            cursor.execute("""
                SELECT COUNT(*) FROM sys.views 
                WHERE name = 'v_group_statistics'
            """)

            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    CREATE VIEW [dbo].[v_group_statistics] AS
                    SELECT
                        g.id AS group_id,
                        g.name AS group_name,
                        COUNT(DISTINCT pg.person_id) AS total_persons,
                        COUNT(DISTINCT e.id) AS total_events
                    FROM [group] g
                    LEFT JOIN person_group pg ON g.id = pg.group_id
                    LEFT JOIN event e ON pg.person_id = e.person_id
                    GROUP BY g.id, g.name
                """)
                conn.commit()

            conn.close()

        except Exception as e:
            # Если возникла ошибка - игнорируем (возможно таблицы еще не созданы)
            print(f"Warning: Could not ensure views exist: {e}")
