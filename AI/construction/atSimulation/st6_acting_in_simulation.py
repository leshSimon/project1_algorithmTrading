from AI.construction.atSimulation.st5_learn_in_simulation import St5_learn_in_simulation
import numpy as np
import math
import random
import torch


class St6_acting_in_simulation(St5_learn_in_simulation):
    def __init__(self):
        super().__init__()

    def simulation_at_one_point(self, learning: bool = True):
        """핵심 함수"""
        if self.mySituation[1] < self.today:
            with torch.autograd.set_detect_anomaly(True):
                for _ in range(random.randint(4, 6)):
                    self.actingAndStateChange(learning)
                self.momentMovementForward()

    def actingAndStateChange(self, learning: bool = True) -> bool:
        """행동을 취하고 그 결과를 처리"""
        self.inputData = self.make_input_state_for_AI_in_simulation()

        if len(self.inputData) < 1:
            return

        if learning:
            self.learning_by_simulation()

        prediction = self.network_global.pi(self.inputData)
        actionsList = prediction.detach()[0][0]

        ramdomNum = np.random.rand(1)[0]
        accum = 0
        self.selectedID_in_simulation = int(np.random.rand(1)[0])
        for i in range(self.the_number_of_choices):
            accum += actionsList[i].item()
            if ramdomNum < accum:
                self.selectedID_in_simulation = i
                break

        self.pi_selected_action = prediction[0][0][self.selectedID_in_simulation]

        self.trade_in_simulation(self.selectedID_in_simulation)
        self.exiledCodeSell()
        print(
            f"총자산: {round(self.currentAssetValue_in_simulation())}, 잔고: {math.floor(self.deposit_dp2)} at {self.mySituation[1:4]} / ACT: {self.selectedID_in_simulation} {self.AI_act_explicate()}"
        )
        return

    def momentMovementForward(self):
        """시점을 1분 앞으로 이동"""
        self.mySituation[3] += 1
        self.pseudoTime[2] += 1
        if self.mySituation[3] >= 60:
            self.mySituation[3] = 0
            self.pseudoTime[2] = self.pseudoTimeReserved[1]
            self.mySituation[2] += 1
            self.pseudoTime[1] += 1
        if self.mySituation[2] > 15 or (self.mySituation[2] == 15 and self.mySituation[3] > 30):
            self.mySituation[2] = 9
            self.pseudoTime[1] = self.pseudoTimeReserved[0]
            self.mySituation[1] += 1
            self.pseudoTime[0] += 1
        year = self.mySituation[1] // 10000
        date = self.mySituation[1] % 10000
        month = date // 100
        if date % 100 > 31:
            self.mySituation[1] = year * 10000 + month * 100 + 101
            month += 1
        if month > 12:
            self.mySituation[1] = year * 10000 + 10101
            year += 1

    def exiledCodeSell(self):
        codeListInPortfolio = [i[0] for i in self.portfolio]
        for idx, value in enumerate(self.exileCodeStack):
            if value > 6 * 5:
                self.exileCodeStack[idx] = 0
                if idx in codeListInPortfolio:
                    self.selling_in_simulation_by_code(idx, 1, compulsoryDisposition=True)
                    self.codeListInMarket[idx] = 0
