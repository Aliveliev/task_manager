import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_database.db"
        self.db = Database(self.db_file)
        self.db.create_table()

    def tearDown(self):
        os.remove(self.db_file)

    def test_add_task(self):
        task = ('Test Task', 'Test Description', '2023-12-31 23:59:59', 1, 0)
        task_id = self.db.add_task(task)
        self.assertIsNotNone(task_id)

    def test_get_tasks(self):
        task = ('Test Task', 'Test Description', '2023-12-31 23:59:59', 1, 0)
        self.db.add_task(task)
        tasks = self.db.get_tasks()
        self.assertEqual(len(tasks), 1)

    def test_update_task(self):
        task = ('Test Task', 'Test Description', '2023-12-31 23:59:59', 1, 0)
        task_id = self.db.add_task(task)
        updated_task = ('Updated Task', 'Updated Description', '2023-12-31 23:59:59', 2, 1, task_id)
        self.db.update_task(updated_task)
        tasks = self.db.get_tasks()
        self.assertEqual(tasks[0][1], 'Updated Task')

    def test_delete_task(self):
        task = ('Test Task', 'Test Description', '2023-12-31 23:59:59', 1, 0)
        task_id = self.db.add_task(task)
        self.db.delete_task(task_id)
        tasks = self.db.get_tasks()
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()