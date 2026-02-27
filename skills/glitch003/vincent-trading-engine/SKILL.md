---
name: Vincent - Trading Engine for agents
description: >
  针对 Polymarket 的策略驱动型自动化交易功能：当用户需要创建交易策略、设置止损/止盈/跟踪止损规则或管理自动化交易时，可以使用此技能。该功能支持以下事件触发：  
  - “交易策略”（Trading Strategy）  
  - “止损”（Stop Loss）  
  - “止盈”（Take Profit）  
  - “跟踪止损”（Trailing Stop）  
  - “自动化交易”（Automated Trading）  
  - “交易引擎”（Trading Engine）  
  - “交易规则”（Trade Rules）  
  - “策略监控”（Strategy Monitoring）
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
# Vincent交易引擎 - 基于策略的自动化交易

使用此技能可以创建和管理用于Polymarket预测市场的自动化交易策略。该交易引擎结合了数据监控（网络搜索、Twitter、价格推送）和基于大语言模型（LLM）的决策制定功能，根据您的交易策略自动执行交易。它还包含了独立的止损、止盈和跟踪止损规则，这些规则无需LLM的支持即可运行。

所有命令均使用`@vincentai/cli`包。

## 工作原理

**交易引擎是一个具有两种模式的统一系统：**

1. **基于LLM的策略** — 创建一个带有监控功能的策略版本（网络搜索关键词、Twitter账户、价格触发器、新闻推送）。当监控器检测到新信息时，LLM（通过OpenRouter使用Claude）会评估这些信息，并决定是进行交易、设置保护性订单还是向您发出警报。
2. **独立的交易规则** — 为头寸设置止损、止盈和跟踪止损规则。当价格条件满足时，这些规则会自动执行——无需LLM的参与。

**架构：**
- 集成到Vincent后端（无需单独的服务运行）
- 策略端点位于 `/api/skills/polymarket/strategies/...`
- 交易规则端点位于 `/api/skills/polymarket/rules/...`
- 使用与Polymarket技能相同的API密钥
- 所有交易都通过Vincent的政策执行流程
- LLM的费用会从用户的信用余额中扣除
- 每次LLM调用都会记录完整的审计追踪（令牌、费用、操作、持续时间）

## 安全模型

- **LLM无法绕过政策** — 所有交易都必须通过 `polymarketSkill.placeBet()`，该函数会执行支出限制、审批阈值和白名单检查
- **后端LLM密钥** — OpenRouter API密钥不会离开服务器。代理和用户无法直接调用LLM
- **信用限制** — 如果信用余额不足，则无法调用LLM
- **工具限制** — LLM可用的工具由策略的 `config.tools` 设置控制。如果 `canTrade: false`，则不提供交易工具
- **速率限制** — 限制同时进行的LLM调用次数，以防止费用过高
- **审计追踪** — 每次调用都会记录完整的提示、响应、操作和费用
- **无需私钥** — 交易引擎使用Vincent的API进行所有交易。私钥保存在Vincent的服务器上

## 第1部分：基于LLM的策略

### 策略生命周期

策略遵循一个版本化的生命周期：`DRAFT` → `ACTIVE` → `PAUSED` → `ARCHIVED`

- **DRAFT**：可以编辑。尚未开始监控或调用LLM。
- **ACTIVE**：监控器正在运行。新数据会触发LLM的调用。
- **PAUSED**：监控已停止。可以恢复。
- **ARCHIVED**：永久停止。无法重新激活。

要迭代一个策略，可以复制它创建一个新的版本（创建一个具有递增版本号和相同配置的新DRAFT）。

### 创建策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy \
  --key-id <KEY_ID> \
  --name "AI Token Momentum" \
  --alert-prompt "AI tokens are about to re-rate as funding accelerates. Buy dips in AI-related prediction markets. Sell if the thesis breaks." \
  --poll-interval 15 \
  --web-keywords "AI tokens,GPU shortage,AI funding" \
  --twitter-accounts "@DeepSeek,@nvidia,@OpenAI" \
  --newswire-topics "artificial intelligence,GPU,semiconductor" \
  --can-trade \
  --can-set-rules \
  --max-trade-usd 50
```

**参数：**
- `--name`：策略的友好名称
- `--alert-prompt`：您给LLM的指令和提示。这是最重要的部分——明确指出哪些信息重要以及应采取什么行动。
- `--poll-interval`：定期检查监控器的频率（以分钟为单位）（默认：15分钟）
- `--web-keywords`：用于Brave网络搜索监控的关键词，用逗号分隔
- `--twitter-accounts`：用于监控的Twitter账户，用逗号分隔（包括或不包括@符号）
- `--newswire-topics`：用于Finnhub市场新闻监控的关键词，用逗号分隔（任何匹配关键词的头条都会触发LLM）
- `--can-trade`：允许LLM进行交易（省略则仅限于发送警报）
- `--can-set-rules`：允许LLM创建止损/止盈/跟踪止损规则
- `--max-trade-usd`：LLM每次交易的最大USD金额

### 列出策略

```bash
npx @vincentai/cli@latest trading-engine list-strategies --key-id <KEY_ID>
```

### 查看策略详情

```bash
npx @vincentai/cli@latest trading-engine get-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 激活策略

开始监控和LLM调用。策略必须处于DRAFT状态。

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

注意：`resume`命令在内部使用与`activate`相同的命令端点，暂停到激活的转换由服务器处理。

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

查看策略的LLM决策日志——哪些数据触发了它，LLM做出了什么决定，采取了哪些行动，以及费用是多少。

```bash
npx @vincentai/cli@latest trading-engine invocations --key-id <KEY_ID> --strategy-id <STRATEGY_ID> --limit 20
```

### 查看费用摘要

查看某个策略的所有LLM费用的汇总。

```bash
npx @vincentai/cli@latest trading-engine costs --key-id <KEY_ID>
```

### 监控配置

#### 网络搜索监控器

在创建策略时添加 `--web-keywords`。引擎会定期在Brave中搜索这些关键词，并在新结果出现时触发LLM。

```bash
--web-keywords "AI tokens,GPU shortage,prediction market regulation"
```

每个关键词都会被独立搜索。结果会被去重——相同的URL不会被多次触发LLM。

#### Twitter监控器

在创建策略时添加 `--twitter-accounts`。引擎会定期检查这些账户的新推文，并在新推文出现时触发LLM。

```bash
--twitter-accounts "@DeepSeek,@nvidia,@OpenAI"
```

推文会通过推文ID去重——只有真正新的推文才会触发LLM。

#### 新闻推送监控（Finnhub）

在创建策略时添加 `--newswire-topics`。引擎会定期查询Finnhub的市场新闻API（包括一般和加密类别），并在匹配主题关键词的头条出现时触发LLM。

```bash
--newswire-topics "artificial intelligence,GPU shortage,semiconductor"
```

每个主题字符串可以包含逗号分隔的关键词。头条和摘要会不区分大小写地进行匹配。文章会根据主题哈希值进行去重，每个主题最多保留100条记录。

**注意：**需要在服务器上设置 `FINNHUB_API_KEY` 环境变量。Finnhub的免费 tier允许每分钟60次API调用——对于策略监控来说绰绰有余。每次调用不会扣除信用。

#### 价格触发器

价格触发器在策略的JSON配置中设置，并通过Polymarket的WebSocket推送实时评估。当价格条件满足时，会调用LLM。

触发类型：
- `ABOVE` — 当价格超过阈值时触发
- `BELOW` — 当价格低于阈值时触发
- `CHANGE_PCT` — 当价格相对于参考价格变化百分比时触发

价格触发器是一次性的：一旦触发，它们就会被标记为已使用。如果需要，LLM可以创建新的触发器。

### 警报提示的最佳实践

警报提示是您给LLM的指令。好的提示应该是：

1. **明确策略内容**：“我认为AI代币将会上涨，因为GPU需求正在增加。购买任何价格低于40美分的AI相关预测市场头寸。”
2. **明确行动标准**：“只有当新信息直接支持或反驳你的策略时才进行交易。如果信息不明确，就向我发出警报。”
3. **明确风险**：“永远不要在一个头寸上投入超过50美元。为任何新头寸设置15%的跟踪止损。”
4. **具有上下文性**：“忽略常规的公司公告。关注监管行动、重大产品发布和竞争威胁。”

### LLM可用工具

当LLM被调用时，它可以使用以下工具（取决于策略配置）：

| 工具 | 描述 | 是否需要 |
|---|---|---|
| `place_trade` | 买入或卖出头寸 | `canTrade: true` |
| `set_stop_loss` | 为头寸设置止损规则 | `canSetRules: true` |
| `set_take_profit` | 设置止盈规则 | `canSetRules: true` |
| `set_trailing_stop` | 设置跟踪止损 | `canSetRules: true` |
| `alert_user` | 发送警报但不进行交易 | 始终可用 |
| `no_action` | 不采取任何行动（并给出理由） | 始终可用 |

### 费用跟踪

每次LLM调用都会被计量：
- **令牌费用**：输入和输出令牌的价格根据模型的费率计算
- **从信用余额中扣除**：与数据源信用（`dataSourceCreditUsd`）来自同一个池
- **预飞行检查**：如果信用不足，调用将被跳过并记录
- **数据源费用**：Brave搜索（约0.005美元/次）和Twitter（约0.005-0.01美元/次）也会被计量。Finnhub新闻推送调用是免费的（不扣除信用）

典型的LLM调用费用：根据上下文的不同，费用在0.05至0.30美元之间。

---

## 第2部分：独立的交易规则

当价格条件满足时，交易规则会自动执行——无需LLM的参与。这些规则与原始的Trade Manager中的止损、止盈和跟踪止损规则相同，现在统一在Trading Engine的命名空间下。

### 检查工作进程状态

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
# Returns: worker status, active rules count, last sync time, circuit breaker state
```

### 创建止损规则

如果价格跌低于阈值，自动卖出头寸：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type STOP_LOSS --trigger-price 0.40
```

**参数：**
- `--market-id`：来自市场数据的Polymarket条件ID
- `--token-id`：您持有的结果令牌ID（来自市场数据）
- `--rule-type`：`STOP_LOSS`（如果价格 <= 触发器则卖出），`TAKE_PROFIT`（如果价格 >= 触发器则卖出），或 `TRAILING_STOP`
- `--trigger-price`：价格阈值，范围在0到1之间（例如，0.40表示40美分）

### 创建止盈规则

如果价格涨高于阈值，自动卖出头寸：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TAKE_PROFIT --trigger-price 0.75
```

### 创建跟踪止损规则

跟踪止损会随着价格上涨而调整止损价格：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TRAILING_STOP --trigger-price 0.45 --trailing-percent 5
```

**跟踪止损的行为：**
- `--trailing-percent` 是百分比（例如 `5` 表示5%）
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
- `RULE CREATED` — 规则被创建
- `RULE_TRAILING_UPDATED` — 跟踪止损的触发价格上升
- `RULE_evalUATED` — 工作进程根据当前价格检查了规则
- `RULE_TRIGGERED` — 触发条件被满足
- `ACTION_PENDING_APPROVAL` — 交易需要人工批准，规则暂停
- `ACTION_EXECUTED` — 交易成功执行
- `ACTION_FAILED` — 交易执行失败
- `RULE_CANCELED` — 规则被手动取消

### 规则状态

- `ACTIVE` — 规则正在运行并被监控
- `TRIGGERED` — 条件被满足，交易已执行
- `PENDING_APPROVAL` — 交易需要人工批准；规则暂停
- `CANCELED` — 在触发前被手动取消
- `FAILED` — 触发但交易执行失败

---

## 完整工作流程：策略 + 交易规则

### 第1步：使用Polymarket技能下注

```bash
npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456789 --side BUY --amount 10 --price 0.55
```

### 第2步：创建一个监控策略的策略

```bash
npx @vincentai/cli@latest trading-engine create-strategy --key-id <KEY_ID> \
  --name "Bitcoin Bull Thesis" \
  --alert-prompt "Bitcoin is likely to break $100k on ETF inflows. Buy dips, sell if ETF outflows accelerate." \
  --web-keywords "bitcoin ETF inflows,bitcoin institutional" \
  --twitter-accounts "@BitcoinMagazine,@saborskycnbc" \
  --can-trade --can-set-rules --max-trade-usd 25 --poll-interval 10
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
```

## 后台工作进程

交易引擎运行两个独立的后台工作进程：

1. **策略引擎工作进程** — 每30秒运行一次，检查哪些策略的监控器需要更新数据，当检测到新数据时调用LLM。同时连接到Polymarket的WebSocket以实时评估价格触发器。
2. **交易规则工作进程** — 通过WebSocket实时监控价格（带有回退机制），评估止损/止盈/跟踪止损规则，并在条件满足时执行交易。

**断路器：** 两个工作进程都使用断路器模式。如果Polymarket API连续失败5次以上，工作进程会暂停并在冷却后恢复。状态检查使用：

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
```

## 最佳实践

1. **先从仅发送警报开始** — 初始时设置 `canTrade: false`，以查看LLM的行为
2. **使用具体的警报提示** — 模糊的提示会导致模糊的决策。明确您的策略和行动标准
3. **为头寸设置止损和止盈** 以提供保护
4. **监控调用费用** — 定期检查 `cost` 命令
5. **通过版本迭代** — 复制策略来微调提示或监控器，同时保留原始设置
6. **不要将触发器设置得离当前价格太近** — 市场噪声可能会导致过早触发

## 用户示例提示

当用户说：
- **“创建一个监控AI代币的策略”** → 创建一个包含网络搜索和Twitter监控器的策略
- **“设置40美分的止损”** → 创建一个STOP_LOSS规则
- **“我的策略在做什么？”** → 显示该策略的调用记录
- **“交易引擎花费了我多少钱？”** → 显示费用摘要
- **“暂停我的策略”** → 暂停策略
- **“用不同的提示创建一个新版本”** → 复制策略，然后更新草稿
- **“设置5%的跟踪止损”** → 创建一个TRAILING_STOP规则

## 输出格式

策略创建：

```json
{
  "strategyId": "strat-123",
  "name": "AI Token Momentum",
  "status": "DRAFT",
  "version": 1
}
```

规则创建：

```json
{
  "ruleId": "rule-456",
  "ruleType": "STOP_LOSS",
  "triggerPrice": 0.40,
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

| 错误 | 原因 | 解决方案 |
|-------|-------|------------|
| `401 Unauthorized` | API密钥无效或缺失 | 确认密钥ID是否正确；如有需要，请重新链接 |
| `403 Policy Violation` | 交易被服务器端政策阻止 | 用户必须在heyvincent.ai调整政策 |
| `402 Insufficient Credit` | LLM调用所需的信用不足 | 用户必须在heyvincent.ai添加信用 |
| `INVALID_STATUS_TRANSITION` | 策略无法转换到请求的状态 | 检查当前状态（例如，只有DRAFT状态可以激活） |
| `CIRCUIT_BREAKER_OPEN` | Polymarket API失败触发了断路器 | 等待冷却时间；使用 `status` 命令检查状态 |
| `429 Rate Limited` | 请求过多或同时进行的LLM调用次数过多 | 等待并重试 |
| `Key not found` | API密钥被吊销或从未创建 | 从钱包所有者处重新获取新的令牌 |

## 重要说明

- **授权：** 所有端点都需要使用与Polymarket技能相同的Polymarket API密钥
- **仅限本地访问**：API监听在 `localhost:19000` — 仅可以从同一VPS访问
- **无需私钥**：所有交易都使用Vincent的API — 您的私钥安全地保存在Vincent的服务器上
- **政策执行**：所有交易（包括LLM和独立规则）都经过Vincent的政策检查
- **幂等性**：规则只触发一次。LLM调用会根据监控器的状态进行去重

---

## 第3部分：V2多场所策略

V2扩展了交易引擎，支持多场所交易，包括基于驱动程序的监控系统、策略跟踪、6层信号处理流程、高级头寸调整和升级策略。V2策略可以在任何支持的场所进行交易（不仅仅是Polymarket）。

### V2相比V1新增的功能

| 功能 | V1 | V2 |
|---|---|---|
| 场所 | 仅限Polymarket | 多场所（驱动程序 `sources` + 场所适配器） |
| 监控 | 网络搜索、Twitter、新闻推送、价格触发器 | 基于驱动程序：带有实体、关键词、嵌入锚点的加权驱动程序 |
| 策略 | 警报提示（自由文本） | 结构化策略：估计、方向、置信度、理由 |
| 信号处理流程 | 监控器 → LLM | 6层：摄取 → 过滤 → 评分 → 升级 → LLM → 执行 |
| 头寸调整 | 固定最大交易金额 | 根据边缘规模、固定金额或Kelly标准进行调整，同时考虑投资组合限制 |
| 交易规则 | 独立的规则 | 集成的自动行动（止损、止盈、跟踪止损、价格差触发器） |
| 通知 | 无 | 交易或策略变化时通过Webhook或Slack通知 |

### 核心概念

- **工具**：场所上的可交易资产。由 `id`、`type`（股票、期货、掉期、期权）、`venue` 和可选的约束条件（杠杆、保证金、流动性、费用）定义。
- **策略**：您的方向性观点 — `estimate`（目标价格/价值）、`direction`（多头/空头/中性）、`confidence`（0–1）和 `reasoning`。
- **驱动程序**：提供信号的处理程序。每个驱动程序都有一个 `weight`、`direction`（看涨/看跌/上下文相关）和 `monitoring` 配置（实体、关键词、嵌入锚点、来源、轮询间隔）。
- **升级策略**：控制LLM何时被唤醒。`signalScoreThreshold`（批量处理的最低分数）、`highConfidenceThreshold`（触发立即唤醒的分数）、`maxWakeFrequency`（例如“每15分钟一次”）、`batchWindow`（例如“5分钟”）。
- **交易规则**：入场规则（最小边缘、订单类型）、退出规则（策略无效的触发条件）、自动行动（止损、止盈、跟踪止损、价格差触发器）和调整规则（方法、最大头寸、投资组合百分比、每日最大交易数量）。

### 策略生命周期

与V1相同的状态：`DRAFT` → `ACTIVE` → `PAUSED` → `ARCHIVED`

### 创建V2策略

```bash
npx @vincentai/cli@latest v2 create-strategy \
  --key-id <KEY_ID> \
  --name "BTC Multi-Venue Momentum" \
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
- `--config`：完整的V2StrategyConfig JSON（参见上述核心概念的结构）
- `--data-source-secret-id`：可选的DATA_SOURCES秘密，用于驱动程序监控API调用
- `--poll-interval`：驱动程序监控的轮询间隔（以分钟为单位）（默认：15分钟）

### V2策略管理

```bash
# List all V2 strategies
npx @vincentai/cli@latest v2 list-strategies --key-id <KEY_ID>

# Get strategy details
npx @vincentai/cli@latest v2 get-strategy --key-id <KEY_ID> --strategy-id <ID>

# Update a DRAFT strategy (pass only fields to change)
npx @vincentai/cli@latest v2 update-strategy --key-id <KEY_ID> --strategy-id <ID> \
  --name "Updated Name" --config '{ "thesis": { ... } }'

# Activate (DRAFT → ACTIVE)
npx @vincentai/cli@latest v2 activate --key-id <KEY_ID> --strategy-id <ID>

# Pause (ACTIVE → PAUSED)
npx @vincentai/cli@latest v2 pause --key-id <KEY_ID> --strategy-id <ID>

# Resume (PAUSED → ACTIVE)
npx @vincentai/cli@latest v2 resume --key-id <KEY_ID> --strategy-id <ID>

# Archive (permanent)
npx @vincentai/cli@latest v2 archive --key-id <KEY_ID> --strategy-id <ID>
```

### 投资组合与监控

```bash
# Portfolio overview (positions + balances across all venues)
npx @vincentai/cli@latest v2 portfolio --key-id <KEY_ID>

# Signal log — raw signals from drivers
npx @vincentai/cli@latest v2 signal-log --key-id <KEY_ID> --strategy-id <ID> --limit 50

# Decision log — LLM thesis updates and trade decisions
npx @vincentai/cli@latest v2 decision-log --key-id <KEY_ID> --strategy-id <ID> --limit 50

# Trade log — order execution results
npx @vincentai/cli@latest v2 trade-log --key-id <KEY_ID> --strategy-id <ID> --limit 50

# Performance metrics (P&L, win rate, per-instrument breakdown)
npx @vincentai/cli@latest v2 performance --key-id <KEY_ID> --strategy-id <ID>

# Filter stats — signals passed/dropped at each pipeline layer
npx @vincentai/cli@latest v2 filter-stats --key-id <KEY_ID> --strategy-id <ID>

# Escalation stats — wake frequency, batch counts, threshold breaches
npx @vincentai/cli@latest v2 escalation-stats --key-id <KEY_ID> --strategy-id <ID>
```

### 手动覆盖

```bash
# Place a manual order on any venue
npx @vincentai/cli@latest v2 place-order --key-id <KEY_ID> \
  --instrument-id <TOKEN_ID> --venue polymarket \
  --side BUY --size 10 --order-type market

# Place a limit order
npx @vincentai/cli@latest v2 place-order --key-id <KEY_ID> \
  --instrument-id <TOKEN_ID> --venue polymarket \
  --side BUY --size 10 --order-type limit --limit-price 0.45

# Cancel an order
npx @vincentai/cli@latest v2 cancel-order --key-id <KEY_ID> \
  --venue polymarket --order-id <ORDER_ID>

# Close a position (opposite-side market order)
npx @vincentai/cli@latest v2 close-position --key-id <KEY_ID> \
  --instrument-id <TOKEN_ID> --venue polymarket

# Emergency kill switch — pause all strategies + cancel all orders
npx @vincentai/cli@latest v2 kill-switch --key-id <KEY_ID>
```

### 信号处理流程架构

V2策略通过6层处理流程处理信息：

1. **摄取** — 来自驱动程序来源的原始数据（网络搜索、Twitter、新闻推送、价格推送、RSS、Reddit、链上数据、文件、期权流）
2. **过滤** — 去重和相关性过滤。丢弃已经看到或质量低于阈值的信号
3. **评分** — 根据驱动程序的权重、与嵌入锚点的相似度以及实体/关键词的匹配程度，对每个信号进行评分（0–1）
4. **升级** — 根据升级策略，将评分信号分批处理。低分信号会在批次窗口中累积；高分信号会立即触发LLM
5. **LLM** — LLM根据当前的策略评估分批处理的信号。它可以更新策略、发出交易决策、更新驱动程序的状态或不采取任何行动
6. **执行** — 交易决策经过政策检查后，会被路由到适当的场所适配器进行执行

### V2的最佳实践

1. **从 `confidence: 0.5` 开始**，让LLM进行调整 — 避免对初始策略过于自信
2. **根据重要性对驱动程序进行加权** — 权重为 `3.0` 的驱动程序对信号评分的贡献是权重为 `1.0` 的三倍
3. **使用 `edgeScaled` 来根据策略的置信度和边缘情况调整头寸大小**
4. **设置 `maxPortfolioPct` 以限制风险** — 即使是高置信度的策略也不应冒险投资整个投资组合
5. **监控 `filter-stats` 以调整升级策略** — 如果太多信号被批量处理而没有行动，降低 `signalScoreThreshold`；如果LLM唤醒过于频繁，提高该阈值
6. **使用 `thesisInvalidation` 退出规则** 来定义应触发头寸退出的明确条件
7. **使用紧急停止开关** — 在紧急情况下，它可以暂停所有策略并取消所有未完成的订单

### 用户示例提示（V2）

当用户说：
- **“创建一个针对BTC的多场所策略”** → 创建一个包含工具和策略的V2策略
- **“显示我在各个场所的投资组合情况”** → 调用v2投资组合功能
- **“显示信号处理流程的活动情况”** → 调用信号日志和过滤统计
- **“LLM做出了什么决定？”** **调用决策日志**
- **“我的策略表现如何？”** **调用性能评估**
- **“手动下达买入订单”** **调用v2下单功能**
- **“紧急停止所有操作”** **调用v2紧急停止功能**
- **“暂停我的V2策略”** **调用v2暂停功能**