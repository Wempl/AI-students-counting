from PyQt5 import QtWidgets, QtCore, QtGui


class RegistrationWindow(QtWidgets.QWidget):
    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 350)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Регистрация")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        # Поля ввода
        self.username_input = self.create_input("Логин")
        self.password_input = self.create_input("Пароль", True)
        self.password_repeat_input = self.create_input("Повтор пароля", True)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_repeat_input)

        # Кнопка регистрации
        register_button = QtWidgets.QPushButton("Зарегистрироваться")
        register_button.setFixedHeight(40)
        register_button.setStyleSheet(self.button_style("#28a745"))
        register_button.clicked.connect(self.handle_registration)
        layout.addWidget(register_button)

        # Ссылка на авторизацию
        switch_to_login_label = QtWidgets.QLabel('Есть аккаунт? <a href="#">Войдите</a>!')
        switch_to_login_label.setAlignment(QtCore.Qt.AlignCenter)
        switch_to_login_label.setStyleSheet("font-size: 12px; color: #0078D7;")
        switch_to_login_label.linkActivated.connect(self.handle_back)
        layout.addWidget(switch_to_login_label)

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
                border: 2px solid #28a745;
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
        return "#1e7e34"

    def handle_registration(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        password_repeat = self.password_repeat_input.text().strip()

        if not username or not password or not password_repeat:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if password != password_repeat:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        QtWidgets.QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались!")
        self.handle_back()

    def handle_back(self):
        if self.on_back:
            self.on_back()
        self.close()
