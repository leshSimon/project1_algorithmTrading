import torch
from AI.construction.atSimulation.st2_library_in_simulation import St2_library_in_simulation
import numpy as np
import random


class St3_make_input_in_simulation(St2_library_in_simulation):
    def __init__(self):
        super().__init__()

    def make_input_state_for_AI_in_simulation(self):
        dataFromDB = self.past_data_in_DB()
        if len(dataFromDB) == 0:
            return []
        menuForInput = [np.concatenate([i, [0, 0]]) for i in dataFromDB]  # [순번, 시가, 고가, 저가, 종가, 거래량, 보유량, 매입평균]
        for idx, stock_in_protfolio in enumerate(self.portfolio):
            targetStockCode = stock_in_protfolio[0]
            if targetStockCode != -1:
                codeInPfInMarket: bool = False
                for idx_in_market, stock_in_market in enumerate(dataFromDB):
                    if targetStockCode == stock_in_market[0]:
                        self.portfolio[idx][3] = stock_in_market[4]
                        menuForInput[idx_in_market][6] = stock_in_protfolio[1]
                        menuForInput[idx_in_market][7] = stock_in_protfolio[4]
                        codeInPfInMarket = True
                        self.exileCodeStack[idx_in_market] = 0
                        break
                if not codeInPfInMarket:
                    self.exileCodeStack[targetStockCode] += 1
                    menuForInput[targetStockCode] = np.concatenate(
                        [
                            [targetStockCode],
                            [stock_in_protfolio[3] for _ in range(4)],
                            [0, stock_in_protfolio[1], stock_in_protfolio[4]],
                        ]
                    )

        self.menu = menuForInput
        menuForInput = [i[1:] for i in menuForInput]

        ret = np.concatenate([[self.mySituation[0]], menuForInput], axis=None)
        ret = np.reshape(ret, (1, 1, len(ret)))
        ret = torch.Tensor(ret)

        return ret

    def past_data_in_DB(self):
        if self.mySituation[2] >= 15 and self.mySituation[3] >= 31:
            return []
        if self.new_date != self.mySituation[1]:
            self.data_precured_byDate()
            if len(self.atDateData) < 1:
                self.mySituation[1] += 1
                return []
            self.new_date = self.mySituation[1]
        if self.new_hour != self.mySituation[2]:
            self.atHourData = self.atDateData[self.atDateData["hour"] == self.mySituation[2]]
            self.new_hour = self.mySituation[2]

        data = self.atHourData[self.atHourData["minute"] == self.mySituation[3]]
        data = data[["code", "open_price", "high_price", "low_price", "close_price", "volume"]]
        if len(data.index) == 0:
            return []
        data["code"] = data["code"].apply(lambda x: self.codeEncoding(x))

        menu = np.unique(data.to_numpy(), axis=0)
        nonExistDataCount = 200 - len(menu)
        if nonExistDataCount < 0:
            menu = menu[0:200]
        flask = [[0, 0, 0, 0, 0, 0] for _ in range(200)]
        for stock in menu:
            flask[stock[0]] = stock

        return flask

    def codeEncoding(self, originalCode: int) -> int:
        """종목코드에게 순서가 있는 자리를 배정해준다."""
        strOgn = str(originalCode)
        if strOgn in self.codeListInMarket:
            return self.codeListInMarket.index(strOgn)

        vacancy = []
        for idx, value in enumerate(self.codeListInMarket):
            if value == 0:
                vacancy.append(idx)

        choiced = random.choice(vacancy)
        self.codeListInMarket[choiced] = strOgn

        return choiced

    def codeDecoding(self, encodedCode: int) -> int:
        """배정된 순서에 해당하는 종목의 원래 코드를 반환한다"""
        code = self.codeListInMarket[encodedCode]
        return code

    def data_precured_byDate(self):
        sql = "SELECT * FROM selected_by_code where date = %s;"
        arguments = [self.mySituation[1]]
        self.atDateData = self.mysql.query(sql, arguments=arguments)

    def change_selected_stocks(self):
        selected_stock_list200 = [i + 1 for i in np.random.choice(500, 200, replace=False)]
        selected_stock_list200.sort(key=lambda x: x)
        self.mysql.mutation("TRUNCATE TABLE selected_by_code;")
        order = 1
        for i in selected_stock_list200:
            sql = "INSERT INTO selected_by_code SELECT * FROM kospi200_candle_minute where code = %s;"
            self.mysql.mutation(sql, arguments=[i])
            print(f"Loop {order}: save finished at {i}")
            order += 1
