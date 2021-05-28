from AI.dezero import Model
import AI.dezero.layers as L
import AI.dezero.functions as F


class ValueTargetNetwork(Model):
    def __init__(self, hidden_size: int = 650, dropout_ratio: float = 0.5):
        super().__init__()
        self.dropout_ratio = dropout_ratio

        self.affine1 = L.Linear(hidden_size)
        self.lstm1 = L.LSTM(hidden_size)
        self.lstm2 = L.LSTM(hidden_size)
        self.lstm3 = L.LSTM(hidden_size)
        self.lstm4 = L.LSTM(hidden_size)
        self.affine2 = L.Linear(1)

    def reset_state(self):
        self.lstm1.reset_state()
        self.lstm2.reset_state()
        self.lstm3.reset_state()
        self.lstm4.reset_state()

    def __call__(self, x):
        y = F.reshape(x, (1, len(x)))
        y = self.affine1(y)
        y = F.relu(y)

        y = self.lstm1(y)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm2(y)
        y_mediate2 = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm3(y)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = self.lstm4(y)
        y = F.dropout(y, dropout_ratio=self.dropout_ratio)

        y = y + y_mediate2
        y = self.affine2(y)

        return y.data

