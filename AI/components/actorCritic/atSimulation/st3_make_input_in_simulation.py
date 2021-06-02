from AI.components.actorCritic.atSimulation.st2_library_in_simulation import St2_library_in_simulation
import numpy as np


class St3_make_input_in_simulation(St2_library_in_simulation):
    def __init__(self):
        super().__init__()

    def make_input_state_for_AI_in_simulation(self):
        self.menu = self.past_data_in_DB()
        if len(self.menu) == 0:
            return []
        for idx, lst in enumerate(self.portfolio):
            if lst[0] != 0:
                for lst_menu in self.menu:
                    if lst[0] == lst_menu[0]:
                        self.portfolio[idx][3] = lst_menu[4]
        npFolio = np.array(self.portfolio)
        np.random.shuffle(npFolio)
        return np.concatenate([np.array([self.mySituation[0]] + self.pseudoTime), npFolio, self.menu], axis=None)

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
        elif nonExistDataCount > 0:
            fake_data = [[0, 0, 0, 0, 0, 0] for _ in range(nonExistDataCount)]
            fake_data = np.array(fake_data)
            menu = np.concatenate((menu, fake_data), axis=0)
        np.random.shuffle(menu)
        return menu

    def codeEncoding(self, originalCode: int) -> int:
        strOgn = str(originalCode)
        if strOgn in self.codeHashedDictInv:
            return self.codeHashedDictInv[strOgn]
        newKey = self.randomIntList[0]
        self.codeHashedDict[str(newKey)] = originalCode
        self.codeHashedDictInv[strOgn] = newKey
        self.randomIntList = self.randomIntList[1:]
        return newKey

    def codeDecoding(self, encodedCode: int) -> int:
        strKey = str(encodedCode)
        return self.codeHashedDict[strKey]

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
