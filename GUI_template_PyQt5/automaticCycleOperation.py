from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI_template_PyQt5.operationEnvironment import OperationEnvironment


class AutomaticCycleOperation(OperationEnvironment):
    def __init__(self):
        super().__init__()

        self.timer_connection_check = QTimer(self)
        self.timer_connection_check.start(1000)
        self.timer_connection_check.timeout.connect(self.serverConnectionCheckPer1Sec)

        self.timer_checkBalance = QTimer(self)
        self.timer_checkBalance.start(1000 * 10)
        self.timer_checkBalance.timeout.connect(self.checkBalancePer10Sec)

        self.timer_AI_trigger = QTimer(self)
        self.timer_AI_trigger.start(1000 * 1)
        self.timer_AI_trigger.timeout.connect(self.AI_simulationPerNsec)

    def AI_simulationPerNsec(self,):
        if self.ai_run_in_simulation:
            self.ai.simulation_at_one_point(learning=self.checkBox_include_learning.isChecked())
            self.check_balance_in_simulation()
            [date, hour, minute] = self.ai.mySituation[1:4]
            self.label_simulation_time_at.setText(
                f"{date//10000}. {(date%10000)//100}. {(date%10000)%100}. {hour}:{minute} at test"
            )

    def serverConnectionCheckPer1Sec(self):
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

    def checkBalancePer10Sec(self):
        if self.checkBox.isChecked():
            self.check_balance()

