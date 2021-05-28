from AI.components.actorCritic.atSimulation.st3_make_input_in_simulation import St3_make_input_in_simulation
import AI.dezero.functions as F
import numpy as np
import math
import random


class St4_trade_calculate(St3_make_input_in_simulation):
    def __init__(self):
        super().__init__()

    def trade_in_simulation(self, actionIndex):
        """actionIndex가 결정되면 시뮬레이션에서 구체적인 행위를 수행."""
        if actionIndex < 0 or actionIndex >= 4200:  # hold
            return
        elif actionIndex < 4000:  # buy
            buyingIndex: int = actionIndex // 20
            targetStock = self.menu[buyingIndex][:]
            code = targetStock[0]
            closePrice = targetStock[4]
            if code == 0:
                return
            my_folio = [info[0] for info in self.portfolio]
            if (0 not in my_folio) and (code not in my_folio):
                return
            buyAmountRate: float = (actionIndex % 20 + 1) / 20
            buyingBudget = self.deposit_dp2 * buyAmountRate * 0.95
            buyingQuantity: int = math.floor(buyingBudget / closePrice)
            if buyingQuantity < 1:
                return
            purchasePrice = closePrice * buyingQuantity
            transactionFee = purchasePrice * self.fees

            targetStockCodeInLst = False
            for index, lst in enumerate(self.portfolio):
                if code == lst[0]:
                    targetStockCodeInLst = True
                    self.portfolio[index][4] = math.ceil(
                        ((self.portfolio[index][1] * self.portfolio[index][4]) + purchasePrice)
                        / (self.portfolio[index][1] + buyingQuantity)
                    )
                    self.portfolio[index][1] += buyingQuantity
                    self.portfolio[index][2] += transactionFee
                    break
            if not targetStockCodeInLst:
                for index, lst in enumerate(self.portfolio):
                    if lst[0] == 0:
                        self.portfolio[index] = [code, buyingQuantity, transactionFee, closePrice, closePrice]
                        break

            self.deposit_dp2 -= purchasePrice
            self.mySituation[0] = self.deposit_dp2
        else:  # sell
            actionIndex -= 4000
            sellingIndex: int = actionIndex // 10
            sellAmountRate: float = (actionIndex % 10 + 1) / 10
            self.selling_in_simulation(sellingIndex, sellAmountRate)

    def selling_in_simulation(self, sellingIndex: int, sellAmountRate: float):
        """매도 행위를 하는 함수(시뮬레이션에서)"""
        targetStock = self.portfolio[sellingIndex][:]
        [code, reserveAmount, fee, currentPrice, _] = targetStock
        if code == 0:
            return
        sellingQuantity: int = math.floor(reserveAmount * sellAmountRate)
        if sellingQuantity < 1:
            return
        paymentFee = fee * (sellingQuantity / reserveAmount)
        totalSellingPrice = currentPrice * sellingQuantity
        if sellAmountRate >= 1:
            self.portfolio[sellingIndex] = [0, 0, 0, 0, 0]
        else:
            self.portfolio[sellingIndex][1] -= sellingQuantity
            self.portfolio[sellingIndex][2] -= paymentFee
        self.deposit_dp2 = self.deposit_dp2 + totalSellingPrice - paymentFee
        self.mySituation[0] = self.deposit_dp2

    def sellThemAll_in_simulation(self):
        """전량매도행위를 하는 함수(시뮬레이션에서)"""
        for i in range(len(self.portfolio)):
            self.selling_in_simulation(i, 1)

