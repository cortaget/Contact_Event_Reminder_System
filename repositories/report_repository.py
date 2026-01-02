from database import Database


class ReportRepository:
    def __init__(self):
        self.db = Database()

    def get_upcoming_events_report(self, days_ahead=30):
        query = """
        SELECT 
            e.id, e.event_type, e.event_date,
            p.first_name, p.last_name,
            g.name as group_name
        FROM event e
        INNER JOIN person p ON e.person_id = p.id
        LEFT JOIN person_group pg ON p.id = pg.person_id
        LEFT JOIN [group] g ON pg.group_id = g.id
        WHERE e.event_date BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(day, ?, CAST(GETDATE() AS DATE))
        ORDER BY e.event_date
        """
        return self.db.execute_query(query, (days_ahead,), fetch=True)

    def get_events_statistics_by_group(self):
        query = """
        SELECT 
            ISNULL(g.name, 'Bez skupiny') as group_name,
            COUNT(e.id) as event_count
        FROM [group] g
        LEFT JOIN person_group pg ON g.id = pg.group_id
        LEFT JOIN person p ON pg.person_id = p.id
        LEFT JOIN event e ON p.id = e.person_id
        GROUP BY g.name
        ORDER BY event_count DESC
        """
        return self.db.execute_query(query, fetch=True)

    def get_notifications_statistics(self):
        query = """
        SELECT 
            status,
            COUNT(*) as count
        FROM notification
        GROUP BY status
        ORDER BY count DESC
        """
        return self.db.execute_query(query, fetch=True)

    def get_persons_statistics(self):
        query = """
        SELECT 
            ISNULL(g.name, 'Bez skupiny') as group_name,
            COUNT(DISTINCT p.id) as person_count
        FROM [group] g
        LEFT JOIN person_group pg ON g.id = pg.group_id
        LEFT JOIN person p ON pg.person_id = p.id
        GROUP BY g.name
        ORDER BY person_count DESC
        """
        return self.db.execute_query(query, fetch=True)
