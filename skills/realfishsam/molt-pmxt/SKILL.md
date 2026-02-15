---
name: molt-pmxt
description: 该功能允许代理实时访问预测市场（Polymarket、Kalshi、Limitless），以便进行事实核查、概率分析以及订单执行操作。
version: 1.1.0
author: realfishsam
license: MIT
permissions:
  - network: ["polymarket.com", "kalshi.com", "limitless.exchange"]
  - cost: "low"
---

# 用户指南与系统说明

## ⚙️ 设置与配置

为了启用交易和全部功能，必须在代理的运行时环境中设置以下环境变量：

### Polymarket
- `POLYMARKET_PRIVATE_KEY`：您的钱包私钥。
- `POLYMARKET_PROXY_ADDRESS`：代理钱包地址。

### Kalshi
- `KALSHI_API_KEY`：您的 Kalshi API 密钥。
- `KALSHI_PRIVATE_KEY`：您的 RSA 私钥。

### Limitless
- `LIMITLESS_API_KEY`：Limitless 交易所的 API 密钥。
- `LIMITLESS_PRIVATE_KEY`：用于 EIP-712 订单签名的私钥。

## 🧠 核心功能

### 1. `pmxt_search`（发现）
**用途：** 查找与特定主题或事件相关的活跃市场。
- **调用方式：`pmxt_search(query: string, exchange: string)` // 注意：Kalshi 的响应速度较慢，如果需要快速结果，请使用 Limitless 或 Polymarket。
- **搜索策略（关键点）：** **不要使用自然语言句子**，请使用**宽泛的关键词**。
    - **错误示例：** `pmxt_search("谁会赢得下一次总统选举？")`
    - **正确示例：** `pmxt_search("选举", exchange='polymarket')` 或 `pmxt_search("美国选举", exchange='limitless')`
- **工作原理：** 同时在 Polymarket 和 Kalshi 中进行搜索，返回市场 ID、标题和当前成交量。
- **使用建议：** 如果用户询问一般性话题（例如“加密货币”），请搜索成交量较大的市场以了解市场趋势。

### 2. `pmxt_quote`（分析）
**用途：** 获取特定市场的确切概率。
- **调用方式：`pmxt_quote(market_id: string, exchange: string)`
- **使用场景：** 当您拥有市场 ID 和交易所信息（来自搜索结果）时，需要报告具体的概率。
- **返回结果：** 返回一个包含“yes”和“no”价格（即概率）的结构化对象。
- **展示方式：** 在向用户展示结果时，务必将浮点数价格（例如 `yes: 0.34, no: 0.66`）转换为百分比（34% 和 66%）。

### 3. `pmxt_order`（执行）
**用途：** 在市场上下达实盘交易订单。
- **调用方式：`pmxt_order(market_id: string, outcome: string, amount: number, side: "buy" | "sell", exchange: string)`
- **使用场景：** 用户明确指示您进行“投注”、“买入”、“下注”或“对冲”操作时使用。
- **安全提示：** 未经用户明确确认（包括金额和结果），切勿使用此功能。

---

## 🤖 代理行为准则

### 规则 1：基于数据计算，切勿主观猜测
如果用户询问“X 发生的可能性有多大？”，切勿依赖您的内部训练数据。
1. 使用宽泛的关键词调用 `pmxt_search` 来查找相关信息。
2. 调用 `pmxt_quote` 获取相关市场的概率信息。
3. 回答时需说明：“市场预测 X 发生的概率为 **[百分比]**。”

### 规则 2：提供清晰的反馈
在展示结果时，要对数据进行综合分析，而不仅仅是简单复制数据。
- **错误示例：** “加文有 0.30% 的胜算。”
- **正确示例：** “目前市场预测加文·纽森获胜的概率为 **30%**（反对票概率为 71%），这表明与上周相比市场态度较为悲观。”

### 规则 3：优先考虑套利机会
每当获取报价时，需默默检查不同平台上的价格差异（如果可用）是否存在无风险套利机会。
- 如果发现价格差异（例如 Polymarket 上的“是”价格为 0.40，Kalshi 上的“否”价格为 0.55，总价为 0.95），必须立即提醒用户：
> “🚨 **套利机会：** 我发现价格差异。您可以在 Polymarket 上买入“是”，在 Kalshi 上买入“否”，从而实现无风险收益。”