# 自动化实时交易系统使用说明

## 目录

1. [项目简介](#项目简介)
2. [前提条件](#前提条件)
3. [项目结构](#项目结构)
4. [快速启动指南](#快速启动指南)
    - [步骤 1：克隆项目仓库](#步骤-1克隆项目仓库)
    - [步骤 2：配置环境变量](#步骤-2配置环境变量)
    - [步骤 3：构建并启动 Docker 容器](#步骤-3构建并启动-docker-容器)
    - [步骤 4：部署到 Kubernetes](#步骤-4部署到-kubernetes)
    - [步骤 5：设置监控与报警](#步骤-5设置监控与报警)
    - [步骤 6：运行策略优化](#步骤-6运行策略优化)
    - [步骤 7：设置持续集成与持续部署（CI/CD）](#步骤-7设置持续集成与持续部署-cicd)
    - [步骤 8：启动 QuantConnect Lean](#步骤-8启动-quantconnect-lean)
5. [代码结构详解](#代码结构详解)
    - [数据获取模块](#数据获取模块)
    - [回测模块](#回测模块)
    - [CI/CD 配置](#cicd-配置)
6. [后续步骤](#后续步骤)
7. [常见问题](#常见问题)
8. [联系方式](#联系方式)

---

## 项目简介

本项目旨在构建一个自动化的实时交易系统，支持股票、期货、期权及加密货币等多资产类别的交易。系统基于现有的开源框架构建，确保灵活性和可扩展性。主要技术栈包括 QuantConnect 的 Lean 框架、Docker、Kubernetes 以及多家交易平台的 API（如 Alpaca、Interactive Brokers、Binance 等）。

## 前提条件

在开始之前，请确保您的开发环境满足以下条件：

1. **安装 Docker 和 Docker Compose**
   - [Docker 安装指南](https://docs.docker.com/get-docker/)
   - [Docker Compose 安装指南](https://docs.docker.com/compose/install/)

2. **安装 Kubernetes 和 Helm**
   - [Kubernetes 安装指南](https://kubernetes.io/docs/setup/)
   - [Helm 安装指南](https://helm.sh/docs/intro/install/)

3. **安装 Git**
   - [Git 安装指南](https://git-scm.com/book/zh/v2)

4. **安装 kubectl**
   - [kubectl 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

5. **注册并获取各 API 密钥**
   - [Alpaca](https://alpaca.markets/)
   - [Interactive Brokers](https://www.interactivebrokers.com/)
   - [Binance](https://www.binance.com/)

## 项目结构
```
auto_trading_system/
├── data_acquisition/
│ ├── main.py
│ └── requirements.txt
├── backtesting/
│ └── optimize.py
├── deployment/
│ └── .env
└── README.md
```

## 快速启动指南

按照以下步骤操作，以确保系统能够顺利运行。

### 步骤 1：克隆项目仓库

首先，克隆您的项目仓库到本地机器：
```bash
git clone https://github.com/BingerOne/auto_trading_system.git
cd auto_trading_system
```

### 步骤 2：配置环境变量

在 `deployment` 目录下，创建一个名为 `.env` 的文件，并添加以下内容：

```plaintext
ALPACA_KEY_ID=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret
```

### 步骤 3：构建并启动 Docker 容器

**注意**：`deployment/docker-compose.yml` 文件目前为过时版本，请根据最新需求更新或跳过此步骤。

### 步骤 4：部署到 Kubernetes

**注意**：`kubernetes/deployment.yaml` 文件目前为过时版本，请根据最新需求更新或跳过此步骤。

### 步骤 5：设置监控与报警

**注意**：监控模块相关文件（`monitoring/alert.rules`）和配置目前为过时版本，请根据最新需求更新或跳过此步骤。

### 步骤 6：运行策略优化

进入 `backtesting` 模块，运行策略优化脚本：
```bash
cd backtesting
python optimize.py
```

### 步骤 7：设置持续集成与持续部署（CI/CD）

**注意**：CI/CD 配置文件（`.github/workflows/ci-cd.yml`）目前为过时版本，请根据最新需求更新或跳过此步骤。

### 步骤 8：启动 QuantConnect Lean

**注意**：`Lean` 框架集成相关文件目前为过时版本，请根据最新需求更新或跳过此步骤。

## 代码结构详解

### 数据获取模块

**`data_acquisition/requirements.txt`**
```plaintext
alpaca-trade-api
ib_insync
python-binance
pandas
```
**`data_acquisition/main.py`**
```python:data_acquisition/main.py
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
if name == "main":
# 示例获取数据
alpaca_data = get_alpaca_data('AAPL', 'minute')
ib_data = get_ib_data('AAPL', '1 D', '1 min')
binance_data = get_binance_data('BTCUSDT', '1m')
# 数据处理和存储
# TODO: 将数据存储到数据库或内存中
```
### 回测模块

**`backtesting/optimize.py`**
```python:backtesting/optimize.py
import backtrader as bt
import pandas as pd
class SmaCross(bt.Strategy):
params = (('period', 14), )
def init(self):
self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.period)
def next(self):
if self.datas[0].close[0] > self.sma[0] and not self.position:
self.buy()
elif self.datas[0].close[0] < self.sma[0] and self.position:
self.sell()
if name == 'main':
cerebro = bt.Cerebro()
cerebro.optstrategy(SmaCross, period=range(10, 31))
data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=pd.Timestamp('2023-01-01'), todate=pd.Timestamp('2023-12-31'))
cerebro.adddata(data)
cerebro.broker.set_cash(100000)
optimized_runs = cerebro.run()
for run in optimized_runs:
for strategy in run:
print(f"Period: {strategy.params.period}, Final Portfolio Value: {strategy.broker.getvalue()}")
```
## 后续步骤

1. **扩展交易策略**：根据需要编写和优化更多交易策略，支持不同的资产类别和交易逻辑。
2. **优化系统性能**：根据监控数据优化系统资源分配和性能，确保交易的高效执行。
3. **增强安全性**：进一步加强环境变量管理和数据加密措施，确保系统的安全性。
4. **自动化测试**：完善测试用例，确保系统稳定性和策略的可靠性。
5. **用户界面开发**：根据需求开发前端界面，提供友好的用户交互体验。

## 常见问题

### 1. Docker 容器无法启动

- **原因**：检查 `Dockerfile` 和 `docker-compose.yml` 中的配置是否正确，确保所有依赖项已正确安装。
- **解决方法**：运行 `docker-compose logs` 查看详细错误日志，根据日志信息排查问题。

### 2. Kubernetes 部署失败

- **原因**：集群配置错误或资源不足。
- **解决方法**：使用 `kubectl describe deployment trading-system` 查看详细信息，确保集群配置正确且有足够的资源。

### 3. API 数据获取失败

- **原因**：API 密钥错误或网络问题。
- **解决方法**：确保 `.env` 文件中的 API 密钥正确，并检查网络连接。

## 联系方式

如在使用过程中遇到任何问题或需要进一步的帮助，欢迎通过以下方式联系：

- **邮箱**：support@yourdomain.com
- **GitHub Issues**：[GitHub Issues 页面](https://github.com/your_username/auto_trading_system/issues)
- **Slack**：加入我们的 [Slack 社区](https://your_slack_invite_link) 进行交流。

---

感谢您使用本自动化实时交易系统！祝您交易顺利！