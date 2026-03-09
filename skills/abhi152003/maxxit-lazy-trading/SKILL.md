---
emoji: 📈
name: maxxit-lazy-trading
version: 1.2.10
author: Maxxit
description: 通过 Maxxit 的 Lazy Trading API，在 Ostium、Aster 和 Avantis 上执行永久性交易（即长期持有的交易）。该 API 提供了用于开仓/平仓、风险管理、获取市场数据、复制交易其他 OpenClaw 代理的程序化接口，以及一个无需信任的 Alpha Marketplace，用于买卖经过 ZK（Zcash-Kernel）验证的交易信号（这些信号来自 Arbitrum Sepolia）。
homepage: https://maxxit.ai
repository: https://github.com/Maxxit-ai/maxxit-latest
disableModelInvocation: true
requires:
  env:
    - MAXXIT_API_KEY
    - MAXXIT_API_URL
metadata:
  openclaw:
    requiredEnv:
      - MAXXIT_API_KEY
      - MAXXIT_API_URL
    bins:
      - curl
    primaryCredential: MAXXIT_API_KEY
---
# Maxxit 懒人交易（Lazy Trading）

通过 Maxxit 的懒人交易 API，在 Ostium、Aster DEX 和 Avantis DEX 上执行永久性期货交易。此技能允许通过程序化接口自动开仓/平仓和管理风险。

## 内置策略脚本

该技能包含独立的 Python 策略脚本。当用户希望代理执行预定义的交易系统而不是手动指定每笔交易时，可以使用这些脚本。

- `ema-strategy.py`  
  - 基于 Binance 的 Kline 图表数据，使用收盘价进行趋势跟随的 EMA 交叉交易策略。

- `rsi-bollinger-strategy.py`  
  - 等值回归系统，等待价格突破 Bollinger Band 并在 RSI 确认后重新进入市场。

- `donchian-adx-strategy.py`  
  - 仅当 ADX 确认强烈趋势时，才进行 Donchian 通道突破的交易策略。

- `taker-strategy.py`  
  - 一种激进的 Taker（订单流）高频交易策略。分析 Binance 的买卖比率以检测激进的市场参与者并捕捉快速的市场波动。

- `mean-reversion-strategy.py`  
  - 使用 RSI 和 Bollinger Band 的等值回归策略。这是一种适用于横盘或乏味市场的高频剥削技术方法。

- `breakout-strategy.py`  
  - 基于波动性突破的策略，当价格突破标准差通道且 ATR 确认波动性和动量增加时进入市场。

- `vwap-strategy.py`  
  - 使用成交量加权平均价格（VWAP）的策略。

所有脚本：  
  - 直接从 `https://api.binance.com/api/v3/klines` 获取 Binance Kline 数据。  
  - 使用 `MAXXIT_API_URL` 和 `MAXXIT_API_KEY`。  
  - 通过 Maxxit 的程序化交易接口执行交易。  
  - 在 OpenClaw 工作区中维护每个符号和每个交易场所的状态。

### 示例调用：  
（此处应插入具体的 API 调用示例代码）

## 何时使用此技能

- 用户希望在 Ostium 上执行交易。  
- 用户希望在 Aster DEX 上执行交易。  
- 用户询问他们的懒人交易账户详情。  
- 用户希望查看他们的 USDC/ETH 余额。  
- 用户希望查看他们的未平仓头寸或投资组合。  
- 用户希望查看他们的已平仓头寸历史或利润/损失（PnL）。  
- 用户希望发现可用的交易符号。  
- 用户希望获取市场数据或 LunarCrush 指标以供分析。  
- 用户需要市场研究、市场摘要或以交易为中心的研究简报。  
- 用户需要整个市场快照用于交易目的。  
- 用户希望比较不同代币的排名（AltRank）。  
- 用户希望识别高情绪的交易机会。  
- 用户希望了解加密货币资产的社会媒体流量趋势。  
- 用户希望开新的交易头寸（多头/空头）。  
- 用户希望平仓现有的头寸。  
- 用户希望设置或修改止盈水平。  
- 用户希望设置或修改止损水平。  
- 用户希望获取当前的代币/市场价格。  
- 用户提到“懒人交易”、“永久性合约”或“期货交易”。  
- 用户希望自动化他们的交易工作流程。  
- 用户希望复制交易或镜像其他交易者的头寸。  
- 用户希望找到其他 OpenClaw 代理以学习。  
- 用户希望查看表现最好的交易者的交易记录。  
- 用户希望找到高影响因子的交易者进行复制。  
- 用户希望出售他们的交易信号作为“阿尔法产品”（alpha product）。  
- 用户希望浏览或购买来自 ZK 验证的交易者的无信任阿尔法产品。  
- 用户希望生成他们的交易表现的 ZK 证明，或将头寸标记为阿尔法产品。