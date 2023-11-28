import sys
import sqlite3
import datetime

from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from design import Ui_MainWindow



class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pixmap = QPixmap("image/image1.png")
        self.nadpis11.setPixmap(self.pixmap)
        self.nadpis_racxod_doxod.setPixmap(QPixmap("image/image4.png"))
        self.nadpis_kartina_doxoda.setPixmap(QPixmap("image/image3.png"))
        self.nadpis_kartinkaproverki.setPixmap(QPixmap("image/image5.png"))


        first_screen = QMessageBox()
        first_screen.setWindowTitle("Контроль финансов")
        first_screen.setText("<p align='center'>Приветствуем!<br>"
                             "Если счет не создан пожалуйста создайте новый.<br>"
                             "Создавайте доходы и расходы, смотрите аналитику</p>")
        first_screen.setInformativeText("<p align='center'>Удачи вам выйти в плюс в этом месяце! </p>")

        first_screen.exec_()


        self.con = sqlite3.connect("data.db")
        self.vibrat_proverku_deneg()
        self.vibrat_doxod()
        self.vibrat_datu_deneg()
        self.balance()
        self.combo()


        self.cnopka1.clicked.connect(self.new_checking)
        self.cnopka_doxod.clicked.connect(self.new_income)
        self.cnopka_racxod.clicked.connect(self.new_spent)
        self.cnopka_statistika.clicked.connect(self.spent_statistic)


        date_now = datetime.datetime.today()
        self.date_racxod.setDateTime(date_now)
        self.date_doxod.setDateTime(date_now)
        self.date_statistika1.setDateTime(date_now)
        self.date_statistika2.setDateTime(date_now)

    def spent_statistic(self):

        racxod = self.comboBox.currentText()
        baza1 = tuple([int(i) for i in self.date_statistika1.text().split('.')][::-1])
        baza2 = tuple([int(i) for i in self.date_statistika2.text().split('.')][::-1])
        cur = self.con.cursor()
        query = f"SELECT money, date FROM spent_table WHERE type = '{racxod}'"
        dengi = cur.execute(query).fetchall()
        baza1 = datetime.datetime(*baza1)
        baza2 = datetime.datetime(*baza2)
        result = []
        for i in dengi:
            date_spent = tuple([int(j) for j in i[1].split('.')][::-1])
            date_spent = datetime.datetime(*date_spent)
            if baza1 <= date_spent <= baza2:
                result.append(i[0])
        self.labelzadoxod.setText(f'{sum(result)} руб')
        self.labelzadoxod.setAlignment(Qt.AlignCenter)

    def balance(self):
        cur = self.con.cursor()
        querydengi = f"SELECT money FROM checking"
        proverkadeneg = cur.execute(querydengi).fetchall()
        res = sum([i[0] for i in proverkadeneg])
        self.dengiseichas.setText(f'{res} руб')
        self.dengiseichas.setAlignment(Qt.AlignCenter)
        if res < 30000:
            self.citati.setText('Деньги - это не главное, возможно...')
        elif res < 60000:
            self.citati.setText('Время и деньги по большей части взаимозаменяемы...')
        elif res < 100000:
            self.citati.setText('Нельзя купить счастье за деньги, но можно арендовать...')
        else:
            self.citati.setText('Жизнь — игра, а деньги — способ вести счет...')
        self.citati.setAlignment(Qt.AlignCenter)
        self.citati.setFont(QFont('Monotype Corsiva', 15))
        querydengi = f"SELECT money FROM income_table"
        dengi_doxodi = cur.execute(querydengi).fetchall()
        res = sum([i[0] for i in dengi_doxodi])
        self.vse_dengi.setText(f'{res} руб')
        self.vse_dengi.setAlignment(Qt.AlignCenter)
        querydengi = f"SELECT money FROM spent_table"
        dengi_doxodi = cur.execute(querydengi).fetchall()
        res = sum([i[0] for i in dengi_doxodi])
        self.vse_rasxodi.setText(f'{res} руб')
        self.vse_rasxodi.setAlignment(Qt.AlignCenter)

    def new_spent(self):
        denejki = float(self.napiji_denegin_rasxod.text().replace(',', '.'))
        drugoi = self.napiji_rasxod.text()
        opat_racxodi = self.napiji_racxod.currentText()
        proverit = self.napiji_tip_doxod.currentText()
        date_income = self.date_racxod.text()
        cur = self.con.cursor()
        query = f"""INSERT INTO spent_table(date, money, type, checking, note)
                    VALUES(?, ?, ?, ?, ?)"""
        datatuple = (date_income, denejki, opat_racxodi, proverit, drugoi)
        cur.execute(query, datatuple)
        proverka_denejek = f"SELECT money FROM checking where name='{proverit}'"
        dengi_iz_prosh = cur.execute(proverka_denejek).fetchall()[0][0]
        dengi_iz_prosh -= denejki
        query = f"UPDATE checking set money = {dengi_iz_prosh} WHERE name = '{proverit}'"
        cur.execute(query)
        self.con.commit()
        self.vibrat_proverku_deneg()
        self.vibrat_datu_deneg()
        self.balance()

    def new_income(self):
        dengi = float(self.napiji_doxod.text().replace(',', '.'))
        drugoe = self.drugoi_doxod.text()
        tip_doxoda = self.napisat_tip_doxoda.currentText()
        tip_proverka = self.napiji_tip_proverki_doxoda.currentText()
        data_racxoda = self.date_doxod.text()
        cur = self.con.cursor()
        query = f"""INSERT INTO income_table(date, money, type_income, checking, note)
                    VALUES(?, ?, ?, ?, ?)"""
        dt_spisok = (data_racxoda, dengi, tip_doxoda, tip_proverka, drugoe)
        cur.execute(query, dt_spisok)
        nemnogo_deneg = f"SELECT money FROM checking where name='{tip_proverka}'"
        starie_dengi = cur.execute(nemnogo_deneg).fetchall()[0][0]
        dengi += starie_dengi
        query = f"UPDATE checking set money = {dengi} WHERE name = '{tip_proverka}'"
        cur.execute(query)
        self.con.commit()
        self.vibrat_proverku_deneg()
        self.vibrat_doxod()
        self.balance()

    def new_checking(self):
        name1 = self.novii_scet.text()
        cur = self.con.cursor()
        query = f"""INSERT INTO checking(name) VALUES('{name1}')"""
        cur.execute(query)
        self.con.commit()
        self.vibrat_proverku_deneg()
        self.combo()
        self.balance()

    def combo(self):
        res = self.con.cursor().execute("SELECT name FROM spent_type").fetchall()
        racxod_tip = [i[0] for i in res]
        self.napiji_racxod.addItems(racxod_tip)
        self.comboBox.clear()
        self.comboBox.addItems(racxod_tip)
        query = "SELECT name FROM checking"
        res = self.con.cursor().execute(query).fetchall()
        spisok_scitov = [i[0] for i in res]
        self.napiji_tip_doxod.clear()
        self.napiji_tip_proverki_doxoda.clear()
        self.napiji_tip_doxod.addItems(spisok_scitov)
        self.napiji_tip_proverki_doxoda.addItems(spisok_scitov)
        res = self.con.cursor().execute("SELECT name FROM income_type").fetchall()
        doxod_tip = [i[0] for i in res]
        self.napisat_tip_doxoda.clear()
        self.napisat_tip_doxoda.addItems(doxod_tip)

    def vibrat_datu_deneg(self):
        query = "SELECT * FROM spent_table"
        res = self.con.cursor().execute(query).fetchall()
        self.tablica_racxodov.setColumnCount(6)
        self.tablica_racxodov.setRowCount(0)
        hed = ['№', 'Датa', 'Сумма' + ' ' * 20, 'Причина расхода',
               'Счёт списания', 'Примечание']
        self.tablica_racxodov.setHorizontalHeaderLabels(hed)
        for i, row in enumerate(res):
            self.tablica_racxodov.setRowCount(
                self.tablica_racxodov.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tablica_racxodov.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tablica_racxodov.resizeColumnsToContents()

    def vibrat_doxod(self):
        query = "SELECT * FROM income_table"
        res = self.con.cursor().execute(query).fetchall()
        self.tablica_doxodov.setColumnCount(6)
        self.tablica_doxodov.setRowCount(0)
        hed = ['№', 'Датa', 'Сумма' + ' ' * 20, 'Источник дохода',
               'Счёт поступления', 'Примечание']
        self.tablica_doxodov.setHorizontalHeaderLabels(hed)
        for i, row in enumerate(res):
            self.tablica_doxodov.setRowCount(
                self.tablica_doxodov.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tablica_doxodov.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tablica_doxodov.resizeColumnsToContents()

    def vibrat_proverku_deneg(self):
        query = "SELECT name, money FROM checking"
        res = self.con.cursor().execute(query).fetchall()
        self.tablica_scetov.setColumnCount(2)
        self.tablica_scetov.setRowCount(0)
        self.tablica_scetov.setHorizontalHeaderLabels(["Назавание счёта" + ' ' * 70, "Остаток" + ' ' * 100])
        for i, row in enumerate(res):
            self.tablica_scetov.setRowCount(
                self.tablica_scetov.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tablica_scetov.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tablica_scetov.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
