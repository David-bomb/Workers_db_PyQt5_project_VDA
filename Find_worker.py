import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

# Импортирование БД, интерфейса, окна и таблиц

NAMES = ['id', 'ФИО', 'Возраст', 'image_data']  # константа


class Find_Workers(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('filter_base.ui', self)  # загружаем интерфейс
        self.connection = sqlite3.connect("workers_db.sqlite")  # загружаем базу данных
        self.find_btn.clicked.connect(self.select_data)  # Вызываем функцию, создающую таблицу с фильтром при нажатии
        self.create_table()  # Вызываем функцию, создающую таблицу с фильтром
        self.back_btn.clicked.connect(self.go_back)  # Подключение кнопки "назад" к фунции закрытия окна
        self.setFixedSize(429, 533)

    def go_back(self):
        self.close()

    def create_table(self):
        # Создаем запрос
        query = "SELECT * FROM workers_db"
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.table_wgt.setColumnCount(4)
        self.table_wgt.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.table_wgt.setRowCount(
                self.table_wgt.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_wgt.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        # Даем название колонкам таблицы
        self.table_wgt.setHorizontalHeaderLabels(NAMES)

    def select_data(self):
        # Создаем запрос
        query = ''
        # Попытка проверить корректность информации с дальнейшим ее использованием для фильтрации, при провале которой
        # будет выведена ошибка
        try:
            self.filter_text.setText('Фильтр')
            if self.id_pole.text().isalpha() or self.name_pole.text().isdigit() or self.age_pole.text().isalpha():
                self.filter_text.setText('ОШИБКА ФИЛЬТРА')
            elif self.id_pole.text() and self.name_pole.text() and self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 full_name like '%{self.name_pole.text()}%' AND
                 id = {self.id_pole.text()} AND 
                 age = {self.age_pole.text()} '''
            elif self.id_pole.text() and self.name_pole.text() and not self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 full_name like '%{self.name_pole.text()}%' AND
                 id = {self.id_pole.text()} '''
            elif self.id_pole.text() and not self.name_pole.text() and not self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 id = {self.id_pole.text()} '''
            elif self.id_pole.text() and not self.name_pole.text() and self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 id = {self.id_pole.text()} AND 
                 age = {self.age_pole.text()} '''
            elif not self.id_pole.text() and self.name_pole.text() and self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 full_name like '%{self.name_pole.text()}%' AND
                 age = {self.age_pole.text()} '''
            elif not self.id_pole.text() and not self.name_pole.text() and self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 age = {self.age_pole.text()} '''
            elif not self.id_pole.text() and self.name_pole.text() and not self.age_pole.text():
                query = f'''SELECT * FROM workers_db WHERE
                 full_name like '%{self.name_pole.text()}%' '''
            elif not self.id_pole.text() and not self.name_pole.text() and not self.age_pole.text():
                query = f'''SELECT * FROM workers_db'''
        except Exception:
            self.filter_text.setText('ОШИБКА ФИЛЬТРА')

        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.table_wgt.setColumnCount(4)
        self.table_wgt.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.table_wgt.setRowCount(
                self.table_wgt.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_wgt.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.table_wgt.setHorizontalHeaderLabels(NAMES)

    def closeEvent(self, event):
        # Отключаемся от БД
        self.connection.close()
