import pandas as pd
from stock_API.kiwoomAPI.userFunctions.formatChange import date14digit_to_easyRead


def opt10079_out(trcode, record_name, get_comm_data, get_repeat_cnt):
    """주식 틱차트 조회 요청"""

    data_cnt = get_repeat_cnt(trcode, record_name)
    ohlcv = {
        "date": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": [],
    }

    for i in range(data_cnt):
        date = get_comm_data(trcode, record_name, i, "체결시간")
        open_P = get_comm_data(trcode, record_name, i, "시가")
        high_P = get_comm_data(trcode, record_name, i, "고가")
        low_P = get_comm_data(trcode, record_name, i, "저가")
        close_P = get_comm_data(trcode, record_name, i, "현재가")
        volume = get_comm_data(trcode, record_name, i, "거래량")

        ohlcv["date"].append(date14digit_to_easyRead(date))
        ohlcv["open"].append(int(open_P))
        ohlcv["high"].append(int(high_P))
        ohlcv["low"].append(int(low_P))
        ohlcv["close"].append(int(close_P))
        ohlcv["volume"].append(int(volume))

    ret = pd.DataFrame(ohlcv, columns=["date", "open", "high", "low", "close", "volume"])
    pd.set_option("display.max_rows", None)

    return ret


class Opt10079_input:
    """주식 틱차트 조회 설정"""

    def __init__(self, set_input_value, comm_rq_data):
        self.set_input_value = set_input_value
        self.comm_rq_data = comm_rq_data
        self.code = ""
        self.tic_serise = "1:1틱"
        self.adjustedClosingPrice = "1"

    def firstInput(self, code: str, tic_serise: str = "1:1틱", adjustedClosingPrice: int = 1):
        """주식 틱차트 최초 입력"""
        self.code = code
        self.tic_serise = tic_serise
        self.adjustedClosingPrice = str(adjustedClosingPrice)
        self.set_input_value("종목코드", code)
        self.set_input_value("틱범위", tic_serise)
        self.set_input_value("수정주가구분", adjustedClosingPrice)
        self.comm_rq_data("opt10079_req", "opt10079", 0, "2079")

    def requestNext(self):
        """주식 틱차트 다음 정보 조회"""
        self.set_input_value("종목코드", self.code)
        self.set_input_value("틱범위", self.tic_serise)
        self.set_input_value("수정주가구분", self.adjustedClosingPrice)
        self.comm_rq_data("opt10079_req", "opt10079", 2, "2079")
