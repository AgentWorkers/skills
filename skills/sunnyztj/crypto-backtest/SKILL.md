---
name: crypto-backtest
description: 这款加密货币期货回测引擎内置了EMA（指数移动平均线）、RSI（相对强弱指数）、MACD（移动平均收敛发散指标）和Bollinger Band（布林带）等交易策略。它可以从任何支持ccxt协议的交易所（如Bybit、Binance、OKX等）获取OHLCV（开市价、最高价、最低价、收盘价）数据，同时支持多种交易策略的并行回测。该引擎能够计算交易策略的胜率、盈亏（PnL）和最大回撤率，并将回测结果以JSON格式导出。适用于回测交易策略、比较不同参数组合的效果、评估加密货币交易信号，或构建量化交易系统。
---
# 加密货币回测引擎

这是一个用于加密期货策略的快速、可脚本化的回测工具。它通过 ccxt 获取数据，执行策略，并生成相应的指标报告。

## 快速入门

```bash
pip install ccxt numpy
python scripts/backtest_engine.py --symbol ETH/USDT:USDT --strategy ema --fast 12 --slow 26
```

## 主要功能

- **支持多交易所**：任何由 ccxt 支持的交易所（Bybit、Binance、OKX、Bitget 等）
- **内置策略**：EMA 交叉、RSI、MACD、Bollinger Bands
- **参数扫描**：自动测试所有可能的参数组合
- **风险模拟**：可配置杠杆率、持仓大小、止损/止盈点以及交易费用
- **JSON 输出**：以机器可读的格式输出结果，便于集成到自动化流程中
- **自定义策略**：提供简单的插件接口

## 使用方法

### 单一策略
```bash
python scripts/backtest_engine.py \
  --symbol SOL/USDT:USDT \
  --strategy rsi \
  --period 14 --oversold 30 --overbought 70 \
  --capital 1000 --leverage 5
```

### 参数扫描
```bash
python scripts/sweep.py \
  --symbol ETH/USDT:USDT \
  --strategies ema,rsi,macd,bbands \
  --capital 1000 --leverage 5 \
  --output results.json
```

### 自定义策略
有关自定义策略的插件接口，请参阅 `references/custom_strategy.md`。

## 输出指标

每次回测都会生成以下报告：
- 总交易次数、胜率、盈利因子
- 总盈亏（绝对值及百分比）
- 最大回撤幅度
- 最佳/最差交易记录
- 最终账户余额

## 相关文件

- `scripts/backtest_engine.py`：包含 EMA、RSI、MACD、Bollinger Bands 策略的核心引擎
- `scripts/sweep.py`：用于执行多策略参数扫描的工具
- `references/custom_strategy.md`：自定义策略添加指南
- `references/strategy_notes.md`：关于各内置策略的注意事项及使用技巧