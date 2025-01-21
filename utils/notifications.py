from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QApplication
from PyQt5.QtCore import QTimer, QDateTime

from models.database import Database


class NotificationManager:
    def __init__(self, db, tray_icon):
        self.db: Database = db
        self.tray_icon: QSystemTrayIcon = tray_icon
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_deadlines)
        self.timer.start(60000)  # Check every minute

    def check_deadlines(self):
        """ Check task deadlines and generate notifications """
        tasks = self.db.get_tasks()
        now = QDateTime.currentDateTime()
        for task in tasks:
            deadline = QDateTime.fromString(task[3], "yyyy-MM-dd HH:mm:ss")
            if deadline <= now and not task[5]:  # Task is not completed
                self.show_notification(task)

    def show_notification(self, task):
        """ Show a notification for the given task """
        self.tray_icon.showMessage(
            "Task Reminder",
            f"Task '{task[1]}' is due!",
            QSystemTrayIcon.Information,
            5000  # Display for 5 seconds
        )