---
name: alpaca
description: 通过 Alpaca API 进行股票和加密货币的交易。该 API 可用于获取市场数据（报价、历史价格图表、新闻）、下达交易订单（市价单、限价单、止损单）、查看持仓情况、管理投资组合以及查询账户信息。同时支持模拟交易和真实交易。适用于用户查询股票价格、买卖证券、查看投资组合或管理交易场景。
---

# Alpaca交易技能

通过Alpaca的API以编程方式交易股票和加密货币。

## 设置

需要将API凭据存储在环境变量或配置文件中：

```bash
# Set environment variables
export ALPACA_API_KEY="your-api-key"
export ALPACA_SECRET_KEY="your-secret-key"
export ALPACA_PAPER="true"  # "true" for paper, "false" for live
```

或者将其存储在`~/.openclaw/credentials/alpaca.json`文件中：

```json
{
  "apiKey": "your-api-key",
  "secretKey": "your-secret-key",
  "paper": true
}
```

## 快速参考

### 获取报价
```bash
python3 scripts/alpaca_cli.py quote AAPL
python3 scripts/alpaca_cli.py quote AAPL,TSLA,NVDA
```

### 获取历史数据（K线图）
```bash
python3 scripts/alpaca_cli.py bars AAPL --timeframe 1Day --limit 10
python3 scripts/alpaca_cli.py bars AAPL --timeframe 1Hour --start 2026-02-01
```

### 检查账户余额
```bash
python3 scripts/alpaca_cli.py account
```

### 列出持仓
```bash
python3 scripts/alpaca_cli.py positions
```

### 下单
```bash
# Market order
python3 scripts/alpaca_cli.py order buy AAPL 10

# Limit order
python3 scripts/alpaca_cli.py order buy AAPL 10 --limit 150.00

# Stop order
python3 scripts/alpaca_cli.py order sell TSLA 5 --stop 200.00

# Stop-limit order
python3 scripts/alpaca_cli.py order sell TSLA 5 --stop 200.00 --limit 195.00

# Skip price validation (use with caution)
python3 scripts/alpaca_cli.py order buy AAPL 10 --limit 999.00 --force
```

**订单限制规则：**

1. **证券代码验证** — 拒绝无效或未知的证券代码
2. **资金充足性检查** — 阻止超出可用资金的订单，并显示最大可购买股数
3. **重复订单检测** — 如果您对同一证券代码有未完成的订单，会发出警告
4. **价格验证** — 如果限价低于市场价，会发出警告
5. **市场时段检测** — 识别盘前、盘后和休市时段：
   - 盘前（美国东部时间凌晨4:00 - 9:30）：可以下达盘前订单
   - 盘后（美国东部时间下午4:00 - 晚上8:00）：可以下达盘后订单
   - 休市时段：会提示订单将排队等待市场开放
6. **费用确认** — 显示总费用并需要用户确认

使用`--force`选项可以跳过所有确认提示（请谨慎使用）。

### 列出已下订单
```bash
python3 scripts/alpaca_cli.py orders
python3 scripts/alpaca_cli.py orders --status open
python3 scripts/alpaca_cli.py orders --status closed --limit 20
```

### 取消订单
```bash
python3 scripts/alpaca_cli.py cancel ORDER_ID
python3 scripts/alpaca_cli.py cancel all  # Cancel all open orders
```

### 获取新闻
```bash
python3 scripts/alpaca_cli.py news AAPL
python3 scripts/alpaca_cli.py news AAPL,TSLA --limit 5
```

### 关注列表
```bash
python3 scripts/alpaca_cli.py watchlist list
python3 scripts/alpaca_cli.py watchlist create "Tech Stocks" AAPL,MSFT,GOOGL
python3 scripts/alpaca_cli.py watchlist add WATCHLIST_ID NVDA
python3 scripts/alpaca_cli.py watchlist delete WATCHLIST_ID
```

### 实时数据流（WebSocket）
```bash
# Stream trades (default)
python3 scripts/alpaca_cli.py stream AAPL

# Stream quotes
python3 scripts/alpaca_cli.py stream AAPL,TSLA --type quotes

# Stream bars (1-min)
python3 scripts/alpaca_cli.py stream NVDA --type bars

# Stream all data types
python3 scripts/alpaca_cli.py stream AAPL --type all
```

按Ctrl+C停止数据流。

### 价格警报
```bash
# Add alert - notify when INTU drops below $399
python3 scripts/alpaca_cli.py alert add --symbol INTU --price 399 --condition below

# Add alert - notify when AAPL goes above $300
python3 scripts/alpaca_cli.py alert add --symbol AAPL --price 300 --condition above

# List active alerts
python3 scripts/alpaca_cli.py alert list

# Check alerts (used by cron)
python3 scripts/alpaca_cli.py alert check

# Remove an alert
python3 scripts/alpaca_cli.py alert remove --alert_id ABC123

# Clear all alerts
python3 scripts/alpaca_cli.py alert clear
```

警报信息存储在`~/.openclaw/data/alpaca-alerts.json`文件中。

## 脚本位置

所有命令均使用`scripts/alpaca_cli.py`脚本（相对于当前技能目录）。

## API参考

详细API文档和响应格式请参阅`references/api.md`。

## 安全提示

- 在进行实际交易前，请务必与用户确认
- 建议使用模拟交易（`ALPACA_PAPER=true`）进行测试
- 下大单前请检查资金是否充足
- 提交订单前请核实订单详情