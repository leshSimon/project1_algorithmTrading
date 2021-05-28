from stock_API.kiwoomAPI import order as orderAPI
from stock_API.kiwoomAPI.initiate import version_up_to_date


class Kiwoom(orderAPI.KiwoomOrder):
    """
    키움증권 API를 종합하여 외부로 전달한다.
    
    클래스는 다음과 같이 위에서 아래로 상속된다.

    QAxWidget
    login
    lookup
    tr_lists
    order
    kiwoom
    
    """

    def __init__(self):
        super().__init__()

        # version_up_to_date()

