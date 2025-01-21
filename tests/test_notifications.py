import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtCore import QDateTime
from utils.notifications import NotificationManager
from models.database import Database

class TestNotifications(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Database)
        self.tray_icon = MagicMock()
        self.tray_icon.Information = 1  # Set the Information attribute
        self.notification_manager = NotificationManager(self.db, self.tray_icon)

    def test_check_deadlines(self):
        tasks = [
            (1, 'Task 1', 'Description 1', '2023-12-31 23:59:59', 1, 0),
            (2, 'Task 2', 'Description 2', '2023-12-30 23:59:59', 2, 1)
        ]
        self.db.get_tasks.return_value = tasks
        self.notification_manager.check_deadlines()
        self.tray_icon.showMessage.assert_called_once_with(
            "Task Reminder",
            "Task 'Task 1' is due!",
            self.tray_icon.Information,
            5000
        )

if __name__ == '__main__':
    unittest.main()