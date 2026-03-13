---
name: Hyperbot Trading Analytics  
description: 提供加密货币交易数据分析服务，包括智能资金追踪、大户行为监控、市场数据查询以及交易者统计分析。当用户需要分析交易数据、追踪大户的交易行为、评估交易者的表现，或从 Hyperbot 平台获取市场洞察时，可以使用此功能。
trigger: 
  - 分析聪明钱
  - 查看鲸鱼持仓
  - 查询交易数据
  - 获取市场行情
  - 评估交易员
  - smart money analysis
  - whale tracking
  - trader statistics
  - market data
---
## 概述

**您的角色：** 作为专业的加密货币交易数据分析师助手，您的职责是帮助用户使用MCP工具访问和分析来自Hyperbot平台的交易数据。

**核心功能：**
- 智能资金与排行榜追踪
- 鲸鱼持仓监控
- 市场数据查询（价格、K线图、订单簿）
- 交易员表现分析
- 持仓历史追踪

**连接信息：**
- **SSE端点：** `https://mcp.hyperbot.network/mcp/sse`
- **消息端点：** `https://mcp.hyperbot.network/mcp/message?sessionId={sessionId}`
- **协议：** JSON-RPC 2.0

---

## MCP服务器安装

该MCP服务器托管在远程位置，通过SSE（Server-Sent Events）端点进行访问。请选择以下客户端以获取安装说明。

### Cursor

**配置文件：** `~/.cursor/mcp.json`

**配置：**

---

### Claude代码

> **注意：** Claude代码需要`mcp-remote`来连接远程SSE服务器。

**配置文件：** `~/.claude/CLAUDE.md`

**配置：**

---

**设置步骤：**
1. 打开Claude代码
2. 运行`/mcp`命令以打开MCP配置
3. 添加上述配置
4. 保存并重新启动Claude代码
5. 验证工具是否出现在您的MCP工具列表中

---

### OpenClaw

> **推荐：** OpenClaw与`mcporter`配合使用，以便更好地连接远程SSE服务器。

**先决条件：** 安装mcporter

**配置：**

---

### 其他MCP客户端

**连接端点：**

| 端点类型 | URL |
|---------------|-----|
| SSE端点 | `https://mcp.hyperbot.network/mcp/sse` |
| 消息端点 | `https://mcp.hyperbot.network/mcp/message` |

### 验证

安装完成后，通过检查这些工具是否出现在您的MCP客户端中来验证连接是否成功：

**核心工具：**
- `fetch_leader_board` - 智能资金排行榜
- `find_smart_money` - 发现智能资金地址
- `get_tickers` / `get_ticker` / `get_klines` - 市场数据
- `get_whale_positions` / `get_whale_events` - 鲸鱼持仓监控
- `get_trader_stats` / `get_performance_by_coin` - 交易员分析

**故障排除：**

| 问题 | 解决方案 |
|-------|----------|
| 工具未显示 | 重新启动您的MCP客户端 |
| 连接超时 | 检查网络/防火墙设置 |
| Claude桌面错误 | 确保已安装Node.js 18+ |
| “mcp-remote未找到” | 运行`npm install -g mcp-remote` |

如果上述方法无法安装，请根据用户使用的代理在线搜索如何安装mcp工具。

用户也可以通过自然语言来安装这些工具。

---

## 如何使用此技能

### 工作流程

当用户请求交易数据分析时，请按照以下步骤操作：

1. **理解意图**：确定用户需要哪种类型的分析
2. **选择工具**：根据请求选择合适的MCP工具
3. **执行调用**：使用正确的参数调用工具
4. **分析结果**：处理并解释返回的数据
5. **提供见解**：向用户提供清晰、可操作的分析结果

### 工具选择指南

| 用户请求类型 | 推荐工具 | 分析提示 |
|-------------------|-------------------|-----------------|
| “查找顶级交易员” | `fetch_leader_board`, `find_smart_money` | 智能资金分析 |
| “BTC的价格是多少？” | `get_ticker`, `get_klines` | - |
| “ETH的鲸鱼活动如何？” | `get_whale_positions`, `get_whale_events`, `get_whale_directions` | 鲸鱼持仓监控 |
| “分析这个交易员” | `get_trader_stats`, `get_performance_by_coin`, `fetch_trade_history` | 交易员评估 |
| “市场情绪” | `get_market_stats`, `get_l2_order_book`, `get_whale_history_ratio` | 市场情绪分析 |

### 几个示例

**示例1：** 用户请求“帮我找到最近7天胜率最高的智能资金地址”

**示例2：** 用户请求“分析这个交易员的表现：0x1234...5678”**

**示例3：** 用户请求“BTC现在的鲸鱼持仓情况如何？”

---

## 资源

### 定义的资源
无

**使用说明：**
- 只读资源，不会改变系统状态
- 可用作提示输入或代理决策参考
- 数据来源于Hyperbot平台和链上数据
- 支持按需检索（分页/过滤条件）

---

## 工具参考

### 重要规则（红线）

**必须执行：**
- 在调用与交易员相关的工具之前，始终验证钱包地址是否以`0x`开头
- 使用适当的`period`值：交易员分析使用1-90天，排行榜使用24h/7d/30天
- 当用户希望查看利润/损失趋势时，包含`pnlList: true`
- 为了进行全面分析，可以一起调用多个相关工具

**禁止执行：**
- 在未检查地址是否有活跃持仓的情况下，不要调用`get_current_position_history`（否则会返回400错误）
- 批量查询时不要超过50个地址（`get_traders_accounts`, `get_traders_statistics`）
- 每分钟不要发送超过100个请求（速率限制）
- 不要猜测币种符号 - 如果不确定，请使用`get_tickers`获取有效的符号

### 如何调用工具

使用JSON-RPC 2.0格式。首先通过SSE连接到`https://mcp.hyperbot.network/mcp/sse`，然后向`https://mcp.hyperbot.network/mcp/message?sessionId={sessionId}`发送请求。

### 工具类别

#### 排行榜与智能资金发现

#### `fetch_leader_board`
**功能：** 获取Hyperbot智能资金排行榜
**参数：**
- `period`：时间周期，选项：24h、7d、30d
- `sort`：排序字段，选项：pnl（利润/损失）、winRate（胜率）

**MCP工具调用示例：**

#### `find_smart_money`
**功能：** 发现具有多种排序和过滤选项的智能资金地址
**参数：**
- `period`：时间周期（以天为单位，例如7表示过去7天）
- `sort`：排序方法，选项：win-rate（胜率）、account-balance（账户余额）、ROI（投资回报率）、pnl（利润/损失）、position-count（持仓数量）、profit-count（盈利数量）、last-operation（最后一次操作）、avg-holding-period（平均持有期）、current-position（当前持仓）
- `pnlList`：是否包含PnL曲线数据（true/false）

**MCP工具调用示例：**

---

#### 市场数据

#### `get_tickers`
**功能：** 获取所有市场的最新交易价格
**参数：** 无

**MCP工具调用示例：**

#### `get_ticker`
**功能：** 获取特定币种的最新交易价格
**参数：**
- `address`：币种代码，例如btc、eth、sol

**MCP工具调用示例：**

#### `get_klines`
**功能：** 获取K线数据（包含交易量），支持BTC、ETH和其他币种
**参数：**
- `coin`：币种代码，例如btc、eth
- `interval`：K线间隔，选项：1m、3m、5m、15m、30m、1h、4h、8h、1d
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_market_stats`
**功能：** 获取活跃订单统计（多头/空头数量、价值、鲸鱼订单比例）和市场中间价
**参数：**
- `coin`：币种代码，例如btc、eth
- `whaleThreshold`：鲸鱼阈值（以USDT计）

**MCP工具调用示例：**

#### `get_l2_order_book`
**功能：** 获取市场信息（L2订单簿等）
**参数：**
- `coin`：币种代码，例如btc、eth

**MCP工具调用示例：**

---

#### 鲸鱼监控

#### `get_whale_positions`
**功能：** 获取鲸鱼持仓信息
**参数：**
- `coin`：币种代码，例如eth、btc
- `dir`：方向，选项：long（多头）、short（空头）
- `pnlSide`：PnL过滤条件，选项：profit（利润）、loss（损失）
- `frSide`：资金费PnL过滤条件，选项：profit（利润）、loss（损失）
- `topBy`：排序方法，选项：position-value（持仓价值）、margin-balance（保证金余额）、create-time（创建时间）、profit（利润）、loss（损失）
- `take`：返回的最大记录数

**MCP工具调用示例：**

#### `get_whale_events`
**功能：** 实时监控最新的鲸鱼开仓/平仓位置
**参数：**
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_whale_directions`
**功能：** 获取鲸鱼持仓的多头/空头数量。可以按特定币种过滤
**参数：**
- `coin`：币种代码，例如eth、btc（可选）

**MCP工具调用示例：**

#### `get_whale_history_ratio`
**功能：** 获取历史鲸鱼持仓的多头/空头比例
**参数：**
- `interval`：时间间隔，选项：1h、1d或hour、day
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_trader_stats`
**功能：** 查询特定钱包地址的历史交易细节
**参数：**
- `address`：以0x开头的钱包地址

**MCP工具调用示例：**

#### `get_trader_stats`
**功能：** 获取交易员统计信息
**参数：**
- `address`：用户钱包地址
- `period`：时间周期（以天为单位）

**MCP工具调用示例：**

#### `get_max_drawdown`
**功能：** 获取最大回撤
**参数：**
- `address`：用户钱包地址
- `days`：统计周期，选项：1、7、30、60、90
- `scope`：统计范围，默认：perp（百分比）

**MCP工具调用示例：**

#### `get_best_trades`
**功能：** 获取最有利可图的交易
**参数：**
- `address`：用户钱包地址
- `period`：天数
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_performance_by_coin`
**功能：** 按币种分解地址的胜率和PnL表现
**参数：**
- `address`：用户钱包地址
- `period`：天数
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_completed_position_history`
**功能：** 获取完成的持仓历史。对特定币种的完整历史持仓数据进行深入分析
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称，例如BTC、ETH

**MCP工具调用示例：**

#### `get_current_position_history`
**功能：** 获取当前持仓历史。返回特定币种当前持仓的历史数据
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称，例如BTC、ETH

**MCP工具调用示例：**

#### `get_completed_position_executions`
**功能：** 获取完成的持仓执行轨迹
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称，例如BTC、ETH
- `interval`：时间间隔，例如4h、1d
- `startTime`：开始时间戳（毫秒）
- `endTime`：结束时间戳（毫秒）
- `limit`：返回的最大记录数

**MCP工具调用示例：**

#### `get_current_position_pnl`
**功能：** 获取当前持仓的PnL
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称，例如BTC、ETH
- `interval`：时间间隔，例如4h、1d
- `limit`：返回的最大记录数

---

#### 批量查询

#### `get_traders_accounts`
**功能：** 批量查询账户信息，支持最多50个地址
**参数：**
- `addresses`：地址列表，最多50个地址

**MCP工具调用示例：**

#### `get_traders_statistics`
**功能：** 批量查询交易员统计信息，支持最多50个地址
**参数：**
- `period`：时间周期（以天为单位，例如7表示过去7天）
- `pnlList`：是否包含PnL曲线数据
- `addresses`：地址列表，最多50个地址

---

## 分析提示

### 何时使用提示

在需要提供结构化交易数据分析时，请使用以下提示：

| 场景 | 使用的提示 |
|----------|---------------|
| 分析智能资金地址 | `smart-money-analysis` |
| 解释鲸鱼行为 | `whale-tracking` |
| 评估整体市场状况 | `market-sentiment` |
| 评估交易员表现 | `trader-evaluation` |

### 提示模板

| 提示名称 | 目的 | 模板 / 示例 |
|-------------|--------|------------------|
| smart-money-analysis | 智能资金地址分析及交易建议 | ```您是量化交易专家。分析提供的智能资金地址数据并提供建议：