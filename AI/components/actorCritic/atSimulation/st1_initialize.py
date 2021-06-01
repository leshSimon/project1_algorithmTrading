import datetime
import os
from AI.dezero import Model
import AI.dezero.optimizers as Opt
from AI.components.networks.policy_network import PolicyNetwork
from AI.components.networks.value_network import ValueNetwork
from AI.components.networks.value_target_network import ValueTargetNetwork
from stock_API.deashinAPI.db_API import MySQL_command
import numpy as np
import random


class St1_initialize_actorCritic(Model):
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
        self.simulationInit()
        self.selected_stock_shuffle_incoding_labels = [i + 1 for i in np.random.choice(500, 200)]
        print("situation init for sumulation successful ✅")

    def networkSet(self):
        self.weightsFilePath_policy = "AI/components/networks/policyNetworkWeights.npz"
        self.weightsFilePath_value = "AI/components/networks/valueNetworkWeights.npz"
        self.pi = PolicyNetwork(out_size=self.the_number_of_choices)
        self.v = ValueNetwork()
        self.v_target = ValueTargetNetwork()
        if os.path.exists(self.weightsFilePath_policy):
            self.pi.load_weights(self.weightsFilePath_policy)
        if os.path.exists(self.weightsFilePath_value):
            self.v.load_weights(self.weightsFilePath_value)
            self.v_target.load_weights(self.weightsFilePath_value)
        self.optimizer_for_pi = Opt.MomentumSGD().setup(self.pi)
        self.optimizer_for_v = Opt.MomentumSGD().setup(self.v)
        print("networkSet successful ✅")

    def simulationInit(self, startDate: int = 20190502):
        print("Accessed in simulation_at_one_point function ✅")
        self.deposit_dp2 = 1000000
        self.mySituation = [self.deposit_dp2, startDate, 9, 0]  # [d+2예수금, 날짜, 시, 분]
        self.portfolio = [[0, 0, 0, 0, 0] for _ in range(20)]  # [종목명, 보유량, 수수료 총합, 현재가, 매입가 평균]
        self.new_date = 0
        self.new_hour = 8

        self.init_value = self.deposit_dp2
        self.baselineValue = self.currentAssetValue_in_simulation()
        self.interimBaselineValue = self.baselineValue
        self.s1_old_simulation = None
        self.s1_new_simulation = None
        self.pi_selected_action = None

        self.randomIntList = [i + 1 for i in np.random.choice(998, 200, replace=False)]
        self.codeHashedDict: dict = {}
        self.codeHashedDictInv: dict = {}
        self.pseudoTime = [random.randint(10000000, 90000000), random.randint(1, 9), random.randint(1, 38)]
        self.pseudoTimeReserved = self.pseudoTime[1:]

    def reset_state(self):
        self.pi.reset_state()
        self.v.reset_state()
        self.v_target.reset_state()

