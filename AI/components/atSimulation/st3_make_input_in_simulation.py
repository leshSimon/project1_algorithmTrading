import torch
from AI.components.atSimulation.st2_library_in_simulation import St2_library_in_simulation
import numpy as np
import random


class St3_make_input_in_simulation(St2_library_in_simulation):
    """시뮬레이션 환경에서 신경망에게 전달해 줄 input data를 작성하고 클래스 변수를 갱신한다."""

    def __init__(self):
        super().__init__()

    def make_input_state_for_AI_in_simulation(self):
        """신경망의 input작성"""
        dataFromDB = self.past_data_in_DB()
        if len(dataFromDB) == 0:
            return []
        menuForInput = [np.concatenate([i, [0, 0]]) for i in dataFromDB]  # [순번, 시가, 고가, 저가, 종가, 거래량, 보유량, 매입평균]
        for idx, stock_in_protfolio in enumerate(self.portfolio):
            targetStockCode = stock_in_protfolio[0]
            if targetStockCode != -1:
                codeInPfInMarket: bool = False
                for stock_in_market in dataFromDB:
                    if targetStockCode == stock_in_market[0]:
                        self.portfolio[idx][3] = stock_in_market[4]
                        menuForInput[targetStockCode][6] = stock_in_protfolio[1]
                        menuForInput[targetStockCode][7] = stock_in_protfolio[4]
                        codeInPfInMarket = True
                        self.exileCodeStack[targetStockCode] = 0
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
        ret = ret.to(self.device)

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
        """특정일의 주가 데이터를 DB에서 획득"""
        sql = f"SELECT * FROM {self.target_database_name} where date = %s;"
        arguments = [self.mySituation[1]]
        self.atDateData = self.mysql.query(sql, arguments=arguments)

    def change_selected_stocks_one(self):
        """Table하나만 선정 종목 변경"""
        table_name = self.target_database_name
        selected_stock_list200 = [i + 1 for i in np.random.choice(500, 200, replace=False)]
        selected_stock_list200.sort(key=lambda x: x)
        self.mysql.mutation(f"TRUNCATE TABLE {table_name};")
        order = 1
        for i in selected_stock_list200:
            sql = f"INSERT INTO {table_name} SELECT * FROM kospi200_candle_minute where code = %s;"
            self.mysql.mutation(sql, arguments=[i])
            print(f"Table {table_name} Loop {order}: save finished at {i}")
            order += 1

    def change_selected_stocks_all(self):
        """모든 Table의 선정 종목 변경"""
        for table_num in range(1, 5):
            table_name = "selected_by_code" + str(table_num)
            selected_stock_list200 = [i + 1 for i in np.random.choice(500, 200, replace=False)]
            selected_stock_list200.sort(key=lambda x: x)
            self.mysql.mutation(f"TRUNCATE TABLE {table_name};")
            order = 1
            for i in selected_stock_list200:
                sql = f"INSERT INTO {table_name} SELECT * FROM kospi200_candle_minute where code = %s;"
                self.mysql.mutation(sql, arguments=[i])
                print(f"Table {table_num} Loop {order}: save finished at {i}")
                order += 1
