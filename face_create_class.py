from PyQt5 import QtWidgets, QtGui, QtCore
import os
import shutil
import face_recognition
import numpy as np
import sys

class AddStudentsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, student_count, parent_window):
        super().__init__()
        self.class_name = class_name
        self.student_count = student_count
        self.parent_window = parent_window
        self.added_students = 0
        self.students_data = {}
        self.setWindowTitle(f"Добавление учеников - {class_name}")
        self.setFixedSize(600, 450)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel(f"Добавление учеников - {self.class_name}")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        self.student_count_label = QtWidgets.QLabel(f"Кол-во учеников: {self.added_students}/{self.student_count}")
        self.student_count_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.student_count_label)

        self.add_photo_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_photo_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005499;
            }
        """)
        self.add_photo_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_photo_button)

        self.students_list = QtWidgets.QListWidget()
        layout.addWidget(self.students_list)

        self.finish_button = QtWidgets.QPushButton("Завершить")
        self.finish_button.setEnabled(False)
        self.finish_button.clicked.connect(self.finish_adding)
        self.finish_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

    def add_student(self):
        photo_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Выберите фотографии ученика", "", "Images (*.png *.jpg *.jpeg)")
        if photo_paths:
            student_name, ok = QtWidgets.QInputDialog.getText(self, "Имя ученика", "Введите имя ученика:")
            if ok and student_name:
                self.students_list.addItem(f"{student_name} - {len(photo_paths)} фото")
                self.added_students += 1
                self.student_count_label.setText(f"Кол-во учеников: {self.added_students}/{self.student_count}")
                if self.added_students >= self.student_count:
                    self.finish_button.setEnabled(True)

    def finish_adding(self):
        QtWidgets.QMessageBox.information(self, "Завершено", "Ученики добавлены!")
        self.close()

class CreateClassWindow(QtWidgets.QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание нового класса")
        self.setFixedSize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Название класса
        class_name_label = QtWidgets.QLabel("Название класса:")
        class_name_label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(class_name_label)

        self.class_name_input = QtWidgets.QLineEdit()
        self.class_name_input.setPlaceholderText("Введите название класса")
        self.class_name_input.setFixedHeight(40)
        self.class_name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.class_name_input)

        # Количество учеников
        student_count_label = QtWidgets.QLabel("Количество учеников:")
        student_count_label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(student_count_label)

        self.student_count_input = QtWidgets.QSpinBox()
        self.student_count_input.setRange(1, 100)
        self.student_count_input.setFixedHeight(40)
        self.student_count_input.setStyleSheet("""
            QSpinBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                height: 20px;
                border-left: 1px solid #aaa;
                border-top-right-radius: 5px;
                background: #e0e0e0;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                height: 20px;
                border-left: 1px solid #aaa;
                border-bottom-right-radius: 5px;
                background: #e0e0e0;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #d0d0d0;
            }
            QSpinBox::up-arrow {
                image: url(icons/33.png);
                width: 10px;
                height: 10px;
            }
            QSpinBox::down-arrow {
                image: url(icons/22.png);
                width: 10px;
                height: 10px;
            }
        """)
        layout.addWidget(self.student_count_input)

        # Создание класса
        self.create_class_button = QtWidgets.QPushButton("Создать класс")
        self.create_class_button.setFixedHeight(40)
        self.create_class_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.create_class_button.clicked.connect(self.create_class)
        layout.addWidget(self.create_class_button)

        self.setLayout(layout)

    def create_class(self):
        class_name = self.class_name_input.text().strip()
        student_count = self.student_count_input.value()

        if not class_name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите название класса!")
            return

        QtWidgets.QMessageBox.information(self, "Создано", f"Класс {class_name} с {student_count} учениками создан!")
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CreateClassWindow(None)
    window.show()
    sys.exit(app.exec_())
