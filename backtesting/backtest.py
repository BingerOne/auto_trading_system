import backtrader as bt
import pandas as pd

class SmaCross(bt.Strategy):
    params = (('period', 14), )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.period)

    def next(self):
        if self.datas[0].close[0] > self.sma[0] and not self.position:
            self.buy()
        elif self.datas[0].close[0] < self.sma[0] and self.position:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=pd.Timestamp('2023-01-01'), todate=pd.Timestamp('2023-12-31'))
    cerebro.adddata(data)

    cerebro.broker.set_cash(100000)
    cerebro.run()
    cerebro.plot()
