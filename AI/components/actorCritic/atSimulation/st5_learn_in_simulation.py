from AI.components.actorCritic.atSimulation.st4_trade_calculate import St4_trade_calculate
import AI.dezero.functions as F


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
        if hour == 15 and minute == 19:
            currentValue = self.currentAssetValue_in_simulation()
            reward = (currentValue / self.baselineValue - 1) * 1.2
            self.baselineValue = currentValue
            self.weight_update_in_simulation(reward=reward)
            self.saveNetworkWeights()
        elif (hour == 11 or hour == 13) and minute == 0:
            currentValue = self.currentAssetValue_in_simulation()
            reward = (currentValue / self.interimBaselineValue - 1) * 0.8
            self.interimBaselineValue = currentValue
            self.weight_update_in_simulation(reward=reward)
        else:
            self.weight_update_in_simulation()
        if hour == 14 and minute == 0:
            self.saveNetworkWeights()
            self.v_target.load_weights(self.weightsFilePath_value)

    def weight_update_in_simulation(self, reward: int = 0, unchain_backward: bool = True):
        """손실함수를 정의하고 신경망의 역전파를 수행한다."""
        delta = reward + self.future_value_retention_rate * self.s2_simulation - self.s1_old_simulation
        Loss_v = delta ** 2
        Loss_pi = -F.log(self.pi_selected_action) * delta.data
        self.pi.cleargrads()
        self.v.cleargrads()
        self.v_target.cleargrads()
        Loss_pi.backward()
        Loss_v.backward()
        if unchain_backward:
            Loss_pi.unchain_backward()
            Loss_v.unchain_backward()
        self.optimizer_for_pi.update()
        self.optimizer_for_v.update()
        self.s1_old_simulation = self.s1_new_simulation

    def saveNetworkWeights(self):
        self.pi.save_weights(self.weightsFilePath_policy)
        self.v.save_weights(self.weightsFilePath_value)
