from PyQt5 import QtWidgets, QtCore
from auth_manager import init_db, register_user, authenticate_user

class AuthWindow(QtWidgets.QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 300)
        self.on_success = on_success 

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()


        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if authenticate_user(username, password):
            QtWidgets.QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.on_success()  
            self.parent_window.logged_in_user = username
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if register_user(username, password):
            QtWidgets.QMessageBox.information(self, "Успех", "Регистрация успешна! Теперь вы можете войти.")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Имя пользователя уже существует.")
