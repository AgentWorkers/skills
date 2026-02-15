---
name: vibetrader
description: 通过自然语言创建和管理基于人工智能的交易机器人。支持模拟交易（Paper Trading）和实时交易（Live Trading）、投资组合监控（Portfolio Monitoring）、回测（Backtesting）、股票报价（Stock Quotes）以及期权链（Option Chains）功能。
homepage: https://vibetrader.markets
metadata: {"openclaw":{"homepage":"https://vibetrader.markets","category":"finance","requires":{"env":["VIBETRADER_API_KEY"]}}}
---

# VibeTrader - 人工智能交易机器人

使用自然语言创建和管理由人工智能驱动的交易机器人，可自动执行股票、ETF、加密货币和期权的交易策略。

## 您可以做什么

### 🤖 机器人管理
- **通过自然语言创建机器人**：例如：“创建一个在RSI指数低于30时买入AAPL的机器人”
- **列出、启动、暂停或删除您的机器人**
- **查看机器人性能**和交易历史记录**
- **在上线前对策略进行回测**

### 📊 投资组合与交易
- **查看持仓**和账户余额**
- **获取股票、ETF和加密货币的实时报价**
- **下达手动交易指令（买入/卖出）**
- **在模拟交易和真实交易模式之间切换**

### 📈 市场数据
- **股票和ETF的报价**
- **包含希腊字母的期权链**
- **市场状态查询**

## 设置

1. 从 [vibetrader.markets/settings](https://vibetrader.markets/settings) 获取您的API密钥。

2. 在您的OpenClaw配置文件（`~/.openclaw/openclaw.json`）中设置环境变量：

```json
{
  "skills": {
    "entries": {
      "vibetrader": {
        "env": {
          "VIBETRADER_API_KEY": "vt_your_api_key_here"
        }
      }
    }
  }
}
```

或者通过shell导出该密钥：
```bash
export VIBETRADER_API_KEY="vt_your_api_key_here"
```

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `authenticate` | 使用API密钥进行连接（如果设置了环境变量，则自动使用该密钥） |
| `create_bot` | 通过自然语言创建交易机器人 |
| `list_bots` | 列出所有机器人的状态 |
| `get_bot` | 获取机器人的详细信息和交易策略 |
| `start_bot` | 启动暂停的机器人 |
| `pause_bot` | 暂停正在运行的机器人 |
| `delete_bot` | 删除机器人 |
| `get_portfolio` | 查看持仓和余额 |
| `get_positions` | 查看当前未平仓的头寸 |
| `get_account_summary` | 获取账户余额和可用资金 |
| `place_order` | 下达买入/卖出订单 |
| `close_position` | 平仓现有头寸 |
| `get_quote` | 获取股票/ETF/加密货币的报价 |
| `get_trade_history` | 查看最近的交易记录 |
| `run_backtest` | 对机器人的策略进行回测 |
| `get_market_status` | 检查市场是否开放 |

## 示例指令

### 创建交易机器人
- “创建一个在RSI指数低于30时买入TSLA、在高于70时卖出的动量交易机器人”
- “创建一个带有5%追踪止损的NVDA交易机器人”
- “创建一个在5分钟图表上针对BTC/USD的加密货币剥头皮交易机器人”
- “当IV等级高于50时，为SPY创建一个铁秃鹫交易机器人”

### 管理您的机器人
- “显示我所有的机器人及其运行状态”
- “暂停我的AAPL动量机器人”
- “我的机器人今天进行了哪些交易？”
- “删除我所有暂停的机器人”

### 投资组合管理
- “我的当前投资组合价值是多少？”
- “显示我的未平仓头寸及其盈亏情况”
- “买入价值500美元的NVDA”
- “平仓我的TSLA头寸”

### 市场研究
- “苹果股票的当前价格是多少？”
- “获取本周五到期的SPY期权链”
- “市场现在是否开放？”

### 回测
- “对我的RSI机器人进行过去30天的回测”
- “移动平均线交叉策略在QQQ上的表现如何？”

## 交易模式

- **模拟交易**（默认）：使用虚拟资金进行练习，无风险
- **真实交易**：通过Alpaca经纪平台进行真实资金交易

使用以下命令切换模式：“Switch to live trading mode” 或 “Use paper trading”

## MCP服务器

此功能连接到VibeTrader的MCP服务器：
```
https://vibetrader-mcp-289016366682.us-central1.run.app/mcp
```

## 支持

- 网站：[vibetrader.markets](https://vibetrader.markets)
- 文档：[vibetrader.markets/docs](https://vibetrader.markets/docs)