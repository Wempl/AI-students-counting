import cv2
import face_recognition
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import os
from datetime import datetime
import sys


class AbsentStudentsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, known_faces, known_names, parent_window=None):
        super().__init__()
        self.setWindowTitle(f"Класс: {class_name}")
        self.setFixedSize(1200, 600)
        self.class_name = class_name
        self.known_faces = known_faces
        self.known_names = known_names
        self.recognized_students = set()
        self.parent_window = parent_window

        self.initUI()
        self.start_camera()

    import dlib
    import sys



    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()


        title_label = QtWidgets.QLabel(f"Класс: {self.class_name}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle_label = QtWidgets.QLabel(f"{len(self.known_names)} учеников")
        subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)


        content_layout = QtWidgets.QHBoxLayout()


        self.camera_label = QtWidgets.QLabel()
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("border: 1px solid black;")
        content_layout.addWidget(self.camera_label)


        side_layout = QtWidgets.QVBoxLayout()


        absent_layout = QtWidgets.QVBoxLayout()
        absent_label = QtWidgets.QLabel("Отсутствуют:")
        absent_label.setStyleSheet("font-size: 18px; font-weight: bold; color: red;")
        self.absent_list = QtWidgets.QListWidget()
        self.absent_list.setFixedHeight(205)  
        absent_layout.addWidget(absent_label)
        absent_layout.addWidget(self.absent_list)
        side_layout.addLayout(absent_layout)

        present_layout = QtWidgets.QVBoxLayout()
        present_label = QtWidgets.QLabel("Присутствуют:")
        present_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.present_list = QtWidgets.QListWidget()
        self.present_list.setFixedHeight(205) 
        present_layout.addWidget(present_label)
        present_layout.addWidget(self.present_list)
        side_layout.addLayout(present_layout)

        content_layout.addLayout(side_layout)
        main_layout.addLayout(content_layout)

 
        finish_button = QtWidgets.QPushButton("Завершить проверку")
        finish_button.setStyleSheet("font-size: 16px; font-weight: bold;")
        finish_button.clicked.connect(self.finish_check)
        finish_button.setFixedHeight(40)
        main_layout.addWidget(finish_button)

        self.setLayout(main_layout)

    def start_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)

    def update_camera(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Неизвестный"

                if True in matches:
                    match_index = matches.index(True)
                    name = self.known_names[match_index]
                    self.recognized_students.add(name)

               
                color = (0, 255, 0) if name != "Неизвестный" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
            self.camera_label.setPixmap(QtGui.QPixmap.fromImage(image))

            self.update_lists()

    def update_lists(self):
        present_students = list(self.recognized_students)
        absent_students = [student for student in self.known_names if student not in self.recognized_students]

        self.present_list.clear()
        self.present_list.addItems(present_students)

        self.absent_list.clear()
        self.absent_list.addItems(absent_students)

    def finish_check(self):
        self.timer.stop()
        self.camera.release()
        self.close()

       
        self.save_logs()

      
        absent_students = [student for student in self.known_names if student not in self.recognized_students]
        self.results_window = ResultsWindow(absent_students, self.class_name, self.known_faces, self.known_names, self.parent_window)
        self.results_window.show()

    def save_logs(self):
        logs_dir = os.path.join("classes", self.class_name, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%d.%m")
        log_file = os.path.join(logs_dir, f"{timestamp}.txt")

        with open(log_file, "w", encoding="utf-8") as file:
            for student in self.known_names:
                if student in self.recognized_students:
                    file.write(f"{student} - ПР\n")  
                else:
                    file.write(f"{student} - Б\n")  

        print(f"Лог сохранён: {log_file}")



class ResultsWindow(QtWidgets.QWidget):
    def __init__(self, absent_students, class_name, known_faces, known_names, main_window):
        super().__init__()
        self.setWindowTitle("Результаты проверки")
        self.setFixedSize(600, 500)
        self.main_window = main_window
        self.absent_students = absent_students
        self.class_name = class_name
        self.known_faces = known_faces
        self.known_names = known_names

        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Проверка завершена!")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        absent_label = QtWidgets.QLabel("Отсутствуют:")
        absent_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        layout.addWidget(absent_label)

        self.absent_list = QtWidgets.QListWidget()
        self.absent_list.addItems(self.absent_students)
        layout.addWidget(self.absent_list)

    
        buttons_layout = QtWidgets.QHBoxLayout()

        restart_button = QtWidgets.QPushButton("Перезапустить")
        restart_button.clicked.connect(self.restart_check)
        buttons_layout.addWidget(restart_button)

        main_menu_button = QtWidgets.QPushButton("Главное меню")
        main_menu_button.clicked.connect(self.return_to_main_menu)
        buttons_layout.addWidget(main_menu_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def restart_check(self):
        self.close()
        self.check_window = AbsentStudentsWindow(self.class_name, self.known_faces, self.known_names, self.main_window)
        self.check_window.show()

    def return_to_main_menu(self):
        self.close()
        if self.main_window:
            self.main_window.show()
