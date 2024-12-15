from PyQt5 import QtWidgets, QtCore, QtGui
from registration_window import RegistrationWindow
from auth_manager import authenticate_user


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 300)
        self.on_success = on_success
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)

        # Заголовок
        title_label = QtWidgets.QLabel("Вход в аккаунт")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # Поля ввода
        self.username_input = self.create_input("Логин")
        self.password_input = self.create_input("Пароль", True)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        # Кнопка входа
        login_button = QtWidgets.QPushButton("Войти")
        login_button.setFixedHeight(40)
        login_button.setStyleSheet(self.button_style("#0078D7"))
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Ссылка на регистрацию
        register_label = QtWidgets.QLabel('Нет аккаунта? <a href="#">Создайте новый</a>!')
        register_label.setAlignment(QtCore.Qt.AlignCenter)
        register_label.setStyleSheet("font-size: 12px; color: #0078D7;")
        register_label.linkActivated.connect(self.open_registration_window)
        layout.addWidget(register_label)

    def create_input(self, placeholder, is_password=False):
        input_field = QtWidgets.QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
            }
        """)
        return input_field

    def button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """

    def darken_color(self, color):
        return "#005499" if color == "#0078D7" else "#1e7e34"

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return
        if authenticate_user(username, password):
            QtWidgets.QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.on_success()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def open_registration_window(self):
        self.close()
        self.registration_window = RegistrationWindow(on_back=self.show)
        self.registration_window.show()
