import cv2
from PyQt5 import QtWidgets, QtGui, QtCore


class SettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def closeEvent(self, event):
        """Событие закрытия окна."""
        if self.parent_window:
            self.parent_window.show() 
        super().closeEvent(event)  

    def initUI(self):
        self.setWindowTitle("Настройки")
        self.setFixedSize(800, 600)
        
        


        layout = QtWidgets.QVBoxLayout()

       
        title_label = QtWidgets.QLabel("Настройки камеры")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        self.camera_preview = QtWidgets.QLabel("Предпросмотр камеры")
        self.camera_preview.setFixedSize(640, 480)
        self.camera_preview.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.camera_preview, alignment=QtCore.Qt.AlignCenter)

    
        self.camera_dropdown = QtWidgets.QComboBox()
        self.camera_dropdown.setPlaceholderText("Выберите камеру")
        self.camera_dropdown.currentIndexChanged.connect(self.update_camera_preview)
        layout.addWidget(self.camera_dropdown, alignment=QtCore.Qt.AlignCenter)

        
        self.populate_camera_dropdown()

        self.setLayout(layout)

    def populate_camera_dropdown(self):
        """Находим доступные камеры и заполняем выпадающий список."""
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
        """Обновляет предпросмотр камеры на основе выбранной в списке."""
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
        """Обновляет изображение с камеры в окне предпросмотра."""
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                self.camera_preview.setPixmap(QtGui.QPixmap.fromImage(qt_image))
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Ошибка считывания кадра")
                self.timer.stop()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
