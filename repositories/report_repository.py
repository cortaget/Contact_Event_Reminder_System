from database import Database


class ReportRepository:
    def __init__(self):
        self.db = Database()

    def get_upcoming_events_report(self, days_ahead=30):
        """Получить ближайшие события (используя VIEW)"""
        query = """
        SELECT * FROM v_upcoming_events 
        WHERE days_until_event <= ? 
        ORDER BY event_date
        """
        return self.db.execute_query(query, (days_ahead,), fetch=True)

    def get_events_by_category(self, category='все'):
        """Получить события по категории времени (используя VIEW)"""
        if category == 'все':
            query = "SELECT * FROM v_event_summary ORDER BY event_date"
            return self.db.execute_query(query, fetch=True)
        else:
            query = "SELECT * FROM v_event_summary WHERE time_category = ? ORDER BY event_date"
            return self.db.execute_query(query, (category,), fetch=True)

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
