---
name: alpaca-py-cli
description: >
  **AI代理技能：用于Alpaca Markets交易**  
  该AI代理具备智能设置向导（alpaca init），可引导用户完成注册流程。用户可通过自然语言指令进行股票/加密货币交易、管理投资组合以及执行交易订单。其设计注重高效利用资源（低Token消耗），并提供运行时指导。系统默认提供模拟交易功能（使用10万美元虚拟资金）。**重要提示：**设置过程中需要用户在shell环境中配置API密钥。
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3"],"packages":["alpaca-py","pytz"],"env":["ALPACA_API_KEY","ALPACA_SECRET_KEY","ALPACA_PAPER"]},"install":[{"id":"pip-alpaca","kind":"pip","package":"alpaca-py","label":"Install alpaca-py (pip3 install alpaca-py)"},{"id":"pip-pytz","kind":"pip","package":"pytz","label":"Install pytz (pip3 install pytz)"}],"setup":{"instructions":["USER must run: alpaca init (interactive setup - requires user input)","USER will be prompted to enter API keys manually","Keys are saved to shell config by the CLI (user consent required)","Test: alpaca clock"],"warnings":["Setup modifies shell startup files (~/.zshrc, ~/.bashrc, ~/.profile)","API keys will be stored as environment variables","User must provide explicit consent before running setup","Do not run setup autonomously - requires user interaction"]}}}
---
# Alpaca Trading (Python CLI) - OpenClaw 代理技能

[![ClawHub](https://img.shields.io/badge/ClawHub-alpaca--py--cli-blue)](https://clawhub.ai/skills/alpaca-py-cli)
[![GitHub](https://img.shields.io/badge/GitHub-zijunl%2Falpaca--py--cli-green)](https://github.com/zijunl/alpaca-py-cli)

通过基于 Python 的 CLI 工具，利用 Alpaca 的 API 进行股票和加密货币的程序化交易。

## ⚠️ 安全性与设置要求

**重要提示 - 使用前请阅读：**

此技能需要用户的交互式设置。**切勿自动运行设置命令**。

**设置过程中会发生什么：**
- `alpaca init` 会提示用户输入 API 密钥
- 密钥将保存到 shell 启动文件（`~/.zshrc`、`~/.bashrc` 或 `~/.profile`）
- 这会创建持久的环境变量，可供所有 shell 会话使用
- 在 CLI 写入 shell 配置之前，用户必须明确同意

**安全注意事项：**
- ✅ API 密钥以环境变量的形式存储（标准做法）
- ✅ 输入秘密密钥时会被隐藏
- 默认为模拟交易（虚拟资金，无风险）
- ⚠️ shell 配置中的密钥对该 shell 中的任何进程都是可访问的
- ⚠️ 如果代理具有 shell 访问权限，它可以读取环境变量
- ⚠️ 设置会修改用户的 shell 配置文件

**推荐做法：**
1. **手动运行设置** - 不要让代理自动运行 `alpaca init`
2. **使用模拟交易密钥** - 先用虚拟资金进行测试
3. **同意前先查看** - 了解哪些文件会被修改
4. **最小权限原则** - 使用具有最低必要权限的 API 密钥
5. **监控活动** - 定期检查你的 Alpaca 账户

**对于代理：**
- 未经用户明确许可，**不得运行 `alpaca init` 或 `alpaca auth`
- 通知用户设置会修改 shell 配置文件
- 解释 API 密钥将被保存为环境变量
- 在继续设置之前获取用户同意

**链接：**
- ClawHub: https://clawhub.ai/skills/alpaca-py-cli
- GitHub: https://github.com/zijunl/alpaca-py-cli
- Alpaca Markets: https://alpaca.markets




# Alpaca Trading (Python CLI)

[![ClawHub](https://img.shields.io/badge/ClawHub-alpaca--py--cli-blue)](https://clawhub.ai/skills/alpaca-py-cli)
[![GitHub](https://img.shields.io/badge/GitHub-zijunl%2Falpaca--py--cli-green)](https://github.com/zijunl/alpaca-py-cli)

通过基于 Python 的 CLI 工具，利用 Alpaca 的 API 进行股票和加密货币的程序化交易。

**链接：**
- ClawHub: https://clawhub.ai/skills/alpaca-py-cli
- GitHub: https://github.com/zijunl/alpaca-py-cli
- Alpaca Markets: https://alpaca.markets




## 概述

使用 `alpaca` CLI 工具和 Python SDK 管理你的 Alpaca Markets 交易账户。支持模拟交易（Paper Trading）和实时交易（Live Trading）。

## 安装

### 推荐：使用 Homebrew Python（避免 urllib3/LibreSSL 警告）

```bash
# Install Homebrew Python 3.11+
brew install python@3.11

# Install alpaca-py
/opt/homebrew/bin/pip3.11 install alpaca-py pytz
```

### 替代方案：系统自带的 Python

```bash
pip3 install alpaca-py pytz
```

**注意：**在 macOS 上，系统自带的 Python 可能会因 LibreSSL 兼容性问题而显示 urllib3 警告。建议使用 Homebrew Python 以获得更稳定的体验。

## 配置

### 使用 CLI 快速设置

```bash
alpaca auth
```

系统会交互式地提示你输入：
- API 密钥
- 秘密密钥（输入内容会被隐藏）
- 交易模式（模拟交易或实时交易）

命令会自动将你的凭据保存到 shell 配置文件（`~/.zshrc`、`~/.bashrc` 或 `~/.profile`）。

### 手动设置

或者，你也可以手动在 shell 配置文件中设置这些信息：

```bash
export ALPACA_API_KEY="your_api_key"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER="true"  # Use "false" for live trading
```

从 https://alpaca.markets 获取你的 API 密钥（控制面板 → API 密钥）

**模拟交易**（推荐用于测试）：
- 使用模拟交易 API 密钥
- 初始虚拟资金为 100,000 美元
- 无实际资金风险

**实时交易**（使用真实资金）：
- 使用实时交易 API 密钥
- 有实际资金风险
- 先用模拟交易彻底测试

## CLI 命令

### 设置与配置

#### 配置凭据

```bash
alpaca auth
```

交互式设置向导会引导你完成以下步骤：
1. 输入 API 密钥
2. 输入秘密密钥（输入内容会被隐藏）
3. 选择交易模式（模拟交易/实时交易）
4. 自动保存到 shell 配置文件

### 账户与市场信息

#### 检查账户

```bash
alpaca account
```

显示：
- 账户号码和状态
- 投资组合价值、现金、买入能力
- 盈亏（权益、最新权益）
- 交易限制（例如：每日交易限制）

#### 检查市场状态

```bash
alpaca clock
```

显示：
- 市场状态（🟢 开市中 或 🔴 关闭）
- 当前时间
- 下一次开盘/收盘时间

#### 查看市场日历

```bash
# Show next 30 trading days (default)
alpaca calendar

# Show next 7 trading days
alpaca calendar --days 7
```

显示交易日的开盘/收盘时间（东部时间）。

#### 查看投资组合历史

```bash
# Default: 1 month, daily bars
alpaca history

# Last week
alpaca history --period 1W

# Last 3 months with hourly bars
alpaca history --period 3M --timeframe 1H
```

**时间范围：** 1天、1周、1个月、3个月、1年
**时间帧：** 1分钟、5分钟、15分钟、1小时、1天

显示：
- 开始和结束时的权益
- 总变化额（美元和百分比）
- 最近的历史数据（最近10个数据点）

### 投资组合管理

#### 查看持仓

```bash
alpaca positions
```

显示所有当前持仓：
- 证券代码、数量、当前价格
- 入场价格和市场价格
- 未实现的盈亏（美元和百分比）
- 总投资组合价值和盈亏

#### 获取股票报价

```bash
# Single symbol
alpaca quote AAPL

# Multiple symbols
alpaca quote AAPL,TSLA,MSFT
```

显示：
- 买价和卖价
- 中间价和价差
- 报价时间戳

**注意：**在市场关闭期间，报价可能显示不完整的数据。建议在市场开放时间（东部时间上午9:30 - 下午4:00）使用此功能。

### 订单管理

#### 查看订单

```bash
# Show open orders (default)
alpaca orders

# Show all recent orders
alpaca orders --status all

# Show last 20 closed orders
alpaca orders --status closed --limit 20
```

显示：
- 订单状态（用表情符号表示：⏳ 待处理、✓ 已成交、✗ 已取消）
- 证券代码、方向（买入/卖出）、数量
- 订单 ID 和创建时间
- 成交价格（如果已成交）

#### 下单

```bash
# Buy shares
alpaca buy AAPL 10

# Sell shares
alpaca sell AAPL 5
```

在市场开放时，以市场价格下达市价单。

#### 取消订单

```bash
# Cancel specific order
alpaca cancel <order_id>

# Cancel all open orders
alpaca cancel-all
```

### 持仓管理

#### 关闭持仓

```bash
# Close specific position
alpaca close AAPL

# Close all positions (requires confirmation)
alpaca close-all
```

**注意：**`close-all` 命令在关闭所有持仓前会要求确认。

## 示例工作流程

### 首次设置

```bash
# Configure credentials
alpaca auth

# Check account
alpaca account

# Check if market is open
alpaca clock
```

### 交易工作流程

```bash
# Check current price
alpaca quote TSLA

# Check account balance
alpaca account

# Buy some shares
alpaca buy TSLA 5

# Check pending orders
alpaca orders

# View positions (after order fills)
alpaca positions

# Get updated quote
alpaca quote TSLA

# Sell some shares
alpaca sell TSLA 2

# Check order history
alpaca orders --status all
```

### 投资组合分析

```bash
# View current positions
alpaca positions

# View portfolio history
alpaca history --period 1M

# Check market calendar
alpaca calendar --days 7
```

### 风险管理

```bash
# Check all open orders
alpaca orders

# Cancel specific order
alpaca cancel <order_id>

# Cancel all orders
alpaca cancel-all

# Close specific position
alpaca close AAPL

# Close all positions
alpaca close-all
```

## 代理使用方法

当用户询问其投资组合或想要进行交易时：

1. **配置凭据**：运行 `alpaca auth` 进行首次设置
2. **检查市场状态**：运行 `alpaca clock` 以确认市场是否开放
3. **检查账户**：运行 `alpaca account` 以查看当前余额和买入能力
4. **查看持仓**：运行 `alpaca positions` 以列出当前持仓
5. **查看订单**：运行 `alpaca orders` 以查看待处理/最近的订单
6. **获取报价**：运行 `alpaca quote <证券代码>` 以查看当前价格
7. **下达订单**：运行 `alpaca buy/sell` 以执行交易
8. **管理风险**：根据需要运行 `alpaca cancel/close` 命令

## 安全提示

- **始终先使用模拟交易进行测试**（`ALPACA_PAPER=true`）
- 使用 `alpaca auth` 安全地配置凭据（秘密密钥会被隐藏）
- 在交易前运行 `alpaca clock` 以确认市场是否开放
- 在下达订单前查看报价以了解当前价格
- 在下达订单前查看 `account.buying_power` 以确保有足够的买入能力
- 使用 `TimeInForce.DAY` 在市场关闭时自动取消未成交的订单
- 定期使用 `alpaca positions` 监控持仓
- 使用 `alpaca orders` 查看订单状态
- 使用 `alpaca history` 查看投资组合表现
- 使用 `alpaca cancel-all` 快速取消所有待处理的订单
- 使用 `alpaca close-all` 时要谨慎（需要确认）
- 设置止损订单以管理风险
- 绝不要公开分享你的 API 密钥

## 市场时间

美国股市时间（东部时间）：
- **正常交易时间**：上午9:30 - 下午4:00
- **盘前时间**：上午4:00 - 上午9:30
- **盘后时间**：下午4:00 - 下午8:00

在市场关闭期间下达的订单将被排队，并在市场开放时执行。

在市场关闭期间，报价可能显示不完整或过时的数据。

使用 `alpaca clock` 来查看当前市场状态。

## 故障排除

### urllib3 警告（LibreSSL）

如果你遇到以下情况：
```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently using LibreSSL
```

**解决方案：**安装并使用 Homebrew Python 3.11+（它使用 OpenSSL）：
```bash
brew install python@3.11
/opt/homebrew/bin/pip3.11 install alpaca-py pytz
```

然后更新脚本的 shebang 以使用 Homebrew Python：
```bash
sed -i '' '1s|#!/usr/bin/env python3|#!/opt/homebrew/bin/python3.11|' ~/.openclaw/workspace/skills/alpaca-py-cli/scripts/alpaca
```

### 缺少 pytz

如果你遇到以下情况：
```
ModuleNotFoundError: No module named 'pytz'
```

**解决方案：**
```bash
pip3 install pytz
# or
/opt/homebrew/bin/pip3.11 install pytz
```

### 命令未找到

如果找不到 `alpaca` 命令，可以使用完整路径：
```bash
~/.openclaw/workspace/skills/alpaca-py-cli/scripts/alpaca
```

或者将路径添加到你的 shell 配置文件中：
```bash
export PATH="$HOME/.openclaw/workspace/skills/alpaca-py-cli/scripts:$PATH"
```

## 文件

- **CLI 工具**：`~/.openclaw/workspace/skills/alpaca-py-cli/scripts/alpaca`
- **配置文件**：环境变量位于 `~/.zshrc`（或 `~/.bashrc`、`~/.profile`）

## 官方文档

- Python SDK：https://alpaca.markets/docs/python-sdk/
- API 参考：https://docs.alpaca.markets/reference/
- 交易 API：https://docs.alpaca.markets/docs/trading-api
- 市场数据 API：https://docs.alpaca.markets/docs/market-data

## 初始化（对于代理）

### 使用 `alpaca init` 快速设置

当用户需要设置 Alpaca 交易时，只需运行：

```bash
alpaca init
```

**CLI 将：**
- 检查是否已配置
- 检测代理功能（电子邮件访问、浏览器自动化）
- 选择自动或手动设置模式
- 逐步引导用户完成注册流程
- 收集并保存 API 密钥
- 验证设置

**代理的角色：**
- 当用户想要开始交易时运行 `alpaca init`
- 让 CLI 处理所有的指导和提示
- 向导设计得非常直观易懂
- 完成设置后，使用 `alpaca clock` 进行验证

**示例：**
```
User: "I want to start trading stocks"
Agent: "I'll help you set up Alpaca paper trading (virtual money, no risk)."
       *runs: alpaca init*
       *follows the wizard's prompts*
Agent: "✓ Setup complete! You have $100,000 in paper money to practice with."
```

`init` 向导会处理所有复杂步骤——代理只需运行它并跟随提示即可。