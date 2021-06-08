from stock_API.deashinAPI.db_API import MySQL_command
import win32com.client

cpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
cpMarkEye = win32com.client.Dispatch("CpSysDib.MarketEye")
mysql = MySQL_command()


def kospi_Top_N(N_th: int = 200, sql_save: bool = False):
    """
      kospi 시총 상위 N개 종목의 [종목코드, 이름, 시가총액]를 리스트로 반환하는 함수.
    """
    kospi_N = []
    codeList = cpCodeMgr.GetStockListByMarket(1)
    codesCNT = len(codeList)

    rqField = [0, 4, 20]  # 요청 필드
    cpMarkEye.SetInputValue(0, rqField)  # 요청 필드

    for j in range(codesCNT // 198 + 1):
        startIdx = j * 198
        endIdx = min((j + 1) * 198, codesCNT)
        codeListMini = codeList[startIdx:endIdx]
        cpMarkEye.SetInputValue(1, codeListMini)  # 종목코드 or 종목코드 리스트
        cpMarkEye.BlockRequest()

        for i in range(cpMarkEye.GetHeaderValue(2)):
            code = cpMarkEye.GetDataValue(0, i)
            secondCode = cpCodeMgr.GetStockSectionKind(code)
            if secondCode == 1:
                name = cpCodeMgr.CodeToName(code)
                cur = cpMarkEye.GetDataValue(1, i)  # 종가
                listedStock = cpMarkEye.GetDataValue(2, i)  # 상장주식수
                maketAmt = listedStock * cur
                if cpCodeMgr.IsBigListingStock(code):
                    maketAmt *= 1000

                item = [code, name, maketAmt]
                kospi_N.append(item)

    kospi_N.sort(key=lambda x: -x[2])
    kospi_N = kospi_N[:N_th]

    for stock in kospi_N:
        print(stock)

    if sql_save:
        for_save_to_db = []
        for stock in kospi_N:
            for_save_to_db.append(stock[0][1:])
            for_save_to_db.append(stock[1])

        sql = "INSERT INTO kospi500_lists (code, name) VALUES"
        sql = sql + " (%s, %s)," * (len(kospi_N) - 1) + " (%s, %s);"
        mysql.mutation(sql, arguments=for_save_to_db)

    return kospi_N


def kospi_Top_N_from_database(N_th: int = 200):
    sql = "select * from kospi500_lists limit %s;"
    ret = mysql.query(sql, [N_th])
    return ret
