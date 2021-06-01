from AI.components.actorCritic.atSimulation.st4_trade_calculate import St4_trade_calculate
import AI.dezero.functions as F
import gc


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
            self.network.save_weights()
        elif (hour == 11 or hour == 13) and minute == 0:
            currentValue = self.currentAssetValue_in_simulation()
            reward = (currentValue / self.interimBaselineValue - 1) * 0.8
            self.interimBaselineValue = currentValue
            self.weight_update_in_simulation(reward=reward)
            collected = gc.collect()
            print(f"memory garbage : {collected}")
        else:
            self.weight_update_in_simulation()
        if hour == 14 and minute == 0:
            self.network.save_weights()

    def weight_update_in_simulation(self, reward: int = 0):
        """손실함수를 정의하고 신경망의 역전파를 수행한다."""
        TD_target = reward + self.future_value_retention_rate * self.s2_simulation
        delta = TD_target - self.s1_old_simulation
        Loss_v = F.smooth_l1_loss(delta)
        Loss_pi = -(F.log(self.pi_selected_action)) * delta.data
        Loss = Loss_pi + Loss_v
        print(f"v 손실: {Loss_v}")
        print(f"pi 손실: {Loss_pi}")

        self.network.cleargrads()
        Loss.backward()
        Loss.unchain_backward()
        self.optimizer.update()

        self.s1_old_simulation = self.s1_new_simulation

        # self.network.reset_state()

