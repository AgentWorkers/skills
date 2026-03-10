---
name: Hyperbot Trading Analytics  
description: 为Hyperbot平台提供交易数据分析功能，包括智能资金追踪、大户行为监控、市场数据查询以及交易者统计分析。适用于进行市场分析和决策制定的加密货币交易者。
---
## 1. 概述

**MCP服务器技能文档**

**版本：** 1.0.0  

### 代理快速入门

该MCP服务器提供加密货币交易分析工具。要使用这些工具，请按照以下步骤操作：

1. **通过SSE连接：** `https://mcp.hyperbot.network/mcp/sse`
2. **发送请求至：** `https://mcp.hyperbot.network/mcp/message?sessionId={your-session-id}`
3. **协议：** JSON-RPC 2.0

**可用工具类别：**
- **智能资金与排行榜：** `fetch_leader_board`, `find_smart_money`
- **市场数据：** `get_tickers`, `get_ticker`, `get_klines`, `get_market_stats`, `get_l2_order_book`
- **鲸鱼交易者监控：** `get_whale_positions`, `get_whale_events`, `get_whale_directions`, `get_whale_history_ratio`
- **交易者分析：** `fetch_trade_history`, `get_trader_stats`, `get_max_drawdown`, `get_best_trades`, `get_performance_by_coin`
- **持仓历史：** `get_completed_position_history`, `get_current_position_history`, `get_completed_position_executions`, `get_current_position_pnl`
- **批量查询：** `get_traders_accounts`, `get_traders_statistics`

---

## 2. MCP服务器安装

### 2.1 对于Cursor用户

在您的Cursor MCP设置中添加以下配置：

**方法1：通过UI**
- 打开`Cursor Settings` → `Tools & MCP` → `Add New MCP Server`
- 名称：`hyperbot-trading`
- 类型：`sse`
- URL：`https://mcp.hyperbot.network/mcp/sse`

**方法2：直接编辑配置文件**

编辑`~/.cursor/mcp.json`：

**配置完成后：** 重启Cursor以应用更改。

---

### 2.2 对于Claude Desktop用户

> **重要提示：** Claude Desktop需要`mcp-remote`来连接远程SSE服务器。请确保已安装Node.js。

**配置文件位置：**
- **macOS：** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows：** `%APPDATA%\Claude\claude_desktop_config.json`

**配置内容：**

**设置步骤：**
1. 打开Claude Desktop → Settings → Developer → Edit Config
2. 添加上述配置
3. 保存并重启Claude Desktop（Cmd/Ctrl + R）
4. 验证工具是否出现在您的MCP工具列表中

**前提条件：** 必须安装Node.js 18+。安装方式如下：
- macOS：`brew install node`
- Windows：从https://nodejs.org/下载`

---

### 2.3 对于OpenClaw用户

在您的OpenClaw MCP设置中添加以下配置：

**方法1：通过UI**
- 打开Settings → MCP → Add Server
- 名称：`hyperbot-trading`
- URL：`https://mcp.hyperbot.network/mcp/sse`

**方法2：编辑配置文件**

**配置完成后：** 重启OpenClaw以应用更改。

---

### 2.4 对于Linux用户

**配置文件位置：**

| 客户端 | 配置文件路径 |
|--------|-------------|
| Cursor | `~/.cursor/mcp.json` |
| Claude Desktop (AppImage) | `~/.config/Claude/claude_desktop_config.json` |
| Claude Desktop (Snap) | `~/.local/share/Claude/claude_desktop_config.json` |

**快速设置 - Linux上的Cursor：**

**快速设置 - Linux上的Claude Desktop：**

---

### 2.5 其他MCP客户端

**连接端点：**

| 端点类型 | URL |
|---------------|-----|
| SSE端点 | `https://mcp.hyperbot.network/mcp/sse` |
| Message端点 | `https://mcp.hyperbot.network/mcp/message` |

**对于支持直接SSE URL的客户端：**

**对于需要mcp-remote的客户端（如Claude Desktop）：**

---

### 2.6 验证

安装完成后，通过检查MCP客户端中是否包含以下工具来验证连接是否成功：

**核心工具：**
- `fetch_leader_board` - 智能资金排行榜
- `find_smart_money` - 发现智能资金地址
- `get_tickers` / `get_ticker` / `get_klines` - 市场数据
- `get_whale_positions` / `get_whale_events` - 鲸鱼交易者监控
- `get_trader_stats` / `get_performance_by_coin` - 交易者分析

**故障排除：**

| 问题 | 解决方案 |
|-------|----------|
| 工具未显示 | 重启您的MCP客户端 |
| 连接超时 | 检查网络/防火墙设置 |
| Claude Desktop错误 | 确保已安装Node.js 18+ |
| “mcp-remote未找到” | 运行`npm install -g mcp-remote` |

---

## 3. 资源

### 3.1 定义的资源
无

**使用说明：**
- 仅用于读取的资源，不会改变系统状态
- 可用作提示输入或代理决策参考
- 数据来源于Hyperbot平台和链上数据
- 支持按需检索（分页/过滤条件）

---

## 4. 工具

> **如何调用工具：** 使用JSON-RPC 2.0格式。首先通过SSE连接到`https://mcp.hyperbot.network/mcp/sse`获取sessionId，然后向`https://mcp.hyperbot.network/mcp/message?sessionId={sessionId}`发送请求。

### 4.1 排行榜与智能资金发现

#### `fetch_leader_board`
**功能：** 获取Hyperbot智能资金排行榜  
**参数：**
- `period`：时间周期（选项：24小时、7天、30天）
- `sort`：排序字段（选项：pnl（利润/亏损）、winRate（胜率）  

**MCP工具调用示例：**
---

#### `find_smart_money`
**功能：** 发现具有多种排序和过滤选项的智能资金地址  
**参数：**
- `period`：时间周期（例如，7表示过去7天）
- `sort`：排序方式（选项：win-rate、account-balance、ROI、pnl、position-count、profit-count、last-operation、avg-holding-period、current-position）
- `pnlList`：是否包含PnL曲线数据（true/false）  

**MCP工具调用示例：**
---

### 4.2 市场数据

#### `get_tickers`
**功能：** 获取所有市场的最新交易价格  
**参数：** 无  

**MCP工具调用示例：**
---

#### `get_ticker`
**功能：** 获取特定币种的最新交易价格  
**参数：**
- `address`：币种代码（例如，btc、eth、sol）  

**MCP工具调用示例：**
---

#### `get_klines`
**功能：** 获取K线数据（包含交易量），支持BTC、ETH等币种  
**参数：**
- `coin`：币种代码（例如，btc、eth）
- `interval`：K线间隔（选项：1分钟、3分钟、5分钟、15分钟、30分钟、1小时、4小时、8小时、1天）
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

#### `get_market_stats`
**功能：** 获取活跃订单统计（多头/空头数量、价值、鲸鱼订单比例）和市场中间价  
**参数：**
- `coin`：币种代码（例如，btc、eth）
- `whaleThreshold`：鲸鱼交易者的阈值（以USDT计）  

**MCP工具调用示例：**
---

#### `get_l2_order_book`
**功能：** 获取市场信息（L2订单簿等）  
**参数：**
- `coin`：币种代码（例如，btc、eth）  

**MCP工具调用示例：**
---

### 4.3 鲸鱼交易者监控

#### `get_whale_positions`
**功能：** 获取鲸鱼交易者的持仓信息  
**参数：**
- `coin`：币种代码（例如，eth、btc）
- `dir`：方向（选项：多头、空头）
- `pnlSide`：PnL过滤条件（选项：利润、亏损）
- `frSide`：资金费PnL过滤条件（选项：利润、亏损）
- `topBy`：排序方式（选项：持仓价值、保证金余额、创建时间、利润、亏损）
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

#### `get_whale_events`
**功能：** 实时监控最新的鲸鱼交易者开仓/平仓位置  
**参数：**
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

#### `get_whale_directions`
**功能：** 获取鲸鱼交易者的多头/空头数量。可以按特定币种过滤  
**参数：**
- `coin`：币种代码（例如，eth、btc）  

**MCP工具调用示例：**
---

#### `get_whale_history_ratio`
**功能：** 获取历史鲸鱼交易者多头/空头比例  
**参数：**
- `interval`：时间间隔（选项：1小时、1天或小时、天）
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

### 4.4 交易者分析

#### `fetch_trade_history`
**功能：** 查询特定钱包地址的历史交易详情  
**参数：**
- `address`：以0x开头的钱包地址  

**MCP工具调用示例：**
---

#### `get_trader_stats`
**功能：** 获取交易者统计信息  
**参数：**
- `address`：用户钱包地址
- `period`：时间周期（以天为单位）  

**MCP工具调用示例：**
---

#### `get_max_drawdown`
**功能：** 获取最大回撤幅度  
**参数：**
- `address`：用户钱包地址
- `days`：统计周期（选项：1天、7天、30天、60天、90天）
- `scope`：统计范围（默认：perp）  

**MCP工具调用示例：**
---

#### `get_best_trades`
**功能：** 获取最有利可图的交易  
**参数：**
- `address`：用户钱包地址
- `period`：时间周期
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

#### `get_performance_by_coin`
**功能：** 按币种分解地址的胜率和PnL表现  
**参数：**
- `address`：用户钱包地址
- `period`：时间周期
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

### 4.5 持仓历史

#### `get_completed_position_history`
**功能：** 获取完成的持仓历史。深入分析特定币种的历史持仓数据  
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称（例如，BTC、ETH）  

**MCP工具调用示例：**
---

#### `get_current_position_history`
**功能：** 获取当前持仓历史。返回特定币种当前持仓的历史数据  
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称（例如，BTC、ETH）  

**MCP工具调用示例：**
---

#### `get_completed_position_executions`
**功能：** 获取完成的持仓执行轨迹  
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称（例如，BTC、ETH）
- `interval`：时间间隔（例如，4小时、1天）
- `startTime`：开始时间戳（毫秒）
- `endTime`：结束时间戳（毫秒）
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

#### `get_current_position_pnl`
**功能：** 获取当前持仓的PnL  
**参数：**
- `address`：用户钱包地址
- `coin`：币种名称（例如，BTC、ETH）
- `interval`：时间间隔（例如，4小时、1天）
- `limit`：返回的最大记录数  

**MCP工具调用示例：**
---

### 4.6 批量查询

#### `get_traders_accounts`
**功能：** 批量查询账户信息，支持最多50个地址  
**参数：**
- `addresses`：地址列表（最多50个地址）  

**MCP工具调用示例：**
---

#### `get_traders_statistics`
**功能：** 批量查询交易者统计信息，支持最多50个地址  
**参数：**
- `period`：时间周期（例如，7表示过去7天）
- `pnlList`：是否包含PnL曲线数据
- `addresses`：地址列表（最多50个地址）  

**MCP工具调用示例：**
---

## 5. 提示

| 提示名称 | 目的 | 模板 / 示例 |
|-------------|--------|------------------|
| smart-money-analysis | 智能资金地址分析与交易建议 | ```您是一位量化交易专家。分析提供的智能资金地址数据并提供可操作的见解：  
**输入数据结构：**  
- 包含胜率、PnL、ROI、交易次数的地址列表  
- 持仓数据和交易历史  
- 按时间周期划分的性能指标  

**分析要求：**  
1. **高胜率地址特征**：识别常见模式（交易频率、持仓规模、币种偏好）  
2. **交易风格分类**：根据持有周期将其分类为 scalper（短线交易者）、swing trader（波段交易者）或 position trader（长期交易者）  
3. **风险评估**：分析最大回撤幅度、持仓集中度、杠杆使用情况  
4. **复制交易策略**：提供具体建议，包括：  
   - 根据风险承受能力选择跟随的地址  
   - 持仓规模建议  
   - 入场/出场时机指导  
   - 风险管理规则  

**输出格式（JSON）：**  
```json  
{
  "topAddresses": [{"address": "...", "winRate": "...", "style": "...", "riskLevel": "..."}],  
  "patterns": {"commonTraits": [...], "avoidTraits": [...]},  
  "recommendations": {"followList": [...], "positionSizing": "...", "riskRules": [...]}  
}  
```  

| whale-tracking | 鲸鱼行为分析与市场影响评估 | ```您是一位市场情报分析师，专门研究鲸鱼交易者的行为。分析提供的鲸鱼数据并评估市场影响：  
**输入数据结构：**  
- 鲸鱼交易者的持仓数据（规模、方向、PnL）  
- 最近的鲸鱼交易事件（开仓/平仓位置）  
- 历史多头/空头比例趋势  
- 当前价格附近的订单簿深度  

**分析要求：**  
1. **鲸鱼持仓分析**：  
   - 当前的多头/空头分布  
   - 持仓集中度（按币种）  
   - 主要持仓的利润/亏损状态  
2. **意图解读**：  
   - 识别积累与分散模式  
   - 检测潜在的市场操纵信号  
   - 根据持仓规模判断信心水平  
3. **市场影响预测**：  
   - 短期价格压力评估（1-24小时）  
   - 对订单簿的流动性影响  
   - 如果鲸鱼交易者退出可能产生的连锁效应  
4. **交易建议**：  
   - 根据鲸鱼交易者的动向确定最佳入场/出场时机  
   - 需要的风险管理调整  
   - 需关注的币种  

**输出格式（JSON）：**  
```json  
{
  "whaleSummary": {"totalPositions": "...", "longShortRatio": "...", "avgPositionSize": "..."},  
  "intentAnalysis": {"dominantSentiment": "...", "keyPatterns": [...]},  
  "marketImpact": {"shortTerm": "...", "liquidityRisk": "..."},  
  "recommendations": {"action": "...", "targetCoins": "...", "riskLevel": "..."}  
}  
```  

| market-sentiment | 市场情绪分析 | ```您是一位市场情绪分析师。分析提供的市场数据以确定整体市场状况：  
**输入数据结构：**  
- 订单簿深度（买卖订单、价差、不平衡）  
- 活跃订单统计（多头/空头比例、鲸鱼订单百分比）  
- 最近的价格走势和成交量  
- 鲸鱼交易者的历史多头/空头趋势  

**分析要求：**  
1. **情绪分类**：  
   - 分类为极度恐惧、恐惧、中性、贪婪或极度贪婪  
   - 提供信心评分（0-100%）  
   - 识别情绪趋势（改善/恶化）  
2. **技术层面**：  
   - 关键支撑和阻力水平及其强度  
   - 需关注的关键价格区间  
3. **市场结构分析**：  
   - 订单簿不平衡解读  
   - 鲸鱼交易者与散户情绪的差异  
   - 流动性集中区域  
4. **趋势预测**：  
   - 短期趋势预测（未来4-24小时）  
   - 可能改变情绪的关键催化剂  
   - 需监控的风险事件  

**输出格式（JSON）：**  
```json  
{
  "sentiment": {"classification": "...", "score": "...", "trend": "..."},  
  "keyLevels": {"support": "...", "resistance": "..."},  
  "marketStructure": {"orderBookBias": "...", "whaleRetailDivergence": "..."},  
  "forecast": {"shortTerm": "...", "catalysts": "...", "riskLevel": "..."}  
}  
```  

## 6. 使用示例

### 示例1：发现并分析智能资金地址

1. 调用工具：`find_smart_money(7, "win-rate", true)`  
2. 获取高胜率智能资金地址列表  
3. 使用提示：`smart-money-analysis` 分析这些地址的特征  
4. 生成分析报告和复制交易建议  

### 示例2：鲸鱼行为监控

1. 调用工具：`get_whale_events(20)` 获取最新的鲸鱼交易者活动  
2. 调用工具：`get_whale_directions("BTC")` 查看BTC鲸鱼的交易者方向  
3. 使用提示：`whale-tracking` 分析鲸鱼行为  
4. 生成市场影响评估报告  

### 示例3：深入交易者分析

1. 调用工具：`get_trader_stats(address, 30)` 获取基本统计信息  
2. 调用工具：`get_performance_by_coin(address, 30, 20)` 查看特定币种的绩效  
3. 调用工具：`get_completed_position_history(address, "BTC")` 查看历史持仓  
4. 使用提示：`trader-evaluation` 生成综合评估报告  

### 示例4：全面市场情绪分析

1. 调用工具：`get_all_mids()` 获取市场中间价  
2. 调用工具：`get_l2_order_book("BTC")` 获取订单簿数据  
3. 调用工具：`get_market_stats("BTC", 100000)` 获取活跃订单统计  
4. 调用工具：`get_whale_history_ratio("1d, 30)` 获取历史多头/空头比例  
5. 使用提示：`market-sentiment` 生成市场情绪分析报告  

---

## 7. 重要说明

### 7.1 MCP调用说明

**请求格式（JSON-RPC 2.0）：**  
**关键点：**  
- **sessionId**：通过SSE连接到`https://mcp.hyperbot.network/mcp/sse`后获取  
- **method**：始终使用`tools/call`来调用工具  
- **params.name**：工具名称（例如，`fetch_leader_board`、`get_ticker`）  
- **params.arguments**：以键值对形式提供的工具特定参数  

### 7.2 速率限制  
- 单个IP的请求频率限制：每分钟100次  
- 批量接口支持最多50个地址  

### 7.3 数据更新频率  
| 数据类型 | 更新频率 |  
|-----------|------------------|
| 市场数据 | 实时 |
| 智能资金排行榜 | 每小时 |
| 鲸鱼交易者持仓 | 实时 |
| 交易者统计 | 每5分钟一次 |