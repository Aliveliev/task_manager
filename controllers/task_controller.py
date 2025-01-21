from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDateTime
from ui.task_dialog import TaskDialog
from models.database import Database


class TaskController(QDialog):
    def __init__(self, db, task=None):
        super().__init__()
        self.ui = TaskDialog()
        self.ui.setupUi(self)
        self.db: Database = db
        self.task = task

        if self.task:
            self.load_task_data()

        self.ui.save_button.clicked.connect(self.save_task)
        self.ui.cancel_button.clicked.connect(self.reject)

    def load_task_data(self):
        """ Load task data into the dialog fields """
        self.ui.title_edit.setText(self.task[1])
        self.ui.description_edit.setText(self.task[2])
        # Convert string to QDateTime
        deadline = QDateTime.fromString(self.task[3], "yyyy-MM-dd HH:mm:ss")
        self.ui.deadline_edit.setDateTime(deadline)
        self.ui.priority_edit.setValue(self.task[4])
        self.ui.status_checkbox.setChecked(self.task[5])

    def validate_input(self):
        """ Validate the input data """
        if not self.ui.title_edit.text():
            QMessageBox.warning(self, "Input Error", "Title cannot be empty")
            return False
        return True

    def save_task(self):
        """ Save the task to the database """
        if not self.validate_input():
            return

        title = self.ui.title_edit.text()
        description = self.ui.description_edit.toPlainText()
        deadline = self.ui.deadline_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        priority = self.ui.priority_edit.value()
        status = self.ui.status_checkbox.isChecked()

        if self.task:
            task_id = self.task[0]
            updated_task = (title, description, deadline, priority, status, task_id)
            self.db.update_task(updated_task)
        else:
            new_task = (title, description, deadline, priority, status)
            self.db.add_task(new_task)

        self.accept()