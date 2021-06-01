from AI.components.networks.sharing_network import SharingNetwork
from AI.components.networks.value_network import ValueNetwork
from AI.components.networks.policy_network import PolicyNetwork
from AI.dezero import Model


class ActorCriticNetwork(Model):
    def __init__(self, hidden_size: int = 650, policy_network_outsize: int = 4201, dropout_ratio: float = 0.5):
        super().__init__()
        self.sharing_network = SharingNetwork(hidden_size=hidden_size, dropout_ratio=dropout_ratio)
        self.policy_network = PolicyNetwork(
            hidden_size=hidden_size, out_size=policy_network_outsize, dropout_ratio=dropout_ratio
        )
        self.value_network = ValueNetwork(hidden_size=hidden_size, dropout_ratio=dropout_ratio)

    def reset_state(self):
        self.sharing_network.reset_state()
        self.policy_network.reset_state()
        self.value_network.reset_state()

    def pi(self, x):
        y = self.sharing_network(x)
        y = self.policy_network(y)
        return y

    def v(self, x):
        y = self.sharing_network(x)
        y = self.value_network(y)
        return y

