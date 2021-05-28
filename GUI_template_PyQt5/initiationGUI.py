# from stock_API.deashinAPI.login import autoLogin
from AI.pymon import PyMon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from stock_API.kiwoomAPI import Kiwoom

form_class = uic.loadUiType("./GUI_template_PyQt5/assets/pytrader2.ui")[0]


class Initiation_GUI(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # autoLogin()
        self.kiwoom = Kiwoom()
        self.ai = PyMon()

        self.comboBox.addItems(self.kiwoom.accounts_list)

        self.label_operating_env.setText("시뮬레이션")
        self.ai_run_in_simulation: bool = False
        self.ai_run_in_imitation: bool = False
        self.ai_run_in_real: bool = False
        self.label_simulation_time_at.setText("")
