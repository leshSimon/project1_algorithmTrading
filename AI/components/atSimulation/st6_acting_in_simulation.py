from torch.distributions.categorical import Categorical
from AI.components.atSimulation.st5_learn_in_simulation import St5_learn_in_simulation
import random


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
            # with torch.autograd.set_detect_anomaly(True):
            self.oneStep(learning=learning)
            self.momentMoveStep += 1
            if self.momentMoveStep > 0 and (
                self.momentMoveStep % random.randint(5, 6) == 0 or self.momentMoveStep % 6 == 0
            ):
                self.momentMovementForward()
                self.momentMoveStep = 0

    def oneStep(self, learning: bool = True):
        """행동을 취하고 그 결과를 처리"""
        self.inputData = self.make_input_state_for_AI_in_simulation()
        if len(self.inputData) < 1:
            return
        if learning:
            self.learning_by_simulation()

        if self.queues_for_multiprocessing == None:
            [self.selectedID_in_simulation, self.pi_selected_action] = self.inference_in_simulation(self.inputData)
        else:
            if self.queues_for_multiprocessing["actors_act_container"].qsize() > 0:
                [self.selectedID_in_simulation, self.pi_selected_action] = self.queues_for_multiprocessing[
                    "actors_act_container"
                ].get()
        self.trade_in_simulation(self.selectedID_in_simulation)
        self.exiledCodeSell()

    def inference_in_simulation(self, inputData):
        """inputData를 얻어서 추론하여 결정한 행동을 반환"""
        prediction = self.network.pi(inputData)
        categorized_prediction = Categorical(prediction)
        selectedID = categorized_prediction.sample().detach().item()
        return [selectedID, prediction[0][0][selectedID]]

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
        """
        일정 기간 연속되어 정보가 주어지지 않은 주식을 강제로 청산하는 함수
        """
        codeListInPortfolio = [i[0] for i in self.portfolio]
        for idx, value in enumerate(self.exileCodeStack):
            if value > 6 * 5:
                self.exileCodeStack[idx] = 0
                if idx in codeListInPortfolio:
                    self.selling_in_simulation_by_code(idx, 1, compulsoryDisposition=True)
                    self.codeListInMarket[idx] = 0

