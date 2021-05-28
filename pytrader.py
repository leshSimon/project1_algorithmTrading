import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI_template_PyQt5.automaticCycleOperation import AutomaticCycleOperation


class PyTrader:
    """
    자작 자동 증권 거래 프로그램 GUI를 실행한다.
    
    클래스는 GUI_template_PyQt5에서 다음과 같이 위에서 아래로 상속된다.

    Initiation_GUI
    balanceAndHoldingStatus
    controlBox
    operationEnvironment
    automaticCycleOperation
    
    """

    def __init__(self):
        self.LastHeirOfGUI = AutomaticCycleOperation()

    def show(self):
        self.LastHeirOfGUI.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = PyTrader()
    myWindow.show()
    app.exec_()
