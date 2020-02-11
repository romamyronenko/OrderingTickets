import unittest
import service.db
import mysql.connector

db = service.db.DataBase(user='debian-sys-maint',
                         password='PggWbsvEVgDZUYar',
                         host='127.0.0.1',
                         database='ordtick_test', path_to_sql='../')


class DataBaseTest(unittest.TestCase):
    def test_add_get_event(self):
        test_data = ('Test Event', '2000-12-11', 'Kyiv', 30)
        db.add_event(*test_data)

        result_data = list(db.get_event_by_name(test_data[0])[1:])
        result_data[1] = str(result_data[1])

        self.assertEqual(test_data, tuple(result_data))
        db.clear()
        db.close()
