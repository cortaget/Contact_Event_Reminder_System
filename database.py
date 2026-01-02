import pyodbc
from config import Config


class Database:
    def __init__(self):
        self.config = Config()
        self.connection_string = self.config.get_connection_string()

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
