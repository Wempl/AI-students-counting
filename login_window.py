from PyQt5 import QtWidgets, QtCore
from registration_window import RegistrationWindow
from auth_manager import authenticate_user


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 250)
        self.on_success = on_success  # Функция, вызываемая при успешной авторизации
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Заголовок
        title_label = QtWidgets.QLabel("Вход в аккаунт")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # Поле логина
        login_layout = QtWidgets.QHBoxLayout()
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        login_layout.addWidget(self.username_input)
        layout.addLayout(login_layout)

        # Поле пароля
        password_layout = QtWidgets.QHBoxLayout()
        self.password_input = QtWidgets.QLineEdit()  # Сначала создаем объект
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Ссылка на регистрацию
        register_label = QtWidgets.QLabel()
        register_label.setText("Нет аккаунта? <a href='#' color='blue'>Создайте новый</a>!")
        register_label.setAlignment(QtCore.Qt.AlignCenter)
        register_label.setStyleSheet("font-size: 12px;")
        register_label.linkActivated.connect(self.open_registration_window)
        layout.addWidget(register_label)

        # Кнопка Войти
        login_button = QtWidgets.QPushButton("Войти")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Проверяем, чтобы все поля были заполнены
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        # Аутентификация пользователя
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
