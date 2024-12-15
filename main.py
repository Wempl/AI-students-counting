from PyQt5 import QtWidgets, QtGui, QtCore
import os
import shutil
import pandas as pd
import numpy as np
import subprocess
from class_settings_window import ClassSettingsWindow
import face_recognition
from login_window import LoginWindow


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Счетовод")
        self.setFixedSize(800, 600) 

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.logged_in_user = None  
        self.update_class_list()
    
    def setup_top_bar(self):
        """Создание верхней панели с кнопками настроек и выхода"""
        top_layout = QtWidgets.QHBoxLayout()
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #0078D7, stop: 1 #66A8FF
            );
            border-radius: 10px;
        """)

        # Кнопка настроек
        settings_button = QtWidgets.QPushButton("⚙️")
        settings_button.setFixedSize(50, 50)
        settings_button.setStyleSheet(self.round_button_style())
        settings_button.clicked.connect(self.open_settings)

        # Кнопка выхода
        exit_button = QtWidgets.QPushButton("🖨")
        exit_button.setFixedSize(50, 50)
        exit_button.setStyleSheet(self.round_button_style())
        exit_button.clicked.connect(self.close)  # Закрытие текущего окна

        # Добавляем кнопки в верхнюю панель
        top_layout.addWidget(settings_button, alignment=QtCore.Qt.AlignLeft)
        top_layout.addStretch()
        top_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignRight)

        self.layout.addWidget(top_widget, alignment=QtCore.Qt.AlignTop)

    def round_button_style(self):
        """Стиль для круглых кнопок"""
        return """
            QPushButton {
                font-size: 18px;
                border-radius: 25px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

    def update_class_list(self):
        # Очистка текущего layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Стилизация основного окна с мягким градиентом
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e6e9f0, stop: 1 #eef1f5
                );
                border-radius: 10px;
            }
        """)

        # Верхняя панель с кнопкой настроек и кнопкой выхода
        top_layout = QtWidgets.QHBoxLayout()
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #0078D7, stop: 1 #66A8FF
            );
            border-radius: 10px;
        """)

        # Кнопка настроек
        settings_button = QtWidgets.QPushButton("⚙️")
        settings_button.setFixedSize(50, 50)
        settings_button.setStyleSheet(self.round_button_style())
        settings_button.clicked.connect(self.open_settings)

        # Кнопка выхода
        exit_button = QtWidgets.QPushButton("🚪")
        exit_button.setFixedSize(50, 50)
        exit_button.setStyleSheet(self.round_button_style())
        exit_button.clicked.connect(self.close)  # Закрытие текущего окна

        # Добавление кнопок в верхнюю панель
        top_layout.addWidget(settings_button, alignment=QtCore.Qt.AlignLeft)
        top_layout.addStretch()
        top_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignRight)

        self.layout.addWidget(top_widget, alignment=QtCore.Qt.AlignTop)

        # Путь к папке с классами
        classes_path = "classes"
        if not os.path.exists(classes_path):
            os.makedirs(classes_path)

        classes = [d for d in os.listdir(classes_path) if os.path.isdir(os.path.join(classes_path, d))]

        # Область с прокруткой
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(400)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #0078D7;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #005499;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

        # Виджет и сетка для карточек классов
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QGridLayout(scroll_content)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        # Пути к изображениям
        start_icon_path = "icons/115-1154871_power-on-energy-start-button-multimedia-power-icon-start-png.png"
        edit_icon_path = "icons/i.webp"

        # Добавление карточек классов с мягкими градиентами
        for index, cls in enumerate(classes):
            card_widget = QtWidgets.QWidget()
            card_widget.setFixedSize(160, 120)
            card_widget.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #ffffff, stop: 1 #f1f1f1
                    );
                    border: 1px solid #ddd;
                    border-radius: 10px;
                }
                QWidget:hover {
                    border: 1px solid #0078D7;
                }
            """)

            card_layout = QtWidgets.QVBoxLayout(card_widget)
            card_layout.setContentsMargins(5, 5, 5, 5)

            # Название класса
            class_label = QtWidgets.QLabel(f"{cls}")
            class_label.setAlignment(QtCore.Qt.AlignCenter)
            class_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
            card_layout.addWidget(class_label)

            # Кнопки действий
            button_layout = QtWidgets.QHBoxLayout()
            button_layout.setSpacing(5)

            buttons = {
                "start": (start_icon_path, lambda _, name=cls: self.start_class(name)),  # Запуск
                "analytics": ("📊", lambda _, name=cls: self.open_analytics(name)),      # Аналитика
                "edit": (edit_icon_path, lambda _, name=cls: self.rename_class(name)),            # Редактирование
                "delete": ("🗑", lambda _, name=cls: self.delete_class(name)),          # Удаление
            }


            for name, (icon, action) in buttons.items():
                button = QtWidgets.QPushButton()
                button.setFixedSize(30, 30)

                if name in ["start", "edit"]:
                    button.setIcon(QtGui.QIcon(icon))
                    button.setIconSize(QtCore.QSize(20, 20))
                else:
                    button.setText(icon)

                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f5f5f5;
                        border: 1px solid #ddd;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
                button.clicked.connect(action)
                button_layout.addWidget(button)

            card_layout.addLayout(button_layout)
            scroll_layout.addWidget(card_widget, index // 4, index % 4)

        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

        # Кнопка "Создать класс" с градиентом
        create_class_button = QtWidgets.QPushButton("Создать класс")
        create_class_button.setFixedHeight(50)
        create_class_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #28a745, stop: 1 #34d058
                );
                border-radius: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1e7e34, stop: 1 #2ca342
                );
            }
        """)
        self.layout.addWidget(create_class_button)
        create_class_button.clicked.connect(self.create_class)

    def start_class(self, class_name):
        QtWidgets.QMessageBox.information(self, "Запуск", f"Запущен класс: {class_name}")

    def edit_class(self, class_name):
        QtWidgets.QMessageBox.information(self, "Редактирование", f"Редактирование класса: {class_name}")

    def show_analytics(self, class_name):
        QtWidgets.QMessageBox.information(self, "Аналитика", f"Аналитика для класса: {class_name}")

    def delete_class(self, class_name):
        reply = QtWidgets.QMessageBox.question(
            self, "Удаление класса",
            f"Вы действительно хотите удалить класс '{class_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            class_path = os.path.join("classes", class_name)
            if os.path.exists(class_path):
                shutil.rmtree(class_path)
                self.update_class_list()
                QtWidgets.QMessageBox.information(self, "Удаление", f"Класс '{class_name}' удалён.")
    
    def save_logs(self, class_name, students_present):
        import datetime
        log_date = datetime.datetime.now().strftime("%d.%m")
        logs_path = os.path.join("classes", class_name, "logs")

        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        log_file = os.path.join(logs_path, f"{log_date}.txt")
        with open(log_file, "w", encoding="utf-8") as f:
            for student in students_present:
                f.write(f"{student}\n")

    def start_class(self, class_name):
        class_path = os.path.join("classes", class_name)
        known_faces_path = os.path.join(class_path, "known_faces.npy")
        known_names_path = os.path.join(class_path, "known_names.npy")

        if not os.path.exists(known_faces_path) or not os.path.exists(known_names_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"У класса {class_name} отсутствуют обученные данные.")
            return

        known_faces = np.load(known_faces_path, allow_pickle=True)
        known_names = np.load(known_names_path, allow_pickle=True)

        from gui_absent_students import AbsentStudentsWindow
        self.absent_students_window = AbsentStudentsWindow(
            class_name, known_faces, known_names, parent_window=self
        )
        self.absent_students_window.show()
        self.hide()  

    def create_class(self):
        try:
            from face_create_class import CreateClassWindow
            self.create_class_window = CreateClassWindow(parent_window=self)
            self.create_class_window.show()
            self.hide()  

            def on_close_event(event):
                self.update_class_list()
                self.show()
                event.accept()

            self.create_class_window.closeEvent = on_close_event

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при создании класса: {e}")


    def open_settings(self):
        from setting import SettingsWindow
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()  
        self.show()





    def rename_class(self, class_name):
        self.class_settings_window = ClassSettingsWindow(
            class_name, update_main_window_callback=self.update_class_list
        )
        self.class_settings_window.show()
        self.hide()  # Скрываем главное окно
    
    def show_and_update_main_window(self):
        self.update_class_list()
        self.show()




    def delete_class(self, class_name):
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить класс '{class_name}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            class_path = os.path.join("classes", class_name)
            if os.path.exists(class_path):
                shutil.rmtree(class_path)
            self.update_class_list()  

    def open_analytics(self, class_name):
        logs_path = os.path.join("classes", class_name, "logs")
        if not os.path.exists(logs_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Для класса {class_name} нет логов!")
            return

        self.analytics_window = AnalyticsWindow(class_name, logs_path)
        self.analytics_window.show()

class AnalyticsWindow(QtWidgets.QWidget):
    def __init__(self, class_name, logs_path):
        super().__init__()
        self.setWindowTitle(f"Аналитика - {class_name}")
        self.setFixedSize(800, 600)
        self.logs_path = logs_path
        self.class_name = class_name
        self.initUI()

    def initUI(self):
        # Основной макет
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок
        header_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel(f"Аналитика посещаемости - {self.class_name}")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px; 
                font-weight: bold; 
                color: #333;
            }
        """)

        # Кнопка экспорта
        export_button = QtWidgets.QPushButton("🖨")
        export_button.setToolTip("Сохранить как Excel")
        export_button.setFixedSize(40, 40)
        export_button.clicked.connect(self.export_to_excel)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                border: none;
                border-radius: 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addWidget(export_button)

        # Добавляем заголовок и кнопку в основной макет
        layout.addLayout(header_layout)

        # Таблица
        self.logs_table = QtWidgets.QTableWidget()
        self.logs_table.setStyleSheet("""
        QTableWidget {
            gridline-color: #A9A9A9; /* Цвет разделительных линий */
            font-size: 12px; /* Размер шрифта */
            border: none;
        }
        QHeaderView::section {
            background-color: #0078D7; /* Цвет заголовков */
            color: white; /* Цвет текста заголовков */
            font-weight: bold;
            border: 1px solid #A9A9A9;
            padding: 5px;
        }
        QTableWidget::item {
            border: 1px solid #E0E0E0; /* Границы между ячейками */
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #B0E0E6; /* Цвет выделенной ячейки */
            color: black;
        }
        QTableWidget::item:first-column {
            color: black; /* Цвет текста для первой колонки */
            font-weight: normal; /* Убираем лишний акцент */
        }
        """)


        layout.addWidget(self.logs_table)

        self.setLayout(layout)
        self.load_logs()

    def load_logs(self):
        try:
            # Считываем файлы логов
            files = sorted([f for f in os.listdir(self.logs_path) if f.endswith(".txt")])
            attendance_data = {}

            # Чтение данных из логов и формирование словаря
            for file in files:
                date = file.replace(".txt", "")
                filepath = os.path.join(self.logs_path, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = [line.strip().split(" - ") for line in f if line.strip()]
                    attendance_data[date] = {line[0]: line[1] for line in lines}

            # Получаем полный список студентов
            all_students = set()
            for students in attendance_data.values():
                all_students.update(students.keys())

            # Настройка таблицы
            self.logs_table.setRowCount(len(all_students))
            self.logs_table.setColumnCount(len(attendance_data) + 1)
            self.logs_table.setHorizontalHeaderLabels(["Фамилия Имя"] + list(attendance_data.keys()))
            self.logs_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

            # Заполнение таблицы с центрированием текста
            for row, student in enumerate(sorted(all_students)):
                # Центрируем текст для первой колонки (Фамилия Имя)
                student_item = QtWidgets.QTableWidgetItem(student)
                student_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.logs_table.setItem(row, 0, student_item)

                # Центрируем текст для колонок с датами
                for col, date in enumerate(attendance_data.keys(), start=1):
                    status = attendance_data[date].get(student, "")
                    status_item = QtWidgets.QTableWidgetItem(status)
                    status_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.logs_table.setItem(row, col, status_item)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении логов: {e}")


    def export_to_excel(self):
        try:    
            # Извлекаем данные из таблицы
            headers = [self.logs_table.horizontalHeaderItem(i).text() for i in range(self.logs_table.columnCount())]
            data = []
            for row in range(self.logs_table.rowCount()):
                row_data = []
                for col in range(self.logs_table.columnCount()):
                    item = self.logs_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # Сохранение в Excel
            df = pd.DataFrame(data, columns=headers)
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            output_file = os.path.join(downloads_path, f"Аналитика_{self.class_name}.xlsx")
            df.to_excel(output_file, index=False)

            QtWidgets.QMessageBox.information(self, "Успех", f"Файл сохранён в: {output_file}")
            subprocess.run(["explorer", downloads_path])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {e}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
