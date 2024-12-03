from PyQt5 import QtWidgets, QtGui, QtCore
import os

class AnalyticsWindow(QtWidgets.QWidget):
    def __init__(self, class_name):
        super().__init__()
        self.setWindowTitle(f"Аналитика: {class_name}")
        self.setFixedSize(800, 600)

        self.class_name = class_name
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel(f"Аналитика посещаемости для класса: {self.class_name}")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Дата", "Присутствующие", "Отсутствующие"])
        layout.addWidget(self.table)

        self.load_logs()

        self.setLayout(layout)

    def load_logs(self):
        logs_dir = os.path.join("classes", self.class_name, "logs")
        if not os.path.exists(logs_dir):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логи для этого класса не найдены.")
            return

        try:
            log_files = sorted(os.listdir(logs_dir))
            for log_file in log_files:
                with open(os.path.join(logs_dir, log_file), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    self.logs_table.addItem(f"{log_file}: {''.join(lines[:1])}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении логов: {e}")
            