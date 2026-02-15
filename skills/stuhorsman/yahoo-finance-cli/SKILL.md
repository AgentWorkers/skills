---
name: yahoo-finance
description: 当用户请求“获取股票价格”、“查看股票报价”、“查询收益信息”、“获取财务数据”、“寻找热门股票”，或需要从 Yahoo Finance 获取股票市场数据时，应使用此技能。
metadata: {"clawdbot":{"requires":{"bins":["jq","yf"]},"install":[{"id":"brew","kind":"brew","package":"jq","bins":["jq"],"label":"Install jq (Homebrew)"},{"id":"npm","kind":"node","package":"yahoo-finance2","bins":["yahoo-finance"],"label":"Install Yahoo Finance CLI (npm)"},{"id":"link-yf","kind":"exec","command":"ln -sf $(npm bin -g)/yahoo-finance /usr/local/bin/yf","label":"Link yf binary"}]}}
---

# Yahoo Finance CLI

这是一个基于 Node.js 的命令行工具（CLI），使用 `yahoo-finance2` 库从 Yahoo Finance 获取全面的股票数据。

## 必备条件

- Node.js
- `yahoo-finance2` 已全局安装，或可通过 `yf` 命令访问
- `jq` 工具

## 安装

```bash
brew install jq
npm install yahoo-finance2
sudo ln -s /opt/homebrew/bin/yahoo-finance /usr/local/bin/yf
```

## 使用方法

该工具可通过 `yf` 命令使用。它输出 JSON 格式的数据，您可以将这些数据通过管道（`|`）传递给 `jq` 工具进行进一步处理或过滤。

```bash
yf <module> <symbol> [queryOptions]
```

## 模块功能

### **报价（实时价格与数据）**
获取股票的实时价格、价格变动及基本信息。

```bash
yf quote AAPL
yf quote AAPL | jq '.regularMarketPrice'
```

### **报价概要（基本面信息等）**
获取股票的详细信息，如收益、财务数据及公司概况。

```bash
# Get specific sub-modules
yf quoteSummary AAPL '{"modules":["assetProfile", "financialData", "defaultKeyStatistics"]}'

# Common modules to request:
# - assetProfile (Company info, sector)
# - financialData (Target price, margins, cash)
# - defaultKeyStatistics (Enterprise value, float, shares)
# - calendarEvents (Earnings dates)
# - earnings (History and trend)
# - recommendationTrend (Analyst ratings)
# - upgradeDowngradeHistory
```

### **市场洞察**
提供关于股票的技术分析和基本面分析（如估值、市场前景）。

```bash
yf insights AAPL
```

### **搜索**
允许用户搜索股票代码。

```bash
yf search "Apple"
yf search "BTC-USD"
```

### **历史数据（已弃用）**
可获取股票的历史价格（OHLCV）数据。注意：`historical` 功能已弃用，建议使用 `chart` 功能代替。

```bash
# Deprecated - use chart instead
yf historical AAPL '{"period1":"2024-01-01","period2":"2024-12-31"}'

# Recommended: use chart
yf chart AAPL '{"period1":"2024-01-01","period2":"2024-12-31"}'
```

### **热门股票**
显示当前热门的股票。

```bash
yf trendingSymbols US
```

## 使用示例

**快速查询股票价格**
```bash
# Full JSON then filter with jq
yf quote NVDA | jq '{symbol: .symbol, price: .regularMarketPrice, changePct: .regularMarketChangePercent}'
```

**查询下一个财报发布日期**
```bash
# Use single quotes around the JSON option in zsh/bash
yf quoteSummary TSLA '{"modules":["calendarEvents"]}' | jq '.calendarEvents.earnings.earningsDate'
```

**查看分析师推荐**
```bash
yf quoteSummary AAPL '{"modules":["recommendationTrend"]}'
```

**查看公司概况**
```bash
yf quoteSummary MSFT '{"modules":["assetProfile"]}'
```

**获取股票的历史价格（OHLCV）数据**
```bash
# Using chart (recommended)
yf chart AAPL '{"period1":"2024-01-01","period2":"2024-12-31","interval":"1d"}' | jq '.quotes[0:5]'

# Using historical (deprecated, but still works)
yf historical AAPL '{"period1":"2024-01-01","period2":"2024-12-31","interval":"1d"}' | jq '.[0:5]'
```

**搜索股票代码**
```bash
yf search 'Apple'
yf search 'BTC-USD'
```

**查询美国市场的热门股票**
```bash
yf trendingSymbols US
```

**获取股票的市场洞察（估值、市场前景）**
```bash
yf insights AAPL
```

## 故障排除

- **Cookies：** 该工具会自动处理存储在 `~/.yf2-cookies.json` 文件中的 Cookies。如果遇到问题，请尝试删除该文件。
- **JSON 输出：** 输出的数据为纯 JSON 格式，可使用 `jq` 工具进行解析或进一步处理。

**其他提示：**
- 如果遇到身份验证或解析错误，请删除 `~/.yf2-cookies.json` 文件后重新尝试。
- 在使用 zsh 的 macOS 环境中，JSON 参数应使用单引号；字符串内容则使用双引号（参见上面的示例）。
- 如果只需要获取简洁的数值信息（无需使用 `jq`），可以使用简单的 `jq` 过滤器，例如：

```bash
yf quote AAPL | jq -r '.regularMarketPrice'
```