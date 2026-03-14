---
name: gate-exchange-vipfee
version: "2026.3.11-2"
updated: "2026-03-11"
description: "查询 Gate 的 VIP 等级及交易费率。当用户询问其 VIP 等级、交易费率、现货费率或期货/合约费率时，请使用此技能。相关触发短语包括：“VIP 等级”、“交易费率”、“费率”、“现货费率”、“期货费率”。"
---
# Gate VIP与费用查询助手

## 通用规则

在继续操作之前，请阅读并遵守共享的运行时规则：
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

查询用户的Gate VIP等级及交易费用率，包括现货和期货的费用信息。

## 快速入门

以下是一些常用的查询提示，可帮助您快速开始使用该工具：

1. **查询VIP等级**
   > 我的VIP等级是多少？

2. **查询交易费用**
   > 显示我的现货和期货交易费用。

3. **同时查询VIP等级和费用**
   > 查看我的VIP等级和交易费用。

## 领域知识

### 按领域划分的工具

| 组别 | 工具调用 |
|-------|------------|
| 账户/VIP等级 | `cex_account_get_account_detail` |
| 交易费用率 | `cex_wallet_get_wallet_fee` |

### 关键概念

- **VIP等级**：Gate根据交易量和资产持有量为用户分配VIP等级（VIP 0 – VIP 16）。VIP等级越高，费用率越低。
- **现货费用**：应用于现货交易对的做市/撮合费用率。
- **期货费用**：应用于期货/合约交易的做市/撮合费用率，费用率会因结算货币（BTC、USDT、USD）而有所不同。
- `cex_wallet_get_wallet_fee`工具会在一个响应中返回现货和期货的费用率。使用`settle`参数可以查询特定于期货的费用。

### API行为说明

- **账户级别的定价**：Gate的费用率由用户的VIP等级决定。`currency_pair`参数不会改变返回的费用值——所有交易对都使用相同的账户级别费率。
- **`settle`参数的作用**：`settle`参数仅影响期货费用字段（`futuresMakerFee` / `futuresTakerFee`）。无论`settle`参数如何设置，现货费用（`makerFee` / `takerFee`）保持不变。
- **处理无效的`currency_pair`**：如果查询的交易对不存在，API不会返回错误，而是会默默地返回默认的账户级别费用。切勿将成功的响应视为该交易对存在的确认。

## 工作流程

当用户询问VIP等级或交易费用时，请按照以下步骤操作：

### 第1步：确定查询类型

将请求分类为以下几种类型之一：

1. **查询VIP等级** — 用户想知道当前的VIP等级
2. **查询费用率** — 用户想知道现货和/或期货的交易费用率
3. **同时查询VIP等级和费用** — 用户同时需要VIP等级和费用信息

需要提取的关键数据：
- `query_type`："vip"、"fee"或"combined"
- `currency_pair`（可选）：用于查询特定交易对的费用
- `settle`（可选）：期货的结算货币（BTC / USDT / USD）

### 第2步：查询VIP等级（如需要）

如果`query_type`为"vip"或"combined"：

调用`cex_account_get_account_detail`，无需传递任何参数。

需要提取的关键数据：
- `vip_level`：用户的当前VIP等级（例如，VIP 0、VIP 1等）

### 第3步：查询交易费用率（如需要）

如果`query_type`为"fee"或"combined"：

调用`cex_wallet_get_wallet_fee`，并传递以下参数：
- `currency_pair`（可选）：指定交易对的上下文（注意：费用率是账户级别的，不会因交易对而异）
- `settle`（可选）：期货的结算货币

需要提取的关键数据：
- `maker_fee_rate`：现货的做市费用率
- `taker_fee_rate`：现货的撮合费用率
- `futures_maker_fee_rate`：期货的做市费用率
- `futures_taker_fee_rate`：期货的撮合费用率

### 第4步：返回结果

根据报告模板格式化响应。`cex_wallet_get_wallet_fee` API始终会返回完整的费用结构（现货 + 期货 + 交割费用）。根据用户的查询需求过滤输出结果：

- 如果用户仅询问**现货费用** → 仅显示`makerFee` / `takerFee`
- 如果用户仅询问**期货/合约费用** → 仅显示`futuresMakerFee` / `futuresTakerFee`
- 如果用户询问**交易费用**（总体费用） → 同时显示现货和期货的费用
- 如果用户仅询问**VIP等级** → 仅显示VIP等级，不显示费用数据
- 如果用户指定了`currency_pair` → 在响应中添加说明：“注意：API返回的是账户级别的费用率。所显示的费用适用于所有交易对；如果指定的交易对不存在，结果仍会显示默认的账户费用率。”

## 判断逻辑总结

| 条件 | 操作 |
|-----------|--------|
| 用户仅询问VIP等级 | 调用`cex_account_get_account_detail`，返回VIP等级 |
| 用户仅询问交易费用 | 调用`cex_wallet_get_wallet_fee`，返回现货和期货的费用率 |
| 用户同时询问VIP等级和费用 | 调用两个工具，返回合并后的结果 |
| 用户指定了交易对 | 将`currency_pair`参数传递给`cex_wallet_get_wallet_fee` |
| 用户指定了期货结算货币 | 将`settle`参数传递给`cex_wallet_get_wallet_fee` |
| 用户仅询问现货费用 | 调用`cex_wallet_get_wallet_fee`，仅返回现货费用部分 |
| 用户仅询问期货/合约费用 | 调用`cex_wallet_get_wallet_fee`并设置`settle`参数，仅返回期货费用部分 |
| 用户指定了`currency_pair` | 在响应中添加说明：API不验证交易对的有效性；返回的费用是账户级别的默认费用，指定的交易对可能不存在 |
| API返回错误或空数据 | 通知用户问题所在，并建议检查账户认证信息 |

## 报告模板

```markdown
## Query Result

{vip_section}

{fee_section}
```

**VIP部分**（当查询VIP等级时）：

```markdown
### VIP Tier

| Item | Value |
|------|-------|
| VIP Level | {vip_level} |
```

**费用部分**（当查询费用时）：

```markdown
### Trading Fee Rates

| Category | Maker Fee | Taker Fee |
|----------|-----------|-----------|
| Spot | {spot_maker_fee} | {spot_taker_fee} |
| Futures | {futures_maker_fee} | {futures_taker_fee} |
```

**综合示例输出**：

```markdown
## Query Result

### VIP Tier

| Item | Value |
|------|-------|
| VIP Level | VIP 1 |

### Trading Fee Rates

| Category | Maker Fee | Taker Fee |
|----------|-----------|-----------|
| Spot | 0.1% | 0.1% |
| Futures (USDT) | 0.015% | 0.05% |
```

## 错误处理

| 错误类型 | 常见原因 | 处理策略 |
|------------|---------------|-------------------|
| 认证失败 | API密钥无效或过期 | 通知用户检查MCP配置和API密钥的有效性 |
| 空响应 | 账户数据不可用 | 通知用户查询未返回数据，建议重试 |
| 网络错误 | MCP连接问题 | 建议用户检查MCP服务器的连接状态 |

## 安全规则

- 本技能仅用于读取数据，不执行任何交易或账户修改操作。
- 由于所有操作均为查询，因此无需用户确认。
- 请勿在响应中泄露原始API密钥或敏感的认证信息。