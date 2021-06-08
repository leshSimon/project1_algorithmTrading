from GUI_template_PyQt5.controlBox import ControlBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AiControl(ControlBox):
    def __init__(self):
        super().__init__()

        self.pushButton_ai_operate.clicked.connect(self.operateAI)
        self.pushButton_ai_stop.clicked.connect(self.stopAI)
        self.pushButton_AI_stopAndSellThemAll.clicked.connect(self.stopAI_andSellThemAll)
        self.simulationFirstStart: bool = True

    def operateAI(self):
        self.label_ai_status.setText("동작중")
        if self.label_operating_env.text() == "실제투자":
            self.ai_run_in_real = True
        elif self.label_operating_env.text() == "모의투자":
            self.ai_run_in_imitation = True
        else:
            if self.simulationFirstStart:
                self.ai.simulationInit(startDate=20190518)
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
