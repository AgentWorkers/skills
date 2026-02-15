---
name: dwlf
description: >
  Interact with DWLF (dwlf.co.uk), a market analysis platform for crypto and stocks.
  Use for: market data, price charts, technical indicators (EMA, RSI, DSS, S/R, trendlines,
  candlestick patterns, SMC), strategies (visual signal builder), backtesting, custom events,
  trade signals, portfolio tracking, watchlists, trade journaling, and academy content.
  Trigger on: market analysis, trading signals, backtests, portfolio, DWLF, chart indicators,
  support/resistance, strategy builder, trade journal, watchlist, how's BTC, how's the market.
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["curl", "jq"]
---

# DWLF — 市场分析平台

API 基础地址：`https://api.dwlf.co.uk/v2`

## 认证

使用 API 密钥进行认证。请参阅 `TOOLS.md` 以获取密钥。请求头中的密钥格式如下：
```
Authorization: ApiKey dwlf_sk_...
```

辅助脚本：`scripts/dwlf-api.sh`

## 快速入门

```bash
# Generic GET request
./scripts/dwlf-api.sh GET /market-data/BTC-USD

# With query params
./scripts/dwlf-api.sh GET "/events?symbol=BTC-USD&limit=10"

# POST request
./scripts/dwlf-api.sh POST /visual-backtests '{"strategyId":"...","symbol":"BTC-USD"}'
```

## 符号格式

- 加密货币：`BTC-USD`、`ETH-USD`、`SOL-USD`（始终带有 `-USD` 后缀）
- 股票/ETF：`TSLA`、`NVDA`、`META`、`MARA`、`RIOT`
- 外汇：`GBP-USD`、`EUR-USD`

如果用户输入 “BTC”，则使用 `BTC-USD`；如果输入 “TSLA”，则使用 `TSLA`。

## 核心端点

### 市场数据
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/market-data/{symbol}?interval=1d&limit=50` | 获取 OHLCV 图表数据 |
| GET | `/market-data/symbols` | 列出所有跟踪的符号 |
| GET | `/support-resistance/{symbol}` | 获取带有评分的支持/阻力水平 |
| GET | `/chart-indicators/{symbol}?interval=1d` | 获取所有指标（RSI、EMA、MACD 等） |
| GET | `/trendlines/{symbol}` | 自动检测的趋势线 |
| GET | `/events?symbol={symbol}&limit=20` | 系统事件（价格突破等） |
| GET | `/events?type=custom_event&scope=user&symbol={symbol}&days=30` | 用户自定义事件（如价格波动、趋势反转等） |

### 策略与信号
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/visual-strategies` | 列出用户的策略 |
| GET | `/visual-strategies/{id}` | 查看策略详情 |
| POST | `/visual-strategies` | 创建策略 |
| PUT | `/visual-strategies/{id}` | 更新策略 |
| GET | `/user/trade-signals/active` | 查看活跃的交易信号 |
| GET | `/user/trade-signals/recent?limit=20` | 查看最近的信号 |
| GET | `/user/trade-signals/stats` | 查看信号性能统计 |
| GET | `/user/trade-signals/symbol/{symbol}` | 获取特定符号的信号 |

### 回测
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | `/visual-backtests` | 触发回测（异步进行） |
| GET | `/visual-backtests/{id}` | 获取回测结果 |

回测是异步的——先发送 POST 请求触发回测，然后通过 GET 请求获取结果。

### 投资组合与交易
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/portfolios` | 列出投资组合 |
| GET | `/portfolios/{id}` | 查看投资组合详情及持仓 |
| GET | `/trades?status=open` | 查看未平仓的交易 |
| POST | `/trades` | 记录新的交易 |
| PUT | `/trades/{id}` | 更新交易信息 |
| GET | `/trade-plans` | 查看交易计划 |

### 关注列表
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/watchlist` | 查看关注列表 |
| POST | `/watchlist` | 添加符号（例如：`{"symbol":"BTC-USD"}`） |
| DELETE | `/watchlist/{symbol}` | 删除符号 |

### 自定义事件
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/custom-events` | 列出所有自定义事件 |
| POST | `/custom-events` | 创建自定义事件 |
| GET | `/custom-events/{id}` | 查看事件详情 |

### 自定义事件符号的激活
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | `/custom-event-symbols/:eventId/enable-all` | 为某个事件批量激活符号 |
| POST | `/custom-event-symbols/:eventId/disable-all` | 为某个事件批量停用符号 |
| GET | `/custom-event-symbols/event/:eventId` | 查看某个事件下的活跃符号 |
| GET | `/custom-event-symbols` | 查看所有事件与符号的关联关系 |

### 策略符号的激活
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | `/strategy-symbols/:strategyId/enable-all` | 为某个策略批量激活符号 |
| POST | `/strategy-symbols/:strategyId/disable-all` | 为某个策略批量停用符号 |
| GET | `/strategy-symbols/strategy/:strategyId` | 查看某个策略下的活跃符号 |
| GET | `/strategy-symbols` | 查看所有策略与符号的关联关系 |

### 评估
| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | `/evaluations` | 触发评估流程 |
| GET | `/evaluations/{id}` | 查看评估结果 |

## 符号激活（创建后必须执行）

> ⚠️ **重要提示：** 创建自定义事件或策略后，**不会自动**激活任何符号。创建后，**必须**询问用户要为哪些符号激活该事件或策略，然后调用相应的激活端点。否则，该事件/策略将不会触发或生成信号。

### 工作流程：

**自定义事件：**
1. 创建事件 → `POST /custom-events`
2. 编译事件 → `POST /custom-events/{id}/compile`
3. **询问用户**要为哪些符号激活该事件
4. **激活符号** → `POST /custom-event-symbols/{eventId}/enable-all`，参数示例：`{"symbols": ["BTC-USD", "ETH-USD"]`

**策略：**
1. 创建策略 → `POST /visual-strategies`
2. 编译策略 → `POST /visual-strategies/{id}/compile`
3. **询问用户**要为哪些符号激活该策略
4. **激活符号** → `POST /strategy-symbols/{strategyId}/enable-all`，参数示例：`{"symbols": ["BTC-USD", "ETH-USD"]`

### 检查活跃符号
- 事件相关的符号：`GET /custom-event-symbols/event/{eventId}`
- 策略相关的符号：`GET /strategy-symbols/strategy/{strategyId}`
- 所有激活的符号：`GET /custom-event-symbols` 和 `GET /strategy-symbols`（查询参数：`?activeOnly=true`）

### 停用符号
- 事件相关的符号：`POST /custom-event-symbols/{eventId}/disable-all`，参数示例：`{"symbols": [...] }`
- 策略相关的符号：`POST /strategy-symbols/{strategyId}/disable-all`，参数示例：`{"symbols": [...] }`

## 响应格式

向用户展示数据时：
- **市场概览**：显示价格、百分比变化、关键的支持/阻力水平以及最近的事件。
- **信号**：显示符号、方向、入场价、止损价、置信度评分以及策略名称。
- **支持/阻力水平**：按评分排序（评分最高的在前），显示具体水平和触碰次数。
- **回测结果**：显示交易数量、胜率、总回报、夏普比率以及最佳/最差的交易记录。

## 可用的指标

EMA（多个周期）、SMA、RSI、MACD、Bollinger Bands、DSS（双平滑随机指标）、Stochastic RSI、ATR、ADX、OBV、成交量分布图、Ichimoku Cloud、Fibonacci 回撤线、支持/阻力线、趋势线、K线形态、SMC（订单块、FVGs、BOS/ChoCH）。

## 学院

DWLF 学院是一个通过 CDN 提供的教育资源集合（包含 15 个主题、60 多节课），涵盖指标、事件、策略、图表分析等内容。无需认证即可使用。

使用学院工具来阅读课程内容并理解 DWLF 的概念：
- `dwlf_list_academy_tracks` — 浏览所有主题和课程
- `dwlf_search_academy` — 按关键词搜索课程
- `dwlf_get_academy_lesson` — 阅读特定课程（格式为 Markdown）

当用户询问 “X 在 DWLF 中是如何工作的？” 或 “DSS 是什么？” 时，建议先查看学院的相关课程——很可能会有相关解释。

## 详细参考资料

- **API 端点**（参数、响应格式）：请参阅 `references/api-endpoints.md`
- **策略构建器**（节点类型、连接方式、示例）：请参阅 `references/strategy-builder.md`