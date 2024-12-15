import cv2
from PyQt5 import QtWidgets, QtGui, QtCore


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Убираем стандартную рамку окна
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Прозрачность окна
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)

        # Основной контейнер с белым фоном и закруглёнными углами
        wrapper = QtWidgets.QWidget(self)
        wrapper.setGeometry(0, 0, 800, 600)
        wrapper.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)

        # Картинка закрытия окна (красный крестик)
        close_button = QtWidgets.QPushButton(wrapper)
        close_button.setFixedSize(40, 40)
        close_button.setIcon(QtGui.QIcon("icons/1.png"))  # Убедитесь, что картинка находится в папке icons
        close_button.setIconSize(QtCore.QSize(40, 40))
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
        """)
        close_button.clicked.connect(self.close_window)
        close_button.move(750, 10)  # Позиция крестика (справа вверху)

        # Основной layout
        layout = QtWidgets.QVBoxLayout(wrapper)
        layout.setContentsMargins(20, 60, 20, 20)

        # Предпросмотр камеры
        self.camera_preview = QtWidgets.QLabel("Предпросмотр камеры")
        self.camera_preview.setFixedSize(640, 480)
        self.camera_preview.setStyleSheet("""
            QLabel {
                border: 2px solid #0078D7;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.camera_preview, alignment=QtCore.Qt.AlignCenter)

        # Выпадающий список
        self.camera_dropdown = QtWidgets.QComboBox()
        self.camera_dropdown.setStyleSheet("""
            QComboBox {
                border: 1px solid #0078D7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.camera_dropdown.currentIndexChanged.connect(self.update_camera_preview)
        layout.addWidget(self.camera_dropdown, alignment=QtCore.Qt.AlignCenter)

        self.populate_camera_dropdown()
        self.setLayout(layout)

    def populate_camera_dropdown(self):
        """Заполняет список доступных камер."""
        self.camera_dropdown.clear()
        self.cameras = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                break
            camera_name = f"Камера {index}"
            self.cameras.append(index)
            self.camera_dropdown.addItem(camera_name)
            cap.release()
            index += 1
        if not self.cameras:
            self.camera_preview.setText("Камеры не найдены")

    def update_camera_preview(self):
        """Обновляет предпросмотр камеры."""
        selected_camera_index = self.camera_dropdown.currentIndex()
        if selected_camera_index == -1 or not self.cameras:
            return

        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()

        self.camera = cv2.VideoCapture(self.cameras[selected_camera_index], cv2.CAP_DSHOW)
        if not self.camera.isOpened():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось открыть камеру")
            return

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.display_camera_frame)
        self.timer.start(30)

    def display_camera_frame(self):
        """Отображает кадры с камеры."""
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qt_image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
                self.camera_preview.setPixmap(QtGui.QPixmap.fromImage(qt_image))

    def close_window(self):
        """Закрывает окно настроек и показывает главное окно."""
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()
        self.main_window.show()
        self.close()

    # Логика для перетаскивания окна
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.pos() - self.old_pos
            self.move(self.pos() + delta)

    def mouseReleaseEvent(self, event):
        self.old_pos = None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Главное окно-заглушка
    main_window = QtWidgets.QWidget()
    main_window.setWindowTitle("Главное окно")
    main_window.setFixedSize(800, 600)

    # Открытие окна настроек
    settings_window = SettingsWindow(main_window)
    settings_window.show()
    sys.exit(app.exec_())
