from database import Database


class PersonGroupRepository:
    def __init__(self):
        self.db = Database()

    def add_person_to_group(self, person_id, group_id):
        query = "INSERT INTO person_group (person_id, group_id) VALUES (?, ?)"
        return self.db.execute_query(query, (person_id, group_id), commit=True)

    def remove_person_from_group(self, person_id, group_id):
        query = "DELETE FROM person_group WHERE person_id=? AND group_id=?"
        return self.db.execute_query(query, (person_id, group_id), commit=True)

    def get_groups_for_person(self, person_id):
        query = """
        SELECT g.* FROM [group] g
        INNER JOIN person_group pg ON g.id = pg.group_id
        WHERE pg.person_id = ?
        """
        rows = self.db.execute_query(query, (person_id,), fetch=True)
        from models import Group
        return [Group(r.id, r.name) for r in rows]

    def get_persons_in_group(self, group_id):
        query = """
        SELECT p.* FROM person p
        INNER JOIN person_group pg ON p.id = pg.person_id
        WHERE pg.group_id = ?
        """
        rows = self.db.execute_query(query, (group_id,), fetch=True)
        from models import Person
        return [Person(r.id, r.first_name, r.last_name, r.birth_date, r.gender, r.is_active) for r in rows]
