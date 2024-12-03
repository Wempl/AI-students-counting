import sys
from PyQt5 import QtWidgets
from login_window import LoginWindow
from main import MainApp
from auth_manager import init_db

class AuthMain:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        init_db()
        self.show_login_window()

    def show_login_window(self):
        self.login_window = LoginWindow(on_success=self.show_main_window)
        self.login_window.show()

    def show_main_window(self):
        self.main_window = MainApp()
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    program = AuthMain()
    program.run()
