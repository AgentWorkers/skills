---
name: Vincent - Trading Engine for agents
description: >
  **策略驱动的自动化交易功能（适用于Polymarket和HyperLiquid）**  
  当用户需要创建交易策略、设置止损/止盈/追踪止损规则或管理自动化交易时，可使用此功能。  
  该功能支持以下事件触发：  
  - **交易策略（Trading Strategy）**  
  - **止损（Stop Loss）**  
  - **止盈（Take Profit）**  
  - **追踪止损（Trailing Stop）**  
  - **自动化交易（Automated Trading）**  
  - **交易引擎（Trading Engine）**  
  - **交易规则（Trade Rules）**  
  - **策略监控（Strategy Monitor）**
allowed-tools: Read, Write, Bash(npx:@vincentai/cli*)
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
# Vincent交易引擎 - 基于策略的自动化交易

使用此技能可以为Polymarket预测市场和HyperLiquid永续合约/现货合约创建和管理自动化交易策略。该交易引擎结合了基于驱动程序的监控（网络搜索、Twitter、新闻通讯、价格数据流）与信号处理流程，以及由大型语言模型（LLM）驱动的决策机制，根据您的交易策略自动执行交易。它还包含了独立的止损、止盈和跟踪止损规则，这些规则可以在不使用LLM的情况下独立运行。

所有命令都使用`@vincentai/cli`包。

## 工作原理

**交易引擎是一个具有两种模式的统一系统：**

1. **基于LLM的策略** — 创建一个具有结构化交易策略的版本，包括驱动因素（网络搜索关键词、Twitter账户、新闻主题、价格触发条件）和升级策略。当驱动因素检测到新信息时，会对这些信号进行评分并批量处理。当达到升级阈值时，LLM（通过OpenRouter使用Claude）会根据您的交易策略评估这些信号，并决定是进行交易、更新策略、设置保护性订单还是向您发送警报。
2. **独立的交易规则** — 为头寸设置止损、止盈和跟踪止损规则。当价格条件满足时，这些规则会自动执行——无需LLM的参与。

**架构：**

- 集成到Vincent后端中（无需单独的服务运行）
- 策略端点位于`/api/skills/polymarket/strategies/...`
- 交易规则端点位于`/api/skills/polymarket/rules/...`
- HyperLiquid规则使用`venue: "hyperliquid"`并通过HL适配器路由
- 使用与Polymarket或HyperLiquid技能相同的API密钥（取决于交易场所）
- 所有交易都通过Vincent的政策执行流程
- LLM的费用会从用户的信用余额中扣除
- 每次LLM调用都会被记录下来，包括完整的审计追踪（令牌、费用、操作和持续时间）

## 安全模型

- **LLM无法绕过策略** — 所有交易都必须通过交易场所的政策执行机制（`polymarketSkill.placeBet()`或`hyperliquidSkill.trade()`），该机制会执行费用限制、审批阈值和白名单检查
- **后端LLM密钥** — OpenRouter API密钥不会离开服务器。代理和用户无法直接调用LLM
- **信用限制** — 如果信用余额不足，LLM将无法被调用
- **工具限制** — LLM可用的工具由策略的`config.tools`设置控制。如果`canTrade: false`，则不会提供交易工具
- **速率限制** — 限制LLM的最大并发调用次数，以防止费用失控
- **审计追踪** — 每次调用都会记录下完整的提示、响应、操作和费用
- **不使用私钥** — 交易引擎使用Vincent的API进行所有交易。私钥保存在Vincent的服务器上

## 第一部分：基于LLM的策略

### 核心概念

- **工具**：交易场所上的可交易资产。由`id`、`type`（股票、永续合约、掉期合约、二元期权、期权）、`venue`以及可选的约束条件（杠杆率、保证金、流动性、费用）定义。
- **交易策略**：您的方向性观点——包括`estimate`（目标价格/价值）、`direction`（多头/空头/中性）、`confidence`（0–1）和`reasoning`（推理依据）。
- **驱动因素**：提供信号的数据源。每个驱动因素都有一个`weight`（权重）、`direction`（看涨/看跌/上下文相关）和`monitoring`配置（实体、关键词、嵌入锚点、数据源、轮询间隔）。
- **升级策略**：控制何时唤醒LLM。`signalScoreThreshold`（批量处理的最低分数）、`highConfidenceThreshold`（触发立即唤醒的分数）、`maxWakeFrequency`（例如“每15分钟一次”）、`batchWindow`（例如“5分钟”）。
- **交易规则**：入场规则（最小利润空间、订单类型）、退出规则（策略无效的触发条件）、自动操作（止损、止盈、跟踪止损）和规模规则（方法、最大头寸、投资组合百分比、每日最大交易数量）。

### 信号处理流程

策略通过一个六层处理流程来处理信息：

1. **摄取** — 来自驱动因素源的原始数据（网络搜索、Twitter、新闻通讯、价格数据流、RSS、Reddit、链上数据、期权流）
2. **过滤** — 去重和相关性过滤。丢弃已经看到的或质量低于阈值的信号
3. **评分** — 根据驱动因素的权重、与嵌入锚点的相似度以及实体/关键词的匹配程度对每个信号进行评分（0–1）
4. **升级** — 根据升级策略将评分后的信号进行批量处理。低分信号会在一个批次窗口中累积；高置信度信号会立即触发LLM的唤醒
5. **LLM** — LLM根据当前的策略评估批量处理的信号。它可以更新策略、做出交易决策、更新驱动因素的状态或不采取任何行动
6. **执行** — 交易决策通过政策执行机制，并被路由到相应的交易场所适配器进行执行

### 策略生命周期

策略遵循一个版本化的生命周期：`DRAFT` → `ACTIVE` → `PAUSED` → `ARCHIVED`

- **DRAFT**：可以编辑。尚未开始监控或调用LLM。
- **ACTIVE**：驱动因素正在运行。新信号会触发处理流程。
- **PAUSED**：监控已停止。可以恢复。
- **ARCHIVED**：永久停止。无法重新激活。

要迭代一个策略，可以复制它作为一个新版本（创建一个带有递增版本号和相同配置的新DRAFT）。

### 创建策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy \
  --key-id <KEY_ID> \
  --name "BTC Momentum" \
  --config '{
    "instruments": [
      { "id": "btc-usd-perp", "type": "perp", "venue": "polymarket" },
      { "id": "BTC", "type": "perp", "venue": "hyperliquid" }
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
- `--config`：完整的策略配置JSON（参见上述核心概念）
- `--data-source-secret-id`：可选的DATA_SOURCES秘密ID，用于驱动因素监控API调用
- `--poll-interval`：驱动因素监控的轮询间隔（默认：15分钟）

### 列出策略

```bash
npx @vincentai/cli@latest trading-engine list-strategies --key-id <KEY_ID>
```

### 查看策略详情

```bash
npx @vincentai/cli@latest trading-engine get-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 更新策略

更新一个DRAFT策略。仅传递您想要更改的字段——配置是一个部分对象。

```bash
npx @vincentai/cli@latest trading-engine update-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID> \
  --name "Updated Name" --config '{ "thesis": { "confidence": 0.8, "reasoning": "Updated reasoning" } }'
```

**参数：**

- `--strategy-id`：策略ID（必需）
- `--name`：新策略名称
- `--config`：部分策略配置JSON — 仅包括要更新的字段
- `--data-source-secret-id`：DATA_SOURCES秘密ID
- `--poll-interval`：新的轮询间隔（分钟）

### 激活策略

开始驱动因素监控和信号处理流程。策略必须处于DRAFT状态。

```bash
npx @vincentai/cli@latest trading-engine activate --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 暂停策略

停止监控。策略必须处于ACTIVE状态。

```bash
npx @vincentai/cli@latest trading-engine pause --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 恢复策略

恢复监控。策略必须处于PAUSED状态。

```bash
npx @vincentai/cli@latest trading-engine resume --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 归档策略

永久停止策略。无法撤销。

```bash
npx @vincentai/cli@latest trading-engine archive --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 复制策略（新版本）

创建一个具有相同配置、递增版本号和父版本链接的新DRAFT。

```bash
npx @vincentai/cli@latest trading-engine duplicate-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看版本历史

查看策略的所有版本。

```bash
npx @vincentai/cli@latest trading-engine versions --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看LLM调用历史

查看策略的LLM决策日志——是什么数据触发了它，LLM做出了什么决定，采取了哪些行动，以及费用是多少。

```bash
npx @vincentai/cli@latest trading-engine invocations --key-id <KEY_ID> --strategy-id <STRATEGY_ID> --limit 20
```

### 查看费用汇总

查看某个秘密策略下的所有LLM费用汇总。

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

添加一个驱动因素，设置`sources`为`["web_search"]`。引擎会定期在Brave网站上搜索驱动因素的关键词，并在新结果出现时触发信号处理流程。

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

每个关键词都会被独立搜索。结果会被去重——相同的URL不会被重复触发处理流程。

#### Twitter驱动因素

添加一个驱动因素，设置`sources`为`["twitter"]`。引擎会定期检查指定的实体以获取新推文。

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

推文会通过推文ID去重——只有真正新的推文才会触发处理流程。

#### 新闻通讯驱动因素（Finnhub）

添加一个驱动因素，设置`sources`为`["newswire"]`。引擎会定期轮询Finnhub的市场新闻API，并在出现与您的关键词匹配的新标题时触发处理流程。

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

标题和摘要是不区分大小写的。文章会通过标题哈希进行去重，并使用滑动窗口。

**注意：**需要在服务器上设置`FINNHUB_API_KEY`环境变量。Finnhub的免费 tier允许每分钟60次API调用。每次调用不会扣除信用。

#### 价格触发条件

价格触发条件通过Polymarket的WebSocket数据流实时评估。当价格条件满足时，会调用信号处理流程。

触发类型：

- `ABOVE` — 当价格超过阈值时触发
- `BELOW` — 当价格低于阈值时触发
- `CHANGE_PCT` — 当价格相对于参考价格变化了一定百分比时触发

价格触发条件是一次性的：一旦触发，它们就会被标记为已使用。如果需要，LLM可以创建新的触发条件。

### 交易策略的最佳实践

交易策略是您的结构化方向性观点。好的策略应该包括：

1. **明确的估计**：市场应该达到的目标价格或价值
2. **置信度水平**：从0.5开始，随着新数据的到来让LLM进行调整
3. **具体的推理依据**：例如“ETF流入加速，供应冲击即将发生”比“BTC会上涨”更有说服力
4. **明确的无效条件**：使用`tradeRules.exit.thesisInvalidation`来定义什么情况会导致策略失效

### LLM可用工具

当LLM被调用时，它可以使用以下工具（取决于策略配置）：

| 工具                | 描述                                      | 是否需要                         |
| ------------------- | ---------------------------------- | ---------------------------------- |
| `place_trade`       | 买入或卖出头寸                         | `canTrade: true` 在交易规则中                |
| `set_stop_loss`     | 为头寸设置止损规则                         | `canSetRules: true` 在交易规则中                |
| `set_take_profit`   | 设置止盈规则                         | `canSetRules: true` 在交易规则中                |
| `set_trailing_stop` | 设置跟踪止损                         | `canSetRules: true` 在交易规则中                |
| `alert_user`        | 发送警报（不进行交易）                         | 始终可用                         |
| `no_action`         | 不采取任何行动（并提供理由）                         | 始终可用                         |

### 费用跟踪

每次LLM调用都会被计费：

- **令牌费用**：输入和输出令牌的费用根据模型的费率计算
- **从信用余额中扣除**：与数据源信用相同（`dataSourceCreditUsd`）
- **预调用检查**：如果信用不足，调用将被跳过并记录
- **数据源费用**：Brave搜索（约0.005美元/次）和Twitter（约0.005-0.01美元/次）也会被计费。Finnhub新闻通讯调用是免费的（不扣除信用）

典型的LLM调用费用：根据上下文大小，费用在0.05美元到0.30美元之间。

---

## 第二部分：独立的交易规则

交易规则在价格条件满足时自动执行——不涉及LLM。这些规则包括止损、止盈和跟踪止损规则，用于保护您的头寸。

### 检查工作进程状态

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
# Returns: worker status, active rules count, last sync time, circuit breaker state
```

### 创建止损规则

如果价格跌至阈值以下，自动卖出头寸：

```bash
# Polymarket — triggerPrice is 0–1 (outcome token price)
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type STOP_LOSS --trigger-price 0.40

# HyperLiquid — triggerPrice is absolute USD price, marketId and tokenId are the coin name
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id BTC --token-id BTC \
  --rule-type STOP_LOSS --trigger-price 95000
```

**参数：**

- `--venue`：`polymarket`（默认）或`hyperliquid`
- `--market-id`：Polymarket的条件ID，或HyperLiquid的币名（例如`BTC`、`ETH`）
- `--token-id`：Polymarket的结果令牌ID，或HyperLiquid的币名
- `--rule-type`：`STOP_LOSS`（如果价格≤触发条件则卖出），`TAKE_PROFIT`（如果价格≥触发条件则卖出），或`TRAILING_STOP`
- `--trigger-price`：价格阈值 — 对于Polymarket为0到1，对于HyperLiquid为绝对美元价格

### 创建止盈规则

如果价格升至阈值以上，自动卖出头寸：

```bash
# Polymarket
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TAKE_PROFIT --trigger-price 0.75

# HyperLiquid
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id ETH --token-id ETH \
  --rule-type TAKE_PROFIT --trigger-price 4500
```

### 创建跟踪止损规则

跟踪止损会随着价格的上涨而调整止损价格：

```bash
# Polymarket
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TRAILING_STOP --trigger-price 0.45 --trailing-percent 5

# HyperLiquid
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id SOL --token-id SOL \
  --rule-type TRAILING_STOP --trigger-price 170 --trailing-percent 5
```

**跟踪止损的行为：**

- `--trailing-percent` 是百分比点数（例如`5`表示5%）
- 计算`candidateStop = currentPrice * (1 - trailingPercent/100)`
- 如果`candidateStop` > current `triggerPrice`，则更新`triggerPrice`
- `triggerPrice` 永远不会下降
- 当`currentPrice <= triggerPrice`时，规则会被触发

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

### 查看监控中的头寸

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
- `RULE_TRAILING_UPDATED` — 跟踪止损的触发价格上升
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

## 完整工作流程：策略 + 交易规则

### Polymarket工作流程

### 第1步：使用Polymarket技能下注

```bash
npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456789 --side BUY --amount 10 --price 0.55
```

### 第2步：创建一个策略来监控交易策略

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

### 第3步：设置独立的止损作为即时保护

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0xabc... --token-id 123456789 \
  --rule-type STOP_LOSS --trigger-price 0.40
```

### 第4步：激活策略

```bash
npx @vincentai/cli@latest trading-engine activate --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 第5步：监控活动

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

### HyperLiquid工作流程

### 第1步：使用HyperLiquid技能开立永续合约头寸

```bash
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy true --sz 0.001 --limit-px 106000 --order-type market
```

### 第2步：为头寸设置止损规则

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id BTC --token-id BTC \
  --rule-type STOP_LOSS --trigger-price 95000
```

### 第3步：设置止盈规则

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id BTC --token-id BTC \
  --rule-type TAKE_PROFIT --trigger-price 115000
```

### 第4步：创建一个策略来监控交易策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy --key-id <KEY_ID> \
  --name "BTC Perp Momentum" \
  --config '{
    "instruments": [
      { "id": "BTC", "type": "perp", "venue": "hyperliquid" }
    ],
    "thesis": {
      "estimate": 115000,
      "direction": "long",
      "confidence": 0.7,
      "reasoning": "ETF inflows accelerating, halving supply shock imminent"
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
      "autoActions": { "stopLoss": -0.10, "takeProfit": 0.25, "trailingStop": -0.05 },
      "sizing": { "method": "edgeScaled", "maxPosition": 500, "maxPortfolioPct": 20, "maxTradesPerDay": 5 }
    }
  }' \
  --poll-interval 10
```

### 第5步：激活并监控

```bash
npx @vincentai/cli@latest trading-engine activate --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID>
```

---

## 后台工作进程

交易引擎运行两个独立的后台工作进程：

1. **策略引擎工作进程** — 每30秒运行一次，检查哪些策略的驱动因素需要更新，获取新数据，对信号进行评分，并在达到升级阈值时调用LLM。它连接到Polymarket和HyperLiquid的WebSocket数据流，以实时评估价格触发条件。
2. **交易规则工作进程** — 通过WebSocket实时监控价格（带有轮询备份），评估止损/止盈/跟踪止损规则，并在条件满足时执行交易。支持Polymarket和HyperLiquid两种交易场所。

**断路器机制：** 两个工作进程都使用断路器模式。如果某个交易场所的API连续失败5次以上，工作进程会暂停并在冷却后恢复。状态检查命令如下：

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
```

## 最佳实践

1. **从`confidence: 0.5`开始**，让LLM进行调整——避免对初始策略过于自信
2. **根据重要性对驱动因素进行加权** — 权重为`3.0`的驱动因素的信号贡献是权重为`1.0`的三倍
3. **使用`edgeScaled`来根据策略的置信度和利润空间动态调整头寸规模**
4. **设置`maxPortfolioPct`来限制风险暴露** — 即使是高置信度的策略也不应冒险投资整个投资组合
5. **为头寸设置止损和止盈**（通过配置中的`autoActions`或独立规则）
6. **使用`thesisInvalidation`退出规则**来定义应触发头寸退出的明确条件
7. **监控调用费用** — 定期检查费用
8. **通过版本迭代** — 复制策略来微调配置而不丢失原始设置
9. **不要将触发条件设置得太接近当前价格** — 市场噪声可能导致过早触发

## 用户示例命令

当用户说：

- **“创建一个监控AI代币的策略”** → 创建一个使用网络搜索+Twitter驱动因素的策略
- **“设置40美分的止损”** → 创建一个STOP_LOSS规则
- **“我的策略表现如何？”** → 显示策略的调用记录
- **“我的策略表现如何？”** → 显示性能指标
- **“交易引擎花费了我多少钱？”** → 显示费用汇总
- **“暂停我的策略”** → 暂停策略
- **“创建一个具有不同策略的版本”** → 复制策略，然后更新草稿
- **“设置5%的跟踪止损”** → 创建一个TRAILING_STOP规则

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

LLM调用日志条目：

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

| 错误                       | 原因                                             | 解决方案                                           |
| --------------------------- | ------------------------------------------------- | ---------------------------------------------------- |
| `401 Unauthorized`          | API密钥无效或缺失                         | 确认密钥ID是否正确；如有需要请重新链接                 |
| `403 Policy Violation`      | 交易被服务器端策略阻止                         | 用户必须在heyvincent.ai调整策略                         |
| `402 Insufficient Credit`   | LLM调用所需的信用不足                         | 用户必须在heyvincent.ai增加信用                         |
| `INVALID_STATUS_TRANSITION` | 策略无法转换到请求的状态                         | 检查当前状态（例如，只有DRAFT状态可以激活）                 |
| `CIRCUIT_BREAKER_OPEN`      | Polymarket API失败导致断路器触发                     | 等待冷却时间；使用状态检查命令                         |
| `429 Rate Limited`          | 请求过多或LLM调用并发次数过多                         | 等待并重试                         |
| Key not found`             | API密钥被撤销或从未创建                         | 从钱包所有者处重新获取新的令牌                         |

## 重要说明

- **授权：** 所有端点都需要相关交易场所的API密钥（Polymarket或HyperLiquid钱包密钥）
- **仅限本地访问：** API监听在`localhost:19000` — 仅能从同一VPS访问
- **不使用私钥：** 所有交易都使用Vincent的API — 您的私钥安全地保存在Vincent的服务器上
- **策略执行**：所有交易（包括LLM和独立规则）都经过Vincent的政策检查
- **幂等性：** 规则只触发一次。LLM调用会根据驱动因素的状态进行去重