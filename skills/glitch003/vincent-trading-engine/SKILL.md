# Vincent交易引擎 - 基于策略的自动化交易

使用此技能可以创建和管理用于Polymarket预测市场的自动化交易策略。该交易引擎结合了数据监控（网络搜索、Twitter、价格推送）与基于大型语言模型（LLM）的决策机制，根据您的交易策略自动执行交易。它还包含了独立的止损、止盈和跟踪止损规则，这些规则无需LLM的支持即可运行。

所有命令均使用`@vincentai/cli`包。

## 工作原理

**交易引擎是一个具有两种模式的统一系统：**

1. **基于LLM的策略** — 创建一个带有监控功能的策略版本（包括网络搜索关键词、Twitter账户、价格触发器、新闻推送）。当监控器检测到新信息时，LLM（通过OpenRouter使用Claude）会评估这些信息，并决定是进行交易、设置保护性订单还是向您发出警报。
2. **独立的交易规则** — 为持仓设置止损、止盈和跟踪止损规则。当价格条件满足时，这些规则会自动执行——无需LLM的参与。

**架构：**
- 集成到Vincent后端中（无需单独运行服务）
- 策略端点位于`/api/skills/polymarket/strategies/...`
- 交易规则端点位于`/api/skills/polymarket/rules/...`
- 使用与Polymarket技能相同的API密钥
- 所有交易都通过Vincent的政策检查流程
- LLM的费用会从用户的信用余额中扣除
- 每次LLM调用都会被记录下来，包括完整的审计追踪信息（令牌、费用、操作、持续时间）

## 安全模型

- **LLM无法绕过政策** — 所有交易都必须通过`polymarketSkill.placeBet()`进行，该函数会执行支出限制、审批阈值和白名单检查
- **后端LLM密钥** — OpenRouter API密钥不会离开服务器。代理和用户无法直接调用LLM
- **信用限制** — 信用余额不足时，LLM无法被调用
- **工具限制** — LLM可用的工具由策略的`config.tools`设置控制。如果`canTrade: false`，则不提供交易工具
- **速率限制** — 限制LLM的最大并发调用次数，以防止费用失控
- **审计追踪** — 每次调用都会记录下完整的提示、响应、操作和费用
- **无需私钥** — 交易引擎使用Vincent的API进行所有交易。私钥保存在Vincent的服务器上

## 第一部分：基于LLM的策略

### 策略生命周期

策略遵循一个版本化的生命周期：`DRAFT` → `ACTIVE` → `PAUSED` → `ARCHIVED`

- **DRAFT**：可以编辑。尚未开始监控或调用LLM。
- **ACTIVE**：监控器正在运行。新数据会触发LLM的调用。
- **PAUSED**：监控已停止。可以恢复。
- **ARCHIVED**：永久停止。无法重新激活。

要对策略进行迭代，可以复制它以创建一个新版本（创建一个新的DRAFT版本，版本号递增，并保持相同的配置）。

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
- `--name`：策略的用户友好名称
- `--alert-prompt`：您给LLM的指令和提示。这是最重要的部分——明确指出哪些信息重要以及应采取什么行动。
- `--poll-interval`：定期检查监控器的频率（以分钟为单位）（默认值：15）
- `--web-keywords`：用于Brave网络搜索的关键词，用逗号分隔
- `--twitter-accounts`：用于监控的Twitter账户，用逗号分隔（包含或不包含@符号）
- `--newswire-topics`：用于Finnhub市场新闻监控的关键词，用逗号分隔（任何匹配关键词的标题都会触发LLM）
- `--can-trade`：允许LLM进行交易（省略此参数则仅限于发送警报）
- `--can-set-rules`：允许LLM创建止损/止盈/跟踪止损规则
- `--max-trade-usd`：LLM每次交易的最大允许金额（单位：美元）

### 列出策略

```bash
npx @vincentai/cli@latest trading-engine list-strategies --key-id <KEY_ID>
```

### 查看策略详情

```bash
npx @vincentai/cli@latest trading-engine get-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 激活策略

开始监控并调用LLM。策略必须处于DRAFT状态。

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

**注意：**`resume`命令在内部使用与`activate`相同的命令端点，暂停到激活的转换由服务器处理。

### 归档策略

永久停止策略。无法撤销。

```bash
npx @vincentai/cli@latest trading-engine archive --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 复制策略（新版本）

创建一个具有相同配置的新DRAFT版本，并附有父版本的链接。

```bash
npx @vincentai/cli@latest trading-engine duplicate-strategy --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看版本历史

查看策略的所有版本记录。

```bash
npx @vincentai/cli@latest trading-engine versions --key-id <KEY_ID> --strategy-id <STRATEGY_ID>
```

### 查看LLM调用历史

查看策略的LLM决策日志——哪些数据触发了它，LLM做出了什么决定，采取了哪些行动，以及费用是多少。

```bash
npx @vincentai/cli@latest trading-engine invocations --key-id <KEY_ID> --strategy-id <STRATEGY_ID> --limit 20
```

### 查看费用汇总

查看某个策略的所有LLM费用汇总。

```bash
npx @vincentai/cli@latest trading-engine costs --key-id <KEY_ID>
```

### 监控配置

#### 网络搜索监控器

在创建策略时添加`--web-keywords`。引擎会定期在Brave中搜索这些关键词，并在新结果出现时触发LLM。

```bash
--web-keywords "AI tokens,GPU shortage,prediction market regulation"
```

每个关键词都会被独立搜索。结果会被去重——相同的URL不会被多次触发LLM。

#### Twitter监控器

在创建策略时添加`--twitter-accounts`。引擎会定期检查这些账户的新推文，并在新推文出现时触发LLM。

```bash
--twitter-accounts "@DeepSeek,@nvidia,@OpenAI"
```

推文会通过推文ID去重——只有真正新的推文才会触发LLM。

#### 新闻推送监控（Finnhub）

在创建策略时添加`--newswire-topics`。引擎会定期查询Finnhub的市场新闻API（涵盖一般和加密货币类别），并在出现符合主题关键词的新标题时触发LLM。

```bash
--newswire-topics "artificial intelligence,GPU shortage,semiconductor"
```

每个主题字符串可以包含逗号分隔的关键词。标题和摘要会不区分大小写地进行匹配。文章会根据标题哈希进行去重，每个主题最多保留100条记录。

**注意：**需要在服务器上设置`FINNHUB_API_KEY`环境变量。Finnhub的免费 tier允许每分钟60次API调用——这对于策略监控来说绰绰有余。每次调用不会扣除信用费用（Finnhub免费 tier没有费用）。

#### 价格触发器

价格触发器在策略的JSON配置中设置，并通过Polymarket的WebSocket推送实时评估。当价格条件满足时，会调用LLM并传递价格数据。

触发器类型：
- `ABOVE` — 当价格超过阈值时触发
- `BELOW` — 当价格低于阈值时触发
- `CHANGE_PCT` — 当价格相对于参考价格变化了一定百分比时触发

价格触发器是一次性的：一旦触发，它们就会被标记为已使用。如果需要，LLM可以创建新的触发器。

### 警报提示的最佳实践

警报提示是您给LLM的指令。好的提示应该：
1. **明确策略内容**：“我认为AI代币将会上涨，因为GPU需求在增加。购买任何价格低于40美分的AI相关预测市场持仓。”
2. **明确行动标准**：“只有当新信息直接支持或反驳你的策略时才进行交易。如果信息模糊，请发送警报。”
3. **明确风险**：“永远不要在单个持仓上投入超过50美元。为任何新持仓设置15%的跟踪止损。”
4. **具有上下文性**：“忽略常规的公司公告。关注监管行动、重大产品发布和竞争威胁。”

### LLM可用工具

当LLM被调用时，它可以使用以下工具（取决于策略配置）：

| 工具 | 描述 | 是否需要 |
|---|---|---|
| `place_trade` | 买入或卖出持仓 | `canTrade: true` |
| `set_stop_loss` | 为持仓设置止损规则 | `canSetRules: true` |
| `set_take_profit` | 设置止盈规则 | `canSetRules: true` |
| `set_trailing_stop` | 设置跟踪止损 | `canSetRules: true` |
| `alert_user` | 发送警报但不进行交易 | 始终可用 |
| `no_action` | 什么都不做（并附上理由） | 始终可用 |

### 费用跟踪

每次LLM调用都会被记录费用：
- **令牌费用**：输入和输出令牌的费用根据模型费率计算
- **从信用余额中扣除**：与数据源费用（`dataSourceCreditUsd`）来自同一池
- **预检查**：如果信用不足，调用将被跳过并记录
- **数据源费用**：Brave搜索（每次调用约0.005美元）和Twitter（每次调用约0.005-0.01美元）也会被记录。Finnhub新闻推送调用是免费的（不扣除费用）

典型的LLM调用费用：根据上下文的不同，费用在0.05美元到0.30美元之间。

---

## 第二部分：独立的交易规则

交易规则在价格条件满足时自动执行——无需LLM的参与。这些规则包括原始交易管理器中的止损、止盈和跟踪止损规则，现在统一在交易引擎的命名空间下。

### 检查工作进程状态

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
# Returns: worker status, active rules count, last sync time, circuit breaker state
```

### 创建止损规则

如果价格跌至阈值以下，自动卖出持仓：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type STOP_LOSS --trigger-price 0.40
```

**参数：**
- `--market-id`：Polymarket条件的ID（来自市场数据）
- `--token-id`：您持有的结果令牌的ID（来自市场数据）
- `--rule-type`：`STOP_LOSS`（如果价格≤触发价格则卖出），`TAKE_PROFIT`（如果价格≥触发价格则卖出），或`TRAILING_STOP`
- `--trigger-price`：价格阈值（介于0和1之间，例如0.40表示40美分）

### 创建止盈规则

如果价格升至阈值以上，自动卖出持仓：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TAKE_PROFIT --trigger-price 0.75
```

### 创建跟踪止损规则

跟踪止损规则会随着价格上涨而调整止损价格：

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --market-id 0x123... --token-id 456789 \
  --rule-type TRAILING_STOP --trigger-price 0.45 --trailing-percent 5
```

**跟踪止损的行为：**
- `--trailing-percent`表示百分比（例如`5`表示5%）
- 计算`candidateStop = currentPrice * (1 - trailingPercent/100)`
- 如果`candidateStop`大于当前的`triggerPrice`，则更新`triggerPrice`
- `triggerPrice`永远不会降低
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

### 查看被监控的持仓

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
- `RULE_TRAILING_UPDATED` — 跟踪止损的触发价格被上调
- `RULE_EVALUATED` — 工作进程根据当前价格检查了规则
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
- `FAILED` — 触发条件被满足，但交易执行失败

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
1. **策略引擎工作进程** — 每30秒运行一次，检查哪些策略的监控器需要更新数据，检测到新数据时调用LLM。同时通过Polymarket WebSocket实时评估价格触发条件。
2. **交易规则工作进程** — 通过WebSocket实时监控价格（如果WebSocket失败则使用轮询机制），评估止损/止盈/跟踪止损规则，并在条件满足时执行交易。

**断路器机制：** 两个工作进程都使用断路器模式。如果Polymarket API连续5次失败，工作进程会暂停并在冷却后重新启动。状态检查通过以下命令进行：

```bash
npx @vincentai/cli@latest trading-engine status --key-id <KEY_ID>
```

## 最佳实践

1. **先从仅发送警报开始** — 最初将`canTrade`设置为`false`，以查看LLM的行为，然后再启用自动交易
2. **使用具体的警报提示** — 模糊的提示会导致模糊的决策。明确您的策略和行动标准
3. **为持仓设置止损和止盈** 以提供保护
4. **监控调用费用** — 定期检查费用
5. **通过版本迭代** — 复制策略以调整提示或监控器设置，同时保留原始设置
6. **不要将触发器设置得太接近当前价格** — 市场波动可能会导致不必要的交易

## 用户示例提示

当用户说：
- **“创建一个监控AI代币的策略”** → 创建一个包含网络搜索和Twitter监控器的策略
- **“设置40美分的止损”** → 创建一个STOP_LOSS规则
- **“我的策略在做什么？”** → 查看策略的调用记录
- **“交易引擎花了多少钱？”** → 查看费用汇总
- **“暂停我的策略”** → 暂停策略
- **“使用不同的提示创建一个新版本”** **复制策略并更新草稿**
- **“设置5%的跟踪止损”** → 创建一个TRAILING_STOP规则

## 重要说明

- **授权：** 所有端点都需要使用与Polymarket技能相同的API密钥
- **仅限本地访问**：API监听地址为`localhost:19000` — 仅能从同一VPS访问
- **无需私钥**：所有交易都使用Vincent的API — 您的私钥安全地保存在Vincent的服务器上
- **政策执行**：所有交易（包括LLM和独立规则）都要经过Vincent的政策检查
- **幂等性**：规则只会触发一次。LLM的调用会根据监控器的状态进行去重。