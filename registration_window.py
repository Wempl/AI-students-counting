from PyQt5 import QtWidgets, QtCore


class RegistrationWindow(QtWidgets.QWidget):
    switch_to_login = QtCore.pyqtSignal()  # Сигнал для перехода к окну авторизации

    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back  # Сохраняем функцию "назад", если передана
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Регистрация")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.password_repeat_input = QtWidgets.QLineEdit()
        self.password_repeat_input.setPlaceholderText("Повтор пароля")
        self.password_repeat_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_repeat_input)

        register_button = QtWidgets.QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.handle_registration)
        layout.addWidget(register_button)

        switch_to_login_label = QtWidgets.QLabel('Есть аккаунт? <a href="#" color="blue">Войдите</a>!')
        switch_to_login_label.setAlignment(QtCore.Qt.AlignCenter)
        switch_to_login_label.setOpenExternalLinks(False)
        switch_to_login_label.linkActivated.connect(self.handle_back)
        layout.addWidget(switch_to_login_label)

        self.setLayout(layout)

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

        try:
            from auth_manager import register_user
            success = register_user(username, password)
            if success:
                QtWidgets.QMessageBox.information(self, "Успех", "Вы успешно зарегистрировались!")
                self.handle_back()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка регистрации: {e}")

    def handle_back(self):
        """Возвращает к окну входа."""
        if self.on_back:
            self.on_back()
        else:
            self.switch_to_login.emit()
        self.close()  # Закрываем окно регистрации
