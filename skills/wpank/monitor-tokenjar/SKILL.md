---
name: monitor-tokenjar
description: >-
  Monitor the Uniswap TokenJar with a real-time dashboard showing balances,
  accumulation rates, burn economics, and projected time to next profitable burn.
  Supports one-shot snapshot and streaming modes. Use when user asks "Watch the
  TokenJar", "Track fee accumulation", or "When is the next profitable burn?"
model: opus
allowed-tools:
  - Task(subagent_type:protocol-fee-seeker)
  - mcp__uniswap__get_tokenjar_balances
  - mcp__uniswap__get_firepit_state
  - mcp__uniswap__get_fee_accumulation_rate
  - mcp__uniswap__subscribe_tokenjar
  - mcp__uniswap__get_burn_history
  - mcp__uniswap__get_token_price
---

# 监控 TokenJar

## 概述

这是一个用于监控 Uniswap 协议费用系统的仪表板。TokenJar 会收集来自所有 Uniswap 源（V2、V3、V4、UniswapX 以及 Unichain 原生费用）的费用。该工具可以提供关于 TokenJar 中费用总量、费用增长速度以及下一次费用燃烧何时能够盈利的全面信息——这对于关注协议费用的人来说是最重要的信息。

该工具提供两种模式：**一次性查询**（包含分析结果）和**实时流式监控**（实时跟踪存款事件并更新数据）。

**为什么这个工具比单独使用其他工具好 10 倍：**

1. **可操作的预测结果**：核心输出是“下一次费用燃烧能够盈利的预计时间”——这一结果需要结合 TokenJar 的余额、UNI 的价格、gas 费用以及费用积累速率进行复合计算。没有任何单一工具能够提供这样的信息；手动计算则需要调用 4-5 个工具并自行进行计算。
2. **综合性的仪表板**：它不是简单地展示来自不同工具的原始 JSON 数据，而是提供了一个格式统一、包含余额、积累速率、费用燃烧机制以及历史数据的视图。该工具会交叉参考所有数据源，从而提供其他工具无法单独提供的洞察。
3. **实时流式监控**：原始的 `subscribe_tokenjar` 命令仅返回存款事件，但没有上下文信息。而该工具会为每个存款事件添加累计总额、更新的盈利预测以及在达到阈值时发出的警报，从而将原始数据转化为可操作的情报。
4. **历史数据支持**：仪表板还包含了最近的费用燃烧记录以及市场竞争情况，帮助用户了解系统的动态变化。

## 适用场景

当用户有以下需求时，可以使用该工具：
- “监控 TokenJar 的状态”
- “跟踪协议费用”
- “了解费用积累情况”
- “下一次费用燃烧何时能够盈利？”
- “显示 TokenJar 的分析结果”
- “费用积累的速度有多快？”
- “在费用燃烧盈利时提醒我”
- “查看 TokenJar 仪表板”
- “费用积累的速率是多少？”

**不适用场景**：
- 当用户需要执行费用燃烧操作时（请使用 `seek-protocol-fees` 工具）；
- 当用户需要对费用燃烧的经济情况進行深入的历史分析时（请使用 `analyze-burn-economics` 工具）。

## 参数

| 参数                | 是否必填 | 默认值 | 获取方式                                      |
|-------------------|--------|--------|-----------------------------------------|
| chain             | 否       | ethereum | TokenJar 始终使用以太坊主网数据                         |
| streaming           | 否       | false    | “watch”、“stream”、“live”、“real-time” 表示启用实时流式监控       |
| duration           | 否       | 60       | 流式监控的持续时间（以秒为单位，范围 1-300 秒）；例如：“监控 5 分钟”表示 300 秒 |
| alert-threshold-usd     | 否       | --       | 设置为 “50K” 时，系统会在 TokenJar 余额达到 50,000 美元时发出警报       |
| include-history     | 否       | true     | “Skip history” 或 “just current state” 表示不显示历史数据       |

## 工作流程

### 一次性查询模式（默认）

1. **并行数据收集**：为了提高效率，同时调用以下 MCP 函数：
   - `mcp__uniswap__get_tokenjar_balances` ：获取当前的 TokenJar 余额
   - `mcp__uniswap__get_firepit_state`：获取费用燃烧的阈值、随机数以及是否可以执行燃烧操作
   - `mcp__uniswap__get_fee_accumulation_rate`：获取每日/每周/每月的费用积累速率
   - `mcp__uniswap__get_burn_history`（如果设置了 `include-history`）：获取最近的费用燃烧记录

2. **综合分析**：将数据传递给 `Task(subagent_type:protocol-fee-seeker)` 进行进一步处理：

   ```
   Produce a TokenJar monitoring dashboard.

   Current data:
   - TokenJar balances: {from parallel calls}
   - Firepit state: threshold={threshold}, nonce={nonce}
   - Accumulation rates: {from parallel calls}
   - Recent burn history: {from parallel calls}

   Tasks:
   1. Price all TokenJar assets in USD using get_token_price.
   2. Calculate total jar value.
   3. Calculate current burn cost (threshold UNI * UNI price + gas estimate).
   4. Determine current profitability: jar value vs. burn cost.
   5. Using accumulation rates, project when the next burn will be profitable
      (if not already) or when ROI will exceed 10% (if already profitable).
   6. Summarize recent burn history: last burn date, frequency, average profit.
   7. Identify the top fee-generating tokens and any notable trends.

   Return a structured dashboard report.
   ```

3. **数据展示**：以仪表板的形式展示所有分析结果。

### 实时流式监控模式

1. **初始数据收集**：首先执行一次一次性查询，以建立基准数据。

2. **开始流式监控**：调用 `mcp__uniswap__subscribe_tokenjar` 并设置用户指定的监控时长：
   - 如果设置了 `alert-threshold-usd`，则需要使用 `minDepositUsd` 过滤条件。
   - 默认监控时长为 60 秒。

3. **处理存款事件**：对于接收到的每个存款事件：
   - 将存款的代币价格转换为美元
   - 更新 TokenJar 的累计总额
   - 根据新的总额重新计算盈利情况
   - 如果 TokenJar 的价值超过了费用燃烧的阈值，发出警报：“费用燃烧现在可以盈利！”

4. **最终总结**：监控结束后，展示更新后的仪表板内容，包括：
   - 监控期间发生的所有存款事件
   - 更新后的 TokenJar 总余额
   - 更新后的盈利预测

## 输出格式

### 一次性查询模式的仪表板输出

```text
TokenJar Dashboard (Ethereum)

  ══════════════════════════════════════
  CURRENT BALANCES
  ══════════════════════════════════════
  Token     Balance       USD Value    Share
  WETH      7.20          $18,000      34.6%
  USDC      15,000        $15,000      28.8%
  USDT      8,500         $8,500       16.3%
  WBTC      0.08          $6,400       12.3%
  DAI       4,100         $4,100       7.9%
  ──────────────────────────────────────
  Total                   $52,000      100%

  ══════════════════════════════════════
  ACCUMULATION RATES
  ══════════════════════════════════════
  Daily:    ~$7,400/day
  Weekly:   ~$51,800/week
  Monthly:  ~$222,000/month

  Top Contributors:
    WETH     ~$2,800/day  (37.8%)
    USDC     ~$2,100/day  (28.4%)
    USDT     ~$1,200/day  (16.2%)

  ══════════════════════════════════════
  BURN ECONOMICS
  ══════════════════════════════════════
  Burn Threshold:  4,000 UNI ($28,000)
  Gas Estimate:    ~$45
  Total Burn Cost: $28,045

  Current Jar:     $52,000
  Net Profit:      $23,955
  ROI:             85.4%
  Status:          PROFITABLE

  ══════════════════════════════════════
  RECENT HISTORY
  ══════════════════════════════════════
  Last Burn:       2026-02-03 (7 days ago)
  Burn Frequency:  ~every 5.2 days (avg last 10 burns)
  Avg Profit:      $18,400 per burn
  Nonce:           42

  ══════════════════════════════════════
  PROJECTION
  ══════════════════════════════════════
  Next 10% ROI:    Already exceeded (current: 85.4%)
  Next 100% ROI:   ~0.5 days at current rate
  Competitor Risk:  HIGH — avg burn interval is 5.2 days, currently at 7 days
```

### 实时流式监控的输出结果

```text
TokenJar Live Feed (streaming for 60s)

  Baseline: $52,000 across 5 assets

  [14:00:12] Deposit: 0.15 WETH ($375)  | Running Total: $52,375
  [14:00:28] Deposit: 500 USDC ($500)    | Running Total: $52,875
  [14:00:45] Deposit: 200 USDT ($200)    | Running Total: $53,075

  ──────────────────────────────────────
  Session Summary (60s)
  ──────────────────────────────────────
  Deposits:     3 events, $1,075 total
  Rate:         ~$64,500/hour (this session)
  Updated Total: $53,075
  Profitability: $25,030 net profit (89.3% ROI)
  Status:        PROFITABLE — ready to burn
```

### 警报输出（当达到阈值时）

```text
  ALERT: TokenJar value ($50,125) has crossed your alert threshold ($50,000).
  Current profitability: $22,080 net profit (78.7% ROI).
  Consider running: seek-protocol-fees
```

## 重要说明

- **仅用于数据读取**：该工具不会执行任何交易操作，仅负责读取数据并生成分析结果。如需执行费用燃烧操作，请使用 `seek-protocol-fees` 工具。
- **仅支持以太坊主网**：TokenJar 和 Firepit 都是运行在以太坊主网上的智能合约。
- **费用积累速率是估算值**：这些速率基于过去 7 天内的交易数据计算得出；实际速率可能会因协议流量和费用设置而变化。
- **实时流式监控的时长上限为 300 秒**：MCP 工具会自动限制监控时长。如需更长时间的监控，需要定期重新执行该工具。
- **市场竞争情况仅供参考**：费用燃烧的频率是根据链上数据估算的，实际燃烧时间可能随时发生变化。
- **UNI 价格波动会影响预测结果**：盈利预测基于稳定的 UNI 价格；如果 UNI 价格突然上涨，当前盈利的费用燃烧可能会变得无利可图。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|-------------------|-------------------------------------------------|-----------------------------------------|
| TokenJar 为空             | “TokenJar 为空，尚未积累到任何费用。”                         | 等待协议活动恢复后再进行监控                         |
| 无法获取积累数据           | “数据不足，无法计算费用积累速率。”                         | 增加数据收集的时间范围                         |
| 未找到费用燃烧记录         | “未找到费用燃烧记录，可能是新部署的合约。”                         | 设置 `include-history` 为 `false`                         |
| 流式监控超时             | “流式监控在 {duration} 秒后结束。”                         | 重新开始监控                         |
| 监控期间没有发生存款           | “在 {duration} 秒的监控期间未检测到任何存款。”                         | 增加监控时长或稍后再次尝试                         |
| 无法获取代币价格           | “无法获取 {token} 的价格，仪表板数据可能不完整。”                         | 可能是某些特殊或流动性较低的代币                     |
| RPC 连接失败             | “无法连接到以太坊的 RPC 服务，仪表板无法使用。”                         | 检查 RPC 配置                         |