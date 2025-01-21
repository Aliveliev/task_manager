import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    try:
        controller = MainController()
        controller.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_message = f"An unexpected error occurred:\n{str(e)}"
        QMessageBox.critical(None, "Application Error", error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()