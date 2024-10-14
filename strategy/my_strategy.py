from AlgorithmImports import *

class MyTradingAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        self.symbol = self.AddEquity("AAPL").Symbol
        self.SMA = self.SMA(self.symbol, 14, Resolution.Daily)
        self.lastAction = None

    def OnData(self, data):
        if not self.SMA.IsReady:
            return

        price = self.SMA.Current.Value
        if self.Securities[self.symbol].Price > price and self.lastAction != "BUY":
            self.SetHoldings(self.symbol, 1)
            self.lastAction = "BUY"
            self.Debug("Bought AAPL")
        elif self.Securities[self.symbol].Price < price and self.lastAction != "SELL":
            self.SetHoldings(self.symbol, -1)
            self.lastAction = "SELL"
            self.Debug("Sold AAPL")
