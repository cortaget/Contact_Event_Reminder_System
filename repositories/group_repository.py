from database import Database
from models import Group


class GroupRepository:
    def __init__(self):
        self.db = Database()

    def add_group(self, group):
        query = """
        INSERT INTO [group] (name)
        OUTPUT INSERTED.id
        VALUES (?)
        """
        return self.db.execute_insert_with_identity(query, group.to_tuple())



    def update_group(self, group):
        query = "UPDATE [group] SET name=? WHERE id=?"
        params = group.to_tuple() + (group.id,)
        return self.db.execute_query(query, params, commit=True)

    def delete_group(self, group_id):
        query = "DELETE FROM [group] WHERE id=?"
        return self.db.execute_query(query, (group_id,), commit=True)

    def get_group(self, group_id):
        query = "SELECT * FROM [group] WHERE id=?"
        row = self.db.execute_query(query, (group_id,), fetchone=True)
        if row:
            return Group(row.id, row.name)
        return None

    def get_all_groups(self):
        query = "SELECT * FROM [group] ORDER BY name"
        rows = self.db.execute_query(query, fetch=True)
        return [Group(r.id, r.name) for r in rows]
