---
name: profitabul-mcp
description: 实时期货市场情报、GEX/期权交易数据分析、交易信号生成、模拟交易（paper trading）、回测功能，以及通过MCP进行的实时交易执行。支持的交易品种包括ES、NQ、SPX、NDX、QQQ、IWM、GC、SI、CL等。
version: 0.2.3
metadata:
  openclaw:
    requires:
      env:
        - PROFITABUL_API_KEY
    primaryEnv: PROFITABUL_API_KEY
    emoji: "\U0001F4C8"
    homepage: https://profitabul.ai
---
# Profitabul MCP

为AI交易代理提供实时的期货和期权市场情报。通过一个统一的MCP接口，您可以获取实时市场数据、GEX衍生出的支撑/阻力水平、交易信号、历史数据以及进行模拟交易（paper trading）。

## 主要功能

- **市场概况**：13种证券的实时价格、GEX市场状态、VIX指数波动情况以及蜡烛图摘要。
- **Heatseeker交易信号**：结合伽马风险（gamma exposure）、Vanna风险（vanna exposure）和VIX指数趋势的方向性交易信号。
- **GEX关键水平**：基于真实期权数据计算出的关键支撑/阻力水平，包括“King Node”、“Gatekeeper”、“零伽马”（zero gamma）以及价格上限/下限。
- **历史数据**：支持多种时间框架（1分钟至1天）的历史蜡烛图数据，最多可存储20万条记录。
- **统计分析**：提供实现波动率（realized volatility）、平均价格范围（average range）和成交量（volume stats）等统计信息。
- **报告功能**：包括开盘区间突破（Opening Range Breakout, ORB）和初始余额（Initial Balance, IB）分析。
- **回测功能**：支持服务器端策略回测，可配置参数。
- **模拟交易**：允许用户开设、平仓并追踪假设交易头寸，并计算盈亏（P&L）。
- **实时执行**：启用后可通过ProjectX经纪商进行真实交易。

## 支持的证券

| 类别 | 证券代码 |
|------|---------|
| 指数 | SPX, NDX |
| ETFs | SPY, QQQ, IWM |
| 期货 | ES, NQ, YM, RTY |
| 商品 | GC（黄金）、SI（白银）、CL（原油）、HG（铜） |

## 设置指南

### 1. 获取API密钥

1. 在[profitabul.com](https://profitabul.com)注册账户。
2. 订阅Pro计划（包含API访问权限）。
3. 进入**设置 > 集成**（Settings > Integrations），生成代理API密钥。
4. 复制密钥（密钥仅显示一次，格式为`pab_live_`）。

### 2. 配置环境变量

将以下代码添加到`~/.clawdbot/.env`文件中：
```bash
PROFITABUL_API_KEY=pab_live_YOUR_KEY_HERE
```

### 3. 配置mcporter

将以下代码添加到`config/mcporter.json`文件中：
```json
{
  "mcpServers": {
    "profitabul": {
      "baseUrl": "https://agents.profitabul.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${PROFITABUL_API_KEY}"
      }
    }
  }
}
```

### 4. 验证配置

```bash
mcporter list profitabul
```

## 可用工具（共16个）

### 市场情报工具

| 工具 | 功能描述 |
|------|-------------|
| `get_market_context` | 提供全面的市场概览：价格、GEX市场状态、VIX指数波动情况以及蜡烛图摘要。 |
| `get_signal` | 生成包含方向性、置信度以及入场/出场水平的交易信号。 |
| `get_key_levels` | 计算基于GEX数据的支撑/阻力水平。 |

### 历史数据与分析工具

| 工具 | 功能描述 |
|------|-------------|
| `get_history` | 获取指定证券在指定时间范围内的历史蜡烛图数据。 |
| `get_statistics` | 提供实现波动率、平均价格范围和成交量等统计信息。 |
| `run_report` | 进行开盘区间突破（ORB）和初始余额（IB）分析。 |
| `run_backtest` | 支持服务器端策略回测，参数可配置。 |

### 模拟交易工具

| 工具 | 功能描述 |
|------|-------------|
| `paper_trade` | 允许用户开设、平仓模拟头寸，并追踪盈亏。 |

### 实时执行工具（启用时可用）

| 工具 | 功能描述 |
|------|-------------|
| `live_open` | 开启带有止损/目标价的实时期货交易。 |
| `live_close` | 平仓已跟踪的实时交易。 |
| `live_reduce` | 部分减少未平仓头寸的持仓量。 |
| `live_add_risk` | 为现有头寸添加止损/止盈指令。 |
| `live_cancel_orders` | 取消未执行的交易订单。 |
| `live_account` | 查看账户信息（余额、保证金等）。 |
| `live_positions` | 查看当前未平仓的头寸。 |
| `live_orders` | 查看所有未执行的交易订单。 |

## 使用示例

### 市场分析流程

```bash
# 1. Get current market context
mcporter call 'profitabul.get_market_context(symbol: "SPX")'

# 2. Check key GEX levels
mcporter call 'profitabul.get_key_levels(symbol: "SPX")'

# 3. Get trading signal based on current conditions
mcporter call 'profitabul.get_signal(
  symbol: "SPX",
  gex_bias: "positive",
  vex_bias: "bullish",
  vix_trend: "falling"
)'
```

### 历史数据分析流程

```bash
# Get 30 days of 5-minute candles
mcporter call 'profitabul.get_history(symbol: "ES", timeframe: "5m", days: 30)'

# Run ORB analysis
mcporter call 'profitabul.run_report(reportType: "orb", symbol: "ES", days: 60)'

# Backtest ORB breakout strategy
mcporter call 'profitabul.run_backtest(
  symbol: "ES",
  days: 30,
  strategy: { type: "orb-breakout", params: { stopMult: 0.75, targetMult: 1.0 } }
)'
```

### 模拟交易流程

```bash
# Open a paper trade
mcporter call 'profitabul.paper_trade(
  action: "open",
  symbol: "ES",
  side: "long",
  entry: 5825,
  size: 2,
  reason: "GEX support bounce at zero gamma"
)'

# List open positions
mcporter call 'profitabul.paper_trade(action: "list")'

# Close a trade
mcporter call 'profitabul.paper_trade(
  action: "close",
  trade_id: "pt_1705312200_abc123",
  exit: 5850,
  close_reason: "Target reached at king node"
)'
```

## 推荐使用流程

1. **获取市场概况**：首先调用`get_market_context`了解当前市场状况。
2. **确定支撑/阻力水平**：使用`get_key_levels`获取精确的支撑/阻力位。
3. **生成交易信号**：将GEX市场数据、VIX指数趋势等信息输入`get_signal`函数以生成交易信号。
4. **验证策略有效性**：使用`run_report`或`run_backtest`验证策略的有效性。
5. **执行交易**：根据信号生成的交易策略进行模拟交易（或启用`live_open`进行实时交易）。
6. **管理交易头寸**：根据预设的支撑/阻力水平跟踪并平仓头寸。

## 使用限制

- 每个API密钥每分钟最多发送120个请求。
- 实施滑动窗口速率限制机制。
- 超过限制时，系统会返回`429 Too Many Requests`错误，并附带`Retry-After`头部信息提示重试。

## 相关资源

- [Profitabul平台](https://profitabul.com)
- [API文档](https://profitabul.ai/docs)
- [Discord社区](https://discord.gg/profitabul)