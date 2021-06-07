# from stock_API.deashinAPI.login import autoLogin
import torch
from AI.pymon import PyMon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from stock_API.kiwoomAPI import Kiwoom

form_class = uic.loadUiType("./GUI_template_PyQt5/assets/pytrader2.ui")[0]


class Initiation_GUI(QMainWindow, form_class):
    def __init__(self, bit32: bool = False):
        super().__init__()
        self.setupUi(self)

        self.bit32: bool = bit32
        # autoLogin()
        if self.bit32:
            self.kiwoom = Kiwoom()
            self.comboBox.addItems(self.kiwoom.accounts_list)

        self.label_operating_env.setText("시뮬레이션")
        self.ai_run_in_simulation: bool = False
        self.ai_run_in_imitation: bool = False
        self.ai_run_in_real: bool = False
        self.label_simulation_time_at.setText("")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.ai = PyMon().to(device)

        print(f"cuda GPU is available: {torch.cuda.is_available()}")
