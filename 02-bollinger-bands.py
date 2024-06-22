
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas_ta as ta
import numpy as np
import sys

print(GOOG)

def indicator(data):
    bbands = ta.bbands(close = data.Close.s, std = 1)
    # Get rid of the last column (band_percent)
    return bbands.to_numpy().T[0:3]

class BBStrategy(Strategy):

    def init(self):
        # Note that this returns each column as a row
        # Then extends the length of each row on each iteration
        self.bbands = self.I(indicator, self.data)

    def next(self):

        lower_band = self.bbands[0]
        upper_band = self.bbands[2]

        if self.position:
            if self.data.Close[-1] > upper_band[-1]:
                self.position.close()
        else:
            print(self.data.Close[-1], lower_band[-1])
            if self.data.Close[-1] < lower_band[-1]:
                self.buy()

bt = Backtest(GOOG, DFStrategy, cash=10_000)

stats = bt.run()
print(stats)
bt.plot()
