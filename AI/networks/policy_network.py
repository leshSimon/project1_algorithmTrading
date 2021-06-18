import torch.nn as nn
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, input_size: int, out_size: int = 4201):
        super(PolicyNetwork, self).__init__()

        self.gru = nn.GRU(input_size=input_size, hidden_size=80, num_layers=1)
        self.affine2 = nn.Linear(80, 70)
        self.affine3 = nn.Linear(70, 60)
        self.affine4 = nn.Linear(60, 60)
        self.affine5 = nn.Linear(60, out_size)

        self.softmax = nn.Softmax(dim=2)

    def __call__(self, x):

        output, _ = self.gru(x)
        y = F.dropout(output, p=0.5)

        y = F.leaky_relu(self.affine2(y))
        y = F.dropout(y, p=0.5)

        y = F.leaky_relu(self.affine3(y))
        y = F.dropout(y, p=0.5)

        y = F.leaky_relu(self.affine4(y))
        y = F.dropout(y, p=0.5)

        y = self.affine5(y)

        y = self.softmax(y)

        return y

