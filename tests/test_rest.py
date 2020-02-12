import unittest
import app
import mysql.connector

USER = 'b86271d0784a40'
PASS = 'b40ff7a9'
HOST = 'us-cdbr-iron-east-04.cleardb.net'
DATABASE = 'heroku_a4b07b7f4d206f2'


class DataBaseTest(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(user=USER,
                                            password=PASS,
                                            host=HOST,
                                            database=DATABASE)
        self.cursor = self.conn.cursor()

        for i in open('sql/create_tables.sql', 'r').read().split(';'):
            self.cursor.execute(i)

        self.conn.commit()

        app_test = app
        app_test.DATABASE = DATABASE
        app_test.USER = USER
        app_test.HOST = HOST
        app_test.PASS = PASS
        self.client = app_test.app.test_client()

    def tearDown(self):
        self.cursor.execute('DROP TABLE ticket')
        self.cursor.execute('DROP TABLE event')
        self.conn.close()

    def test_events_get(self):
        test_data = ('Test Event', '2000-12-11', 'Kyiv', 30, 300)
        self.cursor.execute('INSERT INTO event (`Name`, `Date`, `Place`, `Total Available`, `Price`) VALUE '
                            '(%s, %s, %s, %s, %s)', test_data)
        self.conn.commit()

        response = self.client.get('/events')
