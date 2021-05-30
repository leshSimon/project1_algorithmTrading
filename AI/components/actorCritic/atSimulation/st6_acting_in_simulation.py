from AI.components.actorCritic.atSimulation.st5_learn_in_simulation import St5_learn_in_simulation
import numpy as np
import math
import random


class St6_acting_in_simulation(St5_learn_in_simulation):
    def __init__(self):
        super().__init__()

    def simulation_at_one_point(self, learning: bool = True):
        """핵심 함수"""
        if self.mySituation[1] < self.today:
            for _ in range(random.randint(4, 6)):
                self.actingAndStateChange(learning)
            self.momentMovementForward()

    def actingAndStateChange(self, learning: bool = True):
        """행동을 취하고 그 결과를 처리"""
        self.inputData = self.make_input_state_for_AI_in_simulation()
        if len(self.inputData) < 1:
            return
        actionsList = self.pi(self.inputData)
        ramdomNum = np.random.rand(1)[0]
        accum = 0
        selectedID = 4200
        for i in range(self.the_number_of_choices):
            accum += actionsList[i].data
            if ramdomNum < accum:
                selectedID = i
                break
        self.pi_selected_action = actionsList[selectedID]
        if learning:
            self.s1_simulation = self.v(self.inputData)

        self.trade_in_simulation(selectedID)
        print(
            f"currentValue: {round(self.currentAssetValue_in_simulation())}, deposit: {math.floor(self.deposit_dp2)} at {self.mySituation[1:4]}"
        )
        if learning:
            self.learning_by_simulation()
        else:
            self.pi_selected_action.unchain_backward()

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
