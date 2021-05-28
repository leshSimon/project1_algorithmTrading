from GUI_template_PyQt5.balanceAndHoldingStatus import BalanceAndHoldingStatus
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ControlBox(BalanceAndHoldingStatus):
    def __init__(self):
        super().__init__()

        self.pushButton_4.clicked.connect(self.printConsole)
        self.pushButton_ai_operate.clicked.connect(self.operateAI)
        self.pushButton_ai_stop.clicked.connect(self.stopAI)
        self.pushButton_AI_stopAndSellThemAll.clicked.connect(self.stopAI_andSellThemAll)
        self.pushButton_AI_stopAndSellThemAll.clicked.connect(self.stopAI_andSellThemAll)
        self.simulationFirstStart: bool = True
        self.pushButton_200list_stock_change.clicked.connect(self.list200_stock_change)

    def list200_stock_change(self):
        self.ai.change_selected_stocks()

    def operateAI(self):
        self.label_ai_status.setText("동작중")
        if self.label_operating_env.text() == "실제투자":
            self.ai_run_in_real = True
        elif self.label_operating_env.text() == "모의투자":
            self.ai_run_in_imitation = True
        else:
            if self.simulationFirstStart:
                self.ai.simulationInit(startDate=20190515)
                self.simulationFirstStart = False
            self.ai_run_in_simulation = True

    def stopAI(self):
        self.label_ai_status.setText("정지중")
        if self.label_operating_env.text() == "실제투자":
            self.ai_run_in_real = False
        elif self.label_operating_env.text() == "모의투자":
            self.ai_run_in_imitation = False
        else:
            self.ai_run_in_simulation = False

    def stopAI_andSellThemAll(self):
        self.stopAI()
        if self.label_operating_env.text() == "실제투자":
            pass
        elif self.label_operating_env.text() == "모의투자":
            pass
        else:
            self.ai.sellThemAll_in_simulation()
            self.check_balance_in_simulation()

    def simulation_initialization(self):
        self.stopAI_andSellThemAll()
        self.ai.simulationInit(startDate=20190515)
        self.simulationFirstStart = False

    def printConsole(self):
        code = self.lineEdit.text()
        self.kiwoom.tr_input("opt10079")(code, "1:1틱", 1)
        print(self.kiwoom.opt10079)
        while self.kiwoom.remained_data:
            self.kiwoom.tr_request_next("opt10079")
            print(self.kiwoom.opt10079)

    # def findOutNameByCodeChange(self):
    #     code = self.lineEdit.text()
    #     name = self.kiwoom.get_master_code_name(code)
    #     self.lineEdit_2.setText(name)

    # def send_order(self):
    #     order_type_lookup = {"신규매수": 1, "신규매도": 2, "매수취소": 3, "매도취소": 4}
    #     hoga_lookup = {"지정가": "00", "시장가": "03"}

    #     account = self.comboBox.currentText()
    #     order_type = self.comboBox_2.currentText()
    #     code = self.lineEdit.text()
    #     hoga = self.comboBox_3.currentText()
    #     num = self.spinBox.value()
    #     price = self.spinBox_2.value()

    #     self.kiwoom.send_order(
    #         "send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], ""
    #     )
