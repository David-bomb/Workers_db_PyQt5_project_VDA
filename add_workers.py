import time
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import sqlite3
from PyQt5 import uic
import base64


# Импортирование Диалоговых окон, БД, интерфейсов, base64


class AddWorkers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_name = ''
        uic.loadUi('add_worker.ui', self)  # Загрузка интерфейса
        self.image_browse_btn.clicked.connect(self.browse_image)  # При нажатии на кнопку выбора изображения вызывается
        # функция выбора картинки из памяти компьютера пользователя
        self.input_btn.clicked.connect(self.start)  # При нажатии на кнопку ввода информации проверяется введены ли
        # данные корректно и введены ли они вообще
        self.back_btn.clicked.connect(self.go_back)  # Подключение кнопки "назад" к фунции закрытия окна
        self.setFixedSize(444, 237)

    def go_back(self):
        self.close()

    def browse_image(self):
        self.image_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                      '', 'Картинка (*.jpg)')[0]
        self.way_label.setText(self.image_name)

    def start(self):
        if self.full_name_pole.text() == '':  # Проверка наличия ФИО
            self.stat_label.setText('ФИО не введен')
        elif self.age_pole.text() == '':  # Проверка наличия возраста
            self.stat_label.setText('Возраст не введен')
        elif not self.age_pole.text().isdigit():
            self.stat_label.setText('Введен неккоректный возраст')
        elif not 16 <= int(self.age_pole.text()) < 65:  # Проверка соответствия возраста законам РФ
            self.stat_label.setText('Введен неккоректный возраст')
        elif not self.image_name:  # Проверка наличия картинки
            self.stat_label.setText('Изображение не выбрано')
        elif self.full_name_pole.text().isdigit():
            self.stat_label.setText('Некорректный ФИО')
        else:
            # Внесение данных в базу
            self.conn = sqlite3.connect('workers_db.sqlite')
            self.send_info(self.image_name)
            self.stat_label.setText('Сотрудник добавлен!')
            time.sleep(0.5)
            self.stat_label.setText('---')

    def send_info(self, picture_file):  # Функция заносящая данные в БД
        cur = self.conn.cursor()
        with open(picture_file, mode='rb') as f:  # Считывание бинарного содержимого изображения
            image_data = base64.b64encode(f.read())
        # Запись данных работника в базу данных
        sql = '''INSERT INTO workers_db(full_name, age, image) VALUES(?, ?, ?)'''
        data_tuple = (self.full_name_pole.text(), int(self.age_pole.text()), image_data)
        cur.execute(sql, data_tuple)
        self.conn.commit()
