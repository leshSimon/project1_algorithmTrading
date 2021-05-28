from stock_API.kiwoomAPI.userFunctions.formatChange import change_format


def opw00001_out(trcode, record_name, get_comm_data):
    """예수금 상세 현황 요청"""
    d2_deposit = get_comm_data(trcode, record_name, 0, "d+2추정예수금")
    return change_format(d2_deposit)


def opw00001_in(set_input_value, comm_rq_data, account_number: str):
    """예수금 상세 조회 설정"""

    set_input_value("계좌번호", account_number)
    comm_rq_data("opw00001_req", "opw00001", 0, "1001")
