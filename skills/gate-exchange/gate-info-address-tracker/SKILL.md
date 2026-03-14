---
name: gate-info-addresstracker
version: "2026.3.12-1"
updated: "2026-03-12"
description: "地址追踪与分析功能：当用户提供链上地址或请求追踪/查询某个地址时，可使用此功能。相关触发语句包括：“追踪此地址”、“该地址的拥有者是谁”、“资金流动情况”、“检查地址”。MCP工具包括：`info_onchain_get_address_info`、`info_onchain_get_address_transactions`、`info_onchain_trace_fund_flow`。"
---
# gate-info-addresstracker

> 这是一个基于链上的地址查询工具。用户输入一个链上地址后，系统会首先调用地址信息工具（address info Tool）来获取该地址的详细信息，然后根据用户的查询意图（是简单查询还是资金追踪）来决定是否需要进一步调用交易历史记录和资金流动追踪工具。

**触发场景**：用户提供了一个链上地址（格式为 0x... / bc1... / T...），或者明确表示想要追踪或查询某个地址。

---

## 路由规则

| 用户意图 | 关键词/模式 | 执行操作 |
|-------------|-----------------|--------|
| 查询地址信息 | “这个地址归谁所有” “检查 0x...” | 执行此工具（基本模式） |
| 追踪资金流动 | “追踪” “资金流向” “这笔钱去了哪里” | 执行此工具（深度追踪模式） |
| 代币链上分析 | “ETH 代币分析” “哪些智能资金在购买” | 路由到 `gate-info-tokenonchain` |
| 地址风险检查 | “这个地址安全吗” “这是黑名单地址吗” | 路由到 `gate-info-riskcheck` |
| 单笔交易查询 | “这笔交易是什么” “解码这笔交易” | 直接调用 `info_onchain_get_transaction` |
| 实体/机构追踪 | “跳转至交易持有者” “这个机构的地址” | 路由到 `gate-info-whaletracker` |

---

## 执行流程

### 第一步：意图识别与参数提取

从用户输入中提取以下信息：
- `address`：链上地址（系统会自动检测地址格式）
- `chain`（可选）：链的类型（如 ETH、BSC、TRX、BTC 等；通常可以从地址格式中推断出来）
- `intent_depth`：用户的查询意图深度
  - `basic`：仅询问“这是谁的地址”或“他们持有多少资产”
  - `deep`：请求追踪资金流动或查看交易记录

**自动地址格式检测**：

| 地址前缀 | 推断的链类型 |
|---------------|----------------|
| `0x` | Ethereum（默认；也可能是 BSC、Polygon、Arbitrum 或其他 EVM 链） |
| `bc1` / `1` / `3` | Bitcoin |
| `T` | Tron |
| 其他 | 提示用户指定链的类型 |

### 第二步：获取地址基本信息（必需）

| 步骤 | 使用的工具 | 参数 | 获取的数据 |
|------|----------|------------|----------------|
| 1 | `info_onchain_get_address_info` | `address={address}, chain={chain}, scope="with_defi"` | 地址的基本信息：余额、标签、风险评分、DeFi 持有情况、盈亏情况 |

### 第三步：决策判断

```
get_address_info response
    │
    ├── User only wants a simple query (intent_depth = basic)
    │   └── → Output address profile report directly (skip to Step 5)
    │
    └── User requests deep tracking (intent_depth = deep)
        └── → Proceed to Step 4 parallel calls
```

**自动升级到深度模式的条件**：
- 地址具有特定的标签（例如交易所、黑客、大户等） → 可能需要进一步调查
- 地址余额超过 100 万美元
- 地址存在风险标志

### 第四步：深度追踪（条件性触发）

| 步骤 | 使用的工具 | 参数 | 获取的数据 | 是否并行执行 |
|------|----------|------------|----------------|----------|
| 2a | `info_onchain_get_address_transactions` | `address={address}, chain={chain}, min_value_usd=10000, limit=20` | 大额交易（金额超过 1 万美元） | 是 |
| 2b | `info_onchain_trace_fund_flow` | `start_address={address}, chain={chain}, depth=3, min_value_usd=100000` | 资金流动追踪（深度为 3 层，金额超过 10 万美元） | 是 |

> 这两个工具会同时执行。`min_value_usd` 的阈值会根据地址的规模进行动态调整。

**阈值调整逻辑**：

| 地址总余额 | `info_onchain_get_address_transactions` 的最低金额阈值 | `info_onchain_trace_fund_flow` 的最低金额阈值 |
|----------------------|--------------------------------------------------|-----------------------------------------|
| < 10 万美元 | 1,000 美元 | 10,000 美元 |
| 10 万至 100 万美元 | 10,000 美元 | 100,000 美元 |
| 100 万至 1,000 万美元 | 1,000,000 美元 | 1,000,000 美元 |
| 超过 1,000 万美元 | 1,000,000 美元 | 1,000,000 美元 |

### 第五步：结果整合

---

## 报告模板

### 基本模式

```markdown
## Address Analysis Report

> Address: `{address}`
> Chain: {chain}
> Query time: {timestamp}

### 1. Address Profile

| Metric | Value |
|--------|-------|
| Address Label | {label} (e.g., Exchange Hot Wallet / Whale / Unknown / Hacker-linked) |
| Risk Score | {risk_score}/100 ({Low Risk/Medium Risk/High Risk}) |
| First Transaction | {first_tx_time} |
| Total Transactions | {tx_count} |
| Current Balance | ${total_balance_usd} |

### 2. Asset Holdings

| Token | Amount | Value (USD) | Share |
|-------|--------|-------------|-------|
| {token_1} | {amount} | ${value} | {pct}% |
| {token_2} | ... | ... | ... |
| ... | ... | ... | ... |

**Holding Characteristics**: {LLM analyzes the holding structure, e.g., "Highly concentrated in ETH", "Diversified across multiple DeFi tokens", "Possible market maker"}

### 3. DeFi Positions (if available)

| Protocol | Type | Amount | Status |
|----------|------|--------|--------|
| {protocol} | {Lending/LP/Staking} | ${value} | {Healthy/Near Liquidation} |
| ... | ... | ... | ... |

### 4. PnL Summary (if available)

| Metric | Value |
|--------|-------|
| Realized PnL | ${realized_pnl} |
| Unrealized PnL | ${unrealized_pnl} |
| Win Rate | {win_rate}% |
```

### 深度追踪模式（在基本模式基础上添加更多信息）

```markdown
### 5. Large Transaction History

> Filter: Amount > ${min_value_usd} | Most recent {count} transactions

| Time | Type | Amount | Counterparty | Counterparty Label |
|------|------|--------|--------------|-------------------|
| {time} | {In/Out/Contract Interaction} | ${value} | `{counterparty}` | {label/unknown} |
| ... | ... | ... | ... | ... |

**Transaction Pattern Analysis**:
{LLM analyzes transaction records and identifies patterns:}
- Frequent interactions with an exchange → likely depositing/withdrawing
- Large one-way outflows → possibly liquidating
- Interacting with many new addresses → possibly dispersing funds
- Regular fixed-amount transfers → possibly payroll/OTC

### 6. Fund Flow Tracing

> Trace depth: {depth} levels | Minimum amount: ${min_value_usd}

```
{地址} （来源）
  ├── {金额} → {地址_1} ({标签_1})
  │     ├── {金额} → {地址_1a} ({标签})
  │     └── {金额} → {地址_1b} ({标签})
  ├── {金额} → {地址_2} ({标签_2})
  │     └── {金额} → {地址_2a} ({标签})
  └── {金额} → {地址_3} ({标签_3})
```

**Fund Flow Analysis**:
{LLM analysis based on tracing results:}
- Ultimate destination of funds (exchange? mixer? DeFi protocol?)
- Any suspicious patterns (split transfers, circular transfers, obfuscation paths)
- Associated known entities

### ⚠️ Risk Warnings

{If the address has risk flags, prominently display:}
- ⚠️ This address is flagged as: {risk_label}
- ⚠️ Associated addresses involved in: {risk_detail}
```

---

## 决策逻辑

| 条件 | 评估结果 |
|-----------|------------|
| 风险评分 > 70 | 高风险地址 — 提醒用户谨慎操作 |
| 风险评分 40-70 | 中等风险 — 存在某些风险因素 |
| 风险评分 < 40 | 低风险 |
| 持有集中在某一种代币上超过 80% | 标记为“高度集中持有” |
| DeFi 借贷健康状况 < 1.2 | 接近清算状态 |
| 过去 24 小时内资金流出超过总余额的 50% | 标记为“近期有大额资金流出” |
| 资金流动中包含混币器地址 | 标记为“涉及混币器——高风险” |
| 资金流动中包含受 OFAC 制裁的地址 | 标记为“与受制裁地址有关” |
| 资金追踪结果为空 | 可能是新地址或交易量不足 — 按常规处理 |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| 地址格式无效 | 提示用户检查地址格式，并提供正确的格式示例 |
| 无法识别链类型 | 提示用户指定链的类型（例如：“这个地址是在哪个链上？ETH/BSC/TRX/BTC...”） |
| `info_onchain_get_address_info` 返回空结果 | 可能是新地址或没有链上活动；通知用户 |
| `info_onchain_trace_fund_flow` 无法使用（第一阶段） | 告知用户“资金追踪功能仍在开发中”；仅显示交易历史记录 |
| `info_onchain_get_address_transactions` 超时 | 降低请求限额并重试，或仅显示地址基本信息 |
| 所有工具均失败 | 返回错误信息；建议用户稍后再试 |

---

## 跨技能路由

| 用户后续操作 | 路由到 |
|-----------------------|----------|
| “这个地址安全吗？” | `gate-info-riskcheck` |
| “该代币的链上数据” | `gate-info-tokenonchain` |
| “哪个机构拥有这个地址？” | `gate-info-whaletracker` |
| “帮我分析 XX 代币” | `gate-info-coinanalysis` |
| “为什么会有大量资金流出？” | `gate-news-eventexplain` |

---

## 安全规则

1. **隐私保护**：不要将链上地址与特定个人关联（除非该地址被公开标记为机构地址）
2. **明确的风险提示**：高风险地址必须带有明显且易于理解的风险标签及原因说明
3. **避免使用绝对性词汇**：避免使用“犯罪地址”或“非法资金”等词汇，使用客观的描述（如“标记为高风险”或“与可疑活动有关”）
4. **数据来源透明**：必须注明数据来源（如 BlockInfo、Nansen、Arkham）
5. **缺失数据的处理**：资金追踪功能将分阶段推出；如果数据缺失，需明确告知用户
6. **防止滥用**：如果用户试图追踪多个个人地址以进行骚扰，应提示用户合理使用该工具