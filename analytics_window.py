from PyQt5 import QtWidgets, QtCore
import os

class AnalyticsWindow(QtWidgets.QWidget):
    def __init__(self, class_name):
        super().__init__()
        self.setWindowTitle(f"Аналитика - {class_name}")
        self.setFixedSize(800, 600)
        self.class_name = class_name
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #f8f9fa;")
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel(f"Аналитика посещаемости для класса: {self.class_name}")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Дата", "Присутствующие", "Отсутствующие"])
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                background-color: white;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: white;
                padding: 5px;
            }
        """)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        logs_dir = os.path.join("classes", self.class_name, "logs")
        if not os.path.exists(logs_dir):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логи для этого класса не найдены.")
            return

        log_files = sorted(os.listdir(logs_dir))
        self.table.setRowCount(len(log_files))
        for i, log_file in enumerate(log_files):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(log_file.replace(".txt", "")))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem("Присутствующие"))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem("Отсутствующие"))
