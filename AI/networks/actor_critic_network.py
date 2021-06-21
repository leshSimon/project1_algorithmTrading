from AI.networks.value_network import ValueNetwork
from AI.networks.policy_network import PolicyNetwork
import torch.nn as nn
import torch.nn.functional as F


class ActorCriticNetwork(nn.Module):
    def __init__(self, input_size: int = 1401, policy_network_outsize: int = 4201):
        super(ActorCriticNetwork, self).__init__()

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=180, num_layers=1)

        self.policy_network = PolicyNetwork(input_size=180, out_size=policy_network_outsize)
        self.value_network = ValueNetwork(input_size=180)

    def bottomNetwork(self, x):
        output, _ = self.lstm(x)
        y = F.dropout(output, p=0.5)
        return y

    def pi(self, x):
        y = self.bottomNetwork(x)
        y = self.policy_network(y)
        return y

    def v(self, x):
        y = self.bottomNetwork(x)
        y = self.value_network(y)
        return y

