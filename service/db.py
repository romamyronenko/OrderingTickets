import mysql.connector


class DataBase:
    def __init__(self, user, password, host, database):
        self.conn = mysql.connector.connect(user=user,
                                            password=password,
                                            host=host,
                                            database=database)

        self.cursor = self.conn.cursor()
        self.create_tables()

    def close(self):
        """Save changes and close database"""
        self.conn.commit()
        self.conn.close()

    def clear(self):
        """Drop tables from database"""
        self.cursor.execute('show tables')
        if self.cursor.fetchall():
            self.cursor.execute('drop table ticket')
            self.cursor.execute('drop table event')

    def create_tables(self):
        """Create tables in databas"""
        for i in open('sql/create_tables.sql', 'r').read().split(';'):
            self.cursor.execute(i)

    def add_event(self, name, date, place, total_available, price):
        """Create new event"""
        self.cursor.execute('INSERT INTO event(`Name`, Date, Place, `Total Available`, Price) VALUES("%s", "%s", "%s", %s, %s)' %
                            (name, date, place, total_available, price))

    def add_ticket(self, event_id, owner):
        """Create new ticket"""
        self.cursor.execute('INSERT INTO ticket(event_id, owner) VALUES(%s, "%s")',
                            (event_id, owner))

    def get_event_by_name(self, name):
        """Return data of event by name"""
        self.cursor.execute('SELECT * FROM event WHERE Name=%s', (name,))
        return self.cursor.fetchone()

    def get_event_by_id(self, event_id):
        """Return data of event by id"""
        self.cursor.execute('SELECT * FROM event WHERE id=%s', (event_id,))
        return self.cursor.fetchone()

    def get_ticket(self, ticket_id):
        """Return data of ticket by id"""
        self.cursor.execute('SELECT * FROM ticket WHERE id=%s', (ticket_id,))
        return self.cursor.fetchone()

    def get_events(self):
        """Return list of events"""
        self.cursor.execute('SELECT * FROM event')
        return self.cursor.fetchall()

    def get_tickets(self):
        """Return list of tickets"""
        self.cursor.execute('SELECT * FROM ticket')
        return self.cursor.fetchall()

    def edit_event(self, event_id, new_name, new_date, new_place, new_ta, price):
        """Edit info about event."""
        self.cursor.execute('UPDATE event SET Name = %s, Date = %s, Place = %s, `Total Available` = %s, Price = %s '
                            'WHERE id = %s',
                            (new_name, new_date, new_place, new_ta, price, event_id))

    def edit_ticket(self, ticket_id, new_event_id, new_owner):
        """Edit info about ticket"""
        self.cursor.execute('UPDATE ticket SET event_id = %s, owner = %s WHERE id = %s',
                            (new_event_id, new_owner, ticket_id))

    def remove_event(self, event_id):
        """Remove event"""
        self.cursor.execute('DELETE FROM event WHERE id=%s', (event_id,))

    def remove_ticket(self, ticket_id):
        """Remove ticket"""
        self.cursor.execute('DELETE FROM ticket WHERE id=%s', (ticket_id,))

