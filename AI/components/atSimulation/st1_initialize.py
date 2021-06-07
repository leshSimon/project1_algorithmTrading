from AI.networks.actor_critic_network import ActorCriticNetwork
import datetime
import os
import torch
from stock_API.deashinAPI.db_API import MySQL_command
import random
import torch.nn as nn
import torch.optim as optim


class St1_initialize_actorCritic(nn.Module):
    def __init__(
        self,
        the_number_of_choices: int = 4201,
        securities_transaction_fees: float = 0.0035,
        future_value_retention_rate: float = 0.995,
        name: str = "Tester",
        network_global=None,
        gradient_update_step_for_A3C: int = 5,
        device_arg=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    ):
        super(St1_initialize_actorCritic, self).__init__()
        self.fees: float = securities_transaction_fees
        self.the_number_of_choices: int = the_number_of_choices
        self.future_value_retention_rate: float = future_value_retention_rate
        self.name = name
        self.gradient_update_step_for_A3C = gradient_update_step_for_A3C
        self.step = 0
        self.new_date = None
        self.new_hour = None
        self.network_global = network_global
        self.device = device_arg

        self.mysql = MySQL_command()
        self.situationInit()
        self.networkSet()
        print(f"PyMon {name} initialized ✅")

    def situationInit(self):
        now = datetime.datetime.now()
        self.today = int(now.strftime("%Y%m%d"))
        self.currentHour = int(now.strftime("%H"))
        self.currentMinute = int(now.strftime("%M"))

        self.inputData = None
        self.simulationInit()
        self.ai_act_kinds_state: int = 0

    def networkSet(self):
        self.weightsFilePath: str = "networkWeights.pt"
        self.optimizer = None

        self.network = ActorCriticNetwork(input_size=1401, policy_network_outsize=self.the_number_of_choices)
        if self.network_global == None:
            if os.path.exists(self.weightsFilePath):
                self.load_state_dict(torch.load(self.weightsFilePath))
            self.optimizer = optim.SGD(self.parameters(), lr=0.001, momentum=0.9)
        else:
            self.load_state_dict(self.network_global.state_dict())
            self.optimizer = optim.SGD(self.network_global.parameters(), lr=0.001, momentum=0.9)

        self.accumulatedLoss = 0
        self.globalNetSaveStep = 60 * 5 * random.randint(4, 5) + random.randint(0, 59)

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

