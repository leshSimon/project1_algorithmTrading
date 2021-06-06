from torch.distributions.categorical import Categorical
from AI.components.atSimulation.st5_learn_in_simulation import St5_learn_in_simulation
import random

import torch


class St6_acting_in_simulation(St5_learn_in_simulation):
    def __init__(self):
        super().__init__()

    def simulation_at_one_point(self, learning: bool = True):
        """
        핵심 함수

        만약 가중치 경사 갱신 중
        '인플레이스 연산이 일어났기 때문에 set_detect_anomaly를 사용하라'
        라는 오류가 나왔을 땐,
        아래의 주석을 해제한 코드로 실행해봐서 문제 위치를 찾아본다.
        """
        if self.mySituation[1] < self.today:
            with torch.autograd.set_detect_anomaly(True):
                for _ in range(random.randint(5, 6)):
                    self.actingAndStateChange(learning)
                self.momentMovementForward()

    def actingAndStateChange(self, learning: bool = True) -> bool:
        """행동을 취하고 그 결과를 처리"""
        self.inputData = self.make_input_state_for_AI_in_simulation()

        if len(self.inputData) < 1:
            return

        if learning:
            self.learning_by_simulation()

        prediction = self.network.pi(self.inputData)
        categorized_prediction = Categorical(prediction)
        self.selectedID_in_simulation = categorized_prediction.sample().detach().item()
        self.pi_selected_action = prediction[0][0][self.selectedID_in_simulation]

        self.trade_in_simulation(self.selectedID_in_simulation)
        self.exiledCodeSell()
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
