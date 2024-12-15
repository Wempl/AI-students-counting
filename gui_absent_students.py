import cv2
import face_recognition
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import os
from datetime import datetime


class AbsentStudentsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, known_faces, known_names, parent_window=None):
        super().__init__()
        self.setWindowTitle(f"Класс: {class_name}")
        self.setFixedSize(1200, 650)  # Увеличил высоту
        self.class_name = class_name
        self.known_faces = known_faces
        self.known_names = known_names
        self.recognized_students = set()
        self.parent_window = parent_window

        self.initUI()
        self.start_camera()

    def initUI(self):
            # Основной вертикальный layout
            main_layout = QtWidgets.QVBoxLayout()

            # Верхний заголовок окна
            title_label = QtWidgets.QLabel(f"Класс: {self.class_name}")
            title_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0078D7, stop: 1 #66A8FF);
                border-radius: 8px;
            """)
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            title_label.setFixedHeight(50)
            main_layout.addWidget(title_label)

            # Подзаголовок с количеством учеников
            subtitle_label = QtWidgets.QLabel(f"{len(self.known_names)} учеников")
            subtitle_label.setStyleSheet("font-size: 16px; color: #333;")
            subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
            main_layout.addWidget(subtitle_label)

            # Горизонтальный layout для камеры и списков
            content_layout = QtWidgets.QHBoxLayout()

            # QLabel для камеры
            self.camera_label = QtWidgets.QLabel()
            self.camera_label.setFixedSize(640, 480)
            self.camera_label.setStyleSheet("""
                QLabel {
                    border: none; /* Убираем рамку вокруг камеры */
                    background-color: black; /* Фон камеры */
                }
            """)
            content_layout.addWidget(self.camera_label)

            # Боковая панель со списками
            side_layout = QtWidgets.QVBoxLayout()

            # Список отсутствующих
            absent_label = QtWidgets.QLabel("Отсутствуют:")
            absent_label.setStyleSheet("font-size: 18px; font-weight: bold; color: red;")
            self.absent_list = QtWidgets.QListWidget()
            self.absent_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #ddd;
                    background-color: #fafafa;
                    border-radius: 5px;
                }
            """)
            self.absent_list.setFixedHeight(205)
            side_layout.addWidget(absent_label)
            side_layout.addWidget(self.absent_list)

            # Список присутствующих
            present_label = QtWidgets.QLabel("Присутствуют:")
            present_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
            self.present_list = QtWidgets.QListWidget()
            self.present_list.setStyleSheet("""
                QListWidget {
                    border: 1px solid #ddd;
                    background-color: #fafafa;
                    border-radius: 5px;
                }
            """)
            self.present_list.setFixedHeight(205)
            side_layout.addWidget(present_label)
            side_layout.addWidget(self.present_list)

            content_layout.addLayout(side_layout)
            main_layout.addLayout(content_layout)

            # Кнопка завершения проверки
            finish_button = QtWidgets.QPushButton("Завершить проверку")
            finish_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #28a745, stop: 1 #34d058
                    );
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #218838, stop: 1 #2ca342
                    );
                }
            """)
            finish_button.setFixedHeight(50)
            finish_button.clicked.connect(self.finish_check)
            main_layout.addWidget(finish_button)

            self.setLayout(main_layout)


    def list_style(self):
        """Стиль для списков"""
        return """
            QListWidget {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #d9e5ff;
                color: #0078D7;
            }
        """

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

            # Обработка распознавания лиц
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Неизвестный"

                if True in matches:
                    match_index = matches.index(True)
                    name = self.known_names[match_index]
                    self.recognized_students.add(name)

                # Отрисовка рамки и имени
                color = (0, 255, 0) if name != "Неизвестный" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Конвертация OpenCV изображения в QPixmap
            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
            pixmap = QtGui.QPixmap.fromImage(image)

            # Обновление QLabel с изображением
            self.camera_label.setPixmap(pixmap)

            # Обновление списков присутствующих и отсутствующих
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

        # Сохранение логов
        self.save_logs()

        # Определение отсутствующих учеников
        absent_students = [student for student in self.known_names if student not in self.recognized_students]

        # Открытие окна результатов с правильными аргументами
        self.results_window = ResultsWindow(
            absent_students=absent_students,
            class_name=self.class_name,
            known_faces=self.known_faces,
            known_names=self.known_names,
            main_window=self.parent_window
        )
        self.results_window.show()


    def save_logs(self):
        logs_dir = os.path.join("classes", self.class_name, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%d.%m")
        log_file = os.path.join(logs_dir, f"{timestamp}.txt")

        with open(log_file, "w", encoding="utf-8") as file:
            for student in self.known_names:
                status = "ПР" if student in self.recognized_students else "Б"
                file.write(f"{student} - {status}\n")


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

        self.initUI()

    def initUI(self):
        # Основной layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e6e9f0, stop: 1 #eef1f5
                );
            }
        """)

        # Заголовок окна
        title_label = QtWidgets.QLabel("Проверка завершена!")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #0078D7, stop: 1 #66A8FF
            );
            border-radius: 10px;
            padding: 10px;
        """)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Заголовок "Отсутствуют"
        absent_label = QtWidgets.QLabel("Отсутствуют:")
        absent_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: red;
        """)
        main_layout.addWidget(absent_label)

        # Список отсутствующих
        self.absent_list = QtWidgets.QListWidget()
        self.absent_list.addItems(self.absent_students)
        self.absent_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                background-color: #fafafa;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.absent_list)

        # Кнопки внизу
        buttons_layout = QtWidgets.QHBoxLayout()

        # Кнопка "Перезапустить"
        restart_button = QtWidgets.QPushButton("Перезапустить")
        restart_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #28a745, stop: 1 #34d058
                );
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #218838, stop: 1 #2ca342
                );
            }
        """)
        restart_button.clicked.connect(self.restart_check)
        restart_button.setFixedHeight(40)
        buttons_layout.addWidget(restart_button)

        # Кнопка "Главное меню"
        main_menu_button = QtWidgets.QPushButton("Главное меню")
        main_menu_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #0078D7, stop: 1 #66A8FF
                );
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #005499, stop: 1 #4a90e2
                );
            }
        """)
        main_menu_button.clicked.connect(self.return_to_main_menu)
        main_menu_button.setFixedHeight(40)
        buttons_layout.addWidget(main_menu_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def restart_check(self):
        self.close()
        self.check_window = AbsentStudentsWindow(self.class_name, self.known_faces, self.known_names, self.main_window)
        self.check_window.show()

    def return_to_main_menu(self):
        self.close()
        if self.main_window:
            self.main_window.show()

