from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI_template_PyQt5.initiationGUI import Initiation_GUI
from PyQt5.QtGui import *


class BalanceAndHoldingStatus(Initiation_GUI):
    def __init__(self):
        super().__init__()

        self.pushButton_2.clicked.connect(self.check_balance)

    def check_balance_in_simulation(self):
        account = self.ai.presentStatusInSimulation()
        portfolio = self.ai.portfolioForGUI()
        self.lineEdit_deposit.setText(account["deposit"])
        self.lineEdit_buy_total.setText(account["buy_price"])
        self.lineEdit_value_my_assets.setText(account["value_my_assets"])
        self.lineEdit_profit_total.setText(account["profit_total"])
        self.lineEdit_rate_total.setText(account["rate"])
        self.lineEdit_value_total.setText(account["value_total"])

        item_count = len(portfolio)
        self.tableWidget_2.setRowCount(item_count)
        for j in range(item_count):
            row = portfolio[j]
            for i in range(len(row) - 1):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignRight)
                if row[6] > 0:
                    item.setForeground(QBrush(QColor(214, 48, 49)))
                elif row[6] < 0:
                    item.setForeground(QBrush(QColor(9, 132, 227)))

                self.tableWidget_2.setItem(j, i, item)
        self.tableWidget_2.resizeRowsToContents()

    def check_balance(self):
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(";")[0]

        self.kiwoom.tr_input("opw00001")(account_number)
        self.kiwoom.tr_input("opw00018")(account_number)

        # balance
        item = self.kiwoom.opw00001
        self.lineEdit_deposit.setText(item + " 원")

        item = self.kiwoom.opw00018["single"]
        self.lineEdit_buy_total.setText(item[0] + " 원")
        self.lineEdit_value_total.setText(item[1] + " 원")
        self.lineEdit_profit_total.setText(item[2] + " 원")
        self.lineEdit_rate_total.setText(item[3] + " %")
        self.lineEdit_value_my_assets.setText(item[4] + " 원")

        # Item list
        item_count = len(self.kiwoom.opw00018["multi"])
        self.tableWidget_2.setRowCount(item_count)

        for j in range(item_count):
            row = self.kiwoom.opw00018["multi"][j]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignRight)
                self.tableWidget_2.setItem(j, i, item)

        self.tableWidget_2.resizeRowsToContents()
