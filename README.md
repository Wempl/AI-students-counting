# Счетовод: умная система для учёта посещаемости

## Что это?
**Счетовод** — это приложение, которое помогает школам и другим учебным заведениям автоматизировать учёт посещаемости с помощью распознавания лиц. Больше не нужно тратить время на перекличку — всё делается автоматически!

## Что умеет приложение?
- **Авторизация и регистрация**: каждый пользователь создаёт свой аккаунт, данные хранятся в SQLite.
- **Создание классов**: легко создать класс, добавить учеников и загрузить их фотографии для обучения.
- **Распознавание лиц**: система понимает, кто присутствует, а кто отсутствует, просто глядя на камеру.
- **Аналитика посещаемости**: удобный просмотр статистики, экспорт данных в Excel.
- **Изменения на лету**: можно добавлять или удалять учеников, менять название класса.
- **Удаление классов**: если случайно создали класс — не беда, удалите его одной кнопкой!
- **Настройки камеры**: возможность выбрать камеру и проверить её работу.

## Как запустить?
1. Клонируйте проект:
   ```bash
   git clone https://github.com/Wempl/AI-students-counting
   ```
2. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите приложение:
   ```bash
   python auth_main.py
   ```

## На чём сделано?
- **Python** — язык программирования.
- **PyQt5** — для красивого интерфейса.
- **Face Recognition** — библиотека для работы с лицами.
- **SQLite** — база данных для хранения пользователей и другой информации.

## Что понадобится?
- Python версии 3.8 и выше.
- Установить библиотеки из `requirements.txt`.
- Камера для распознавания лиц.

## Контакты
Есть вопросы или предложения? Пишите на **Andrewbig18@mail.ru**.

------------------------

#### **In English**

# Schetovod: smart attendance tracker

## What is it?
**Schetovod** is an app designed to help schools and educational institutions automate attendance tracking using face recognition. Forget about roll calls — everything is done automatically!

## What does it do?
- **Sign up and Log in**: Every user gets their own account, stored securely in SQLite.
- **Create classes**: Easily create a class, add students, and upload their photos for training.
- **Face recognition**: Detect who’s present and who’s absent just by using a camera.
- **Attendance analytics**: View stats and export them to Excel.
- **Flexible changes**: Add or remove students, rename classes on the fly.
- **Delete classes**: Accidentally created a class? Delete it with a single click!
- **Camera settings**: Choose your camera and check the preview.

## How to run?
1. Clone the project:
   ```bash
   git clone https://github.com/Wempl/AI-students-counting
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bash
   python auth_main.py
   ```

## What’s it made with?
- **Python** — simple and powerful programming language.
- **PyQt5** — for the nice user interface.
- **Face Recognition** — a library to work with facial data.
- **SQLite** — to store users and other information.

## What do you need?
- Python 3.8 or higher.
- Install libraries from `requirements.txt`.
- A camera for face recognition.

## Contacts
Got questions or ideas? Reach out at **Andrewbig18@mail.ru**.

