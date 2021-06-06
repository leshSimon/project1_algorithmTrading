import torch
from AI.components.atSimulation.st4_trade_calculate import St4_trade_calculate
import gc
import torch.nn.functional as F
import math


class St5_learn_in_simulation(St4_trade_calculate):
    def __init__(self):
        super().__init__()

    def learning_by_simulation(self):
        """특정 조건과 시각에 따라 보상을 결정하거나 가중치를 갱신"""
        if self.inputData_old == None:
            self.inputData_old = self.inputData
            return
        if self.pi_selected_action == None or self.pi_selected_action.detach() == 0 or len(self.inputData) == 0:
            return
        [hour, minute] = self.mySituation[2:4]
        reward = 0

        if hour == 15 and minute == 19:
            currentValue = self.currentAssetValue_in_simulation()
            reward = currentValue / self.baselineValue - 1
            reward *= 2
            self.baselineValue = currentValue
            self.save_network_self_weights()
            collected = gc.collect()
            print(f"memory garbage : {collected}")
        elif hour % 2 == 0 and minute == 0:
            currentValue = self.currentAssetValue_in_simulation()
            reward = currentValue / self.interimBaselineValue - 1
            reward *= 1.3
            self.interimBaselineValue = currentValue
        elif minute % 15 == 12:
            currentValue = self.currentAssetValue_in_simulation()
            reward = currentValue / self.per15minuteValue - 1
            self.per15minuteValue = currentValue

        reward *= 10
        self.weight_update_in_simulation(reward=reward)

    def weight_update_in_simulation(self, reward: int = 0):
        """손실함수를 정의하고 신경망의 역전파를 수행한다."""

        v_s = self.network.v(self.inputData_old)
        v_s_prime = self.network.v(self.inputData)

        TD_target = reward + self.future_value_retention_rate * v_s_prime
        delta = TD_target - v_s

        v_Loss = F.smooth_l1_loss(v_s, TD_target.detach())
        pi_Loss = -(torch.log(self.pi_selected_action)) * delta.detach()
        Loss = pi_Loss + v_Loss

        print(
            f"===Actor: {self.name}========================================",
            f"총자산: {round(self.currentAssetValue_in_simulation())}, 잔고: {math.floor(self.deposit_dp2)} at {self.mySituation[1:4]} / ACT: {self.selectedID_in_simulation} {self.AI_act_explicate()}",
            f"v 손실: {format(v_Loss.item(), '.8f')}, pi 손실: {format(pi_Loss.item(),'.8f')}, 보상: {round(reward,4)}, 선택확률: {format(self.pi_selected_action.item(),'.8f')}",
            sep="\n",
        )

        if self.network_global == None:
            self.optimizer.zero_grad()
            Loss.backward()
            self.optimizer.step()
        else:
            self.step += 1
            update_step = self.gradient_update_step_for_A3C
            self.accumulatedLoss = self.accumulatedLoss + Loss

            if self.step > 0 and self.step % update_step == 0:
                self.optimizer.zero_grad()
                self.accumulatedLoss.backward()

                for global_param, local_param in zip(self.network_global.parameters(), self.parameters()):
                    global_param._grad = local_param.grad

                self.optimizer.step()
                self.accumulatedLoss = 0
                self.load_state_dict(self.network_global.state_dict())

                if self.step % self.globalNetSaveStep == 0:
                    self.save_network_global_weights()
                    self.step %= update_step

        self.inputData_old = self.inputData[:]

    def save_network_self_weights(self):
        if self.network_global == None:
            torch.save(self.state_dict(), self.weightsFilePath)

    def save_network_global_weights(self):
        if self.network_global != None:
            torch.save(self.network_global.state_dict(), self.weightsFilePath)
