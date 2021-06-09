from random import randint
from AI.components.atReal.actor_critic import ActorCritic
import torch


class PyMon(ActorCritic):
    """
      이 클래스 모듈은 인공지능 동작에 대한 API를 제공한다.
      클래스는 다음과 같이 위에서 아래로 상속된다.

      ActorCriticSimulation
      ActorCritic
      PyMon
      
    """

    def __init__(
        self,
        the_number_of_choices: int = 4201,
        securities_transaction_fees: float = 0.0035,
        future_value_retention_rate: float = 0.995,
        name: str = "Tester",
        network_global=None,
        gradient_update_step_for_A3C: int = randint(5, 7),
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        target_database_name: str = "selected_by_code1",
    ):
        """인자를 받아서 self에 저장하는 공간."""
        super().__init__()
        self.fees: float = securities_transaction_fees
        self.the_number_of_choices: int = the_number_of_choices
        self.future_value_retention_rate: float = future_value_retention_rate
        self.name: str = name
        self.gradient_update_step_for_A3C: int = gradient_update_step_for_A3C
        self.device = device
        self.network_global = network_global
        self.target_database_name: str = target_database_name

        print(f"cuda GPU is available?: {torch.cuda.is_available()}")
        print(f"PyMon {name} initialized ✅")

        self.situationInit()
        self.networkSet()

