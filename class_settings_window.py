from PyQt5 import QtWidgets, QtGui, QtCore
import os
import shutil
import face_recognition
import numpy as np


class ClassSettingsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, update_main_window_callback=None):
        super().__init__()
        self.class_name = class_name
        self.update_main_window_callback = update_main_window_callback
        self.class_path = os.path.join("classes", class_name)
        self.edit_mode = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Настройки класса - {self.class_name}")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel(f"Настройки класса: {self.class_name}")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        name_layout = QtWidgets.QHBoxLayout()
        self.class_name_input = QtWidgets.QLineEdit(self.class_name)
        self.class_name_input.setEnabled(False)
        self.class_name_input.setStyleSheet(self.input_style())

        self.rename_button = QtWidgets.QPushButton("📝")
        self.rename_button.setFixedSize(30, 30)
        self.rename_button.clicked.connect(self.toggle_edit_mode)
        self.rename_button.setStyleSheet(self.button_style())

        name_layout.addWidget(QtWidgets.QLabel("Название класса:"))
        name_layout.addWidget(self.class_name_input)
        name_layout.addWidget(self.rename_button)

        layout.addLayout(name_layout)

        student_label = QtWidgets.QLabel("Список учеников:")
        student_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(student_label)

        self.student_list = QtWidgets.QListWidget()
        self.student_list.setStyleSheet(self.list_style())
        layout.addWidget(self.student_list)

        button_layout = QtWidgets.QHBoxLayout()
        self.add_student_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_student_button.setStyleSheet(self.button_style())
        self.add_student_button.clicked.connect(self.add_student)

        self.delete_student_button = QtWidgets.QPushButton("Удалить ученика")
        self.delete_student_button.setStyleSheet(self.button_style())
        self.delete_student_button.clicked.connect(self.delete_student)

        button_layout.addWidget(self.add_student_button)
        button_layout.addWidget(self.delete_student_button)
        layout.addLayout(button_layout)

        self.save_button = QtWidgets.QPushButton("Сохранить изменения")
        self.save_button.setStyleSheet(self.button_style(highlight=True))
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.update_student_list()
        self.setLayout(layout)

    def input_style(self):
        return """
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """

    def button_style(self, highlight=False):
        if highlight:
            return """
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """
        return """
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

    def list_style(self):
        return """
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
        """

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.class_name_input.setEnabled(True)
            self.rename_button.setText("✅")
        else:
            new_class_name = self.class_name_input.text().strip()
            if new_class_name and new_class_name != self.class_name:
                new_class_path = os.path.join("classes", new_class_name)
                os.rename(self.class_path, new_class_path)

                self.class_path = new_class_path
                self.class_name = new_class_name

                self.setWindowTitle(f"Настройки класса - {self.class_name}")
                
            self.class_name_input.setEnabled(False)
            self.rename_button.setText("📝")
            self.update_student_list()  


    def update_student_list(self):
        self.student_list.clear()
        students_path = os.path.join(self.class_path, "students")
        if os.path.exists(students_path):
            students = os.listdir(students_path)
            self.student_list.addItems(students)

    def add_student(self):
        file_dialog = QtWidgets.QFileDialog()
        photos, _ = file_dialog.getOpenFileNames(self, "Выберите фото ученика", "", "Фото ученика (*.png *.jpg *.jpeg)")
        if photos:
            student_name, ok = QtWidgets.QInputDialog.getText(self, "Имя ученика", "Введите Имя учащегося:")
            if ok and student_name:
                student_dir = os.path.join(self.class_path, "students", student_name)
                os.makedirs(student_dir, exist_ok=True)
                for photo in photos:
                    shutil.copy(photo, student_dir)
                self.train_model()
                self.update_student_list()
    
    def train_model(self):
        known_faces = []
        known_names = []
        students_path = os.path.join("classes", self.class_name, "students")

        for student_name in os.listdir(students_path):
            student_folder = os.path.join(students_path, student_name)
            for photo_name in os.listdir(student_folder):
                photo_path = os.path.join(student_folder, photo_name)
                image = face_recognition.load_image_file(photo_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_faces.append(encodings[0])
                    known_names.append(student_name)

        np.save(os.path.join("classes", self.class_name, "known_faces.npy"), known_faces)
        np.save(os.path.join("classes", self.class_name, "known_names.npy"), known_names)

    def delete_student(self):
        selected_items = self.student_list.selectedItems()
        if selected_items:
            student_name = selected_items[0].text()
            confirm = QtWidgets.QMessageBox.question(
                self, "Удалить ученика", f"Вы уверены, что хотите удалить ученика {student_name}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                student_dir = os.path.join(self.class_path, "students", student_name)
                if os.path.exists(student_dir):
                    shutil.rmtree(student_dir)
                self.train_model()
                self.update_student_list()

    def save_changes(self):
        from main import MainApp
        QtWidgets.QMessageBox.information(self, "Сохранено", "Изменения успешно сохранены!")
        if self.update_main_window_callback:
            self.update_main_window_callback()
        self.close()
        self.main = MainApp()
        self.main.show()
