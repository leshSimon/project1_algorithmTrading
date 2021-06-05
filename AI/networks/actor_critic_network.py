from AI.networks.sharing_network import SharingNetwork
from AI.networks.value_network import ValueNetwork
from AI.networks.policy_network import PolicyNetwork
import torch.nn as nn
import torch.optim as optim


class ActorCriticNetwork(nn.Module):
    def __init__(
        self,
        input_size: int = 1401,
        hidden_size: int = 170,
        policy_network_outsize: int = 4201,
        dropout_ratio: float = 0.5,
    ):
        super(ActorCriticNetwork, self).__init__()
        self.sharing_network = SharingNetwork(input_size=input_size, hidden_size=200, dropout_ratio=dropout_ratio)
        self.policy_network = PolicyNetwork(
            hidden_size=hidden_size, out_size=policy_network_outsize, dropout_ratio=dropout_ratio
        )
        self.value_network = ValueNetwork(hidden_size=hidden_size, dropout_ratio=dropout_ratio)
        self.optimizer = optim.SGD(self.parameters(), lr=0.001, momentum=0.9)

    def pi(self, x):
        y = self.sharing_network(x)
        y = self.policy_network(y)
        return y

    def v(self, x):
        y = self.sharing_network(x)
        y = self.value_network(y)
        return y

