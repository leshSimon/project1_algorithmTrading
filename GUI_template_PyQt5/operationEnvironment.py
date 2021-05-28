from GUI_template_PyQt5.controlBox import ControlBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class OperationEnvironment(ControlBox):
    def __init__(self):
        super().__init__()

        self.comboBox_operating_env.currentTextChanged.connect(self.selectOperatingEnv)

    def selectOperatingEnv(self):
        text = self.comboBox_operating_env.currentText()
        self.label_operating_env.setText(text)
        if text == "시뮬레이션":
            if self.ai_run_in_simulation:
                self.label_ai_status.setText("동작중")
            else:
                self.label_ai_status.setText("정지중")
            self.pushButton_AI_initialize.show()
        else:
            if text == "실제투자":
                if self.ai_run_in_real:
                    self.label_ai_status.setText("동작중")
                else:
                    self.label_ai_status.setText("정지중")
            elif text == "모의투자":
                if self.ai_run_in_imitation:
                    self.label_ai_status.setText("동작중")
                else:
                    self.label_ai_status.setText("정지중")
            self.pushButton_AI_initialize.hide()

