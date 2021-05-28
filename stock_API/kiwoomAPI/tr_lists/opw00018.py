import time
from stock_API.kiwoomAPI.userFunctions.formatChange import change_format


def opw00018_out(trcode, record_name, get_comm_data, get_repeat_cnt, get_server_gubun):
    """계좌 평가 잔고내역 요청"""

    opw00018_output = {"single": [], "multi": []}

    # single data
    total_purchase_price = get_comm_data(trcode, record_name, 0, "총매입금액")
    total_eval_price = get_comm_data(trcode, record_name, 0, "총평가금액")
    total_eval_profit_loss_price = get_comm_data(trcode, record_name, 0, "총평가손익금액")
    total_earning_rate = get_comm_data(trcode, record_name, 0, "총수익률(%)")
    estimated_deposit = get_comm_data(trcode, record_name, 0, "추정예탁자산")

    opw00018_output["single"].append(change_format(total_purchase_price))
    opw00018_output["single"].append(change_format(total_eval_price))
    opw00018_output["single"].append(change_format(total_eval_profit_loss_price))

    total_earning_rate = change_format(total_earning_rate)

    if get_server_gubun():
        total_earning_rate = float(total_earning_rate) / 100
        total_earning_rate = str(total_earning_rate)

    opw00018_output["single"].append(total_earning_rate)

    opw00018_output["single"].append(change_format(estimated_deposit))

    # multi data
    rows = get_repeat_cnt(trcode, record_name)
    for i in range(rows):
        name = get_comm_data(trcode, record_name, i, "종목명")
        quantity = get_comm_data(trcode, record_name, i, "보유수량")
        purchase_price = get_comm_data(trcode, record_name, i, "매입가")
        current_price = get_comm_data(trcode, record_name, i, "현재가")
        eval_profit_loss_price = get_comm_data(trcode, record_name, i, "평가손익")
        earning_rate = get_comm_data(trcode, record_name, i, "수익률(%)")

        quantity = change_format(quantity)
        purchase_price = change_format(purchase_price)
        current_price = change_format(current_price)
        eval_profit_loss_price = change_format(eval_profit_loss_price)
        earning_rate = change_format2(earning_rate)

        opw00018_output["multi"].append(
            [name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate]
        )

    return opw00018_output


def opw00018_in(set_input_value, comm_rq_data, account_number: str):
    """예수금 상세 조회 설정"""

    set_input_value("계좌번호", account_number)
    comm_rq_data("opw00018_req", "opw00018", 0, "1018")

    # while remained_data:
    #     time.sleep(0.2)
    #     set_input_value("계좌번호", account_number)
    #     comm_rq_data("opw00018_req", "opw00018", 2, "1018")
