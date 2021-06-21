import torch.nn as nn
import torch.nn.functional as F


class ValueNetwork(nn.Module):
    def __init__(self, input_size: int):
        super(ValueNetwork, self).__init__()

        self.affine1 = nn.Linear(input_size, 100)
        self.affine2 = nn.Linear(100, 90)
        self.affine3 = nn.Linear(90, 80)
        self.affine4 = nn.Linear(80, 70)
        self.affine5 = nn.Linear(70, 1)

        self.softmax = nn.Softmax(dim=2)

    def __call__(self, x):

        y = F.leaky_relu(self.affine1(x))
        y = F.dropout(y, p=0.5)

        y = F.leaky_relu(self.affine2(y))
        y = F.dropout(y, p=0.5)

        y = F.leaky_relu(self.affine3(y))
        y = F.dropout(y, p=0.5)

        y = F.leaky_relu(self.affine4(y))
        y = F.dropout(y, p=0.5)

        y = self.affine5(y)

        return y

