from AI.components.construction.atSimulation.st6_acting_in_simulation import St6_acting_in_simulation
import math


class St7_data_for_GUI(St6_acting_in_simulation):
    def __init__(self):
        super().__init__()

    def presentStatusInSimulation(self):
        """GUI에 잔고 현황을 가공해서 넘겨주는 서비스(시뮬레이션에서)"""
        deposit = self.deposit_dp2
        first_value = self.init_value
        last_value = self.currentAssetValue_in_simulation()
        buy_price = sum([stock[4] * stock[1] for stock in self.portfolio])
        data = {
            "deposit": format(math.floor(deposit), ",") + " 원",
            "buy_price": format(buy_price, ",") + " 원",
            "value_my_assets": format(round(last_value - deposit), ",") + " 원",
            "profit_total": format(round(last_value - first_value, 1), ",") + " 원",
            "rate": format(round((last_value / first_value - 1) * 100, 2), ",") + " %",
            "value_total": format(round(last_value), ",") + " 원",
        }
        return data

    def portfolioForGUI(self):
        """GUI에 포트폴리오 정보를 가공해서 넘겨주는 서비스(시뮬레이션에서)"""
        pf = self.portfolio
        data = []
        for stock in pf:
            [code, quant, fee, price, buy_price] = stock
            if code != -1:
                code = self.codeDecoding(code)
                gainOrLoss = (price - buy_price) * quant - fee
                rate = round((((price * quant) - fee) / (buy_price * quant) - 1) * 100, 2)
                name = self.mysql.query("select name from kospi500_lists where id = %s;", [code])
                name = name.loc[0, "name"]
                data.append(
                    [
                        name,
                        quant,
                        format(round(buy_price), ",") + " 원",
                        price,
                        format(round(gainOrLoss, 1), ",") + " 원",
                        format(rate, ",") + " %",
                        gainOrLoss,
                    ]
                )
        data.sort(key=lambda x: -x[1] * x[3])
        for idx, stock in enumerate(data):
            data[idx][1] = format(data[idx][1], ",")
            data[idx][3] = format(data[idx][3], ",") + " 원"
        return data
