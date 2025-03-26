from PyQt5 import QtWidgets, QtGui, QtCore
import os
import shutil
import face_recognition
import numpy as np

class AddStudentsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, student_count, parent_window):
        super().__init__()
        self.class_name = class_name
        self.student_count = student_count
        self.parent_window = parent_window
        self.added_students = 0
        self.students_data = {}
        self.setWindowTitle("Добавление учеников")
        self.setFixedSize(600, 500)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel(f"Добавление учеников - {self.class_name}")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 20px; font-weight: bold; color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0078D7, stop:1 #66A8FF);
            padding: 10px; border-radius: 5px;
        """)
        layout.addWidget(title_label)

        self.status_label = QtWidgets.QLabel(f"Добавлено: {self.added_students}/{self.student_count}")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #555;")
        layout.addWidget(self.status_label)

        self.add_photo_button = QtWidgets.QPushButton("Добавить ученика")
        self.add_photo_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_photo_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_photo_button)

        self.students_list = QtWidgets.QListWidget()
        self.students_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.students_list)

        self.finish_button = QtWidgets.QPushButton("Завершить и обучить нейросеть")
        self.finish_button.setEnabled(False)
        self.finish_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005499;
            }
        """)
        self.finish_button.clicked.connect(self.finish_adding)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

    def add_student(self):
        photo_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Выберите фотографии ученика", "", "Images (*.png *.jpg *.jpeg)")
        if photo_paths:
            student_name, ok = QtWidgets.QInputDialog.getText(self, "Имя ученика", "Введите имя ученика:")
            if ok and student_name:
                student_folder = os.path.join("classes", self.class_name, "students", student_name)
                os.makedirs(student_folder, exist_ok=True)
                for photo_path in photo_paths:
                    shutil.copy(photo_path, os.path.join(student_folder, os.path.basename(photo_path)))
                self.students_list.addItem(f"{student_name} - {len(photo_paths)} фото")
                self.students_data[student_name] = student_folder
                self.added_students += 1

                self.status_label.setText(f"Добавлено: {self.added_students}/{self.student_count}")
                if self.added_students >= self.student_count:
                    self.add_photo_button.setEnabled(False)
                    self.finish_button.setEnabled(True)

    def finish_adding(self):
        self.train_model()
        QtWidgets.QMessageBox.information(self, "Завершено", "Класс успешно обучен и сохранён!")
        self.parent_window.update_class_list()
        self.close()

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



 
class CreateClassWindow(QtWidgets.QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Создание нового класса")
        self.setFixedSize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Создание нового класса")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

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
                font-size: 14px;
            }
        """)
        layout.addWidget(self.class_name_input)

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
                font-size: 14px;
                background-color: white;
            }
        """)
        layout.addWidget(self.student_count_input)

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

        class_path = os.path.join("classes", class_name)
        if os.path.exists(class_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Класс с таким названием уже существует!")
            return

        os.makedirs(os.path.join(class_path, "students"), exist_ok=True)
        os.makedirs(os.path.join(class_path, "logs"), exist_ok=True)

        self.add_students_window = AddStudentsWindow(class_name, student_count, self.parent_window)
        self.add_students_window.show()
        self.close()


 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CreateClassWindow()
    window.show()
    sys.exit(app.exec_())