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
        self.setFixedSize(600, 400)  
        self.initUI()



    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        
        self.student_count_label = QtWidgets.QLabel(f"Кол-во учеников: {self.added_students}/{self.student_count}")
        layout.addWidget(self.student_count_label)

        
        self.add_photo_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_photo_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_photo_button)

    
        self.students_list = QtWidgets.QListWidget()
        layout.addWidget(self.students_list)

        self.finish_button = QtWidgets.QPushButton("Завершить")
        self.finish_button.setEnabled(False)
        self.finish_button.clicked.connect(self.finish_adding)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

    def add_student(self):
     
        photo_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Выберите фотографии ученика", "", "Images (*.png *.jpg *.jpeg)"
        )
        if photo_paths:
       
            student_name, ok = QtWidgets.QInputDialog.getText(self, "Имя ученика", "Введите имя ученика:")
            if ok and student_name:
             
                class_students_path = os.path.join("classes", self.class_name, "students")
                os.makedirs(class_students_path, exist_ok=True)
                student_folder = os.path.join(class_students_path, student_name)
                os.makedirs(student_folder, exist_ok=True)

              
                for photo_path in photo_paths:
                    shutil.copy(photo_path, os.path.join(student_folder, os.path.basename(photo_path)))

                self.students_data[student_name] = student_folder
                self.students_list.addItem(f"{student_name} - {len(photo_paths)} фото")
                self.added_students += 1

      
                self.student_count_label.setText(f"Кол-во учеников: {self.added_students}/{self.student_count}")
                if self.added_students >= self.student_count:
                    self.add_photo_button.setEnabled(False)
                    self.finish_button.setEnabled(True)

    def finish_adding(self):
       
        self.train_model()

     
        QtWidgets.QMessageBox.information(self, "Завершено", f"Класс {self.class_name} успешно создан и обучен!")
        self.parent_window.update_class_list()
        self.parent_window.show()
        self.close()

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


class CreateClassWindow(QtWidgets.QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание нового класса")
        self.setFixedSize(400, 300)  
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        
        self.class_name_input = QtWidgets.QLineEdit()
        self.class_name_input.setPlaceholderText("Введите название класса")
        layout.addWidget(self.class_name_input)

 
        self.student_count_input = QtWidgets.QSpinBox()
        self.student_count_input.setRange(1, 100)
        self.student_count_input.setPrefix("Кол-во учеников: ")
        layout.addWidget(self.student_count_input)

   
        self.create_class_button = QtWidgets.QPushButton("Создать класс")
        self.create_class_button.clicked.connect(self.create_class)
        layout.addWidget(self.create_class_button)

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

        os.makedirs(os.path.join(class_path, "students"), exist_ok=True)
        os.makedirs(os.path.join(class_path, "logs"), exist_ok=True)

        self.add_students_window = AddStudentsWindow(class_name, student_count, self.parent_window)
        self.add_students_window.show()
        self.close()

    def return_to_main_menu(self):
        self.parent_window.show()
        self.close()
