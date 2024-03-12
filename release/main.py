import sys
import sqlite3
from main_ui import Ui_Form as UI_Form_main
from addEditCoffeeForm_ui import Ui_Form as UI_Form_edit
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class CoffeeTableApp(QWidget, UI_Form_main):
    def __init__(self):
        super(CoffeeTableApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.open_change_form)
        self.run()
        self.setWindowTitle('Кофебаза')
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Сорта", "Степень обжарки", "молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()

    def run(self):
        try:
            select = self.lineEdit.text()
            if not select:
                select = 'SELECT * FROM coffee'
            # Подключение к базе данных SQLite
            self.con = sqlite3.connect('data/coffee.db')
            cur = self.con.cursor()

            # Выполнение запроса для извлечения данных
            cur.execute(select)
            data = cur.fetchall()

            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))

            # Заполнение QTableWidget данными из запроса

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.tableWidget.setItem(row_num, col_num, item)
        except Exception as e_:
            print(e_)

    def open_change_form(self):
        self.change_form = EditCoffeeForm()
        self.change_form.show()


class EditCoffeeForm(QWidget, UI_Form_edit):
    def __init__(self):
        super(EditCoffeeForm, self).__init__()
        self.setupUi(self)
        self.titles = ['21', "Название сорта", "Степень обжарки", "молотый / в зернах",
                       'Описание вкуса', 'Цена', '4']

        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый / в зернах",
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый / в зернах",
                                                      'Описание вкуса', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget_2.resizeColumnsToContents()

        self.con = sqlite3.connect('data/coffee.db')
        cur = self.con.cursor()
        try:
            cur.execute(f"PRAGMA table_info(coffee)")
            self.table_column = [col[1] for col in cur.fetchall()[1:]]

            cur.execute('SELECT * FROM coffee')

            data = cur.fetchall()
            self.id_ = QTableWidgetItem(str(data[-1][0] + 1))
            self.tableWidget.setItem(0, 0, self.id_)

            self.pushButton.clicked.connect(self.change)
            self.pushButton_2.clicked.connect(self.add)
        except Exception as e_:
            print(e_)

    def add(self):
        try:
            cur = self.con.cursor()
            cols = self.tableWidget.columnCount()
            items = []
            for col in range(1, cols):
                item = self.tableWidget.item(0, col)
                if item:
                    items.append(item.text())
                else:
                    items.append(None)

            qwe = 'INSERT INTO coffee VALUES('
            qwe += ', '.join([f'"{val}"' for val in (self.id_.text(), *items)])
            qwe += ')'

            cur.execute(qwe)
            self.id_.setText(str(int(self.id_.text()) + 1))
            self.con.commit()
        except Exception as e_:
            print(e_)

    def change(self):
        try:
            cur = self.con.cursor()
            cols = self.tableWidget_2.columnCount()
            items = []
            id_ = self.tableWidget_2.item(0, 0).text()

            for col in range(1, cols):
                item = self.tableWidget_2.item(0, col)
                if item:
                    items.append(item.text())
                else:
                    items.append(None)

            qwe = 'UPDATE coffee SET '
            qwe += ", ".join([f"{self.table_column[i]}='{items[i]}'"
                              for i in range(6) if items[i]])
            qwe += " WHERE id = ?"
            cur.execute(qwe, (id_,))
            self.con.commit()
        except Exception as e_:
            print(e_)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee_app = CoffeeTableApp()
    coffee_app.show()
    sys.exit(app.exec_())
