import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
# Импортирование БД, интерфейса и окна


class Delete_Workers(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('delete_workers.ui', self)  # Загрузка интерфейса
        self.check_btn.clicked.connect(self.check)  # Запуск функции показывающей данные сотрудника
        self.back_btn.clicked.connect(self.go_back)  # Подключение кнопки "назад" к фунции закрытия окна
        self.delete_btn.clicked.connect(self.delete_data)  # подключение функции удаляющией информацию с определенным id
        self.setFixedSize(429, 533)

    def go_back(self):
        self.close()

    def check(self):
        # Инициализация подключения и переменных с данными с их дальнейшим занесением в окно
        conn = sqlite3.connect('workers_db.sqlite')
        cur = conn.cursor()
        id = self.id_pole.text()
        # Проверка корректности полученного id
        if id.isdigit():
            id = int(id)
            checker = cur.execute(f'''SELECT * FROM workers_db WHERE id = {id}''').fetchall()
            if checker:
                name = cur.execute(f'''SELECT full_name FROM workers_db WHERE id = {id}''').fetchall()
                age = cur.execute(f'''SELECT age FROM workers_db WHERE id = {id}''').fetchall()
                self.full_name.setText(*name[0])
                self.age.setText(str(*age[0]))
            else:
                self.stat_txt.setText('Некорректно введна информация')
        else:
            self.full_name.setText('Некорректно введна информация')
            self.age.setText('Некорректно введна информация')

    def delete_data(self):
        # Создание подключения и курсора
        conn = sqlite3.connect('workers_db.sqlite')
        cur = conn.cursor()
        # Инициализация id и его проверка на корректность
        id = self.id_pole.text()
        if id.isdigit():
            id = int(id)
            checker = cur.execute(f'''SELECT * FROM workers_db WHERE id = {id}''').fetchall()
            if checker:
                # Удаление строчки с id, который введен в поле
                cur.execute(f'''DELETE FROM workers_db 
                WHERE id = {id}''')
                text = f'''Пользователь с id = {id} был удален по причине:
                {self.select_combo.currentText()}'''
                self.stat_txt.setText(text)
                conn.commit()
                cur.close()
            else:
                self.stat_txt.setText('Некорректно введна информация')
        else:
            self.stat_txt.setText('Некорректно введна информация')