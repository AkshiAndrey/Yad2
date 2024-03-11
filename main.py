import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget


class CoffeeTableApp(QWidget):
    def __init__(self):
        super(CoffeeTableApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.open_change_form)
        self.run()
        self.setWindowTitle('Кофебаза')
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Сорта", "Степень обжарки", "молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])

    def run(self):
        select = self.lineEdit.text()
        if not select:
            select = 'SELECT * FROM coffee'
        # Подключение к базе данных SQLite
        connection = sqlite3.connect('coffee.db')
        cursor = connection.cursor()

        # Выполнение запроса для извлечения данных
        cursor.execute(select)
        data = cursor.fetchall()
        print(data)

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        # Заполнение QTableWidget данными из запроса

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_num, col_num, item)

    def open_change_form(self):
        self.change_form = EditCoffeeForm()
        self.change_form.show()


class EditCoffeeForm(QWidget):
    def __init__(self):
        super(EditCoffeeForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.titles = ["ID", "Название", "Сорта", "Степень обжарки", "молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки']

        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Сорта", "Степень обжарки", "молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Название", "Сорта", "Степень обжарки", "молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])



        connection = sqlite3.connect('coffee.db')
        cursor = connection.cursor()

        # Выполнение запроса для извлечения данных
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()
        print(data)
        self.id_ = QTableWidgetItem(str(data[-1][0] + 1))
        print(self.id_.text())
        self.tableWidget.setItem(0, 0, self.id_)

        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.add)

    def add(self):
        connection = sqlite3.connect('coffee.db')
        cursor = connection.cursor()
        print('INSERT INTO coffee({0}, {1}, {2}, {3}, {4}, {5}, {6}) VALUES ({7}, {8}, {9}, {10}, {11}, {12}, {13})'.format(*self.titles[1:], *self.titles[1:]))
        # Выполнение запроса для извлечения данных
        # cursor.execute(f'INSERT INTO coffee (Название, Сорта, Степень обжарки, '
        #                'молотый / в зернах, Описание вкуса, Цена, Объем упаковки)'
        #                ' VALUES (?, ?, ?, ?, ?, ?)'.format())
        cursor.execute('INSERT INTO coffee VALUES ({7}, {8}, {9}, {10}, {11}, {12}, {13})'.format(*self.titles[1:], *self.titles[1:]))
        print('тыц')
        pass

    def change(self):
        print('тыц')
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # coffee_app = CoffeeTableApp()
    coffee_app = EditCoffeeForm()
    coffee_app.show()
    sys.exit(app.exec_())
