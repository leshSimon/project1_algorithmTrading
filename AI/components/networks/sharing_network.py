import AI.dezero.layers as L
import AI.dezero.functions as F


class SharingNetwork(L.Layer):
    def __init__(self, hidden_size: int = 650, dropout_ratio: float = 0.5):
        super().__init__()
        self.dropout_ratio = dropout_ratio

        self.lstm1 = L.LSTM(hidden_size)
        self.lstm2 = L.LSTM(hidden_size)
        self.affine = L.Linear(hidden_size)

    def reset_state(self):
        self.lstm1.reset_state()
        self.lstm2.reset_state()

    def __call__(self, x):
        y = F.reshape(x, (1, len(x)))

        y = self.lstm1(y)
        y_mediate = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm2(y_mediate)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = y + (y_mediate * 0.3)
        y = self.affine(y)

        return y

