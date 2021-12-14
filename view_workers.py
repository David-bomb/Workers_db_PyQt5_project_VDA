import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

# Импортирование БД, интерфейса, окна и таблиц
NAMES = ['id', 'ФИО', 'Возраст', 'image_data']  # константа


class View_Workers(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('view_archive.ui', self)
        self.connection = sqlite3.connect("workers_db.sqlite")  # загружаем базу данных
        self.update_btn.clicked.connect(self.table_data)  # Вызываем функцию, обновляющую данные таблицы
        self.table_data()  # Вызываем функцию, создающую таблицу
        self.back_btn.clicked.connect(self.go_back)  # Подключение кнопки "назад" к фунции закрытия окна
        self.setFixedSize(430, 636)

    def go_back(self):
        self.close()

    def table_data(self):
        res = self.connection.cursor().execute("SELECT * FROM workers_db").fetchall()
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

    def closeEvent(self, event):
        # Отключаемся от БД
        self.connection.close()
