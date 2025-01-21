import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.filters import filter_tasks, sort_tasks

class TestFilters(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            (1, 'Task 1', 'Description 1', '2023-12-31 23:59:59', 1, 0),
            (2, 'Task 2', 'Description 2', '2023-12-30 23:59:59', 2, 1),
            (3, 'Task 3', 'Description 3', '2023-12-29 23:59:59', 3, 0)
        ]

    def test_filter_tasks_by_status(self):
        filtered_tasks = filter_tasks(self.tasks, status=0)
        self.assertEqual(len(filtered_tasks), 2)

    def test_filter_tasks_by_priority(self):
        filtered_tasks = filter_tasks(self.tasks, priority=2)
        self.assertEqual(len(filtered_tasks), 1)

    def test_sort_tasks_by_deadline(self):
        sorted_tasks = sort_tasks(self.tasks, sort_by='deadline', ascending=True)
        self.assertEqual(sorted_tasks[0][0], 3)

    def test_sort_tasks_by_priority(self):
        sorted_tasks = sort_tasks(self.tasks, sort_by='priority', ascending=False)
        self.assertEqual(sorted_tasks[0][0], 3)

if __name__ == '__main__':
    unittest.main()