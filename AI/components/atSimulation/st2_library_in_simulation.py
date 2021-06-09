from AI.components.atSimulation.st1_initialize import St1_initialize_actorCritic
import numpy as np


class St2_library_in_simulation(St1_initialize_actorCritic):
    """재사용성이 높은 함수들을 모아둔다."""

    def __init__(self):
        super().__init__()

    def currentAssetValue_in_simulation(self):
        """현재 총 자산가치를 계산해주는 함수(시뮬레이션에서)"""
        ret = self.deposit_dp2
        for stock in self.portfolio:
            [_, quant, fee, price, _] = stock
            ret = ret + quant * price - fee
        return ret
