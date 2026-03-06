---

**名称：Hyperbot交易分析**  
**描述：**为Hyperbot平台提供交易数据分析功能，包括智能资金追踪、鲸鱼投资者监控、市场数据查询和交易者统计信息。适用于进行市场分析和决策的加密货币交易者。  

---

[中文](SKILL_zh.md) | [英文](SKILL.md)

## 1. 概述  

**MCP服务器技能文档**  
**版本：** 1.0.0  

**MCP服务器URL/端点：** https://mcp.hyperbot.network/mcp  

**sessionId：** 通过SSE在 https://mcp.hyperbot.network/mcp/sse 获取  

---

## 2. 资源  

### 2.1 定义的资源  
无  

**使用说明：**  
- 仅用于读取数据，不会改变系统状态  
- 可作为提示输入或供代理进行决策参考  
- 数据来源于Hyperbot平台和链上数据  
- 支持按需检索（分页/过滤条件）  

---

## 3. 工具  

### 3.1 排行榜与智能资金发现  

#### `fetch_leader_board`  
**功能：** 获取Hyperbot智能资金排行榜  
**参数：**  
- `period`：时间周期（选项：24小时、7天、30天）  
- `sort`：排序字段（选项：pnl（盈亏）、winRate（胜率）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"fetch_leader_board","arguments":{"period":"7d","sort":"pnl"}},"jsonrpc":"2.0","id":1}'
```  

#### `find_smart_money`  
**功能：** 发现具有多种排序和过滤选项的智能资金地址  
**参数：**  
- `period`：时间周期（例如：7表示过去7天）  
- `sort`：排序方式（选项：win-rate、account-balance、ROI、pnl、position-count、profit-count、last-operation、avg-holding-period、current-position）  
- `pnlList`：是否包含PnL曲线数据（true/false）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"find_smart_money","arguments":{"period":7,"sort":"win-rate","pnlList":true}},"jsonrpc":"2.0","id":2}'
```  

---

### 3.2 市场数据  

#### `get_tickers`  
**功能：** 获取所有市场的最新交易价格  
**参数：** 无  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_tickers","arguments":{}},"jsonrpc":"2.0","id":3}'
```  

#### `get_ticker`  
**功能：** 获取特定币种的最新交易价格  
**参数：**  
- `address`：币种代码（例如：btc、eth、sol）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_ticker","arguments":{"address":"ETH"}},"jsonrpc":"2.0","id":4}'
```  

#### `get_klines`  
**功能：** 获取K线数据（包含交易量），支持BTC、ETH等币种  
**参数：**  
- `coin`：币种代码（例如：btc、eth）  
- `interval`：K线间隔（选项：1分钟、3分钟、5分钟、15分钟、30分钟、1小时、4小时、8小时、1天）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_klines","arguments":{"coin":"BTC","interval":"15m","limit":100}},"jsonrpc":"2.0","id":5}'
```  

#### `get_market_stats`  
**功能：** 获取活跃订单统计信息（多头/空头数量、价值、鲸鱼投资者订单比例）及市场中间价  
**参数：**  
- `coin`：币种代码（例如：btc、eth）  
- `whaleThreshold`：鲸鱼投资者阈值（以USDT计）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_market_stats","arguments":{"coin":"BTC","whaleThreshold":100000}},"jsonrpc":"2.0","id":6}'
```  

#### `get_l2_order_book`  
**功能：** 获取市场信息（如L2订单簿等）  
**参数：**  
- `coin`：币种代码（例如：btc、eth）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_l2_order_book","arguments":{"coin":"BTC"}},"jsonrpc":"2.0","id":7}'
```  

---

### 3.3 鲸鱼投资者监控  

#### `get_whale_positions`  
**功能：** 获取鲸鱼投资者的持仓信息  
**参数：**  
- `coin`：币种代码（例如：eth、btc）  
- `dir`：方向（选项：多头、空头）  
- `pnlSide`：PnL过滤条件（选项：盈利、亏损）  
- `frSide`：资金费用PnL过滤条件（选项：盈利、亏损）  
- `topBy`：排序方式（选项：持仓价值、保证金余额、创建时间、盈利、亏损）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_positions","arguments":{"coin":"BTC","dir":"long","pnlSide":"profit","frSide":"profit","topBy":"position-value","take":10}},"jsonrpc":"2.0","id":8}'
```  

#### `get_whale_events`  
**功能：** 实时监控最新的鲸鱼投资者开仓/平仓行为  
**参数：**  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_events","arguments":{"limit":20}},"jsonrpc":"2.0","id":9}'
```  

#### `get_whale_directions`  
**功能：** 获取鲸鱼投资者的多头/空头数量（可按特定币种过滤）  
**参数：**  
- `coin`：币种代码（例如：eth、btc）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_directions","arguments":{"coin":"BTC"}},"jsonrpc":"2.0","id":10}'
```  

#### `get_whale_history_ratio`  
**功能：** 获取历史鲸鱼投资者多头/空头比例  
**参数：**  
- `interval`：时间间隔（选项：1小时、1天或小时、天）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_history_ratio","arguments":{"interval":"1d","limit":30}},"jsonrpc":"2.0","id":11}'
```  

---

### 3.4 交易者分析  

#### `fetch_trade_history`  
**功能：** 查询特定钱包地址的历史交易详情  
**参数：**  
- `address`：以0x开头的钱包地址  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"fetch_trade_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678"}},"jsonrpc":"2.0","id":12}'
```  

#### `get_trader_stats`  
**功能：** 获取交易者统计信息  
**参数：**  
- `address`：用户钱包地址  
- `period`：时间周期（以天计）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_trader_stats","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":7}},"jsonrpc":"2.0","id":13}'
```  

#### `get_max_drawdown`  
**功能：** 获取最大回撤幅度  
**参数：**  
- `address`：用户钱包地址  
- `days`：统计周期（选项：1天、7天、30天、60天、90天）  
- `scope`：统计范围（默认：perp）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_max_drawdown","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","days":30,"scope":"perp"}},"jsonrpc":"2.0","id":14}'
```  

#### `get_best_trades`  
**功能：** 获取最盈利的交易记录  
**参数：**  
- `address`：用户钱包地址  
- `period`：时间周期（以天计）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_best_trades","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":7,"limit":10}},"jsonrpc":"2.0","id":15}'
```  

#### `get_performance_by_coin`  
**功能：** 按币种分解地址的胜率和PnL表现  
**参数：**  
- `address`：用户钱包地址  
- `period`：时间周期（以天计）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_performance_by_coin","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":30,"limit":20}},"jsonrpc":"2.0","id":16}'
```  

---

### 3.5 持仓历史  

#### `get_completed_position_history`  
**功能：** 获取完成的持仓历史记录  
**参数：**  
- `address`：用户钱包地址  
- `coin`：币种名称（例如：BTC、ETH）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_completed_position_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC"}},"jsonrpc":"2.0","id":17}'
```  

#### `get_current_position_history`  
**功能：** 获取当前持仓历史记录  
**参数：**  
- `address`：用户钱包地址  
- `coin`：币种名称（例如：BTC、ETH）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_current_position_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC"}},"jsonrpc":"2.0","id":18}'
```  

#### `get_completed_position_executions`  
**功能：** 获取完成的持仓执行轨迹  
**参数：**  
- `address`：用户钱包地址  
- `coin`：币种名称（例如：BTC、ETH）  
- `interval`：时间间隔（例如：4小时、1天）  
- `startTime`：开始时间戳（毫秒）  
- `endTime`：结束时间戳（毫秒）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_completed_position_executions","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC","interval":"4h","limit":50}},"jsonrpc":"2.0","id":19}'
```  

#### `get_current_position_pnl`  
**功能：** 获取当前持仓的PnL  
**参数：**  
- `address`：用户钱包地址  
- `coin`：币种名称（例如：BTC、ETH）  
- `interval`：时间间隔（例如：4小时、1天）  
- `limit`：返回的最大记录数  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_current_position_pnl","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC","interval":"4h","limit":20}},"jsonrpc":"2.0","id":20}'
```  

---

### 3.6 批量查询  

#### `get_traders_accounts`  
**功能：** 批量查询账户信息（最多支持50个地址）  
**参数：**  
- `addresses`：地址列表（最多50个地址）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_traders_accounts","arguments":{"addresses":["0x1234567890abcdef1234567890abcdef12345678","0xabcdef1234567890abcdef1234567890abcdef12"]}},"jsonrpc":"2.0","id":21}'
```  

#### `get_traders_statistics`  
**功能：** 批量查询交易者统计信息（最多支持50个地址）  
**参数：**  
- `period`：时间周期（以天计，例如：7表示过去7天）  
- `pnlList`：是否包含PnL曲线数据  
- `addresses`：地址列表（最多50个地址）  

**MCP工具调用示例：**  
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_traders_statistics","arguments":{"period":7,"pnlList":true,"addresses":["0x1234567890abcdef1234567890abcdef12345678","0xabcdef1234567890abcdef1234567890abcdef12"]}},"jsonrpc":"2.0","id":22}'
```  

---

## 4. 提示  

| 提示名称 | 目的 | 模板/示例 |  
|-------------|--------|------------------|  
| smart-money-analysis | 智能资金地址分析与交易建议 | ```您是量化交易专家。分析输入的智能资金地址数据：1. 识别高胜率地址的特征；2. 分析其持仓偏好和交易风格；3. 提供复制交易策略建议。输出格式：JSON。```  
| whale-tracking | 鲸鱼投资者行为分析与市场影响评估 | ```分析鲸鱼投资者的持仓数据和最新动向：1. 判断主力意图；2. 评估市场影响；3. 预测短期趋势；4. 提供交易建议。输出格式：JSON。```  
| market-sentiment | 市场情绪分析 | **基于市场数据（订单簿、活跃订单、鲸鱼投资者多头/空头比例）：1. 分析当前市场情绪；2. 识别支撑/阻力水平；3. 判断短期趋势。输出格式：JSON。**  
| trader-evaluation | 交易者能力评估 | **全面评估交易者的能力：1. 分析胜率和盈亏比率；2. 评估风险管理能力；3. 分析币种偏好；4. 提供综合评分和改进建议。输出格式：JSON。**  

**使用说明：**  
- 提示内容可动态填充  
- 可组合多个提示以形成推理流程  
- 建议使用JSON格式输出，便于代理解析  

---

## 5. 使用示例  

### 示例1：发现并分析智能资金地址  

1. 调用工具：`find_smart_money(7, "win-rate", true)`  
2. 获取高胜率智能资金地址列表  
3. 使用提示：`smart-money-analysis` 分析这些地址的特征  
4. 生成分析报告和复制交易建议  

### 示例2：鲸鱼投资者行为监控  

1. 调用工具：`get_whale_events(20)` 获取最新鲸鱼投资者动向  
2. 调用工具：`get_whale_directions("BTC")` 查看BTC的鲸鱼投资者多头/空头比例  
3. 使用提示：`whale-tracking` 分析鲸鱼投资者行为  
4. 生成市场影响评估报告  

### 示例3：深入交易者分析  

1. 调用工具：`get_trader_stats(address, 30)` 获取基本统计信息  
2. 调用工具：`get_performance_by_coin(address, 30, 20)` 查看特定币种的业绩  
3. 调用工具：`get_completed_position_history(address, "BTC")` 查看历史持仓  
4. 使用提示：`trader-evaluation` 生成综合评估报告  

### 示例4：全面市场情绪分析  

1. 调用工具：`get_all_mids()` 获取市场中间价  
2. 调用工具：`get_l2_order_book("BTC")` 获取订单簿数据  
3. 调用工具：`get_market_stats("BTC", 100000)` 获取活跃订单统计  
4. 调用工具：`get_whale_history_ratio("1d, 30")` 获取历史多头/空头比例  
5. 使用提示：`market-sentiment` 生成市场情绪分析报告  

---

## 6. 重要说明  

### MCP调用说明  
- **sessionId**：需先通过SSE连接获取会话ID（访问地址：https://mcp.hyperbot.network/mcp/sse）  
- **JSON-RPC 2.0**：遵循标准JSON-RPC 2.0协议  
- **method**：固定为`tools/call`  
- **params.name**：MCP工具名称（对应于`@McpTool`注释的名称属性）  
- **paramsarguments**：工具参数，以键值对形式传递  

### 限制  
- 单个IP的请求频率限制：每分钟100次  
- 批量接口支持最多50个地址  

### 数据更新频率  
- 市场数据：实时更新  
- 智能资金排行榜：每小时更新一次  
- 鲸鱼投资者持仓：实时更新  
- 交易者统计：每5分钟更新一次