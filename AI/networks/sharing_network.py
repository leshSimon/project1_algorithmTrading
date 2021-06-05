import torch.nn as nn
import torch.nn.functional as F


class SharingNetwork(nn.Module):
    def __init__(self, input_size: int = 1401, hidden_size: int = 200, dropout_ratio: float = 0.5):
        super(SharingNetwork, self).__init__()
        self.dropout_ratio = dropout_ratio

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=2, dropout=dropout_ratio)
        self.dropout = nn.Dropout(p=dropout_ratio)
        self.affine = nn.Linear(hidden_size, 170)

    def __call__(self, x):

        output, _ = self.lstm(x)
        y = self.dropout(output)

        y = self.affine(y)

        return y

