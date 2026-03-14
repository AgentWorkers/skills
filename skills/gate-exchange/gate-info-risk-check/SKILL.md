---
name: gate-info-riskcheck
version: "2026.3.12-1"
updated: "2026-03-12"
description: "**令牌与地址风险评估**  
每当用户询问有关令牌、合约或地址安全性的问题时，请使用此技能进行评估。相关触发语句包括：  
“这个令牌安全吗？”、“请检查合约风险”，“这个地址安全吗？”，以及“蜜罐（honeypot）”和“ Rug（恶意交易）”等术语。  
**MCP 工具**：  
`info_compliance_check_token_security`、`info_coin_get_coin_info`  
**地址模式**：  
`info_onchain_get_address_info`"
---
# gate-info-riskcheck

> 这是一项安全防护技能。用户输入代币名称或合约地址后，系统会调用合约安全检测工具来获取30多项风险检测结果、税收分析信息、持有者集中度以及代币名称相关的风险数据。随后，大型语言模型（LLM）会将这些数据整合成一份结构化的风险评估报告。地址合规性检测功能将在后续版本中加入。

**触发场景**：用户提及代币/合约地址，并使用诸如“安全”、“风险”、“检查”、“审计”、“蜜罐”、“合约安全”或“诈骗”等关键词。

---

## 路由规则

| 用户意图 | 关键词/模式 | 执行操作 |
|-------------|-----------------|--------|
| 代币合约安全检测 | “这个代币安全吗？” “PEPE合约有风险吗？” “检查0x...合约” | 执行此技能（代币安全模式） |
| 地址风险检测 | “这个地址安全吗？” “这是黑名单地址吗？” | 执行此技能（地址风险模式 — 目前功能受限） |
| 单一货币分析 | “帮我分析这个代币” | 路由到 `gate-info-coinanalysis` |
| 地址追踪 | “追踪这个地址” | 路由到 `gate-info-addresstracker` |
| 代币链上分析 | “查询这个代币的链上信息” | 路由到 `gate-info-tokenonchain` |
| 项目尽职调查 | “这个项目合法吗？” “团队背景如何？” | 路由到 `gate-info-coinanalysis`（侧重于项目基本信息） |

---

## 执行流程

### 模式A：代币安全检测（核心模式 — 已准备好）

#### 第1步：意图识别与参数提取

从用户输入中提取以下信息：
- `token`：代币符号（例如PEPE、SHIB） — 与 `address` 互斥
- `address`：合约地址（例如0x...） — 与 `token` 互斥
- `chain`：链名（eth / bsc / solana / base / arb等） — **必需**

**参数补充策略**：
- 如果用户仅提供代币名称而未提供链名：提示“请指定链名（例如eth、bsc、solana）”
- 如果用户仅提供合约地址而未提供链名：尝试根据地址格式推断链名（以0x开头的地址通常属于EVM链，但仍需确认具体链名）
- 如果用户询问的是主流货币（如BTC、ETH）：告知用户“主流货币通常没有合约安全风险。如需检测，请提供特定链上的 wrapped token 或 Meme token”

#### 第2步：并行调用两个MCP工具

| 步骤 | MCP工具 | 参数 | 获取的数据 | 是否并行执行 |
|------|----------|------------|----------------|----------|
| 1a | `info_compliance_check_token_security` | `token={token} 或 address={address}, chain={chain}, scope="full", lang="en"` | 风险等级、30多项风险项、税收分析、持有者集中度、蜜罐检测、开源状态 | 是 |
| 1b | `info_coin_get_coin_info` | `query={token or symbol}` | 代币基本信息（项目名称、所属领域、上市交易所等） | 是 |

> 两个工具会并行执行，且互不依赖。

#### 第3步：LLM整合数据 — 生成风险评估报告

将安全检测数据和基本信息传递给LLM，使用以下模板生成评估报告。

### 模式B：地址风险检测（功能受限模式）

> `info_compliance_check_address_risk` 功能尚未开发完成（处于第三阶段）。目前只能使用 `info_onchain_get_address_info` 来获取基本地址信息。

| 步骤 | MCP工具 | 参数 | 获取的数据 | 状态 |
|------|----------|------------|----------------|--------|
| 1 | `info_onchain_get_address_info` | `address={address}, chain={chain}` | 基本地址信息、余额、交易记录 | ✅ 可用 |
| 2 | `info_compliance_check_address_risk` | — | 地址合规性风险标签 | ❌ 尚未开发 |

**功能限制处理**：告知用户“地址合规性风险检测正在开发中。目前仅提供基本地址信息。如需进行代币合约安全检测，请提供代币名称或合约地址。”

---

## 报告模板（代币安全模式）

```markdown
## {token} Contract Security Report

### 1. Risk Overview

| Metric | Result |
|--------|--------|
| Chain | {chain} |
| Contract Address | {address} |
| Overall Risk Level | {risk_level_text} ({highest_risk_level}) |
| High-Risk Items | {high_risk_num} |
| Medium-Risk Items | {middle_risk_num} |
| Low-Risk Items | {low_risk_num} |
| Honeypot Detected | {is_honeypot ? "⛔ Yes" : "✅ No"} |
| Open Source | {is_open_source ? "✅ Yes" : "⚠️ No"} |

### 2. High-Risk Item Details

{If high-risk items exist, list each:}

| Risk Item | Description | Value |
|-----------|------------|-------|
| {risk_name_1} | {risk_desc_1} | {risk_value_1} |
| {risk_name_2} | {risk_desc_2} | {risk_value_2} |
| ... | ... | ... |

{If no high-risk items: "✅ No high-risk items detected"}

### 3. Tax Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Buy Tax | {buy_tax}% | {Normal/Elevated/Extreme} |
| Sell Tax | {sell_tax}% | {Normal/Elevated/Extreme} |
| Transfer Tax | {transfer_tax}% | {Normal/Elevated/Extreme} |

{If multiple DEX pools have different tax rates, list the major pool breakdowns}

### 4. Holder Concentration

| Metric | Value | Status |
|--------|-------|--------|
| Holder Count | {holder_count} | {Many/Normal/Low} |
| Top 10 Holder % | {top10_percent}% | {Normal/High/Extremely Concentrated} |
| Top 100 Holder % | {top100_percent}% | — |
| Developer Holdings | {dev_holding_percent}% | {Normal/High} |
| Insider Holdings | {insider_percent}% | {Normal/High} |
| Largest Single Holder | {max_holder_percent}% | {Normal/High} |

### 5. Name Risk

| Metric | Result |
|--------|--------|
| Domain Token | {is_domain_token ? "⚠️ Yes" : "✅ No"} |
| Contains Sensitive Words | {is_sensitive ? "⚠️ Yes" : "✅ No"} |
| Sensitive Words | {sensitive_words} |

### 6. Project Basic Info (Supplementary)

| Metric | Value |
|--------|-------|
| Project Name | {project_name} |
| Sector | {category} |
| Listed on Major Exchanges | {exchange_list} |

### 7. Overall Assessment

{LLM generates a 3-5 sentence comprehensive risk assessment:}
- Overall contract safety level
- Most critical risk items (if any)
- Whether holder concentration is healthy
- Whether tax rates are reasonable
- Whether further manual audit is recommended

### ⚠️ Risk Warnings

{Auto-generated explicit warnings based on detection results:}
- Honeypot detection (if applicable)
- High tax warning (if applicable)
- Excessive holder concentration (if applicable)
- Contract not open-source (if applicable)

> The above analysis is based on automated on-chain data detection and cannot cover all risk scenarios. Please combine with project due diligence and community research for comprehensive judgment.
```

---

## 决策逻辑

| 条件 | 评估结果 |
|-----------|------------|
| `is_honeypot == true` | **最高级别警告**：“⛔ 检测到蜜罐合约 — 极有可能无法购买。” |
| `is_open_source == false` | 标记“合约不是开源的 — 代码逻辑无法审计，风险增加” |
| `buy_tax > 5%` 或 `sell_tax > 5%` | 标记“税率异常高 — 交易成本极高” |
| `buy_tax > 10%` 或 `sell_tax > 10%` | 标记“⛔ 极高税率 — 可能是恶意合约” |
| `top10_percent > 50%` | 标记“持有者高度集中 — 存在内部人士/大户抛售风险” |
| `top10_percent > 80%` | 标记“持有者高度集中 — 抛售风险极高” |
| `dev_holding_percent > 10%` | 标记“开发者持有比例较高 — 注意可能的抛售风险” |
| `holder_count < 100` | 标记“持有者数量极少 — 流动性和去中心化程度不足” |
| `high_risk_num > 0` | 列出所有高风险项并附上说明 |
| `high_risk_num == 0 && middle_risk_num <= 2` | 标记“合约安全检测通过 — 未检测到显著风险” |
| `is_domain_token == true` | 标记“这是一个域名代币 — 与同名项目无关。请仔细核实” |
| `is_sensitive == true` | 标记“代币名称包含敏感词汇 — 存在冒充/欺诈风险” |
| 任何工具返回空结果/错误 | 跳过该部分；在报告中注明“数据不可用” |

---

## 风险等级划分

| `highest_risk_level` 值 | 风险等级 | 标签 | 描述 |
|---------------------------|------------|-------|-------------|
| 0 | 安全 | ✅ 安全 | 未检测到风险项 |
| 1 | 低风险 | 仅存在低风险项 |
| 2 | 中等风险 | 存在中等风险项 — 需持续监控 |
| 3 | 高风险 | 存在高风险项 — 需格外谨慎 |
| is_honeypot=true | 极高风险 | ⛔ 极高风险 — 强烈建议远离该合约 |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| 缺少链名参数 | 提示用户：“请指定链名（例如eth、bsc、solana、base、arb）” |
| 未提供代币或地址 | 提示用户：“请提供代币符号或合约地址” |
| 合约地址不存在/无法识别 | 提示用户核实地址并确认链名 |
| 代币是主流货币（如BTC/ETH） | 告知用户：“主流货币通常没有合约安全风险。如需检测特定链上的合约，请提供 wrapped token 或 Meme token” |
| `check_token_security` 超时/出错 | 返回错误信息；建议稍后再试 |
| 地址风险检测功能不可用 | 告知用户“地址合规性检测正在开发中”。引导用户使用 `gate-info-addresstracker` 获取基本地址信息 |
| 用户误输入普通地址（以为它是合约地址） | 尝试检测；若结果为空，告知用户“这可能不是合约地址。如需地址信息，请使用地址追踪功能” |

---

## 跨技能路由

| 用户后续操作 | 路由目标 |
|-----------------------|----------|
| “帮我分析这个代币” | `gate-info-coinanalysis` |
| “查询这个代币的链上信息” | `gate-info-tokenonchain` |
| “有最新新闻吗？” | `gate-news-briefing` |
| “追踪这个地址” | `gate-info-addresstracker` |
| “将这个代币与XX进行比较” | `gate-info-coincompare` |
| “这个代币的价格走势如何？” | `gate-info-trendanalysis` |

---

## 可用工具及功能限制说明

| PRD定义的工具 | 实际可用的工具 | 状态 | 功能限制策略 |
|-----------------|----------------------|--------|---------------------|
| `info_compliance_check_token_security` | `info_compliance_check_token_security` | ✅ 已准备好 | — |
| `info_coin_get_coin_info` | `info_coin_get_coin_info` | ✅ 已准备好 | — |
| `info_onchain_get_address_info` | `info_onchain_get_address_info` | ✅ 已准备好 | 可获取基本地址信息 |
| `info_compliance_check_address_risk` | — | ❌ 尚未开发 | 地址合规性风险检测功能不可用 — 引导用户使用地址追踪工具 |

---

## 安全规则

1. **强制性的蜜罐警告**：当检测到 `is_honeypot == true` 时，必须在最显眼的位置显示“⛔ 极高风险”警告 — 绝不能淡化这一风险。
2. **禁止投资建议**：风险评估基于链上数据，必须包含“本报告不构成投资建议”的免责声明。
3. **无法保证绝对安全**：即使所有检测都通过，也要说明“自动化检测无法涵盖所有风险”。
4. **数据透明度**：标注数据来源和时间戳。
5. **数据缺失处理**：当某个维度的数据缺失时，必须明确告知用户 — 绝不能伪造安全结论。
6. **保护地址隐私**：不得主动公开地址持有者的身份信息 — 仅显示链上公开可用的数据。