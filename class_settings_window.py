import os
import shutil
from PyQt5 import QtWidgets, QtCore
import face_recognition
import numpy as np

class ClassSettingsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, update_main_window_callback=None):
        super().__init__()
        self.class_name = class_name
        self.update_main_window_callback = update_main_window_callback  # Обновление главного окна
        self.class_path = os.path.join("classes", class_name)
        self.edit_mode = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Редактирование класса {self.class_name}")
        self.setGeometry(100, 100, 600, 400)
        layout = QtWidgets.QVBoxLayout()

        class_name_layout = QtWidgets.QHBoxLayout()
        self.class_name_input = QtWidgets.QLineEdit(self.class_name)
        self.class_name_input.setEnabled(False)
        self.class_name_input.setFixedHeight(28)  # Устанавливаем высоту 40 пикселей

        self.rename_button = QtWidgets.QPushButton("📝")
        self.rename_button.setFixedSize(30, 30)
        self.rename_button.clicked.connect(self.toggle_edit_mode)

                # Добавляем поле ввода и кнопку в горизонтальный макет
        class_name_layout.addWidget(QtWidgets.QLabel("Название класса:"))
        class_name_layout.addWidget(self.class_name_input)
        class_name_layout.addWidget(self.rename_button)

        # Добавляем горизонтальный макет в основной макет
        layout.addLayout(class_name_layout)

        # Список учеников
        layout.addWidget(QtWidgets.QLabel("Список учеников:"))
        self.student_list = QtWidgets.QListWidget()
        self.update_student_list()
        layout.addWidget(self.student_list)

        # Кнопки управления учениками
        student_buttons_layout = QtWidgets.QHBoxLayout()
        self.add_student_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_student_button.clicked.connect(self.add_student)
        self.delete_student_button = QtWidgets.QPushButton("Удалить ученика")
        self.delete_student_button.clicked.connect(self.delete_student)
        student_buttons_layout.addWidget(self.add_student_button)
        student_buttons_layout.addWidget(self.delete_student_button)
        layout.addLayout(student_buttons_layout)

        # Кнопка сохранения изменений
        self.save_button = QtWidgets.QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def update_student_list(self):
        self.student_list.clear()
        students_path = os.path.join(self.class_path, "students")
        if os.path.exists(students_path):
            students = os.listdir(students_path)
            self.student_list.addItems(students)

    def save_changes(self):
        # Обновляем список учеников
        self.update_student_list()

        # Показываем сообщение об успешном сохранении
        QtWidgets.QMessageBox.information(self, "Сохранено", "Изменения успешно сохранены!")

        # Вызываем обновление главного окна, если функция передана
        if self.update_main_window_callback:
            self.update_main_window_callback()

        # Закрываем текущее окно
        self.close()
        from main import MainApp
        self.main_app = MainApp()
        self.main_app.show()


    def toggle_edit_mode(self):
        if self.edit_mode:
            new_class_name = self.class_name_input.text().strip()
            if new_class_name and new_class_name != self.class_name:
                new_class_path = os.path.join("classes", new_class_name)
                os.rename(self.class_path, new_class_path)
                self.class_path = new_class_path
                self.class_name = new_class_name
                self.class_name_input.setEnabled(False)
                self.rename_button.setText("📝")
                self.edit_mode = False
        else:
            self.class_name_input.setEnabled(True)
            self.rename_button.setText("✅")
            self.edit_mode = True

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
                self.finish_adding()
                self.update_student_list()

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

    def finish_adding(self):
       
        self.train_model()
        if self.update_main_window_callback:
            self.update_main_window_callback()  # Вызываем обновление главного окна


    def train_model(self):

        class_students_path = os.path.join("classes", self.class_name, "students")
        known_faces = []
        known_names = []

        for student_name in os.listdir(class_students_path):
            student_folder = os.path.join(class_students_path, student_name)
            if os.path.isdir(student_folder):
                for photo_name in os.listdir(student_folder):
                    photo_path = os.path.join(student_folder, photo_name)
                    image = face_recognition.load_image_file(photo_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_faces.append(face_encodings[0])
                        known_names.append(student_name)

 
        known_faces_path = os.path.join("classes", self.class_name, "known_faces.npy")
        known_names_path = os.path.join("classes", self.class_name, "known_names.npy")
        np.save(known_faces_path, known_faces)
        np.save(known_names_path, known_names)
        print(f"Модель для класса {self.class_name} успешно обучена!")
