from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, QComboBox, QSpinBox, QCheckBox, QLabel, QFileDialog, QMenuBar, QMenu, QHeaderView

class MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QWidget(MainWindow)
        self.layout = QVBoxLayout(self.centralwidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6)  # Set the number of columns
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Title", "Description", "Deadline", "Priority", "Status"])
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable direct editing
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fit the table
        self.layout.addWidget(self.tableWidget)

        self.filter_layout = QHBoxLayout()
        
        self.statusFilterLabel = QLabel("Status Filter:")
        self.filter_layout.addWidget(self.statusFilterLabel)
        self.statusFilter = QComboBox()
        self.statusFilter.addItems(["All", "Incomplete", "Complete"])
        self.filter_layout.addWidget(self.statusFilter)

        self.priorityFilterLabel = QLabel("Priority Filter:")
        self.filter_layout.addWidget(self.priorityFilterLabel)
        self.priorityFilter = QSpinBox()
        self.priorityFilter.setRange(1, 5)
        self.priorityFilter.setPrefix("Priority ")
        self.priorityFilter.setSpecialValueText("Any")
        self.filter_layout.addWidget(self.priorityFilter)
        self.priorityFilterCheckBox = QCheckBox("Enable")
        self.filter_layout.addWidget(self.priorityFilterCheckBox)

        self.filterButton = QPushButton("Apply Filters")
        self.filter_layout.addWidget(self.filterButton)
        self.layout.addLayout(self.filter_layout)

        self.sort_layout = QHBoxLayout()
        
        self.sortByLabel = QLabel("Sort By:")
        self.sort_layout.addWidget(self.sortByLabel)
        self.sortBy = QComboBox()
        self.sortBy.addItems(["ID", "Title", "Description", "Deadline", "Priority", "Status"])
        self.sort_layout.addWidget(self.sortBy)

        self.sortOrderLabel = QLabel("Sort Order:")
        self.sort_layout.addWidget(self.sortOrderLabel)
        self.sortOrder = QComboBox()
        self.sortOrder.addItems(["Ascending", "Descending"])
        self.sort_layout.addWidget(self.sortOrder)

        self.sortButton = QPushButton("Apply Sorting")
        self.sort_layout.addWidget(self.sortButton)
        self.layout.addLayout(self.sort_layout)

        self.button_layout = QHBoxLayout()
        self.addButton = QPushButton("Add Task")
        self.button_layout.addWidget(self.addButton)
        self.editButton = QPushButton("Edit Task")
        self.button_layout.addWidget(self.editButton)
        self.deleteButton = QPushButton("Delete Task")
        self.button_layout.addWidget(self.deleteButton)
        self.exportButton = QPushButton("Export Tasks")
        self.button_layout.addWidget(self.exportButton)
        self.layout.addLayout(self.button_layout)

        self.pagination_layout = QHBoxLayout()
        self.prevPageButton = QPushButton("Previous Page")
        self.pagination_layout.addWidget(self.prevPageButton)
        self.pageInfoLabel = QLabel("Page 1 of 1")
        self.pagination_layout.addWidget(self.pageInfoLabel)
        self.nextPageButton = QPushButton("Next Page")
        self.pagination_layout.addWidget(self.nextPageButton)
        self.layout.addLayout(self.pagination_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)

        self.menuThemes = QMenu("Themes", self.menubar)
        self.menubar.addMenu(self.menuThemes)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Task Manager")