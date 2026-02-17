---
name: vynn-backtester
description: 使用 Vynn 功能，通过自然语言轻松运行交易策略的回测。
version: 1.0.0
homepage: https://the-vynn.com
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      env: ["VYNN_API_KEY"]
    primaryEnv: "VYNN_API_KEY"
    files: ["plugin.py", "config.example.toml"]
tags: [backtest, trading, quant, finance, strategy, stocks, portfolio, alpha]
---
# Vynn 回测工具

使用自然语言即可回测任何交易策略。几秒钟内即可获取夏普比率（Sharpe Ratio）、收益率、最大回撤率（drawdown）以及完整的资产净值曲线（equity curve）。

## 功能介绍

- **自然语言策略**：用简单的英语描述您的交易策略，Vynn 会将其转换为可执行的回测代码。
- **结构化策略**：高级用户可以通过 JSON 格式提供精确的入场/出场规则。
- **全面指标**：夏普比率、总收益率、最大回撤率、胜率、交易次数以及资产净值曲线。
- **多股票/ETF/指数组合**：支持对任意股票、ETF 或指数组合进行回测。
- **策略对比**：根据夏普比率对多种策略进行排名和对比。
- **无需额外基础设施**：无需下载本地数据，仅依赖 Python 标准库。

## 设置方法

1. 在 [the-vynn.com](https://the-vynn.com) 获取免费的 API 密钥（每月可进行 10 次回测，无需信用卡）。
2. 在您的环境变量或技能配置中设置 `VYNN_API_KEY`。
3. 从任何 OpenClaw 代理程序中运行命令 `/backtest "您的策略内容"`。

### 快速入门

```bash
# Sign up (instant, returns your API key)
curl -X POST https://the-vynn.com/v1/signup -H "Content-Type: application/json" -d '{"email": "you@example.com"}'

# Set the key
export VYNN_API_KEY="vynn_free_..."
```

## 使用示例

### 简单的自然语言回测

```
/backtest "RSI mean reversion on AAPL, 2 year lookback"
```

### 动量交易策略

```
/backtest "MACD crossover on SPY with 20/50 EMA filter"
```

### 多股票组合回测

```
/backtest --tickers AAPL,MSFT,GOOGL --strategy "momentum top 3"
```

### 结构化的入场/出场规则

```
/backtest '{"entries": [{"indicator": "RSI", "op": "<", "value": 30}], "exits": [{"indicator": "RSI", "op": ">", "value": 70}]}' --tickers AAPL
```

### 策略对比

```python
from plugin import VynnBacktesterPlugin

vynn = VynnBacktesterPlugin()
results = vynn.compare(
    strategies=[
        "RSI mean reversion",
        "MACD crossover",
        "Bollinger band breakout",
    ],
    tickers=["SPY"],
)
for r in results:
    print(f"{r.strategy}: Sharpe={r.sharpe_ratio}, Return={r.total_return_pct}%")
```

## 环境变量

| 变量 | 是否必填 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `VYNN_API_KEY` | 是 | 从 the-vynn.com 获取的 API 密钥 | -- |
| `VYNN_BASE_URL` | 否 | 可覆盖 API 基础地址（用于自托管环境） | `https://the-vynn.com/v1` |

## 外部接口

| 接口 | 功能 | 发送的数据 | --- |
| --- | --- | --- |
| `https://the-vynn.com/v1/backtest` | 执行策略回测 | 策略描述、股票代码列表、回测周期 | |
| `https://the-vynn.com/v1/signup` | 注册免费 API 密钥 | 电子邮件地址 | |

## 安全与隐私

- 所有请求均通过 `X-API-Key` 头部进行身份验证。
- 策略描述和股票代码列表仅用于回测，不会被存储。
- 回测结果为临时数据，不会保存在 Vynn 服务器上。
- 该工具不存储任何交易数据、投资组合信息或个人隐私信息。
- 该工具不保存任何凭据，仅通过环境变量存储您的 API 密钥。
- 源代码完全公开：[github.com/beee003/astrai-openclaw](https://github.com/beee003/astrai-openclaw)

## 运行机制

该工具不调用任何大型语言模型（LLM）。它仅将策略描述发送至 Vynn 回测引擎（一个定量执行系统），不会生成任何提示或自动完成内容。

## 价格政策

- **免费版**：每月 10 次回测，所有功能均可用，无需信用卡。
- **专业版**（29 美元/月）：无限次回测、优先执行权限、更长的回测周期。