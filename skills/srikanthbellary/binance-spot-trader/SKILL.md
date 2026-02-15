---
name: binance-spot-trader
description: 这款自主运行的Binance现货交易机器人具备基于大型语言模型（LLM）的市场分析能力，支持动量交易、均值回归以及定期定额投资（DCA）策略，适用于Binance平台上的任意现货交易对。用户可利用它进行Binance交易、设置自动化加密货币交易系统、构建现货交易机器人，或实现定期定额投资的自动化操作。该机器人具备技术分析功能、LLM情绪评估能力、头寸管理功能以及投资组合跟踪功能。
metadata: {"openclaw": {"requires": {"env": ["BINANCE_API_KEY", "BINANCE_SECRET_KEY", "LLM_API_KEY"]}, "primaryEnv": "BINANCE_API_KEY", "homepage": "https://github.com/srikanthbellary"}}
---

# Binance 现货交易机器人

这是一个专为 Binance 设计的自动现货交易机器人。它结合了技术指标和基于大型语言模型（LLM）的市场情绪分析功能，可在任何 Binance 现货交易对上执行交易。

## 先决条件

- 拥有 Binance 账户，并已获取 API 密钥（启用现货交易功能，禁用提款功能）
- 拥有 Anthropic API 密钥（使用 Haiku 服务，每次请求费用约为 0.001 美元）
- 确保使用的 Python 版本为 3.10 或更高

## 设置

### 1. 安装

```bash
bash {baseDir}/scripts/setup.sh
```

### 2. 配置

创建 `.env` 文件：
```
BINANCE_API_KEY=<your-api-key>
BINANCE_SECRET_KEY=<your-secret-key>
LLM_API_KEY=<anthropic-api-key>
PAIRS=BTCUSDT,ETHUSDT,SOLUSDT
STRATEGY=momentum
TRADE_SIZE_PCT=5
MAX_POSITIONS=5
```

### 3. 运行

直接运行脚本：
```bash
python3 {baseDir}/scripts/trader.py
```

或者通过 cron 任务定时运行：
```
*/5 * * * * cd /opt/trader && python3 trader.py >> trader.log 2>&1
```

## 交易策略

### 动量策略（默认策略）
- 当价格突破 20 日移动平均线（20-EMA）且成交量激增时买入
- 当价格跌破 20 日移动平均线或达到止盈/止损（TP/SL）价格时卖出
- 适用于趋势明显的市场（如 BTC、ETH、SOL）

### 均值回归策略
- 当相对强弱指数（RSI）低于 30（市场处于超卖状态）且价格接近布林带下轨时买入
- 当 RSI 高于 70（市场处于超买状态）或价格接近布林带上轨时卖出
- 适用于价格波动较小的市场

### 定投策略（DCA）
- 在固定时间间隔内买入固定金额，不受价格影响
- 可配置间隔时间（每小时、每天、每周）
- 是长期积累资产的低风险策略

### 基于 LLM 的增强策略（所有策略）
- 在每次交易前，通过 Claude Haiku 服务获取市场情绪分析
- 分析因素包括：近期新闻、价格走势、成交量模式、市场结构等
- 如果市场情绪明显不利，可以拒绝执行交易信号

## 交易参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `PAIRS` | `BTCUSDT` | 以逗号分隔的交易对 |
| `STRATEGY` | `momentum` | 可选值：`momentum`（动量策略）、`mean_reversion`（均值回归策略）或 `dca`（定投策略） |
| `TRADE_SIZE_PCT` | `5` | 每笔交易占投资组合的比例（百分比） |
| `MAX_POSITIONS` | `5` | 同时持有的最大开仓数量 |
| `TAKE_PROFIT_PCT` | `5` | 盈利幅度（百分比） |
| `STOP_LOSS_PCT` | `3` | 止损幅度（百分比） |
| `DCA_INTERVAL` | `daily` | 定投间隔：`hourly`（每小时）、`daily`（每天）、`weekly`（每周） |
| `DCA_AMOUNT_USDT` | `50` | 每次定投的金额（单位：USDT） |
| `USE_LLM` | `true` | 是否启用基于 LLM 的市场情绪分析 |

## 监控

```bash
# Check portfolio
python3 {baseDir}/scripts/portfolio.py

# View trade history
tail -50 trades.jsonl

# Check logs
tail -f trader.log
```

## ⚠️ 安全注意事项

- **切勿为 API 密钥启用提款功能**——仅用于交易 |
- 在 Binance 中对 API 密钥设置 IP 限制 |
- 使用资金有限的子账户进行机器人交易 |
- 开始时使用小额资金（50-100 美元）并进行模拟交易 |
- 在运行后的前 24 小时内密切监控交易情况 |
- 为所有交易设置 Binance 的电子邮件提醒 |
- 将 API 密钥存储在安全位置（建议使用 SSH 密钥，并配置防火墙及文件权限（chmod 600） |

## 参考资料

- 有关 REST API 的详细信息，请参阅 `references/binance-api.md`
- 有关技术分析的详细内容，请参阅 `references/indicators.md`