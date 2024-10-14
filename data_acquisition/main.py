import os
from alpaca_trade_api import REST as AlpacaREST
from ib_insync import IB, util
from binance import Client as BinanceClient
import pandas as pd

# Alpaca API配置
alpaca_api = AlpacaREST(os.getenv('ALPACA_KEY_ID'), os.getenv('ALPACA_SECRET_KEY'), base_url=os.getenv('ALPACA_BASE_URL'))

# Interactive Brokers API配置
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Binance API配置
binance_client = BinanceClient(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))

def get_alpaca_data(symbol, timeframe):
    barset = alpaca_api.get_barset(symbol, timeframe, limit=100)
    return barset[symbol]

def get_ib_data(symbol, duration, bar_size):
    contract = Stock(symbol, 'SMART', 'USD')
    bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration,
                                barSizeSetting=bar_size, whatToShow='MIDPOINT', useRTH=True)
    return util.df(bars)

def get_binance_data(symbol, interval):
    klines = binance_client.get_historical_klines(symbol, interval, "1000 hours ago UTC")
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume',
                                       'close_time', 'quote_asset_volume', 'number_of_trades',
                                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    return df

if __name__ == "__main__":
    # 示例获取数据
    alpaca_data = get_alpaca_data('AAPL', 'minute')
    ib_data = get_ib_data('AAPL', '1 D', '1 min')
    binance_data = get_binance_data('BTCUSDT', '1m')

    # 数据处理和存储
    # TODO: 将数据存储到数据库或内存中