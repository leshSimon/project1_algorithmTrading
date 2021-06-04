import AI.dezero.layers as L
import AI.dezero.functions as F


class PolicyNetwork(L.Layer):
    def __init__(self, hidden_size: int = 170, out_size: int = 4201, dropout_ratio: float = 0.5):
        super().__init__()
        self.dropout_ratio = dropout_ratio

        self.lstm1 = L.LSTM(hidden_size)
        self.lstm2 = L.LSTM(hidden_size)
        self.lstm3 = L.LSTM(hidden_size)
        self.affine = L.Linear(out_size)

    def reset_state(self):
        self.lstm1.reset_state()
        self.lstm2.reset_state()
        self.lstm3.reset_state()

    def __call__(self, x):

        y = self.lstm1(x)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm2(y)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm3(y)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.affine(y)
        y = F.softmax(y)
        y = y[0]

        return y

