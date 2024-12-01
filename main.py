from PyQt5 import QtWidgets, QtGui, QtCore
import os
import shutil
import pandas as pd
import numpy as np


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Счетовод")
        self.setFixedSize(800, 600)  # Фиксированный размер окна

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.logged_in_user = None  # Для передачи логина в настройки
        self.update_class_list()

    def update_class_list(self):
        # Очистка текущего содержимого layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Верхний layout для настроек
        top_layout = QtWidgets.QHBoxLayout()
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(top_layout)

        settings_button = QtWidgets.QPushButton("⚙️")
        settings_button.setFixedSize(40, 40)
        settings_button.setStyleSheet("font-size: 18px;")
        settings_button.clicked.connect(self.open_settings)
        top_layout.addWidget(settings_button, alignment=QtCore.Qt.AlignRight)

        # Установить отступ от верха
        top_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(top_widget, alignment=QtCore.Qt.AlignTop)

        # Проверка папки классов
        if not os.path.exists("classes"):
            os.makedirs("classes")

        classes = [f for f in os.listdir("classes") if os.path.isdir(os.path.join("classes", f))]

        if not classes:
            # Если классов нет, отображаем сообщение
            no_classes_label = QtWidgets.QLabel("К сожалению, программа не обнаружила созданных классов!")
            no_classes_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
            no_classes_label.setAlignment(QtCore.Qt.AlignCenter)  # Центрирование текста
            self.layout.addWidget(no_classes_label)

        else:
            for class_name in classes:
                # Создаем горизонтальный layout для класса
                class_layout = QtWidgets.QHBoxLayout()
                class_widget = QtWidgets.QWidget()
                class_widget.setLayout(class_layout)

                # Кнопка запуска класса
                class_button = QtWidgets.QPushButton(class_name)
                class_button.setStyleSheet("font-size: 14px; padding: 10px;")
                class_button.clicked.connect(lambda _, cn=class_name: self.start_class(cn))
                class_layout.addWidget(class_button)

                # Кнопка аналитики
                analytics_button = QtWidgets.QPushButton("📊")
                analytics_button.setFixedSize(40, 40)
                analytics_button.clicked.connect(lambda _, cn=class_name: self.open_analytics(cn))
                class_layout.addWidget(analytics_button)

                # Кнопка изменения названия класса
                edit_button = QtWidgets.QPushButton("📝")
                edit_button.setFixedSize(40, 40)  # Размер кнопки изменения
                edit_button.setStyleSheet("font-size: 14px;")
                edit_button.clicked.connect(lambda _, cn=class_name: self.rename_class(cn))
                class_layout.addWidget(edit_button)

                # Кнопка удаления класса
                delete_button = QtWidgets.QPushButton("🗑")
                delete_button.setFixedSize(40, 40)  # Устанавливаем такой же размер, как у кнопки настроек
                delete_button.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
                delete_button.clicked.connect(lambda _, cn=class_name: self.delete_class(cn))
                class_layout.addWidget(delete_button)

                # Добавляем класс в основной layout
                self.layout.addWidget(class_widget)

        # Кнопка создания нового класса
        create_class_button = QtWidgets.QPushButton("Создать класс")
        create_class_button.setStyleSheet("font-size: 16px; padding: 10px;")
        create_class_button.clicked.connect(self.create_class)
        self.layout.addWidget(create_class_button)
    
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
        # Проверяем, есть ли обученные данные
        class_path = os.path.join("classes", class_name)
        known_faces_path = os.path.join(class_path, "known_faces.npy")
        known_names_path = os.path.join(class_path, "known_names.npy")

        if not os.path.exists(known_faces_path) or not os.path.exists(known_names_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"У класса {class_name} отсутствуют обученные данные.")
            return

        # Загрузка данных
        known_faces = np.load(known_faces_path, allow_pickle=True)
        known_names = np.load(known_names_path, allow_pickle=True)

        # Импортируем AbsentStudentsWindow и запускаем окно
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
            self.hide()  # Скрыть главное окно

            def on_close_event(event):
                self.update_class_list()
                self.show()
                event.accept()

            self.create_class_window.closeEvent = on_close_event

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при создании класса: {e}")


    def open_settings(self):
        from setting import SettingsWindow
        self.settings_window = SettingsWindow()  # Передаём ссылку на главное окно
        self.settings_window.show()  # Показываем окно настроек
        self.show()





    def rename_class(self, class_name):
        new_name, ok = QtWidgets.QInputDialog.getText(self, "Переименовать класс", "Введите новое название класса:")
        if ok and new_name:
            old_path = os.path.join("classes", class_name)
            new_path = os.path.join("classes", new_name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                self.update_class_list()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Класс с именем {new_name} уже существует!")

    def delete_class(self, class_name):
        # Подтверждение удаления класса
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
            self.update_class_list()  # Обновляем список классов

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
        layout = QtWidgets.QVBoxLayout()

        # Создаем горизонтальный layout для заголовка и кнопки
        header_layout = QtWidgets.QHBoxLayout()

        # Заголовок таблицы
        self.label = QtWidgets.QLabel(f"                                                      История успеваемости - {self.class_name}")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.label)

        # Кнопка экспорта
        export_button = QtWidgets.QPushButton("🖨")
        export_button.setToolTip("Сохранить как Excel")
        export_button.setFixedSize(40, 40)
        export_button.clicked.connect(self.export_to_excel)
        header_layout.addWidget(export_button, alignment=QtCore.Qt.AlignRight)

        # Добавляем горизонтальный layout (заголовок + кнопка) в основной layout
        layout.addLayout(header_layout)

        # Таблица
        self.logs_table = QtWidgets.QTableWidget()
        layout.addWidget(self.logs_table)

        self.setLayout(layout)
        self.load_logs()


    def load_logs(self):
        try:
            files = sorted([f for f in os.listdir(self.logs_path) if f.endswith(".txt")])
            attendance_data = {}
            
            for file in files:
                date = file.replace(".txt", "")
                filepath = os.path.join(self.logs_path, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = [line.strip().split(" - ") for line in f if line.strip()]
                    attendance_data[date] = {line[0]: line[1] for line in lines}

            all_students = set()
            for students in attendance_data.values():
                all_students.update(students.keys())

            self.logs_table.setRowCount(len(all_students))
            self.logs_table.setColumnCount(len(attendance_data) + 1)
            self.logs_table.setHorizontalHeaderLabels(["Фамилия Имя"] + list(attendance_data.keys()))

            for row, student in enumerate(sorted(all_students)):
                self.logs_table.setItem(row, 0, QtWidgets.QTableWidgetItem(student))
                for col, date in enumerate(attendance_data.keys(), start=1):
                    status = attendance_data[date].get(student, "")
                    if status != "ПР":  # Если статус не "ПР", добавляем в таблицу
                        self.logs_table.setItem(row, col, QtWidgets.QTableWidgetItem(status))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении логов: {e}")

    def export_to_excel(self):
        try:
            # Получаем данные из таблицы
            headers = [self.logs_table.horizontalHeaderItem(i).text() for i in range(self.logs_table.columnCount())]
            data = []
            for row in range(self.logs_table.rowCount()):
                row_data = []
                for col in range(self.logs_table.columnCount()):
                    item = self.logs_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # Сохраняем в Excel
            df = pd.DataFrame(data, columns=headers)
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            output_file = os.path.join(downloads_path, f"Аналитика_{self.class_name}.xlsx")
            df.to_excel(output_file, index=False)
            
            QtWidgets.QMessageBox.information(self, "Успех", f"Файл сохранён в: {output_file}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {e}")
      


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
