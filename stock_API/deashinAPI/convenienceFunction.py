import time
import win32com.client


cybos = win32com.client.Dispatch("CpUtil.CpCybos")


def informationRequestDelay():
    if cybos.GetLimitRemainCount(1) == 1:
        remainTime = cybos.LimitRequestRemainTime / 1000 + 1
        remainTime = round(remainTime, 3)
        print(f"Sleeping {remainTime} seconds for excessive request...")
        time.sleep(remainTime)


def makeStockCodeEntryCompatible(code: int or str) -> str:
    code = str(code)
    while len(code) < 6:
        code = "0" + code
    if len(code) != 7 or code[0] != "A":
        code = "A" + code
    return code
