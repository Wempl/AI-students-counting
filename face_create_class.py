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
        self.students_data = {}  # Для хранения добавленных студентов
        self.setWindowTitle(f"Добавление учеников - {class_name}")
        self.setFixedSize(600, 400)  # Фиксированный размер окна
        self.initUI()

    # import dlib
    # def get_resource_path(relative_path):
    #     """Получает путь к ресурсу, учитывая временные файлы PyInstaller."""
    #     if hasattr(sys, '_MEIPASS'):  # PyInstaller добавляет _MEIPASS во время выполнения
    #         return os.path.join(sys._MEIPASS, relative_path)
    #     return os.path.join(os.path.abspath("."), relative_path)

    # # Используйте get_resource_path для загрузки модели
    # model_path = get_resource_path("models/shape_predictor_68_face_landmarks.dat")
    # shape_predictor = dlib.shape_predictor(model_path)


    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Поле для отображения количества учеников
        self.student_count_label = QtWidgets.QLabel(f"Кол-во учеников: {self.added_students}/{self.student_count}")
        layout.addWidget(self.student_count_label)

        # Кнопка для добавления фото
        self.add_photo_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_photo_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_photo_button)

        # Список добавленных учеников
        self.students_list = QtWidgets.QListWidget()
        layout.addWidget(self.students_list)

        # Кнопка завершения
        self.finish_button = QtWidgets.QPushButton("Завершить")
        self.finish_button.setEnabled(False)
        self.finish_button.clicked.connect(self.finish_adding)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

    def add_student(self):
        # Открытие диалога для выбора фото
        photo_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Выберите фотографии ученика", "", "Images (*.png *.jpg *.jpeg)"
        )
        if photo_paths:
            # Ввод имени ученика
            student_name, ok = QtWidgets.QInputDialog.getText(self, "Имя ученика", "Введите имя ученика:")
            if ok and student_name:
                # Создание папки для ученика
                class_students_path = os.path.join("classes", self.class_name, "students")
                os.makedirs(class_students_path, exist_ok=True)
                student_folder = os.path.join(class_students_path, student_name)
                os.makedirs(student_folder, exist_ok=True)

                # Сохранение фотографий
                for photo_path in photo_paths:
                    shutil.copy(photo_path, os.path.join(student_folder, os.path.basename(photo_path)))

                # Обновление списка учеников
                self.students_data[student_name] = student_folder
                self.students_list.addItem(f"{student_name} - {len(photo_paths)} фото")
                self.added_students += 1

                # Обновление статуса
                self.student_count_label.setText(f"Кол-во учеников: {self.added_students}/{self.student_count}")
                if self.added_students >= self.student_count:
                    self.add_photo_button.setEnabled(False)
                    self.finish_button.setEnabled(True)

    def finish_adding(self):
        # Обучение модели для добавленных учеников
        self.train_model()

        # Возвращение в главное окно
        QtWidgets.QMessageBox.information(self, "Завершено", f"Класс {self.class_name} успешно создан и обучен!")
        self.parent_window.update_class_list()
        self.parent_window.show()
        self.close()

    def train_model(self):
        # Обучение модели
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

        # Сохранение модели
        known_faces_path = os.path.join("classes", self.class_name, "known_faces.npy")
        known_names_path = os.path.join("classes", self.class_name, "known_names.npy")
        np.save(known_faces_path, known_faces)
        np.save(known_names_path, known_names)
        print(f"Модель для класса {self.class_name} успешно обучена!")


class CreateClassWindow(QtWidgets.QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание нового класса")
        self.setFixedSize(400, 300)  # Фиксированный размер окна
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Поле для ввода названия класса
        self.class_name_input = QtWidgets.QLineEdit()
        self.class_name_input.setPlaceholderText("Введите название класса")
        layout.addWidget(self.class_name_input)

        # Поле для ввода количества учеников
        self.student_count_input = QtWidgets.QSpinBox()
        self.student_count_input.setRange(1, 100)
        self.student_count_input.setPrefix("Кол-во учеников: ")
        layout.addWidget(self.student_count_input)

        # Кнопка создания класса
        self.create_class_button = QtWidgets.QPushButton("Создать класс")
        self.create_class_button.clicked.connect(self.create_class)
        layout.addWidget(self.create_class_button)

        # Кнопка возврата в главное меню
        self.back_to_main_button = QtWidgets.QPushButton("Главное меню")
        self.back_to_main_button.clicked.connect(self.return_to_main_menu)
        layout.addWidget(self.back_to_main_button)

        self.setLayout(layout)

    def create_class(self):
        class_name = self.class_name_input.text()
        student_count = self.student_count_input.value()

        if not class_name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите название класса.")
            return

        class_path = os.path.join("classes", class_name)
        if os.path.exists(class_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Класс с таким названием уже существует.")
            return

        # Создаем папки для класса
        os.makedirs(os.path.join(class_path, "students"), exist_ok=True)
        os.makedirs(os.path.join(class_path, "logs"), exist_ok=True)

        # Переход к добавлению учеников
        self.add_students_window = AddStudentsWindow(class_name, student_count, self.parent_window)
        self.add_students_window.show()
        self.close()

    def return_to_main_menu(self):
        self.parent_window.show()
        self.close()
