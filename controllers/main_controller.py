from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDialog, QSystemTrayIcon, QStyle, QFileDialog, QAction
from ui.main_window import MainWindow
from models.database import Database
from controllers.task_controller import TaskController
from utils.filters import filter_tasks, sort_tasks
from utils.notifications import NotificationManager
from utils.export import export_tasks_to_csv

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.db = Database("database.db")
        self.current_page = 0
        self.page_size = 10
        self.total_tasks = self.db.get_task_count()
        self.total_pages = (self.total_tasks + self.page_size - 1) // self.page_size
        self.load_tasks()

        # Connect buttons to their respective methods
        self.ui.addButton.clicked.connect(self.add_task)
        self.ui.editButton.clicked.connect(self.edit_task)
        self.ui.deleteButton.clicked.connect(self.delete_task)
        self.ui.filterButton.clicked.connect(self.apply_filters)
        self.ui.sortButton.clicked.connect(self.apply_sorting)
        self.ui.exportButton.clicked.connect(self.export_tasks)
        self.ui.nextPageButton.clicked.connect(self.next_page)
        self.ui.prevPageButton.clicked.connect(self.prev_page)

        # Setup system tray icon for notifications
        self.tray_icon = QSystemTrayIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.show()
        self.notification_manager = NotificationManager(self.db, self.tray_icon)

        # Setup theme actions
        self.setup_theme_actions()

    def setup_theme_actions(self):
        """ Setup actions for theme switching """
        light_theme_action = QAction("Light Theme", self)
        light_theme_action.triggered.connect(lambda: self.apply_theme("resources/themes/light_theme.css"))
        dark_theme_action = QAction("Dark Theme", self)
        dark_theme_action.triggered.connect(lambda: self.apply_theme("resources/themes/dark_theme.css"))

        self.ui.menuThemes.addAction(light_theme_action)
        self.ui.menuThemes.addAction(dark_theme_action)

    def apply_theme(self, theme_path):
        """ Apply the selected theme """
        with open(theme_path, "r") as file:
            self.setStyleSheet(file.read())

    def load_tasks(self):
        """ Load tasks from the database into the table """
        self.tasks = self.db.get_tasks(limit=self.page_size, offset=self.current_page * self.page_size)
        self.display_tasks(self.tasks)
        self.update_page_info()

    def display_tasks(self, tasks):
        """ Display tasks in the table """
        self.ui.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(tasks):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def next_page(self):
        """ Go to the next page of tasks """
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_tasks()

    def prev_page(self):
        """ Go to the previous page of tasks """
        if self.current_page > 0:
            self.current_page -= 1
            self.load_tasks()

    def update_page_info(self):
        """ Update the page information label """
        self.ui.pageInfoLabel.setText(f"Page {self.current_page + 1} of {self.total_pages}")

    def add_task(self):
        """ Add a new task to the database and refresh the table """
        dialog = TaskController(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.total_tasks = self.db.get_task_count()
            self.total_pages = (self.total_tasks + self.page_size - 1) // self.page_size
            self.load_tasks()

    def edit_task(self):
        """ Edit the selected task in the database and refresh the table """
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            task_id = int(self.ui.tableWidget.item(selected_row, 0).text())
            task = self.db.get_task(task_id)
            dialog = TaskController(self.db, task)
            if dialog.exec_() == QDialog.Accepted:
                self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to edit")

    def delete_task(self):
        """ Delete the selected task from the database and refresh the table """
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            task_id = int(self.ui.tableWidget.item(selected_row, 0).text())
            self.db.delete_task(task_id)
            self.total_tasks = self.db.get_task_count()
            self.total_pages = (self.total_tasks + self.page_size - 1) // self.page_size
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task to delete")

    def apply_filters(self):
        """ Apply filters to the task list """
        status = self.ui.statusFilter.currentIndex() - 1  # Assuming -1 means no filter
        priority = self.ui.priorityFilter.value() if self.ui.priorityFilterCheckBox.isChecked() else None
        filtered_tasks = filter_tasks(self.tasks, status if status >= 0 else None, priority)
        self.display_tasks(filtered_tasks)

    def apply_sorting(self):
        """ Apply sorting to the task list """
        sort_by = self.ui.sortBy.currentText().lower()
        ascending = self.ui.sortOrder.currentIndex() == 0
        sorted_tasks = sort_tasks(self.tasks, sort_by, ascending)
        self.display_tasks(sorted_tasks)

    def export_tasks(self):
        """ Export tasks to a CSV file """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if file_path:
            export_tasks_to_csv(self.tasks, file_path)
            QMessageBox.information(self, "Export Successful", f"Tasks have been exported to {file_path}")