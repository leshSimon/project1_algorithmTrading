import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
import pywinauto as auto
import time
import os
from dotenv import load_dotenv


def version_up_to_date():
    """자동버전처리를 위한 스크립트"""

    load_dotenv(dotenv_path="account_information.env", verbose=True)
    KIOOM_Id = os.getenv("KIOOM_Id")
    KIOOM_Password = os.getenv("KIOOM_Password")
    Certificate = os.getenv("Accredited_Certificate_for_Securities_Transactions")

    app = auto.application.Application()
    app.start("C:/KiwoomFlash3/bin/nkministarter.exe")

    title = "번개3 Login"
    dlg = auto.timings.wait_until_passes(500000, 0.5, lambda: app.window(title=title))

    id_ctrl = dlg.Edit1
    id_ctrl.set_focus()
    id_ctrl.type_keys(KIOOM_Id)

    password_ctrl = dlg.Edit2
    password_ctrl.set_focus()
    password_ctrl.type_keys(KIOOM_Password)

    cert_ctrl = dlg.Edit3
    cert_ctrl.set_focus()
    cert_ctrl.type_keys(Certificate)

    btn_ctrl = dlg.Button0
    btn_ctrl.click()

    time.sleep(5)
    close_beongea()


def close_beongea():
    try:
        os.system("taskkill /im nkmini.exe")
        print("The version update has been completed normally. ✅")
    except:
        print("번개 hasn't run yet, so wait 5 seconds and try again. ⚠")
        time.sleep(5)
        close_beongea()


if __name__ == "__main__":
    version_up_to_date()
