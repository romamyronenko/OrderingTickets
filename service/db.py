import mysql.connector


class DataBase:
    def __init__(self, user, password, host, database, path_to_sql=''):
        self.path_to_sql = path_to_sql
        self.conn = mysql.connector.connect(user=user,
                                            password=password,
                                            host=host,
                                            database=database)

        self.cursor = self.conn.cursor()
        self.create_tables()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def clear(self):
        self.cursor.execute('show tables')
        if self.cursor.fetchall():
            self.cursor.execute('drop table ticket')
            self.cursor.execute('drop table event')

    def create_tables(self):
        for i in open(self.path_to_sql+'sql/create_tables.sql', 'r').read().split(';'):
            self.cursor.execute(i)

    def add_event(self, name, date, place, total_available):
        self.cursor.execute('INSERT INTO event(`Name`, Date, Place, `Total Available`) VALUES("%s", "%s", "%s", %s)' %
                            (name, date, place, total_available))

    def add_ticket(self, event_id, owner):
        self.cursor.execute('INSERT INTO ticket(event_id, owner) VALUES(%s, "%s")',
                            (event_id, owner))

    def get_event_by_name(self, name):
        self.cursor.execute('SELECT * FROM event WHERE Name=%s', (name,))
        return self.cursor.fetchone()

    def get_event_by_id(self, event_id):
        self.cursor.execute('SELECT * FROM event WHERE id=%s', (event_id,))
        return self.cursor.fetchone()

    def get_ticket(self, ticket_id):
        self.cursor.execute('SELECT * FROM ticket WHERE id=%s', (ticket_id,))
        return self.cursor.fetchone()

    def get_events(self):
        self.cursor.execute('SELECT * FROM event')
        return self.cursor.fetchall()

    def get_tickets(self):
        self.cursor.execute('SELECT * FROM ticket')
        return self.cursor.fetchall()

    def edit_event(self, event_id, new_name, new_date, new_place, new_ta):
        """Edit info about event."""
        self.cursor.execute('UPDATE event SET Name = %s, Date = %s, Place = %s, `Total Available` = %s WHERE id = %s',
                            (new_name, new_date, new_place, new_ta, event_id))

    def edit_ticket(self, ticket_id, new_event_id, new_owner):
        self.cursor.execute('UPDATE ticket SET event_id = %s, owner = %s WHERE id = %s',
                            (new_event_id, new_owner, ticket_id))

    def remove_event(self, event_id):
        self.cursor.execute('DELETE FROM event WHERE id=%s', (event_id,))

    def remove_ticket(self, ticket_id):
        self.cursor.execute('DELETE FROM ticket WHERE id=%s', (ticket_id,))

