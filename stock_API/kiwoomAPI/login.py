from stock_API.kiwoomAPI.initiate import version_up_to_date
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class KiwoomLogin(QAxWidget):
    """로그인 관련 API 집계"""

    def __init__(self):
        super().__init__()

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

        # 로그인 처리 및 프로그램 실행(선후관계 중요)
        self.OnEventConnect.connect(self.event_connect)
        self.comm_connect()

        # 계정정보 setting
        self.accouns_num = int(self.get_login_info("ACCOUNT_CNT"))
        self.accounts_list = self.get_login_info("ACCNO").split(";")[0 : self.accouns_num]

    def comm_connect(self):
        """로그인을 처리하고 완료될때까지 기다리게 한다."""
        # version_up_to_date()
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def event_connect(self, err_code):
        """
          로그인 처리가 완료되면 로그인 성공여부를 콘솔에 출력하고 로그인 이벤트 대기에서 벗어난다.
        """
        if err_code == 0:
            print("connected ✅")
        elif err_code == 100:
            print("사용자 정보교환 실패 (disconnected)")
        elif err_code == 101:
            print("서버 접속 실패 (disconnected)")
        elif err_code == 102:
            print("버전처리 실패 (disconnected)")
        else:
            print("실패원인 미확인 (disconnected)")

        self.login_event_loop.exit()

    def get_connect_state(self):
        """
          서버와 현재 접속 상태를 알려준다.
          리턴값 1:연결, 0:연결안됨
        """
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def get_login_info(self, tag):
        """
          로그인 후 사용할 수 있으며 인자값에 대응하는 정보를 얻을 수 있다.
          인자는 다음값을 사용할 수 있습니다.
          
          "ACCOUNT_CNT" : 보유계좌 갯수를 반환.
          "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환.
          "USER_ID" : 사용자 ID를 반환.
          "USER_NAME" : 사용자 이름을 반환.
          "GetServerGubun" : 접속서버 구분을 반환.(1 : 모의투자, 나머지 : 실거래서버)
          "KEY_BSECGB" : 키보드 보안 해지여부를 반환.(0 : 정상, 1 : 해지)
          "FIREW_SECGB" : 방화벽 설정여부를 반환.(0 : 미설정, 1 : 설정, 2 : 해지)
          
          리턴값으로 인자값에 대응하는 정보를 얻을 수 있다.
        """
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_server_gubun(self):
        """모의투자인지 실제투자인지 알려준다"""
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret
