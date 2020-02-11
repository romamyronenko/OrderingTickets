import unittest
import service.db
import mysql.connector

db = service.db.DataBase(user='b86271d0784a40',
                         password='b40ff7a9',
                         host='us-cdbr-iron-east-04.cleardb.net',
                         database='heroku_a4b07b7f4d206f2')


class DataBaseTest(unittest.TestCase):
    def test_add_get_event(self):
        test_data = ('Test Event', '2000-12-11', 'Kyiv', 30)
        db.add_event(*test_data)

        result_data = list(db.get_event_by_name(test_data[0])[1:])
        result_data[1] = str(result_data[1])

        self.assertEqual(test_data, tuple(result_data))
        db.clear()
        db.close()
