from stock_API.deashinAPI.db_API import MySQL_command
from stock_API.deashinAPI.convenienceFunction import *
from stock_API.deashinAPI.market import *
import win32com.client


cybos = win32com.client.Dispatch("CpUtil.CpCybos")
cpChart = win32com.client.Dispatch("CpSysDib.StockChart")
mysql = MySQL_command()


def chartPrecureByCount(
    code: str or int,
    count: int,
    startDate: int = 20000101,
    candleType: str = "m",
    priceCorrection: bool = True,
    sql_save: bool = False,
):
    """
      과거 차트데이터를 개수를 기준으로 최신 시각부터 구한다.
    """
    code = makeStockCodeEntryCompatible(code)
    cpChart.SetInputValue(0, code)  # 종목 코드 - 삼성전자
    cpChart.SetInputValue(1, ord("2"))  # 개수로 조회
    cpChart.SetInputValue(4, count)  # 최근 count개
    cpChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 날짜,시간,시가,고가,...
    cpChart.SetInputValue(6, ord(candleType))  # '차트 주가 - 틱 차트 요청
    cpChart.SetInputValue(9, ord("1") if priceCorrection else ord("0"))  # 수정주가 사용여부
    informationRequestDelay()
    cpChart.BlockRequest()

    totalCount = 0
    lastRequest = False

    if sql_save:
        connected_code = mysql.query("SELECT id FROM kospi500_lists where code = %s;", arguments=[code[1:]])
        connected_code = connected_code.loc[0, "id"]
    else:
        print("==============================================")
        print("idx", " 날짜 ", "시", "분", "시가", " 고가", "저가", " 종가", "거래량")
    print("==============================================")

    loopCnt = 1
    while True:
        length = cpChart.GetHeaderValue(3)
        if length < 1:
            print("There is less data than the number of requests. So it ends.")
            break
        items = []
        for i in range(length):
            totalCount += 1
            day = cpChart.GetDataValue(0, i)
            atTime = cpChart.GetDataValue(1, i)
            close = cpChart.GetDataValue(5, i)
            vol = cpChart.GetDataValue(6, i)
            if candleType != "T":
                open = cpChart.GetDataValue(2, i)
                high = cpChart.GetDataValue(3, i)
                low = cpChart.GetDataValue(4, i)
                if sql_save:
                    items = items + [connected_code, day, atTime // 100, atTime % 100, open, high, low, close, vol]
                else:
                    print(totalCount, code, day)
            else:
                if not sql_save:
                    print(totalCount, day, atTime // 100, atTime % 100, close, vol)

        if sql_save:
            sql = "INSERT INTO kospi200_candle_minute (code,date,hour,minute,open_price,high_price,low_price,close_price,volume) VALUES"
            sql = (
                sql + " (%s, %s, %s, %s, %s, %s, %s, %s, %s)," * (length - 1) + " (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            )
            mysql.mutation(sql, arguments=items)

        if lastRequest:
            break

        rest = count - totalCount
        if rest > 0:
            if rest < length:
                cpChart.SetInputValue(4, rest)
                lastRequest = True
            informationRequestDelay()
            cpChart.BlockRequest()
        else:
            break

        print(f"loop {loopCnt} at {code}")
        loopCnt += 1


def chartPrecureByTerm(code: str, startDate: int, endDate: int, candleType: str = "D", priceCorrection: bool = True):
    """
      과거 차트데이터를 기간을 기준으로 구한다.
      분봉차트나 틱차트는 이용할 수 없다.
    """
    code = makeStockCodeEntryCompatible(code)
    cpChart.SetInputValue(0, code)  # 종목 코드 - 삼성전자
    cpChart.SetInputValue(1, ord("1"))  # 기간으로 조회
    cpChart.SetInputValue(2, endDate)  # 마지막일 - YYYYMMDD 형식
    cpChart.SetInputValue(3, startDate)  # 시작일
    cpChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,...
    cpChart.SetInputValue(6, ord(candleType))  # '차트 주가 - 틱 차트 요청
    cpChart.SetInputValue(9, ord("1") if priceCorrection else ord("0"))  # 수정주가 사용여부

    informationRequestDelay()
    cpChart.BlockRequest()

    print("idx", " 날짜 ", "시", "분", "시가", " 고가", "저가", " 종가", "거래량")
    print("==============================================")

    totalCount = 0
    while True:
        length = cpChart.GetHeaderValue(3)
        if length < 1:
            break

        for i in range(length):
            totalCount += 1
            day = cpChart.GetDataValue(0, i)
            close = cpChart.GetDataValue(4, i)
            vol = cpChart.GetDataValue(5, i)
            if candleType != "T":
                open = cpChart.GetDataValue(1, i)
                high = cpChart.GetDataValue(2, i)
                low = cpChart.GetDataValue(3, i)
                print(totalCount, day, open, high, low, close, vol)
            else:
                print(totalCount, day, close, vol)

            if day <= startDate:
                return

        informationRequestDelay()
        cpChart.BlockRequest()


def save_chart_history_to_database(code_lists: list, startDate: int = 0, maxCount: int = 10):
    for code in code_lists:
        chartPrecureByCount(code, maxCount, startDate=startDate, sql_save=True)


def save_chart_history_kospi_N(startDate: int = 0, N_th: int = 200, maxCount: int = 10):
    """최근 kospi 시총 상위 N개의 차트 데이터를 데이터베이스에 저장한다."""
    kospi_Nth_lists = kospi_Top_N_from_database(N_th=N_th).to_numpy()
    kospi_Nth_lists_code = [row[1] for row in kospi_Nth_lists]
    save_chart_history_to_database(kospi_Nth_lists_code, startDate=startDate, maxCount=maxCount)


def registration_of_analysis_target(N_th: int = 500):
    """최근 kospi 시총 상위 N개의 종목코드와 이름을 데이터베이스에 저장한다."""
    kospi_Top_N(N_th=N_th, sql_save=True)


def delete_chart_by_codes(code_lists: list):
    if len(code_lists) > 0:
        sql = (
            "delete target_table FROM kospi200_candle_minute as target_table "
            + "left join kospi500_lists on target_table.code = kospi500_lists.id "
            + "where kospi500_lists.code = %s;"
        )
        for i in code_lists:
            mysql.mutation(sql, arguments=[i])
    else:
        print("warning: code_lists are empty at 'delete_chart_by_codes' function")


def delete_chart_by_date(date: int, code_idx_list=range(201, 501)):
    for i in code_idx_list:
        mysql.mutation(
            f"delete FROM algorithm_trading.kospi200_candle_minute where code = {i} and date = {date} and hour < 13;"
        )
        mysql.mutation(
            f"delete FROM algorithm_trading.kospi200_candle_minute where code = {i} and date = {date} and hour >= 13;"
        )
        print(f"{i} th code deleting completed at {date}")
