import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class CoffeeTableApp(QWidget):
    def __init__(self):
        super(CoffeeTableApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_app = CoffeeTableApp()
    coffee_app.show()
    sys.exit(app.exec_())
