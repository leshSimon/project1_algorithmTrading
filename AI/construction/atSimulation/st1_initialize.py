from AI.networks.actor_critic_network import ActorCriticNetwork
import datetime
import os
import torch
from stock_API.deashinAPI.db_API import MySQL_command
import random


class St1_initialize_actorCritic:
    def __init__(
        self,
        the_number_of_choices: int = 4201,
        securities_transaction_fees: float = 0.0035,
        future_value_retention_rate: float = 0.995,
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
        self.networkSet()

    def situationInit(self):
        now = datetime.datetime.now()
        self.today = int(now.strftime("%Y%m%d"))
        self.currentHour = int(now.strftime("%H"))
        self.currentMinute = int(now.strftime("%M"))

        self.inputData = None
        self.simulationInit()
        self.ai_act_kinds_state: int = 0

    def networkSet(self):
        self.weightsFilePath = "networkWeights.pt"
        self.network = None

        if os.path.exists(self.weightsFilePath):
            self.network = torch.load(self.weightsFilePath)
        else:
            self.network = ActorCriticNetwork(policy_network_outsize=self.the_number_of_choices)

        self.optimizer = self.network.optimizer
        print("networkSet successful ✅")

    def simulationInit(self, startDate: int = 20190502):
        self.deposit_dp2 = 1000000
        self.mySituation = [self.deposit_dp2, startDate, 9, 0]  # [d+2예수금, 날짜, 시, 분]
        self.portfolio = [[-1, 0, 0, 0, 0] for _ in range(20)]  # [종목명, 보유량, 수수료 총합, 현재가, 매입가 평균]
        self.new_date = 0
        self.new_hour = 8

        self.init_value = self.deposit_dp2
        self.baselineValue = self.currentAssetValue_in_simulation()
        self.interimBaselineValue = self.baselineValue
        self.per15minuteValue = self.baselineValue
        self.inputData_old = None
        self.pi_selected_action = None

        self.codeListInMarket = [0 for _ in range(200)]
        self.exileCodeStack = [0 for _ in range(200)]
        self.pseudoTime = [random.randint(10000000, 90000000), random.randint(1, 9), random.randint(1, 38)]
        self.pseudoTimeReserved = self.pseudoTime[1:]

