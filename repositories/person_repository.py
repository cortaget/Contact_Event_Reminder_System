from database import Database
from models import Person


class PersonRepository:
    def __init__(self):
        self.db = Database()

    def add_person(self, person):
        query = """
        INSERT INTO person (first_name, last_name, birth_date, gender, is_active)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_insert_with_identity(query, person.to_tuple())

    def update_person(self, person):
        query = """
        UPDATE person 
        SET first_name=?, last_name=?, birth_date=?, gender=?, is_active=?
        WHERE id=?
        """
        params = person.to_tuple() + (person.id,)
        return self.db.execute_query(query, params, commit=True)

    def delete_person(self, person_id):
        query = "DELETE FROM person WHERE id=?"
        return self.db.execute_query(query, (person_id,), commit=True)

    def get_person(self, person_id):
        query = "SELECT * FROM person WHERE id=?"
        row = self.db.execute_query(query, (person_id,), fetchone=True)
        if row:
            return Person(row.id, row.first_name, row.last_name, row.birth_date, row.gender, row.is_active)
        return None

    def get_all_persons(self):
        query = "SELECT * FROM person ORDER BY last_name, first_name"
        rows = self.db.execute_query(query, fetch=True)
        return [Person(r.id, r.first_name, r.last_name, r.birth_date, r.gender, r.is_active) for r in rows]

    def find_person_by_name(self, name):
        query = """
        SELECT * FROM person 
        WHERE first_name LIKE ? OR last_name LIKE ?
        """
        pattern = f'%{name}%'
        rows = self.db.execute_query(query, (pattern, pattern), fetch=True)
        return [Person(r.id, r.first_name, r.last_name, r.birth_date, r.gender, r.is_active) for r in rows]

    def get_persons_by_group(self, group_id):
        query = """
        SELECT p.* FROM person p
        INNER JOIN person_group pg ON p.id = pg.person_id
        WHERE pg.group_id = ?
        """
        rows = self.db.execute_query(query, (group_id,), fetch=True)
        return [Person(r.id, r.first_name, r.last_name, r.birth_date, r.gender, r.is_active) for r in rows]
