import torch.nn as nn
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, input_size: int, out_size: int = 4201, dropout_ratio: float = 0.5):
        super(PolicyNetwork, self).__init__()

        self.dropout_ratio = dropout_ratio

        self.affine1 = nn.Linear(input_size, 70)
        self.affine2 = nn.Linear(70, 60)
        self.affine3 = nn.Linear(60, 50)
        self.affine4 = nn.Linear(50, 40)
        self.affine5 = nn.Linear(40, out_size)

        self.softmax = nn.Softmax(dim=2)

    def __call__(self, x):

        y = F.leaky_relu(self.affine1(x))
        y = F.dropout(y, p=self.dropout_ratio)

        y = F.leaky_relu(self.affine2(y))
        y = F.dropout(y, p=self.dropout_ratio)

        y = F.leaky_relu(self.affine3(y))
        y = F.dropout(y, p=self.dropout_ratio)

        y = F.leaky_relu(self.affine4(y))
        y = F.dropout(y, p=self.dropout_ratio)

        y = self.affine5(y)

        y = self.softmax(y)

        return y

