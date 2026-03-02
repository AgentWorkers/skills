---
name: Vincent - Trading Engine for agents
description: >
  **Polymarket的策略驱动型自动化交易功能**  
  当用户需要创建交易策略、设置止损/止盈/追踪止损规则，或管理自动化交易时，可以使用此功能。  
  相关触发事件包括：  
  - “交易策略”（Trading Strategy）  
  - “止损”（Stop Loss）  
  - “止盈”（Take Profit）  
  - “追踪止损”（Trailing Stop）  
  - “自动化交易”（Automated Trading）  
  - “交易引擎”（Trading Engine）  
  - “交易规则”（Trade Rules）  
  - “策略监控”（Strategy Monitor）
allowed-tools: Read, Write, Bash(npx:*, curl:*)
version: 1.0.0
author: HeyVincent <contact@heyvincent.ai>
license: MIT
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet
        - ./agentwallet
---
# Vincent 交易引擎 - 基于策略的自动化交易

使用此技能可以创建和管理用于 Polymarket 预测市场的自动化交易策略。该交易引擎结合了基于驱动程序的监控（网络搜索、Twitter、新闻稿、价格数据流）与信号处理流程，以及由大型语言模型（LLM）驱动的决策机制，根据您的交易策略自动执行交易。它还包含了独立的止损、止盈和追踪止损规则，这些规则可以在不使用 LLM 的情况下独立运行。

所有命令都使用 `@vincentai/cli` 包。

## 工作原理

**交易引擎是一个具有两种模式的统一系统：**

1. **基于 LLM 的策略** — 创建一个具有结构化交易策略的版本，包括驱动因素（网络搜索关键词、Twitter 账户、新闻稿主题、价格触发器）和升级策略。当驱动因素检测到新信息时，会对这些信号进行评分并批量处理。当达到升级阈值时，LLM（通过 OpenRouter 使用 Claude）会根据您的交易策略评估这些信号，并决定是否进行交易、更新策略或向您发出警报。
2. **独立的交易规则** — 为头寸设置止损、止盈和追踪止损规则。当价格条件满足时，这些规则会自动执行——无需 LLM 的参与。

**架构：**

- 集成到 Vincent 后端（无需单独的服务运行）
- 策略端点位于 `/api/skills/polymarket/strategies/...`
- 交易规则端点位于 `/api/skills/polymarket/rules/...`
- 使用与 Polymarket 技能相同的 API 密钥
- 所有交易都通过 Vincent 的策略执行流程
- LLM 的费用会从用户的信用余额中扣除
- 每次 LLM 调用都会被记录下来，包括完整的审计跟踪信息（令牌、费用、操作和持续时间）

## 安全模型

- **LLM 无法绕过策略** — 所有交易都必须通过 `polymarketSkill.placeBet()`，该函数会执行支出限制、审批阈值和白名单检查
- **后端侧的 LLM 密钥** — OpenRouter API 密钥不会离开服务器。代理和用户无法直接调用 LLM
- **信用限制** — 如果信用余额不足，则无法调用 LLM
- **工具限制** — LLM 可用的工具由策略的 `config.tools` 设置控制。如果 `canTrade: false`，则不会提供交易工具
- **速率限制** — 限制同时进行的 LLM 调用次数，以防止费用过高
- **审计跟踪** — 每次调用都会记录完整的提示、响应、操作和费用信息
- **不使用私钥** — 交易引擎使用 Vincent 的 API 进行所有交易。私钥保存在 Vincent 的服务器上

## 第一部分：基于 LLM 的策略

### 核心概念

- **交易工具**：在交易平台上的可交易资产。由 `id`、`type`（股票、期货、掉期、二元期权、期权）、`venue` 和可选的约束条件（杠杆率、保证金、流动性、费用）定义。
- **交易策略**：您的方向性观点——包括 `estimate`（目标价格/价值）、`direction`（多头/空头/中性）、`confidence`（0–1）和 `reasoning`（推理依据）。
- **驱动因素**：提供信号的数据源。每个驱动因素都有一个 `weight`（权重）、`direction`（看涨/看跌/上下文相关）和 `monitoring` 配置（实体、关键词、嵌入锚点、数据源、轮询间隔）。
- **升级策略**：控制何时唤醒 LLM。`signalScoreThreshold`（批量处理的最低分数）、`highConfidenceThreshold`（触发立即唤醒的分数）、`maxWakeFrequency`（例如“每 15 分钟一次”）、`batchWindow`（例如“5 分钟”）。
- **交易规则**：入场规则（最小利润空间、订单类型）、出场规则（策略失效的触发条件）、自动操作（止损、止盈、追踪止损、价格变化触发条件）和规模规则（方法、最大头寸、投资组合百分比、每日最大交易数量）。

### 信号处理流程

策略通过一个六层处理流程来处理信息：

1. **摄取** — 从驱动因素来源（网络搜索、Twitter、新闻稿、价格数据流、RSS、Reddit、链上数据、文件、期权流）获取原始数据
2. **过滤** — 去重和相关性过滤。丢弃已经看到或质量低于阈值的信号
3. **评分** — 根据驱动因素的权重、与嵌入锚点的相似度以及实体/关键词的匹配程度对每个信号进行评分（0–1）
4. **升级** — 根据升级策略将评分后的信号进行批量处理。低分信号会在批量窗口中累积；高置信度信号会立即触发 LLM 的唤醒
5. **LLM** — LLM 会根据当前的策略评估批量处理的信号。它可以更新策略、做出交易决策、更新驱动因素的状态或不采取任何行动
6. **执行** — 交易决策会通过策略执行流程，并被路由到适当的交易平台适配器进行执行

### 策略生命周期

策略遵循一个版本化的生命周期：`DRAFT` → `ACTIVE` → `PAUSED` → `ARCHIVED`

- **DRAFT**：可以编辑。尚未开始监控或调用 LLM。
- **ACTIVE**：驱动因素正在运行。新信号会触发处理流程。
- **PAUSED**：监控已停止。可以恢复。
- **ARCHIVED**：永久停止。无法重新激活。

要对策略进行迭代，可以将其复制为新的版本（创建一个新的 DRAFT，版本号递增，并保持相同的配置）。

### 创建策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy \
  --key-id <KEY_ID> \
  --name "BTC Momentum" \
  --config '{
    "instruments": [
      { "id": "btc-usd-perp", "type": "perp", "venue": "polymarket" }
    ],
    "thesis": {
      "estimate": 105000,
      "direction": "long",
      "confidence": 0.7,
      "reasoning": "ETF inflows accelerating, halving supply shock imminent"
    },
    "drivers": [
      {
        "name": "ETF Flow Monitor",
        "weight": 2.0,
        "direction": "bullish",
        "monitoring": {
          "entities": ["BlackRock", "Fidelity"],
          "keywords": ["bitcoin ETF", "BTC inflow"],
          "embeddingAnchor": "Bitcoin ETF institutional inflows",
          "sources": ["web_search", "newswire"]
        }
      },
      {
        "name": "Crypto Twitter",
        "weight": 1.0,
        "direction": "contextual",
        "monitoring": {
          "entities": ["@BitcoinMagazine", "@saborskycnbc"],
          "keywords": ["bitcoin", "BTC"],
          "sources": ["twitter"]
        }
      }
    ],
    "escalation": {
      "signalScoreThreshold": 0.3,
      "highConfidenceThreshold": 0.8,
      "maxWakeFrequency": "1 per 15m",
      "batchWindow": "5m"
    },
    "tradeRules": {
      "entry": { "minEdge": 0.05, "orderType": "limit", "limitOffset": 0.01 },
      "autoActions": { "stopLoss": -0.10, "takeProfit": 0.25, "trailingStop": -0.05 },
      "exit": { "thesisInvalidation": ["ETF outflows exceed $500M/week"] },
      "sizing": {
        "method": "edgeScaled",
        "maxPosition": 500,
        "maxPortfolioPct": 20,
        "maxTradesPerDay": 5,
        "minTimeBetweenTrades": "30m"
      }
    },
    "notifications": {
      "onTrade": true,
      "onThesisChange": true,
      "channel": "none"
    }
  }'
```

**参数：**

- `--name`：策略名称
- `--config`：完整的策略配置 JSON（参见上述核心概念的结构）
- `--data-source-secret-id`：可选的 DATA_SOURCES 秘密 ID，用于驱动因素监控 API 调用
- `--poll-interval`：驱动因素监控的轮询间隔（默认：15 分钟）

### 列出策略

```bash
npx @vincentai/cli@latest trading-engine list-strategies --key-id <KEY_ID>
```

### 查看策略详情

```bash
npx @vincentai/cli@latest trading-engine get-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 更新策略

更新 DRAFT 状态的策略。仅传递您想要更改的字段——配置是一个部分对象。

```bash
npx @vincentai/cli@latest trading-engine update-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID> \
  --name "Updated Name" --config '{ "thesis": { "confidence": 0.8, "reasoning": "Updated reasoning" } }'
```

**参数：**

- `--strategy-id`：策略 ID（必需）
- `--name`：新策略名称
- `--config`：部分策略配置 JSON — 仅包括需要更新的字段
- `--data-source-secret-id`：DATA_SOURCES 秘密 ID
- `--poll-interval`：新的轮询间隔（分钟）

### 激活策略

开始驱动因素监控和信号处理流程。策略必须处于 DRAFT 状态。

```bash
npx @vincentai/cli@latest trading-engine activate --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 暂停策略

停止监控。策略必须处于 ACTIVE 状态。

```bash
npx @vincentai/cli@latest trading-engine pause --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 恢复策略

恢复监控。策略必须处于 PAUSED 状态。

```bash
npx @vincentai/cli@latest trading-engine resume --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 存档策略

永久停止策略。无法撤销。

```bash
npx @vincentai/cli@latest trading-engine archive --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 复制策略（新版本）

创建一个具有相同配置、版本号递增的新 DRAFT，并附有父版本的链接。

```bash
npx @vincentai/cli@latest trading-engine duplicate-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看版本历史

查看策略的所有版本。

```bash
npx @vincentai/cli@latest trading-engine versions --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看 LLM 调用历史

查看策略的 LLM 决策日志——哪些数据触发了它、LLM 做出了什么决定、采取了哪些行动以及费用。

```bash
npx @vincentai/cli@latest trading-engine invocations --key-id <KEY_ID> --strategy-id <STRATEGY_ID> --limit 20
```

### 查看费用汇总

查看属于该策略的所有策略的 LLM 费用汇总。

```bash
npx @vincentai/cli@latest trading-engine costs --key-id <KEY_ID>
```

### 查看性能指标

查看策略的性能指标：盈亏、胜率、交易数量和每种工具的详细情况。

```bash
npx @vincentai/cli@latest trading-engine performance --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 驱动因素配置

#### 网络搜索驱动因素

使用 `"sources": ["web_search"]` 添加一个驱动因素。引擎会定期在 Brave 网页上搜索驱动因素的关键词，并在新结果出现时触发信号处理流程。

```json
{
  "name": "AI News Monitor",
  "weight": 1.5,
  "direction": "bullish",
  "monitoring": {
    "keywords": ["AI tokens", "GPU shortage", "prediction market regulation"],
    "embeddingAnchor": "AI technology investment trends",
    "sources": ["web_search"]
  }
}
```

每个关键词都会被独立搜索。结果会被去重——相同的 URL 不会重复触发处理流程。

#### Twitter 驱动因素

使用 `"sources": ["twitter"]` 添加一个驱动因素。引擎会定期检查指定的实体以获取新推文。

```json
{
  "name": "Crypto Twitter",
  "weight": 1.0,
  "direction": "contextual",
  "monitoring": {
    "entities": ["@DeepSeek", "@nvidia", "@OpenAI"],
    "keywords": ["AI", "GPU"],
    "sources": ["twitter"]
  }
}
```

推文会通过推文 ID 进行去重——只有真正新的推文才会触发处理流程。

#### 新闻稿驱动因素（Finnhub）

使用 `"sources": ["newswire"]` 添加一个驱动因素。引擎会定期轮询 Finnhub 的市场新闻 API，并在出现符合您关键词的新标题时触发处理流程。

```json
{
  "name": "Market News",
  "weight": 1.5,
  "direction": "contextual",
  "monitoring": {
    "keywords": ["artificial intelligence", "GPU shortage", "semiconductor"],
    "sources": ["newswire"]
  }
}
```

标题和摘要不区分大小写进行匹配。文章会通过标题哈希进行去重，并使用滑动窗口进行去重。

**注意：** 需要在服务器上设置 `FINNHUB_API_KEY` 环境变量。Finnhub 的免费 tier 允许每分钟 60 次 API 调用。调用不会扣除信用。

#### 价格触发器

价格触发器通过 Polymarket 的 WebSocket 数据流实时评估。当价格条件满足时，会触发信号处理流程。

触发类型：

- `ABOVE` — 当价格超过阈值时触发
- `BELOW` — 当价格低于阈值时触发
- `CHANGE_PCT` — 当价格相对于参考价格变化了一定百分比时触发

价格触发器是一次性的：一旦触发，它们就会被标记为已使用。如果需要，LLM 可以创建新的触发器。

### 交易策略的最佳实践

交易策略是您结构化的方向性观点。好的策略应包括：

1. **明确的估计**：市场应达到的目标价格或价值
2. **置信度水平**：从 0.5–0.7 开始，并允许 LLM 随着新数据的到来进行调整
3. **具体的推理依据**：例如“ETF 流入加速，供应冲击即将发生”比“BTC 会上涨”更具体
4. **明确的失效条件**：使用 `tradeRules.exit.thesisInvalidation` 来定义什么情况会导致策略失效

### LLM 可用的工具

当 LLM 被调用时，它可以使用以下工具（取决于策略配置）：

| 工具                | 描述                                      | 是否需要                         |
| ------------------- | ---------------------------------- | ---------------------------------- |
| `place_trade`       | 买入或卖出头寸                             | `canTrade: true` 在交易规则中                |
| `set_stop_loss`     | 为头寸设置止损规则                         | `canSetRules: true` 在交易规则中                |
| `set_take_profit`   | 为头寸设置止盈规则                         | `canSetRules: true` 在交易规则中                |
| `set_trailing_stop` | 设置追踪止损                             | `canSetRules: true` 在交易规则中                |
| `alert_user`        | 发送警报但不执行交易                         | 始终可用                         |
| `no_action`         | 不采取任何行动（附带解释）                         | 始终可用                         |

### 费用跟踪

每次 LLM 调用都会被记录费用：

- **令牌费用**：输入和输出令牌的费用根据模型的费率计算
- **从信用余额中扣除**：与数据源费用（`dataSourceCreditUsd`）来自同一个池
- **预调用检查**：如果信用不足，调用将被跳过并记录
- **数据源费用**：Brave 搜索（约 0.005 美元/次）和 Twitter（约 0.005–0.01 美元/次）的费用也会被记录。Finnhub 新闻稿调用是免费的（不扣除费用）

典型的 LLM 调用费用：根据上下文的不同，费用在 0.05–0.30 美元之间。

---

## 第二部分：独立的交易规则

交易规则在价格条件满足时自动执行——无需 LLM 的参与。这些规则包括止损、止盈和追踪止损规则，用于保护您的头寸。

### 检查工作进程状态

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
# Returns: worker status, active rules count, last sync time, circuit breaker state
```

### 创建止损规则

如果价格跌至阈值以下，自动卖出头寸：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type STOP_LOSS --trigger-price 0.40
```

**参数：**

- `--market-id`：来自市场数据的 Polymarket 条件 ID
- `--token-id`：您持有的结果令牌 ID（来自市场数据）
- `--rule-type`：`STOP_LOSS`（如果价格 <= 触发条件则卖出）、`TAKE_PROFIT`（如果价格 >= 触发条件则卖出）或 `TRAILING_STOP`
- `--trigger-price`：价格阈值（介于 0 和 1 之间，例如 0.40 表示 40 美分）

### 创建止盈规则

如果价格升至阈值以上，自动卖出头寸：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TAKE_PROFIT --trigger-price 0.75
```

### 创建追踪止损规则

追踪止损会随着价格上涨而提高止损价格：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TRAILING_STOP --trigger-price 0.45 --trailing-percent 5
```

**追踪止损的行为：**

- `--trailing-percent` 是百分比（例如 `5` 表示 5%）
- 计算 `candidateStop = currentPrice * (1 - trailingPercent/100)`
- 如果 `candidateStop` 大于当前的 `triggerPrice`，则更新 `triggerPrice`
- `triggerPrice` 永远不会下降
- 当 `currentPrice <= triggerPrice` 时，规则会被触发

### 列出规则

```bash
# All rules
npx @vincentai/cli@latest trading-engine list-rules --key-id <KEY_ID>

# Filter by status
npx @vincentai/cli@latest trading-engine list-rules --key-id <KEY_ID> --status ACTIVE
```

### 更新规则

```bash
npx @vincentai/cli@latest trading-engine update-rule --key-id <KEY_ID> --rule-id <RULE_ID> --trigger-price 0.45
```

### 取消规则

```bash
npx @vincentai/cli@latest trading-engine delete-rule --key-id <KEY_ID> --rule-id <RULE_ID>
```

### 查看被监控的头寸

```bash
npx @vincentai/cli@latest trading-engine positions --key-id <KEY_ID>
```

### 查看事件日志

```bash
# All events
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID>

# Events for specific rule
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID> --rule-id <RULE_ID>

# Paginated
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID> --limit 50 --offset 100
```

**事件类型：**

- `RULE_CREATED` — 规则被创建
- `RULE_TRAILING_UPDATED` — 追踪止损的触发价格上升
- `RULE_EVALUATED` — 工作进程根据当前价格检查了规则
- `RULE_TRIGGERED` — 触发条件被满足
- `ACTION_PENDING_APPROVAL` — 交易需要人工批准；规则暂停
- `ACTION_EXECUTED` — 交易成功执行
- `ACTION_FAILED` — 交易执行失败
- `RULE_CANCELED` — 规则被手动取消

### 规则状态

- `ACTIVE` — 规则正在运行并被监控
- `TRIGGERED` — 条件被满足，交易已执行
- `PENDING_APPROVAL` — 交易需要人工批准；规则暂停
- `CANCELED` — 在触发前被手动取消
- `FAILED` — 触发条件被满足，但交易执行失败

---

## 完整的工作流程：策略 + 交易规则

### 第一步：使用 Polymarket 技能下注

```bash
npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456789 --side BUY --amount 10 --price 0.55
```

### 第二步：创建一个策略来监控交易策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy --key-id <KEY_ID> \
  --name "Bitcoin Bull Thesis" \
  --config '{
    "instruments": [
      { "id": "123456789", "type": "binary", "venue": "polymarket" }
    ],
    "thesis": {
      "estimate": 0.85,
      "direction": "long",
      "confidence": 0.7,
      "reasoning": "Bitcoin is likely to break $100k on ETF inflows"
    },
    "drivers": [
      {
        "name": "ETF News",
        "weight": 2.0,
        "direction": "bullish",
        "monitoring": {
          "keywords": ["bitcoin ETF inflows", "bitcoin institutional"],
          "sources": ["web_search", "newswire"]
        }
      },
      {
        "name": "Crypto Twitter",
        "weight": 1.0,
        "direction": "contextual",
        "monitoring": {
          "entities": ["@BitcoinMagazine", "@saborskycnbc"],
          "sources": ["twitter"]
        }
      }
    ],
    "escalation": {
      "signalScoreThreshold": 0.3,
      "highConfidenceThreshold": 0.8,
      "maxWakeFrequency": "1 per 15m",
      "batchWindow": "5m"
    },
    "tradeRules": {
      "entry": { "minEdge": 0.05 },
      "autoActions": { "stopLoss": -0.15, "takeProfit": 0.30, "trailingStop": -0.05 },
      "exit": { "thesisInvalidation": ["ETF outflows accelerate above $500M/week"] },
      "sizing": { "method": "edgeScaled", "maxPosition": 100, "maxPortfolioPct": 20, "maxTradesPerDay": 5 }
    }
  }' \
  --poll-interval 10
```

### 第三步：设置独立的止损作为即时保护

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0xabc... --token-id 123456789 \
  --rule-type STOP_LOSS --trigger-price 0.40
```

### 第四步：激活策略

```bash
npx @vincentai/cli@latest trading-engine activate --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 第五步：监控活动

```bash
# Check strategy invocations
npx @vincentai/cli@latest trading-engine invocations --key-id <KEY_ID> --strategy-id <STRATEGY_ID>

# Check trade rule events
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID>

# Check costs
npx @vincentai/cli@latest trading-engine costs --key-id <KEY_ID>

# Check performance
npx @vincentai/cli@latest trading-engine performance --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

## 后台工作进程

交易引擎运行两个独立的后台工作进程：

1. **策略引擎工作进程** — 每 30 秒运行一次，检查哪些策略的驱动因素需要更新数据、评分信号，并在达到升级阈值时调用 LLM。同时会连接到 Polymarket 的 WebSocket 以获取实时价格触发信息。
2. **交易规则工作进程** — 通过 WebSocket 实时监控价格（如果 WebSocket 失效则使用轮询机制），评估止损/止盈/追踪止损规则，并在条件满足时执行交易。

**断路器机制：** 两个工作进程都使用断路器模式。如果 Polymarket API 连续失败 5 次以上，工作进程会暂停并在冷却后恢复。状态检查命令如下：

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
```

## 最佳实践

1. **从 `confidence: 0.5` 开始**，并让 LMM 根据实际情况进行调整——避免对初始策略过于自信
2. **按重要性对驱动因素进行加权** — 权重为 `3.0` 的驱动因素对信号评分的贡献是权重为 `1.0` 的三倍
3. **使用 `edgeScaled` 来根据策略的置信度和利润空间调整头寸规模**
4. **设置 `maxPortfolioPct` 以限制风险** — 即使是高置信度的策略也不应冒险投入整个投资组合
5. **为头寸设置止损和止盈** 以提供保护（通过配置中的 `autoActions` 或独立规则）
6. **使用 `thesisInvalidation` 出场规则** 来定义应触发头寸退出的明确条件
7. **监控调用费用** — 定期检查费用
8. **通过版本迭代** — 复制策略以调整配置而不丢失原始设置
9. **不要将触发条件设置得太接近当前价格** — 市场噪声可能导致过早触发

## 用户示例命令

当用户说：

- **“创建一个监控 AI 代币的策略”** → 创建一个使用网络搜索 + Twitter 驱动因素的策略
- **“设置 40 美分的止损”** → 创建一个 STOP_LOSS 规则
- **“我的策略表现如何？”** → 显示策略的调用记录
- **“我的策略表现如何？”** → 显示性能指标
- **“交易引擎花费了我多少钱？”** → 显示费用汇总
- **“暂停我的策略”** → 暂停策略
- **“创建一个具有不同策略的新版本”** **复制策略并更新草稿**
- **“设置 5% 的追踪止损”** → 创建一个 TRAILING_STOP 规则

## 输出格式

策略创建：

```json
{
  "strategyId": "strat-123",
  "name": "BTC Momentum",
  "status": "DRAFT",
  "version": 1
}
```

规则创建：

```json
{
  "ruleId": "rule-456",
  "ruleType": "STOP_LOSS",
  "triggerPrice": 0.4,
  "status": "ACTIVE"
}
```

LLM 调用日志记录：

```json
{
  "invocationId": "inv-789",
  "strategyId": "strat-123",
  "trigger": "web_search",
  "actions": ["place_trade"],
  "costUsd": 0.12,
  "createdAt": "2026-02-26T12:00:00.000Z"
}
```

## 错误处理

| 错误                         | 原因                                             | 解决方案                                           |
| --------------------------- | ------------------------------------------------- | ---------------------------------------------------- |
| `401 Unauthorized`          | API 密钥无效或缺失                         | 确保密钥 ID 正确；如有需要请重新链接                 |
| `403 Policy Violation`      | 交易被服务器端策略阻止                         | 用户必须在 heyvincent.ai 调整策略                   |
| `402 Insufficient Credit`   | LLM 调用所需的信用不足                         | 用户必须在 heyvincent.ai 添加信用                     |
| `INVALID_STATUS_TRANSITION` | 策略无法转换到请求的状态                         | 检查当前状态（例如，只有 DRAFT 状态才能激活）                 |
| `CIRCUIT_BREAKER_OPEN`      | Polymarket API 失败导致断路器触发                     | 等待冷却时间；使用状态检查命令                     |
| `429 Rate Limited`          | 请求过多或 LLM 调用过多                         | 等待一段时间后重试                         |
| `Key not found`             | API 密钥被撤销或从未创建                         | 从钱包所有者处重新获取新的令牌                     |

## 重要说明

- **授权：** 所有端点都需要使用与 Polymarket 技能相同的 Polymarket API 密钥
- **仅限本地访问**：API 在 `localhost:19000` 上监听——只能从同一 VPS 访问
- **不使用私钥**：所有交易都使用 Vincent 的 API — 私钥安全保存在 Vincent 的服务器上
- **策略执行**：所有交易（包括 LLM 和独立规则）都需通过 Vincent 的策略检查
- **幂等性**：规则只触发一次。LLM 调用会根据驱动因素的状态进行去重