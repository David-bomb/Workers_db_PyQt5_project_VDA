import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
# Импорт БД, интерфейса и окна


class Change_Workers(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(231, 382)
        uic.loadUi('change_workers.ui', self)  # Загрузка интерфейса
        self.check_btn.clicked.connect(self.check)  # Запуск функции показывающей данные сотрудника
        self.back_btn.clicked.connect(self.go_back)  # Подключение кнопки "назад" к фунции закрытия окна
        self.change_btn.clicked.connect(self.change_data)  # подключение функции удаляющией информацию с определенным id
        self.image_name = ''

    def go_back(self):
        self.close()

    def check(self):
        # Инициализация подключения и переменных с данными с их дальнейшим занесением в окно
        conn = sqlite3.connect('workers_db.sqlite')
        cur = conn.cursor()
        # Проверка id на корректность
        id = self.id_pole.text()
        if id.isdigit():
            id = int(id)
            checker = cur.execute(f'''SELECT * FROM workers_db WHERE id = {id}''').fetchall()
            if checker:
                # Вывод текущих данных
                name = cur.execute(f'''SELECT full_name FROM workers_db WHERE id = {id}''').fetchall()
                age = cur.execute(f'''SELECT age FROM workers_db WHERE id = {id}''').fetchall()
                cur.close()
                self.full_name.setText(*name[0])
                self.age.setText(str(*age[0]))
            else:
                self.stat_label.setText('Введен несуществующий id')
        else:
            self.stat_label.setText('Введены некорректные данные')

    def change_data(self):
        # Проверка корректности ФИО и возраста с дальнейшим созданием подключения и курсора
        if (self.full_name_pole.text() and self.age_pole.text()) and \
                (not self.full_name_pole.text().isdigit() and self.age_pole.text().isdigit()) and \
                16 <= int(self.age_pole.text()) < 65:
            conn = sqlite3.connect('workers_db.sqlite')
            cur = conn.cursor()
            id = self.id_pole.text()
            # Проверка корректности полученного id
            if id.isdigit():
                checker = cur.execute(f'''SELECT * FROM workers_db WHERE id = {id}''').fetchall()
                if checker:
                    # Замена возраста и ФИО
                    cur.execute(f'''UPDATE workers_db
                    SET full_name = '{self.full_name_pole.text()}'
                    WHERE id = {id}''')
                    cur.execute(f'''UPDATE workers_db
                    SET age = {self.age_pole.text()}
                    WHERE id = {id}''')
                    conn.commit()
                    cur.close()
                    self.stat_label.setText('-')
                else:
                    self.stat_label.setText('Введены некорректные данные')
            else:
                self.stat_label.setText('Введены некорректные данные')
        else:
            self.stat_label.setText('Введены некорректные данные')
