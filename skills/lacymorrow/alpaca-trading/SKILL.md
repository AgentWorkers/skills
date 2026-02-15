---
name: alpaca-trading
description: 使用 apcacli 命令行工具，通过 Alpaca 的交易 API 来执行交易、分析市场并管理投资组合。当用户需要买卖股票、ETF、期权、加密货币，查看市场数据、管理订单或分析其投资组合时，可以使用该工具。此外，在用户提到“买入”、“卖出”、“交易”、“市场数据”、“股票价格”、“投资组合”、“账户余额”或“Alpaca 交易”等相关术语时，也请使用此工具。
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      bins: ["apcacli"]
      env: ["APCA_API_KEY_ID", "APCA_API_SECRET_KEY"]
    homepage: "https://github.com/d-e-s-o/apcacli"
---

# Alpaca交易技巧

通过`apcacli`命令行工具执行交易并管理投资组合，该工具用于Alpaca的交易API。

## 概述

您是使用`apcacli`进行命令行股票交易的专家。您的目标是通过Alpaca的API帮助用户高效地交易股票、ETF、期权和加密货币，同时强调安全性和最佳实践。

## 如何使用此技巧

在帮助用户进行交易任务时：

1. **安全第一**：始终建议新用户或在进行测试时使用模拟交易。
2. **验证命令**：在执行交易前展示确切的命令。
3. **检查前提条件**：确认市场开放时间、账户余额和有效的交易符号。
4. **解释订单类型**：帮助用户根据需求选择正确的订单类型。
5. **风险管理**：建议设置止损和调整头寸规模。

---

## 该技巧的功能

`apcacli`是一个基于Rust的命令行工具，用于与Alpaca的交易平台交互。它提供以下功能：
- **交易**：提交、修改和取消股票、ETF、期权和加密货币的订单。
- **投资组合管理**：查看头寸、盈亏和账户信息。
- **市场数据**：获取资产信息和市场时钟状态。
- **账户活动**：追踪交易历史和账户变化。
- **实时流式更新**：监控账户和交易事件。

## 何时使用此技巧

当用户希望执行以下操作时，请使用此技巧：
- 执行交易（买入/卖出股票、ETF、期权、加密货币）
- 查看投资组合头寸和表现
- 查看或管理订单（未成交、已成交、已取消）
- 获取账户余额和可用资金
- 获取市场数据和资产信息
- 监控账户活动和事件
- 检查市场是否开放
- 设置止损或追踪止损
- 使用脚本自动化交易流程

**常用指令示例**：
- “买入10股AAPL”
- “显示我的未成交订单”
- “我的账户余额是多少？”
- “列出我所有的订单”
- “取消订单[ID]”
- “市场是否开放？”
- “显示我的投资组合表现”
- “为我的头寸设置止损”
- “关闭我所有的头寸”

**何时不使用此技巧**：
- 用户希望使用基于图形界面的交易方式（引导他们使用Web界面）。
- 用户请求财务建议（您提供工具，而非建议）。
- 用户想要交易Alpaca不支持的证券。
- 用户未安装`apcacli`（请先帮助他们安装）。

## 安装与设置

### 安装`apcacli`

```bash
# Using Cargo (Rust package manager)
cargo install apcacli

# Verify installation
apcacli --help
```

**要求**：
- Rust 1.71或更高版本
- Alpaca账户（模拟交易或真实交易）
- Alpaca API凭证

### 配置环境变量

**用于模拟交易（推荐用于测试）：**
```bash
export APCA_API_KEY_ID='your_paper_key_id'
export APCA_API_SECRET_KEY='your_paper_secret_key'
# Paper trading is the default, no need to set APCA_API_BASE_URL
```

**用于真实交易：**
```bash
export APCA_API_BASE_URL='https://api.alpaca.markets'
export APCA_API_KEY_ID='your_live_key_id'
export APCA_API_SECRET_KEY='your_live_secret_key'
```

**获取API凭证**：
1. 在https://alpaca.markets/注册。
2. 进入您的仪表板。
3. 生成API密钥（模拟交易或真实交易）。
4. 导出环境变量。

## 核心命令

### 账户信息

**查看账户详情**：
```bash
apcacli account get
```
显示账户状态、现金余额、可用资金、资产净值和保证金信息。

**查看账户活动**：
```bash
apcacli account activity
```
显示最近的账户活动，包括交易、股息和转账记录。

**更新账户设置**：
```bash
apcacli account config <options>
```
修改账户设置（使用`--help`查看可用选项）。

### 订单管理

**提交市价单**：
```bash
# Buy with dollar amount
apcacli order submit buy AAPL --value 1000

# Buy specific quantity
apcacli order submit buy AAPL --quantity 10

# Sell shares
apcacli order submit sell TSLA --quantity 5
```

**提交限价单**：
```bash
# Buy at specific price
apcacli order submit buy MSFT --quantity 10 --limit-price 420

# Sell at specific price
apcacli order submit sell NVDA --quantity 20 --limit-price 850
```

**提交高级订单**：
```bash
# Stop order
apcacli order submit sell AAPL --quantity 10 --stop-price 180

# Stop-limit order
apcacli order submit sell TSLA --quantity 5 --stop-price 800 --limit-price 795

# Trailing stop order (percentage)
apcacli order submit sell NVDA --quantity 10 --trail-percent 5
```

**列出所有订单**：
```bash
apcacli order list
```
显示所有订单及其状态（未成交、已成交、已取消等）。

**获取特定订单详情**：
```bash
apcacli order get <ORDER_ID>
```
显示详细的订单信息，包括时间戳、价格和状态。

**取消订单**：
```bash
apcacli order cancel <ORDER_ID>
```
通过订单ID取消待处理的订单。

**取消所有订单**：
```bash
apcacli order cancel-all
```
取消所有未成交的订单。

### 头寸管理

**列出所有未成交的头寸**：
```bash
apcacli position list
```
显示所有未成交的头寸，包括：
- 数量和入场价格
- 当前市场价值
- 日盈亏（百分比）
- 总盈亏（百分比）
- 用颜色编码显示盈利/亏损

**获取特定头寸信息**：
```bash
apcacli position get <SYMBOL>
```
显示特定头寸的详细信息。

**关闭头寸**：
```bash
# Close entire position
apcacli position close <SYMBOL>

# Close partial position
apcacli position close <SYMBOL> --quantity 5
```
关闭所有未成交的头寸。

**关闭所有头寸**：
```bash
apcacli position close-all
```
关闭所有未成交的头寸。

### 资产信息

**列出可用资产**：
```bash
apcacli asset list
```
显示所有可交易的资产。

**获取资产详情**：
```bash
apcacli asset get <SYMBOL>
```
显示资产信息，包括交易所、类别和可交易状态。

**搜索资产**：
```bash
apcacli asset search <QUERY>
```
搜索符合查询条件的资产。

### 市场数据

**查看市场状态**：
```bash
apcacli market clock
```
显示当前市场状态（开放/关闭）、下一个开盘时间和下一个收盘时间。

### 流式更新（实时事件）

**流式更新账户信息**：
```bash
apcacli stream account
```
监控实时账户事件，包括订单更新和成交情况。

**流式更新交易信息**：
```bash
apcacli stream trades
```
监控您头寸的实时交易事件。

## 最佳实践

### 安全与风险管理

1. **从模拟交易开始** - 始终先用模拟交易测试策略。
2. **使用限价单** - 在市场波动时避免使用市价单以更好地控制价格。
3. **验证交易符号** - 在执行交易前仔细核对股票代码。
4. **执行前审核** - 使用`apcacli order get`验证订单详情。
5. **设置止损** - 用止损单保护头寸。
6. **检查账户余额** - 在交易前确保有足够的可用资金。
7. **定期监控头寸** - 使用`apcacli position list`定期查看盈亏。

### 有效使用方法

1. **查看命令帮助** - 使用`apcacli <命令> --help`获取详细选项。
2. **保存订单ID** - 存储返回的订单ID以便后续跟踪和管理。
3. **使用环境变量** - 将凭证安全地保存在环境变量中，切勿硬编码。
4. **检查市场开放时间** - 在下订单前使用`apcacli market clock`确认市场状态。
5. **定期审查活动** - 监控账户活动以发现意外变化。

### 常见工作流程

**简单股票购买**：
```bash
# 1. Check account balance
apcacli account get

# 2. Verify asset is tradeable
apcacli asset get AAPL

# 3. Check market is open
apcacli market clock

# 4. Submit market order
apcacli order submit buy AAPL --value 1000

# 5. Verify position
apcacli position list
```

**带监控的限价单**：
```bash
# 1. Submit limit order
apcacli order submit buy MSFT --quantity 10 --limit-price 420

# 2. Save the returned ORDER_ID
# 3. Check order status
apcacli order get <ORDER_ID>

# 4. If needed, cancel
apcacli order cancel <ORDER_ID>
```

**投资组合审查**：
```bash
# 1. View all positions
apcacli position list

# 2. Check account summary
apcacli account get

# 3. Review recent activity
apcacli account activity
```

**设置止损关闭头寸**：
```bash
# 1. Check current position
apcacli position get AAPL

# 2. Set trailing stop to protect profits
apcacli order submit sell AAPL --quantity 10 --trail-percent 5

# 3. Monitor the order
apcacli order list
```

## 命令参考快速指南

| 任务 | 命令 |
|------|---------|
| 查看账户 | `apcacli account get` |
| 账户活动 | `apcacli account activity` |
| 买入股票（市价） | `apcacli order submit buy SYMBOL --value AMOUNT` |
| 买入股票（限价） | `apcacli order submit buy SYMBOL --quantity N --limit-price PRICE` |
| 卖出股票 | `apcacli order submit sell SYMBOL --quantity N` |
| 列出所有订单 | `apcacli order list` |
| 获取订单详情 | `apcacli order get ORDER_ID` |
| 取消订单 | `apcacli order cancel ORDER_ID` |
| 取消所有订单 | `apcacli order cancel-all` |
| 列出头寸 | `apcacli position list` |
| 获取头寸信息 | `apcacli position get SYMBOL` |
| 关闭头寸 | `apcacli position close SYMBOL` |
| 关闭所有头寸 | `apcacli position close-all` |
| 列出资产 | `apcacli asset list` |
| 获取资产信息 | `apcacli asset get SYMBOL` |
| 查看市场状态 | `apcacli market clock` |
| 流式更新账户事件 | `apcacli stream account` |
| 流式更新交易 | `apcacli stream trades` |

## 订单类型及参数

### 基本订单参数

- `--quantity N` - 要交易的股票数量
- `--value AMOUNT` - 投资金额（市价单）
- `--limit-price PRICE` - 限价单的限价
- `--stop-price PRICE` - 止损单的止损价
- `--trail-percent N` - 追踪止损的百分比
- `--trail-amount AMOUNT` - 追踪止损的金额

### 订单类型

**市价单** - 立即在当前市场价格执行
```bash
apcacli order submit buy AAPL --quantity 10
```

**限价单** - 仅在指定价格或更优价格时执行
```bash
apcacli order submit buy AAPL --quantity 10 --limit-price 185
```

**止损单** - 当达到止损价时转换为市价单
```bash
apcacli order submit sell AAPL --quantity 10 --stop-price 180
```

**止损-限价单** - 当达到止损价时转换为限价单
```bash
apcacli order submit sell AAPL --quantity 10 --stop-price 180 --limit-price 179
```

**追踪止损** - 止损价根据指定百分比或金额跟随市场变动
```bash
# Percentage-based
apcacli order submit sell AAPL --quantity 10 --trail-percent 5

# Dollar-based
apcacli order submit sell AAPL --quantity 10 --trail-amount 10
```

## 重要注意事项

### 要求

- **必须安装`apcacli`二进制文件** - 通过`cargo install apcacli`安装。
- **必须设置环境变量** - 需要`APCA_API_KEY_ID`和`APCA_API_SECRET_KEY`。
- **Alpaca账户** - 活跃的模拟交易或真实交易账户。
- **Rust 1.71+** - 从源代码安装需要此版本。

### 交易限制

- **模拟交易与真实交易**：默认为模拟交易；如需真实交易，请设置`APCA_API_BASE_URL`。
- **市场开放时间**：大多数交易仅在市场开放时间（美国东部时间上午9:30 - 下午4:00）进行。
- **PDT模式交易**：账户余额低于25,000美元的用户受PDT限制。
- **可用资金**：受账户资产净值和保证金要求限制。
- **订单限制**：某些订单类型可能不适用于所有证券。
- **加密货币交易**：可能有不同的规则和交易时间。

### 数据与性能

- **API请求限制**：Alpaca有请求次数限制以防止滥用。
- **实时数据**：可能需要订阅实时数据服务。
- **命令输出**：结果以颜色编码格式显示以便于阅读。
- **订单ID**：保存返回的订单ID以便跟踪和管理。
- **网络依赖**：需要连接到Alpaca的API。

## 故障排除

### 环境变量未设置
```bash
# Error: "Missing APCA_API_KEY_ID"
# Solution: Export required environment variables
export APCA_API_KEY_ID='your_key'
export APCA_API_SECRET_KEY='your_secret'
```

### 命令未找到
```bash
# Error: "apcacli: command not found"
# Solution: Install apcacli
cargo install apcacli

# Verify installation
which apcacli
```

### API认证失败
- 确认API凭证正确。
- 检查是否使用了正确的端点（模拟交易或真实交易）。
- 确认API密钥未被撤销。
- 确认账户状态是否活跃。

### 订单被拒绝
- 确认市场是否开放（对于股票）。
- 检查是否有足够的可用资金。
- 确认交易符号是否有效且可交易。
- 检查订单参数（价格、数量）。
- 检查是否有任何账户限制。

### 头寸未找到
- 确认交易符号是否正确。
- 确认头寸确实存在。
- 检查头寸是否已被关闭。
- 确认使用的账户是否正确（模拟交易或真实交易）。

## 高级功能

### Shell自动补全

生成Shell自动补全功能，以便更快输入命令：
```bash
# Install completion script
cargo run --bin=shell-complete > apcacli.bash
source apcacli.bash

# Now you can use tab completion
apcacli order <TAB>
```

### 实时监控

使用流式命令实时监控账户活动：
```bash
# Terminal 1: Monitor account events
apcacli stream account

# Terminal 2: Execute trades
apcacli order submit buy AAPL --value 1000
# Watch the fill notification appear in Terminal 1
```

### 脚本与自动化

将`apcacli`与Shell脚本结合使用，实现自动化交易策略：
```bash
#!/bin/bash
# Example: Daily portfolio check script

echo "=== Daily Portfolio Report ==="
echo ""
echo "Account Status:"
apcacli account get
echo ""
echo "Open Positions:"
apcacli position list
echo ""
echo "Recent Activity:"
apcacli account activity
```

## 额外资源

- **apcacli仓库**：https://github.com/d-e-s-o/apcacli
- **Alpaca文档**：https://docs.alpaca.markets/
- **Alpaca API参考**：https://docs.alpaca.markets/reference/
- **模拟交易仪表板**：https://app.alpaca.markets/paper/dashboard/overview
- **apca crate（基础库）**：https://github.com/d-e-s-o/apca

## 安全提醒

⚠️ **重要**：
- 始终从**模拟交易**开始，以无风险的方式进行测试。
- 在执行前仔细查看所有订单详情。
- 绝不要分享您的API凭证。
- 使用限价单以更好地控制价格。
- 设置止损以管理风险。
- 确认环境变量设置正确（模拟交易与真实交易）。
- 仔细核对交易符号和数量。
- 定期监控头寸。

## 致谢

`apcacli`由d-e-s-o创建。

该工具基于`apca` Rust库开发，用于与Alpaca API进行交互。