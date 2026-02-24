---
name: zonein
version: 2.0.0
description: 通过 Zonein API，您可以追踪和分析在 Hyperliquid 和 Polymarket 上胜率超过 75% 的顶级交易者。同时，您可以轻松创建用于 Hyperliquid 和 Polymarket 的交易代理程序。整个交易过程实现自动化，但过程中仍会有人工干预（即人类操作员参与决策）。
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz/pm\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---
# Zonein — 智能资金情报

使用配套脚本从Polymarket和HyperLiquid智能资金钱包获取实时交易情报。

## 设置（凭据）

### 获取您的API密钥

1. 访问 **https://app.zonein.xyz/pm**
2. 用您的账户登录（注册需要推荐码）
3. 点击 **“获取API密钥”** 按钮
4. 复制您的API密钥（以 `zn_` 开头）

### 在OpenClaw中设置API密钥

**选项A — Gateway Dashboard（推荐）：**
1. 打开您的 **OpenClaw Gateway Dashboard**
2. 转到侧边栏的 **`/skills`**
3. 在工作区技能中找到 **“zonein”** → 点击 **启用**
4. 输入您的 `ZONEIN_API_KEY` 并保存

**选项B — 环境变量：**
```bash
export ZONEIN_API_KEY="zn_your_key_here"
```

**选项C — 脚本也会自动从 `~/.openclaw/openclaw.json` 中读取**（技能条目 `zonein.apiKey`）。

## 快速参考

| 用户询问... | 命令 |
|-------------|---------|
| “市场发生了什么？” | `signals --limit 5` + `perp-signals --limit 5` |
| “显示政治相关的Polymarket信号” | `signals --categories POLITICS --limit 10` |
| “鲸鱼投资者在加密货币上做了什么？” | `perp-signals --limit 10` |
| “本周Polymarket的顶级交易者” | `leaderboard --period WEEK --limit 10` |
| “哪些币种被智能资金看多？” | `perp-coins` |
| “本月表现最佳的智能资金交易者” | `perp-top --period month --limit 10` |
| “跟踪钱包0x...” | `trader 0x...` 或 `perp-trader 0x...` |
| “智能资金流向哪里？” | `signals --limit 10` + `perp-signals --limit 10` + `perp-coins` |
| “创建一个交易代理” | 遵循代理创建流程（步骤1–6） |
| “列出我的代理” | `agents` |
| “我的代理表现如何？” | `agent-stats <id>` + `agent-trades <id>` |
| “停止我的代理” | `agent-disable <id>` |
| “有哪些代理类型可用？” | `agent-templates` |
| “检查我的代理余额” | `agent-balance <id>` |
| “我的代理持有哪些头寸？” | `agent-positions <id>` |
| “如何为我的代理充值？” | `agent-deposit <id>`，然后发送USDC，接着 `agent-fund <id>` 将资金桥接到Hyperliquid |
| “开立100美元的BTC多头头寸” | `agent-open <id> --coin BTC --direction LONG --size 100` |
| “关闭我的ETH头寸” | `agent-close <id> --coin ETH` |
| “提取我的资金” | `agent-disable <id>` 然后 `agent-withdraw <id> --to 0x...` |
| “对BTC进行回测” | `agent-backtest <id> --symbol BTC --days 30` |
| “显示过去的回测结果” | `agent-backtests <id>` |

## 命令

**展示规则：**
- 以自然、易读的语言展示结果。美观地格式化数字、表格和摘要。
- 如果用户请求查看原始JSON或实际命令，您可以展示它们。

**仅读命令（无需询问即可安全运行）：**
`signals`, `leaderboard`, `consensus`, `trader`, `perp-signals`, `perp-traders`, `perp-top`, `perp-categories`, `perp-coins`, `perp-trader`, `agents`, `agent-get`, `agent-stats`, `agent-trades`, `agent-vault`, `agent-templates`, `agent-assets`, `agent-categories`, `agent-balance`, `agent-positions`, `agent-deposit`, `agent-orders`, `agent-backtests`, `status`

**会改变状态的命令（运行前需询问用户 — 需要 `--confirm` 标志）：**
`agent-create`, `agent-update`, `agent-disable`, `agent-pause`, `agent-delete`

**财务命令（需要 `--confirm` 标志 — 脚本会拒绝执行）：**
`agent-fund`, `agent-open`, `agent-close`, `agent-withdraw`, `agent-enable`, `agent-deploy`, `agent-backtest`

在运行任何会改变状态或财务的命令之前，必须先获得用户的批准。
对于财务命令，只有在用户明确同意后，才在命令后添加 `--confirm`。

**示例 — 用户充值USDC并询问余额：**
- 您运行：`agent-balance <id>`（仅读，安全 — 无需 `--confirm`）
- 您看到：`arbitrum_usdc: 200, needs_funding: true`
- 您告诉用户：“您的Arbitrum钱包中有200 USDC，但尚未桥接到Hyperliquid。您希望我现在就进行桥接以便您的代理可以开始交易吗？”
- 用户同意 → 您运行：`agent-fund <id> --confirm`
- 如果没有 `--confirm`，脚本将拒绝执行并返回错误

所有命令都使用配套的Python脚本。**始终使用这些命令 — 切勿编写内联API调用。**

前缀：`python3 skills/zonein/scripts/zonein.py`

**Polymarket (PM)**

### `signals` — Polymarket智能资金交易信号

| 参数 | 类型 | 默认值 | 可选值 | 描述 |
|-------|------|---------|--------|-------------|
| `--limit` | int | 20 | 1–100 | 返回的最大信号数量 |
| `--categories` | str | all | `POLITICS,CRYPTO,SPORTS,CULTURE,ECONOMICS,TECH,FINANCE` | 逗号分隔的过滤条件 |
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | 回顾周期 |
| `--min-wallets` | int | 3 | 达到共识的最小智能钱包数量 |

### `leaderboard` — 按利润和损失（PnL）排名的Polymarket顶级交易者

| 参数 | 类型 | 默认值 | 可选值 | 描述 |
|-------|------|---------|--------|-------------|
| `--period` | str | WEEK | `DAY`, `WEEK`, `MONTH`, `ALL` | 排名周期 |
| `--category` | str | OVERALL | `OVERALL`, `POLITICS`, `SPORTS`, `CRYPTO`, `CULTURE`, `ECONOMICS`, `TECH`, `FINANCE` | 类别过滤条件 |
| `--limit` | int | 20 | 返回的最大交易者数量 |

### `consensus` — 智能投注者达成共识的Polymarket头寸

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `--min-bettors` | int | 达成共识的最小投注者数量 |

### `trader` — 按钱包查看的Polymarket交易者资料

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `wallet` | str | 是 | Polymarket钱包地址（0x...） |

**Perpetuals (HyperLiquid)**

### `perp-signals` — HyperLiquid的永久性交易信号

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `--limit` | int | 返回的最大信号数量 |
| `--min-wallets` | int | 达到共识的最小钱包数量 |
| `--min-score` | float | 最小交易者可信度得分（0–100） |

### `perp-traders` — 智能资金交易者

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `--limit` | int | 返回的最大交易者数量 |
| `--min-score` | float | 最小交易者得分（0–100） |
| `--categories` | str | all | 逗号分隔：`swing_trading`, `large_cap_trader`, `high_win_rate`, `scalper` 等 |

### `perp-top` | 按利润和损失（PnL）排名的顶级智能资金交易者

| 参数 | 类型 | 默认值 | 可选值 | 描述 |
|-------|------|---------|--------|-------------|
| `--limit` | int | 最大交易者数量 | 1–100 |
| `--period` | str | month | `day`, `week`, `month` | PnL排名周期 |

### `perp-coins` — 智能资金持有的币种分布（多头 vs 短头）

无参数。返回所有被智能资金持有的币种。

### `perp-categories` | 智能资金交易者类别列表

无参数。

### `perp-trader` | 按地址查看的智能资金交易者详情

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `address` | str | 是 | HyperLiquid钱包地址（0x...） |

**代理管理**

### `agents` | 列出您的交易代理

无参数。

### `agent-get` | 获取代理的完整配置和状态

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID（例如 `agent_abc12345` |

### `agent-create` | 创建新的交易代理

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `--name` | str | 必填 | 代理显示名称 |
| `--type` | str | composite | `composite`, `momentum_hunter`, `stable_grower`, `precision_master`, `whale_follower`, `scalping_pro`, `swing_trader` |
| `--assets` | str | BTC,ETH | 逗号分隔：`BTC,ETH,SOL,HYPE` |
| `--categories` | str | 自动从类型确定 | 逗号分隔的智能资金类别 |
| `--leverage` | int | 5 | 最大杠杆（1–20） |
| `--description` | str | 自动 | 代理描述 |
| `--risk-per-trade` | float | 每笔交易的风险百分比 |
| `--max-daily-loss` | float | 最大每日损失百分比 |
| `--risk-reward` | str | 风险：回报比率 |
| `--max-trades-per-day` | int | 每天的最大交易数量 |
| `--min-confidence` | float | 最小LLM置信度（0–1） |
| `--min-consensus` | float | 最小智能资金共识（0–1） |

### `agent-update` | 更新代理配置

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `agent_id` | str | 代理ID |
| `--name` | 新名称 |
| `--assets` | str | 逗号分隔的资产 |
| `--categories` | str | 逗号分隔的类别 |
| `--leverage` | int | 最大杠杆 |
| `--methodology` | str | 交易方法文本 |
| `--entry-strategy` | str | 入场策略文本 |
| `--exit-framework` | str | 出场框架文本 |
| `--strength-thresholds` | json | 每种资产的入场/出场阈值（见《强度阈值指南》） |
| `--timeframe-weights` | json | 时间框架权重分布 |

### `agent-deploy` | 验证配置并启用交易

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 要部署的代理 |

### `agent-enable` / `agent-disable` / `agent-pause` | 代理生命周期控制

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

### `agent-delete` | 删除代理（软删除）

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

### `agent-stats` | 绩效统计（利润和损失，胜率）

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

### `agent-trades` | 交易历史

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `agent_id` | str | 必填 | 代理ID |
| `--limit` | int | 返回的最大交易数量 |

### `agent-vault` | 交易钱包（vault）信息

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

返回：`account_value`, `withdrawable`, `has_positions`, `vault_address`。

### `agent-positions` | 来自Hyperliquid的开放头寸

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

返回每个头寸：`coin`, `side`（多头/空头），`size`, `entry_price`, `unrealized_pnl`, `leverage`, `notional`。

### `agent-deposit` | 获取代理的充值地址

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

返回：`deposit_address`（向此地址发送USDC到Arbitrum One）。

### `agent-fund` | 将USDC从Arbitrum桥接到Hyperliquid

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |

在向Arbitrum上的钱包地址发送USDC后，调用此命令以自动将资金桥接到Hyperliquid。
**重要提示：** 桥接交易需要Arbitrum上的一小笔ETH作为gas费用（通常约为0.0001–0.0005 ETH）。请用户向Arbitrum One上的同一钱包地址发送少量ETH（例如0.001 ETH）后再运行此命令。
返回 `tx_hash` 和 `amount`（桥接的金额）。

### `agent-open` | 通过聊天手动开立头寸

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |
| `--coin` | str | 是 | BTC, ETH, SOL, HYPE |
| `--direction` | str | 否（默认为LONG） | 多头或空头 |
| `--size` | float | 是 | 头寸大小（以USD计） |
| `--leverage` | int | 否 | 杠杆（1–20） |

### `agent-close` | 关闭头寸

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |
| `--coin` | str | 是 | 要关闭的币种（BTC, ETH, SOL, HYPE） |

### `agent-orders` | 手动订单历史

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `agent_id` | str | 必填 | 代理ID |
| `--limit` | int | 返回的最大订单数量 |

### `agent-withdraw` | 将资金提取到您的钱包

| 参数 | 类型 | 必填 | 描述 |
|-------|------|----------|-------------|
| `agent_id` | str | 是 | 代理ID |
| `--to` | str | 是 | 目标0x...钱包地址（在Arbitrum上） |

在提取资金之前，必须先 **禁用** 代理。流程：Hyperliquid → Arbitrum → 您的钱包。

### `agent-backtest` | 运行回测模拟

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `agent_id` | str | 必填 | 代理ID |
| `--symbol` | str | BTC | 回测的币种：BTC, ETH, SOL, HYPE |
| `--days` | int | 30 | 回测周期（7–90天） |
| `--initial-balance` | float | 10000 | 开始余额（以USD计） |

使用代理的配置（阈值、杠杆、风险配置）针对缓存的智能资金信号和真实的OHLC价格运行历史回测。返回性能摘要以及包含交互式图表（股票曲线、带交易标记的蜡烛图、每日PnL、交易表格）的 **仪表板链接**。

**需要 `--confirm`**（这是一个计算密集型操作）。

### `agent-backtests` | 列出过去的回测结果

| 参数 | 类型 | 默认值 | 描述 |
|-------|------|---------|-------------|
| `agent_id` | str | 必填 | 代理ID |
| `--limit` | int | 最大结果数量 |

返回之前回测的结果列表，包括摘要指标和仪表板链接。

### `agent-templates` | 代理类型及默认配置

无参数。返回可用的代理类型及其类别预设和默认风险/交易配置。

### `agent-assets` | 可用的交易资产

无参数。返回：BTC, ETH, SOL, HYPE。

### `agent-categories` | 智能资金类别及实时统计数据

无参数。返回所有类别及其描述和实时交易者数量。

**实用工具**

### `status` | 检查API密钥状态

无参数。

## 操作流程

### 🤖 代理创建流程

当用户想要创建交易代理时，请遵循以下对话流程：

**步骤1：收集偏好**
询问用户的交易目标：
- 您想交易哪些币种？（BTC, ETH, SOL, HYPE）
- 您的风险承受能力如何？（保守、中等、激进）
- 交易风格是什么？（炒单、波段交易、趋势跟随、平衡）
- 杠杆是多少？（1x–20x）
- 最大每日损失容忍度是多少？（1%–10%）

**步骤2：显示可用选项**
运行以下命令以提供用户参考：
1. `agent-templates` — 显示可用的代理类型
2. `agent-categories` — 显示带有统计数据的智能资金类别
3. `agent-assets` — 显示可用的币种

**步骤3：创建代理**
根据收集的偏好创建代理：
```
agent-create --name "BTC Swing Trader" --type swing_trader --assets BTC,ETH --leverage 5 --risk-per-trade 1 --max-daily-loss 3 --risk-reward 1:2 --max-trades-per-day 3 --min-confidence 0.8 --min-consensus 0.7
```

**步骤4：配置策略**
使用交易策略提示更新代理：
```
agent-update <agent_id> --methodology "Follow smart money signals..." --entry-strategy "Enter on SM consensus >70%..." --exit-framework "Take profit at +10%, stop loss at -5%..."
```

**步骤5：审查并部署**
1. `agent-get <agent_id>` — 查看完整配置
2. `agent-deploy <agent_id>` — 验证并启用

**步骤6：为代理充值**
代理的充值地址会自动创建。创建响应中包含该地址。
1. 向用户显示创建响应中的充值地址（或使用 `agent-deposit <agent_id>`）
2. 告诉用户：“请将USDC发送到Arbitrum One上的此地址。”
3. `agent-balance <agent_id>` — 检查 `arbitrum_usdc` 字段以确认资金已到账
4. 告诉用户：“同时向Arbitrum One上的同一钱包地址发送少量ETH（约0.001 ETH）作为gas费用。”
5. `agent-fund <agent_id> --confirm` — 将USDC从Arbitrum桥接到Hyperliquid（需要ETH作为gas）
6. `agent-balance <agent_id>` — 确认Hyperliquid上的 `account_value` 显示资金已到账

**步骤7：监控**
- `agent-balance <agent_id>` — 检查钱包余额
- `agent-positions <agent_id>` — 查看开放头寸
- `agent-stats <agent_id>` — 查看绩效（利润和损失）
- `agent-trades <agent_id>` — 查看交易历史
- `agent-disable <agent_id>` — 如有需要，停止交易

### 💰 充值与提取流程

**充值：**
1. `agent-deposit <agent_id>` — 获取钱包地址
2. 用户向Arbitrum One上的钱包地址发送USDC
3. `agent-balance <agent_id>` — 检查 `arbitrum_usdc` 以确认资金已到账
4. 用户还需向同一钱包地址发送少量ETH（约0.001 ETH）作为gas费用
5. `agent-fund <agent_id> --confirm` — 将USDC从Arbitrum桥接到Hyperliquid（需要ETH作为gas）
6. `agent-balance <agent_id>` — 确认Hyperliquid上的 `account_value` 显示资金已到账

**提取：**
1. `agent-disable <agent_id>` — 必须先禁用代理
2. `agent-withdraw <agent_id> --to 0xYourWallet...` — 提交提取请求
3. 系统处理：Hyperliquid → Arbitrum → 您的钱包

### 📊 通过聊天管理头寸

当用户想要查看头寸或手动交易时：

**查看头寸：**
`agent-positions <agent_id>` — 显示每个头寸：“BTC多头 — 以$95,432的价格开立了500美元的头寸 — 盈利：+23.45美元 — 杠杆5倍”

**开立头寸：**
`agent-open <agent_id> --coin BTC --direction LONG --size 100 --leverage 5 --confirm`

**关闭头寸：**
`agent-close <agent_id> --coin BTC --confirm`

**查看订单状态：**
`agent-orders <agent_id>`

### 市场概览**

当用户询问市场状况时，按顺序运行以下命令：
1. `signals --limit 5` — 最重要的Polymarket信号
2. `perp-signals --limit 5` — 最重要的智能资金信号
3. `perp-coins` — 币种的多头/空头情绪
4. 总结：哪些市场有强烈的共识，哪些币种受到鲸鱼投资者的看涨/看跌影响

### 交易信号

1. 询问：需要预测市场信号、智能资金信号，还是两者都需要？
2. 运行相关命令
3. 按共识强度排序显示顶级信号
4. 解释每个信号，例如：“前100名交易者都认为‘BTC会达到100,000美元吗？’ — 当前价格为42c”

### 跟踪钱包

1. `trader <wallet>` — Polymarket交易者资料
2. `perp-trader <address>` — HyperLiquid交易者资料
3. 显示：绩效、开放头寸、胜率

## 强度阈值指南

`strength_thresholds` 和 `timeframe_weights` 在创建代理时根据 `agent_type` 自动生成。如果用户需要自定义值，可以使用 `agent-update` 进行覆盖。

### 用户可以控制的参数

- **min_strength_buy**：开立头寸所需的智能资金信号强度（数值越高，选择越严格，交易越少）
- **min_strength_sell**：关闭头寸所需的相反方向信号强度（数值越低，退出越快，跟随趋势越强）

### 根据用户偏好自定义的默认值

| 用户设置 | 调整内容 | 示例 |
|-----------|---------------|---------|
| “我想要更多的交易” / 激进 | 降低 `min_strength_buy`（-5至-10） | BTC买入：78 -> 70 |
| “只选择高质量的信号” / 保守 | 提高 `min_strength_buy`（+5） | BTC买入：78 -> 83 |
| “快速止损” / 保护资本 | 降低 `min_strength_sell`（-5） | 卖出：72 -> 65 |
| “让盈利头寸持续持有” / 跟随趋势 | 提高 `min_strength_sell`（+5） | 卖出：72 -> 77 |

### 验证规则

1. 所有值必须 **≥ 55**（最低要求）
2. **OTHERS >= max(BTC, ETH, SOL)**（其他代币波动性更大，需要更强的信号）
3. 通常的排序顺序：BTC <= ETH <= SOL <= OTHERS（买入阈值）

**正确示例：**
- BTC买入70, ETH买入75, SOL买入78, OTHERS买入78（>= 最大值）

**错误示例：**
- BTC买入70, OTHERS买入68 — 错误！OTHERS的值应低于BTC！

### 时间框架权重

总和必须为 **1.0**。三个时间框架：24h, 4h, 1h。

| 用户偏好 | 24h | 4h | 1h | 原因 |
|----------------|-----|----|----|-----|
| 快速交易 / 炒单 | 0.2 | 0.4 | 专注于短期信号 |
| 波段交易 / 多日交易 | 0.5 | 0.35 | 专注于长期趋势 |
| 跟随趋势 | 0.4 | 0.4 | 平衡趋势和波动性 |
| “我跟随每日趋势” | 0.6 | 0.3 | 重点关注24小时内的趋势 |

### 覆盖命令

```
agent-update <agent_id> --strength-thresholds '{"BTC": {"min_strength_buy": 70, "min_strength_sell": 65}, "ETH": {"min_strength_buy": 75, "min_strength_sell": 65}, "SOL": {"min_strength_buy": 80, "min_strength_sell": 65}, "OTHERS": {"min_strength_buy": 80, "min_strength_sell": 65}}' --timeframe-weights '{"24h": 0.5, "4h": 0.35, "1h": 0.15}'
```

## 输出字段

### Polymarket信号
- `direction` — 是/否
- `consensus` — 0到1（1表示所有人都同意）
- `total_wallets` — 持有该头寸的智能交易者数量
- `best_rank` — 最佳排行榜位置
- `cur_yes_price` / `cur_no_price` — 当前价格

### 智能资金信号
- `coin` — 代币（BTC, ETH, SOL, HYPE...）
- `direction` — 多头或空头
- `consensus` — 共识比率（0-1）
- `long_wallets` / `short_wallets` — 每侧的交易者数量
- `long_value` / `short_value` — 每侧的交易金额（以USD计）
- `best_trader_score` — 交易者可信度得分

### 时间段和类别
- **Polymarket时间段：** DAY, WEEK, MONTH, ALL
- **Polymarket类别：** OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, ECONOMICS, TECH, FINANCE
- **智能资金时间段：** day, week, month

## 如何展示结果

### Polymarket信号
```
🔮 [market_title]
Smart money says: [YES/NO] | Agreement: [X]%
[N] top traders holding | Best ranked: #[rank]
Current price: YES [price] / NO [price]
```

### 智能资金信号
```
📊 $[COIN]
Smart money says: [LONG/SHORT] | Agreement: [X]%
[N] whale traders | Top score: [score]
Long: $[X] | Short: $[X]
```

## 安全与隐私

**免责声明：**
- 信号显示了智能资金的行为 — 但不保证结果
- 过去的表现不能预测未来的结果
- 切勿投资超过您能承受的损失
- 始终使用配套脚本。切勿使用curl或内联Python编写原始API调用。

**外部端点：** `https://mcp.zonein.xyz/api/v1/*` — API密钥（X-API-Key头）+ 查询参数。

**数据与访问：**
- 只有您的API密钥会离开系统（作为 `X-API-Key` 头发送）
- 除了密钥和查询参数外，不会发送任何个人数据
- **读取的本地文件：** `~/.openclaw/openclaw.json`（仅作为API密钥的备用）。不会访问其他本地文件
- **写入的本地文件：** 无
- 脚本 **仅** 连接到 `https://mcp.zonein.xyz/api/v1` — 不会安装其他端点，也不会写入文件系统

**确认政策：** 财务命令（`agent-fund`, `agent-open`, `agent-close`, `agent-withdraw`, `agent-deploy`, `agent-enable`, `agent-backtest`）是 **程序控制的** — 除非明确传递 `--confirm`，否则脚本不会执行。代理必须先征求用户同意，然后在用户同意后添加 `--confirm`。这可以防止提示被注入并绕过确认流程。

使用此技能时，您的API密钥和查询参数会被发送到 `https://mcp.zonein.xyz`。只有在您信任Zonein的情况下才进行安装。

## 链接

- **仪表板：** https://app.zonein.xyz/pm/
- **智能资金仪表板：** https://app.zonein.xyz/perp/
- **API文档：** https://mcp.zonein.xyz/docs