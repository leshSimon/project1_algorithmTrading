from AI.components.actorCritic.atSimulation.st4_trade_calculate import St4_trade_calculate
import AI.dezero.functions as F
import gc
import numpy as np


class St5_learn_in_simulation(St4_trade_calculate):
    def __init__(self):
        super().__init__()

    def learning_by_simulation(self):
        """특정 조건과 시각에 따라 보상을 결정하거나 가중치를 갱신"""
        if self.s1_old_simulation == None:
            self.s1_old_simulation = self.s1_new_simulation
        if self.pi_selected_action == None or self.pi_selected_action.data == 0 or len(self.inputData) == 0:
            return
        [hour, minute] = self.mySituation[2:4]
        reward = 0

        if hour == 15 and minute == 19:
            currentValue = self.currentAssetValue_in_simulation()
            reward = (currentValue / self.baselineValue - 1) * 2
            self.baselineValue = currentValue
            self.saveNetworkWeights()
            collected = gc.collect()
            print(f"memory garbage : {collected}")
        elif hour % 2 == 0 and minute == 0:
            currentValue = self.currentAssetValue_in_simulation()
            reward = (currentValue / self.interimBaselineValue - 1) * 1.3
            self.interimBaselineValue = currentValue
        elif minute % 30 == 15:
            currentValue = self.currentAssetValue_in_simulation()
            reward = currentValue / self.per30minuteValue - 1
            self.per30minuteValue = currentValue

        self.weight_update_in_simulation(reward=reward)

    def weight_update_in_simulation(self, reward: int = 0):
        """손실함수를 정의하고 신경망의 역전파를 수행한다."""
        TD_target = reward + self.future_value_retention_rate * self.s2_simulation
        delta = TD_target - self.s1_old_simulation
        Loss_v = F.smooth_l1_loss(delta)
        Loss_pi = -(F.log(self.pi_selected_action)) * delta.data
        Loss = Loss_pi + Loss_v
        print(
            f"v 손실: {format(Loss_v.data[0][0], '.8f')}, pi 손실: {format(Loss_pi.data[0][0],'.8f')}, 보상: {round(reward,4)}, 선택확률: {format(self.pi_selected_action.data,'.8f')}"
        )
        print("=====================================================")

        self.network.cleargrads()
        Loss.backward()
        Loss.unchain_backward()
        self.optimizer.update()

        self.s1_old_simulation = self.s1_new_simulation

    def saveNetworkWeights(self):
        self.network.save_weights(self.weightsFilePath)
