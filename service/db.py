import sqlite3


class DataBase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        for i in open('../sql/create_tables.sql', 'r').read().split(';'):
            self.cursor.execute(i)

    def add_event(self, name, date, place, total_available):
        self.cursor.execute('INSERT INTO event(Name, Date, Place, `Total Available`) VALUES("%s", "%s", "%s", %s)' %
                            (name, date, place, total_available))

    def get_event(self, id):
        self.cursor.execute('SELECT * FROM event WHERE `Name` = "%s"'%id)
        self.conn.commit()
        return self.cursor.fetchall()


dv = DataBase('db.db')
dv.add_event('Event', '2000-11-14', 'Kyiv', 30)

print(dv.get_event('Event'))
