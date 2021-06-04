from AI.components.actorCritic.atSimulation.st3_make_input_in_simulation import St3_make_input_in_simulation
import math


class St4_trade_calculate(St3_make_input_in_simulation):
    def __init__(self):
        super().__init__()

    def trade_in_simulation(self, actionIndex: int):
        """actionIndex가 결정되면 시뮬레이션에서 구체적인 행위를 수행."""
        if actionIndex < 0 or actionIndex >= 4200:  # hold
            self.ai_act_kinds_state = 4201
            return
        elif actionIndex < 4000:  # buy
            buyingIndex: int = actionIndex // 20
            closePrice = self.menuForInput[buyingIndex][3]
            if closePrice == 0:
                self.ai_act_kinds_state = 1001
                return
            my_folio = [info[0] for info in self.portfolio]
            if (-1 not in my_folio) and (buyingIndex not in my_folio):
                self.ai_act_kinds_state = 1003
                return
            buyAmountRate: float = (actionIndex % 20 + 1) / 20
            buyingBudget = self.deposit_dp2 * buyAmountRate * 0.95
            buyingQuantity: int = math.floor(buyingBudget / closePrice)
            if buyingQuantity < 1:
                self.ai_act_kinds_state = 1002
                return
            purchasePrice = closePrice * buyingQuantity
            transactionFee = purchasePrice * self.fees

            targetStockCodeInLst = False
            for index, lst in enumerate(self.portfolio):
                if buyingIndex == lst[0]:
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
                    if lst[0] == -1:
                        self.portfolio[index] = [buyingIndex, buyingQuantity, transactionFee, closePrice, closePrice]
                        break

            self.deposit_dp2 -= purchasePrice
            self.mySituation[0] = self.deposit_dp2
            self.ai_act_kinds_state = 1000
        else:  # sell
            actionIndex -= 4000
            sellingIndex: int = actionIndex // 10
            sellAmountRate: float = (actionIndex % 10 + 1) / 10
            self.selling_in_simulation_by_sellingIndex(sellingIndex, sellAmountRate)

    def selling_in_simulation_by_sellingIndex(self, sellingIndex: int, sellAmountRate: float):
        targetCount = 0
        targetStockCode = -1
        for idx, inputed in enumerate(self.menuForInput):
            if inputed[5] > 0:
                if sellingIndex == targetCount:
                    targetStockCode = idx
                    break
                targetCount += 1
        if targetStockCode == -1:
            self.ai_act_kinds_state = 2001
            return
        self.selling_in_simulation_by_code(targetStockCode, sellAmountRate)

    def selling_in_simulation_by_code(self, targetStockCode: int, sellAmountRate: float):
        """매도 행위를 하는 함수(시뮬레이션에서)"""
        targetStock = None
        whereIsTargetStock = -1
        for idx, stock in enumerate(self.portfolio):
            if stock[0] == targetStockCode:
                targetStock = stock
                whereIsTargetStock = idx
                break
        if targetStock == None:
            print("!!!!Logical contradiction!!!! in 'selling_in_simulation_by_code' function at 'st4_trade_calculate'")
            return

        [_, reserveAmount, fee, currentPrice, _] = targetStock
        sellingQuantity: int = math.floor(reserveAmount * sellAmountRate)
        if sellingQuantity < 1:
            self.ai_act_kinds_state = 2002
            return
        paymentFee = fee * (sellingQuantity / reserveAmount)
        totalSellingPrice = currentPrice * sellingQuantity
        if sellAmountRate >= 1:
            self.portfolio[whereIsTargetStock] = [-1, 0, 0, 0, 0]
        else:
            self.portfolio[whereIsTargetStock][1] -= sellingQuantity
            self.portfolio[whereIsTargetStock][2] -= paymentFee
        self.deposit_dp2 = self.deposit_dp2 + totalSellingPrice - paymentFee
        self.mySituation[0] = self.deposit_dp2
        self.ai_act_kinds_state = 2000

    def sellThemAll_in_simulation(self):
        """전량매도행위를 하는 함수(시뮬레이션에서)"""
        for i in range(len(self.portfolio)):
            self.selling_in_simulation_by_sellingIndex(i, 1)
        self.network.reset_state()

    def AI_act_explicate(self):
        """행위별 결과 설명"""
        ret = ""
        if self.ai_act_kinds_state == 4201:
            ret = "[유보]"

        elif self.ai_act_kinds_state == 1000:
            ret = "[정상매수]"
        elif self.ai_act_kinds_state == 1001:
            ret = "[매수실패] 코드 0 선택"
        elif self.ai_act_kinds_state == 1002:
            ret = "[매수실패] 예산을 초과하는 구매시도"
        elif self.ai_act_kinds_state == 1003:
            ret = "[매수실패] 포트폴리오 최대구성종류 수 20 초과"

        elif self.ai_act_kinds_state == 2000:
            ret = "[정상매도]"
        elif self.ai_act_kinds_state == 2001:
            ret = "[매도실패] 코드 0 선택"
        elif self.ai_act_kinds_state == 2002:
            ret = "[매도실패] 매도비율에 의한 매도개수가 1미만"

        return ret

