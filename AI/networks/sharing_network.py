import torch.nn as nn
import torch.nn.functional as F


class SharingNetwork(nn.Module):
    def __init__(self, input_size: int = 1401, hidden_size: int = 170, dropout_ratio: float = 0.5):
        super(SharingNetwork, self).__init__()
        self.dropout_ratio = dropout_ratio

        self.affine1 = nn.Linear(input_size, hidden_size)

    def __call__(self, x):

        y = F.relu(self.affine(x))
        y = F.dropout(y)

        return y

