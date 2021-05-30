import time
from stock_API.kiwoomAPI import login as loginAPI
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from stock_API.kiwoomAPI.tr_lists import *


class KiwoomLookup(loginAPI.KiwoomLogin):
    """정보조회 관련 기본함수 API 집계"""

    def __init__(self):
        super().__init__()

        self.OnReceiveTrData.connect(self.receive_tr_data)
        self.opt10079_input = Opt10079_input(self.set_input_value, self.comm_rq_data)

    def set_input_value(self, idx, value):
        """
          조회요청시 TR의 Input값을 설정하는 함수.
          idx: TR에 명시된 Input이름
          value: Input이름에 해당하는 값
        """
        self.dynamicCall("SetInputValue(QString, QString)", idx, value)

    def comm_rq_data(self, rqname: str, trcode: str, prevNext: int, screen_no: str):
        """
          조회요청 송신 함수.
          set_input_value로 설정한 인자값들을 송신하고 응답을 대기하는 이벤트를 만든다.
        """
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, prevNext, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def get_comm_data(self, TR_code, recordName, index, item_name):
        """
          OnReceiveTRData()이벤트가 발생될때 수신한 데이터를 얻어오는 함수.
          이 함수는 OnReceiveTRData()이벤트가 발생될때 그 안에서 사용해야 한다.
        """
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", TR_code, recordName, index, item_name)
        return ret.strip()

    def get_repeat_cnt(self, trcode, record_name):
        """
          trcode: TR 이름, record_name: 레코드 이름
          데이터 수신시 멀티데이터의 갯수(반복수)를 얻을수 있다. 
          예를들어 차트조회는 한번에 최대 900개 데이터를 수신할 수 있는데 
          이렇게 수신한 데이터갯수를 얻을때 사용한다.
          이 함수는 OnReceiveTRData()이벤트가 발생될때 그 안에서 사용해야 한다.
        """
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, record_name)
        return ret

    def get_master_code_name(self, code: str) -> str:
        """종목코드 입력, 종목명 반환"""
        code_name: str = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_code_list_by_market(self, market: int):
        """
        시장구분값 입력, 주식 시장별 종목코드 리스트 전부 반환

        [시장구분값]
          0 : 코스피
          10 : 코스닥
          3 : ELW
          8 : ETF
          50 : KONEX
          4 :  뮤추얼펀드
          5 : 신주인수권
          6 : 리츠
          9 : 하이얼펀드
          30 : K-OTC
        """
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", str(market))
        code_list = code_list.split(";")
        return code_list[:-1]

    def receive_tr_data(self, screen_no: str, rqname: str, trcode: str, record_name: str, nextExist: str):
        """
          데이터 요청 후 응답 이벤트가 일어나면 TR에 따라 원하는 데이터를 획득해서 인스턴스 변수에 바인딩한다.
        """
        if nextExist == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        gcd = self.get_comm_data
        grc = self.get_repeat_cnt
        gsg = self.get_server_gubun

        if trcode == "opt10079":
            self.opt10079 = opt10079_out(trcode, record_name, gcd, grc)
        elif trcode == "opt10080":
            self.opt10080 = opt10080_out(trcode, record_name, gcd, grc)
        elif trcode == "opt10081":
            self.opt10081 = opt10081_out(trcode, record_name, gcd, grc)
        elif trcode == "opw00001":
            self.opw00001 = opw00001_out(trcode, record_name, gcd)
        elif trcode == "opw00018":
            self.opw00018 = opw00018_out(trcode, record_name, gcd, grc, gsg)
        else:
            print("Warning: receive_tr_data 함수에 등록된 TR번호가 없습니다.")

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def tr_input(self, trcode):
        """
          데이터 요청 함수의 인수 입력을 간편화 하기 위한 함수.
          다음과 같이 쓴다.
          self.kiwoom.tr_input("opt10079")("066570", tic_serise="3:3틱", adjustedClosingPrice=1)
        """
        siv = self.set_input_value
        crd = self.comm_rq_data

        ret = lambda x: x
        if trcode == "opt10079":
            ret = lambda code_str, ticSerise_str, adjustedClosingPrice_int: self.opt10079_input.firstInput(
                code_str, ticSerise_str, adjustedClosingPrice_int
            )
        elif trcode == "opt10080":
            ret = lambda code_str, minuteSize_str, adjustedClosingPrice_int: opt10080_in(
                siv, crd, code_str, minuteSize_str, adjustedClosingPrice_int
            )
        elif trcode == "opt10081":
            ret = lambda code_str, firstDate_str, adjustedClosingPrice_int: opt10081_in(
                siv, crd, code_str, firstDate_str, adjustedClosingPrice_int
            )
        elif trcode == "opw00001":
            ret = lambda accountNumber_str: opw00001_in(siv, crd, accountNumber_str)
        elif trcode == "opw00018":
            ret = lambda accountNumber_str: opw00018_in(siv, crd, accountNumber_str)
        else:
            print("Warning: tr_input 함수에 등록된 TR번호가 없습니다.")

        return ret

    def tr_request_next(self, trcode):
        """
          최대 조회 개수를 초과하는 데이터가 있을 때 다음번째 데이터를 추가로 요청하는 함수
        """
        crd = self.comm_rq_data

        time.sleep(0.25)

        if trcode == "opt10079":
            self.opt10079_input.requestNext()
        else:
            print("Warning: tr_input_next 함수에 등록된 TR번호가 없습니다.")
