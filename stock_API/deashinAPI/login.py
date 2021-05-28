import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
import pywinauto as auto
import os
import time
from dotenv import load_dotenv
import win32com.client


cybos = win32com.client.Dispatch("CpUtil.CpCybos")


def autoLogin():
    disconnect()
    kill_client()

    load_dotenv(dotenv_path="account_information.env", verbose=True)
    Deashin_Id = os.getenv("Deashin_Id")
    Deashin_Password = os.getenv("Deashin_Password")
    if False:
        Deashin_Id = os.getenv("Deashin_Imitation_Id")
        Deashin_Password = os.getenv("Deashin_Imitation_Password")
    Certificate = os.getenv("Accredited_Certificate_for_Securities_Transactions")

    app = auto.application.Application()
    app.start(
        "C:/DAISHIN/STARTER/ncStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwc} /autostart".format(
            id=Deashin_Id, pwd=Deashin_Password, pwc=Certificate
        )
    )


def kill_client():
    print("########## 기존 CYBOS 프로세스 강제 종료")
    os.system("taskkill /IM ncStarter* /F /T")
    os.system("taskkill /IM CpStart* /F /T")
    os.system("taskkill /IM DibServer* /F /T")
    os.system("wmic process where \"name like '%ncStarter%'\" call terminate")
    os.system("wmic process where \"name like '%CpStart%'\" call terminate")
    os.system("wmic process where \"name like '%DibServer%'\" call terminate")


def connected():
    b_connected = cybos.IsConnect
    if b_connected == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False
    return True


def disconnect():
    if cybos.IsConnect:
        cybos.PlusDisconnect()


def waitForRequest():
    remainCount = cybos.GetLimitRemainCount(1)
    if remainCount <= 0:
        time.sleep(cybos.LimitRequestRemainTime / 1000)

