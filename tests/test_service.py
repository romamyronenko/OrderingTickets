import unittest
import service.db
import mysql.connector

USER = 'b86271d0784a40'
PASS = 'b40ff7a9'
HOST = 'us-cdbr-iron-east-04.cleardb.net'
DATABASE = 'heroku_a4b07b7f4d206f2'


class DataBaseTest(unittest.TestCase):
    def setUp(self):
        self.db = service.db.DataBase(user=USER,
                                      password=PASS,
                                      host=HOST,
                                      database=DATABASE)
        self.db.clear()
        self.db.create_tables()
        self.db.conn.commit()
        self.conn = mysql.connector.connect(user=USER,
                                            password=PASS,
                                            host=HOST,
                                            database=DATABASE)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        self.db.close()

    def test_add_event(self):
        test_data = ('Test Event', '2000-12-11', 'Kyiv', 30, 300)

        self.db.add_event(*test_data)
        self.db.conn.commit()

        self.cursor.execute("SELECT * FROM event WHERE Name='Test Event'")
        result_data = list(self.cursor.fetchone()[1:])
        result_data[1] = str(result_data[1])
        self.assertEqual(test_data, tuple(result_data))

    def test_get_event(self):
        test_data = ('Quest', '2020-10-11', 'Obolon', 30, 500)
        self.cursor.execute('INSERT INTO event (Name, Date, Place, `Total Available`, Price) VALUE '
                            '(%s, %s, %s, %s, %s)', test_data)
        self.conn.commit()
        result_data = list(self.db.get_event_by_name(test_data[0])[1:])
        result_data[1] = str(result_data[1])
        self.assertEqual(test_data, tuple(result_data))

    def test_edit_event(self):
        test_data = ('Meet', '2020-10-11', 'Kyiv', 30, 500)
        new_data = ('Meet', '2020-10-11', 'Lviv', 30, 900)
        self.cursor.execute('INSERT INTO event (Name, Date, Place, `Total Available`, Price) VALUE '
                            '(%s, %s, %s, %s, %s)', test_data)
        self.cursor.execute('SELECT id FROM event WHERE Name=%s', (test_data[0],))
        event_id = self.cursor.fetchone()[0]
        self.conn.commit()
        self.db.edit_event(event_id, new_data[0], new_data[1], new_data[2], new_data[3], new_data[4])
        self.db.conn.commit()

        self.cursor.execute('SELECT * FROM event WHERE Name=%s', (test_data[0],))
        result_data = list(self.cursor.fetchone())[1:]
        result_data[1] = str(result_data[1])

        self.assertEqual(new_data, tuple(result_data))

    def test_delete_event(self):
        test_data = ('Event to Delete', '2020-10-11', 'Obolon', 30, 500)
        self.cursor.execute('INSERT INTO event (Name, Date, Place, `Total Available`, Price) VALUE '
                            '(%s, %s, %s, %s, %s)', test_data)
        self.cursor.execute('SELECT id FROM event WHERE Name=%s', (test_data[0],))
        event_id = self.cursor.fetchone()[0]
        self.conn.commit()
        self.db.remove_event(event_id)
        self.db.conn.commit()
        self.assertFalse(self.cursor.fetchone())
