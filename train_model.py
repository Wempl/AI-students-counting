import face_recognition
import numpy as np
import os
import sys

class FaceRecognitionModel:
    def __init__(self, class_name):
        self.class_name = class_name
        self.known_faces = []
        self.known_names = []
        self.load_known_faces()

    import dlib
    import sys

    # def get_resource_path(relative_path):
    #     """Получает путь к ресурсу, учитывая временные файлы PyInstaller."""
    #     if hasattr(sys, '_MEIPASS'):  # PyInstaller добавляет _MEIPASS во время выполнения
    #         return os.path.join(sys._MEIPASS, relative_path)
    #     return os.path.join(os.path.abspath("."), relative_path)

    # # Используйте get_resource_path для загрузки модели
    # model_path = get_resource_path("models/shape_predictor_68_face_landmarks.dat")
    # shape_predictor = dlib.shape_predictor(model_path)


    def load_known_faces(self):
        """Загружаем известные лица и имена из файлов, если они существуют."""
        known_faces_path = f'classes/{self.class_name}/known_faces.npy'
        known_names_path = f'classes/{self.class_name}/known_names.npy'
        
        if os.path.exists(known_faces_path) and os.path.exists(known_names_path):
            self.known_faces = list(np.load(known_faces_path, allow_pickle=True))
            self.known_names = list(np.load(known_names_path, allow_pickle=True))
            print(f"Известные лица загружены для класса {self.class_name}.")
        else:
            print(f"Нет сохраненных лиц для класса {self.class_name}. Начинаем с пустой базы.")

    def save_known_faces(self):
        """Сохраняем текущие известные лица и имена в файлы."""
        known_faces_path = f'classes/{self.class_name}/known_faces.npy'
        known_names_path = f'classes/{self.class_name}/known_names.npy'
        
        np.save(known_faces_path, self.known_faces)
        np.save(known_names_path, self.known_names)
        print(f"Известные лица сохранены для класса {self.class_name}.")

    def add_student_face(self, student_name, photo_path):
        """Добавляем новое лицо ученика и сразу обучаем модель для этого лица."""
        # Загружаем изображение и вычисляем вектор признаков
        image = face_recognition.load_image_file(photo_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            student_face_encoding = face_encodings[0]
            self.known_faces.append(student_face_encoding)
            self.known_names.append(student_name)
            
            # Сохраняем обновленные данные известных лиц
            self.save_known_faces()
            print(f"Ученик {student_name} добавлен и обучен.")
        else:
            print(f"Лицо на фото для {student_name} не обнаружено. Попробуйте другое изображение.")

    def recognize_faces(self, unknown_image_path):
        """Распознаем лица на изображении и возвращаем список имен."""
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        recognized_names = []
        for unknown_encoding in unknown_encodings:
            # Сравниваем с известными лицами
            results = face_recognition.compare_faces(self.known_faces, unknown_encoding)
            if True in results:
                match_index = results.index(True)
                recognized_names.append(self.known_names[match_index])
            else:
                recognized_names.append("Неизвестный")

        return recognized_names