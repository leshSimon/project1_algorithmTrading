from stock_API.kiwoomAPI import lookup as lookupAPI
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class KiwoomOrder(lookupAPI.KiwoomLookup):
    """주문 관련 API 집계"""

    def __init__(self):
        super().__init__()

        self.OnReceiveChejanData.connect(self.receive_chejan_data)

    def send_order(
        self,
        rqname: str,
        screen_no: str,
        acc_no: str,
        order_type: int,
        code: str,
        quantity: int,
        price: int,
        hoga: str,
        order_no: str,
    ):
        """
          서버에 주문을 전송하는 함수.
          9개 인자값을 가진 주식주문 함수이며 리턴값이 0이면 성공이며 나머지는 에러입니다.
          1초에 5회만 주문가능하며 그 이상 주문요청하면 에러 -308을 리턴합니다.
          ※ 시장가주문시 주문가격은 0으로 입력합니다.
          ※ 취소주문일때 주문가격은 0으로 입력합니다.

          * 입력값
          rqname // 사용자 구분명
          screen_no // 화면번호
          acc_no, // 계좌번호 10자리
          order_type, // 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
          code // 종목코드 (6자리)
          quantity, // 주문수량
          price // 주문가격
          hoga,  // 거래구분(혹은 호가구분)은 아래 참고
          order_no // 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.

          * 거래구분
          00 : 지정가
          03 : 시장가
          05 : 조건부지정가
          06 : 최유리지정가
          07 : 최우선지정가
          10 : 지정가IOC
          13 : 시장가IOC
          16 : 최유리IOC
          20 : 지정가FOK
          23 : 시장가FOK
          26 : 최유리FOK
          61 : 장전시간외종가
          62 : 시간외단일가매매
          81 : 장후시간외종가
          ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.
          
          * 정규장 외 주문
          장전 동시호가 주문
              08:30 ~ 09:00.	거래구분 00:지정가/03:시장가 (일반주문처럼)
              ※ 08:20 ~ 08:30 시간의 주문은 키움에서 대기하여 08:30 에 순서대로 거래소로 전송합니다.
          장전시간외 종가
              08:30 ~ 08:40. 	거래구분 61:장전시간외종가.  가격 0입력
              ※ 전일 종가로 거래. 미체결시 자동취소되지 않음
          장마감 동시호가 주문
              15:20 ~ 15:30.	거래구분 00:지정가/03:시장가 (일반주문처럼)
          장후 시간외 종가
              15:40 ~ 16:00.	거래구분 81:장후시간외종가.  가격 0입력
              ※ 당일 종가로 거래
          시간외 단일가
              16:00 ~ 18:00.	거래구분 62:시간외단일가.  가격 입력
              ※ 10분 단위로 체결, 당일 종가대비 +-10% 가격으로 거래
        """
        self.dynamicCall(
            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
            [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no],
        )

    def get_chejan_data(self, fid: int):
        """
          OnReceiveChejan()이벤트가 발생될때 fid에 해당되는 값을 구하는 함수
          
          * fid 목록
          '9201' : '계좌번호',
          '9203' : '주문번호',
          '9001' : '종목코드',
          '913' : '주문상태',
          '302' : '종목명',
          '900' : '주문수량',
          '901' : '주문가격',
          '902' : '미체결수량',
          '903' : '체결누계금액',
          '904' : '원주문번호',
          '905' : '주문구분',
          '906' : '매매구분',
          '907' : '매도수구분',
          '908' : '주문/,체결시간'
          '909' : '체결번호',
          '910' : '체결가',
          '911' : '체결량',
          '10' : '현재가',
          '27' : '(최,우선)매도호가'
          '28' : '(최,우선)매수호가'
          '914' : '단위체결가',
          '915' : '단위체결량',
          '919' : '거부사유',
          '920' : '화면번호',
          '917' : '신용구분',
          '916' : '대출일',
          '930' : '보유수량',
          '931' : '매입단가',
          '932' : '총매입가',
          '933' : '주문가능수량',
          '945' : '당일순매수수량',
          '946' : '매도/,매수구분'
          '950' : '당일총매도손일',
          '307' : '기준가',
          '8019' : '손익율',
          '957' : '신용금액',
          '958' : '신용이자',
          '918' : '만기일',
          '990' : '당일실현손익(유가)',
          '991' : '당일실현손익률(유가)',
          '992' : '당일실현손익(신용)',
          '993' : '당일실현손익률(신용)',
          '397' : '파생상품거래단위',
          '305' : '상한가',
          '306' : '하한가'
        """
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))
