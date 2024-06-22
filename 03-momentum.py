
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas_ta as ta
import numpy as np
import sys

print(GOOG)

def indicator(data):
    return data.Close.s.pct_change(periods=7).to_numpy() * 100

class MomentumStrategy(Strategy):

    def init(self):
        self.pct_change = self.I(indicator, self.data)

    def next(self):

        change = self.pct_change[-1]

        if self.position:
            if change < 0:
                self.position.close()
        else:
            if change > 5:
                self.buy()

bt = Backtest(GOOG, MomentumStrategy, cash=10_000)

stats = bt.run()
print(stats)
bt.plot()
