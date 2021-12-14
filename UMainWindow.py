import sqlite3
import sys
import os.path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from add_workers import AddWorkers
from Find_worker import Find_Workers
from view_workers import View_Workers
from delete_workers import Delete_Workers
from change_workers import Change_Workers


# Импортирование приложения, БД, интерфейсов, окна, системы, файлов и классов из других файлов проекта


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_file()  # вызов функции создания базу данных при ее отсутствии
        uic.loadUi('MainWindow.ui', self)  # Загрузка интерфейса
        # Вызов функций окрывыющих новое окно после нажатия на соответствующую кнопку
        self.add_archive_btn.clicked.connect(self.open_adder)
        self.find_archive_btn.clicked.connect(self.open_finder)
        self.watch_archive_btn.clicked.connect(self.open_viewer)
        self.delete_archive_btn.clicked.connect(self.open_deleter)
        self.change_archive_btn.clicked.connect(self.open_changer)
        self.setFixedSize(287, 600)

    # Функции, открывающие новые окна
    def open_changer(self):
        self.Next = Change_Workers()
        self.Next.show()

    def open_deleter(self):
        self.Next = Delete_Workers()
        self.Next.show()

    def open_adder(self):
        self.Next = AddWorkers()
        self.Next.show()

    def open_viewer(self):
        self.Next = View_Workers()
        self.Next.show()

    def open_finder(self):
        self.Next = Find_Workers()
        self.Next.show()

    def do_service_line(self):
        conn = sqlite3.connect(r'workers_db.sqlite')
        cur = conn.cursor()
        cur.execute('''INSERT INTO workers_db(id, full_name, image, age) VALUES(1, '-', '', '0')''')
        conn.commit()
        cur.close()

    def check_file(self):
        if not os.path.isfile('workers_db.sqlite'):
            conn = sqlite3.connect(r'workers_db.sqlite')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS workers_db (
    id        INTEGER      PRIMARY KEY AUTOINCREMENT
                           NOT NULL
                           UNIQUE,
    full_name STRING NOT NULL,
    age       INTEGER (99) NOT NULL,
    image     BLOB
);''')
            conn.commit()
            cur.close()
            self.do_service_line()  # Вызов метода, добавляющего в базу 1 начальную строку при пересоздании БД


if __name__ == '__main__':  # Запуск приложения
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
