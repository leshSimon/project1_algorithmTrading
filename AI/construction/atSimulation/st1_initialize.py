from AI.networks.actor_critic_network import ActorCriticNetwork
import datetime
import os
import torch
from stock_API.deashinAPI.db_API import MySQL_command
import random
import copy


class St1_initialize_actorCritic:
    def __init__(
        self,
        the_number_of_choices: int = 4201,
        securities_transaction_fees: float = 0.0035,
        future_value_retention_rate: float = 0.995,
        actors: int = 4,
    ):
        super().__init__()
        print("start ActorCritic class initialization")
        self.fees: float = securities_transaction_fees
        self.the_number_of_choices: int = the_number_of_choices
        self.future_value_retention_rate: float = future_value_retention_rate
        self.new_date = None
        self.new_hour = None

        self.mysql = MySQL_command()
        self.situationInit()
        self.networkSet(actors)

    def situationInit(self):
        now = datetime.datetime.now()
        self.today = int(now.strftime("%Y%m%d"))
        self.currentHour = int(now.strftime("%H"))
        self.currentMinute = int(now.strftime("%M"))

        self.inputData = None
        self.simulationInit()
        self.ai_act_kinds_state: int = 0

    def networkSet(self, actors: int):
        self.weightsFilePath: str = "networkWeights.pt"
        self.network_global = None
        self.network_local_list = []

        if os.path.exists(self.weightsFilePath):
            self.network_global = torch.load(self.weightsFilePath)
        else:
            self.network_global = ActorCriticNetwork(policy_network_outsize=self.the_number_of_choices)

        for _ in range(actors):
            cloneNetwork = copy.deepcopy(self.network_global)
            self.network_local_list.append(cloneNetwork)

        self.optimizer = self.network_global.optimizer
        print(f"networkSet successful ✅ / actors: {actors}")

    def simulationInit(self, startDate: int = 20190502):
        self.deposit_dp2: float = 1000000
        self.mySituation = [self.deposit_dp2, startDate, 9, 0]  # [d+2예수금, 날짜, 시, 분]
        self.portfolio = [[-1, 0, 0, 0, 0] for _ in range(20)]  # [종목명, 보유량, 수수료 총합, 현재가, 매입가 평균]
        self.new_date: int = 0
        self.new_hour: int = 8

        self.init_value: float = self.deposit_dp2
        self.baselineValue: float = self.currentAssetValue_in_simulation()
        self.interimBaselineValue = self.baselineValue
        self.per15minuteValue = self.baselineValue
        self.inputData_old = None
        self.pi_selected_action = None

        self.codeListInMarket = [0 for _ in range(200)]
        self.exileCodeStack = [0 for _ in range(200)]
        self.pseudoTime = [random.randint(10000000, 90000000), random.randint(1, 9), random.randint(1, 38)]
        self.pseudoTimeReserved = self.pseudoTime[1:]

