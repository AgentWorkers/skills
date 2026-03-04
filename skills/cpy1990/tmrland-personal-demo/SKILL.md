---
name: tmrland-personal
description: "TMR Land 是一个专为 AI 商业市场设计的个人代理工具。使用场景包括：  
(1) 搜索 AI 或数据相关企业；  
(2) 发布购买意向；  
(3) 下达和管理托管订单；  
(4) 评估企业的信用评分；  
(5) 浏览 Grand Apparatus 的预测结果。"
homepage: https://tmrland.com
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["node"],"env":["TMR_API_KEY"]},"primaryEnv":"TMR_API_KEY"}}
---
# TMR Land — 个人技能

将您的代理连接到 TMR Land，这是一个提供双语（中文/英文）服务的 AI 商业交易平台。作为个人用户，您可以搜索企业、发布交易意向、下订单，并通过信用评分来评估企业的质量。

## 设置

设置 `TMR_API_KEY` — 通过 `POST /api/v1/api-keys`（角色为 "personal"）来创建一个 API 密钥。

可选地设置 `TMR_BASE_URL`（默认值：`https://tmrland.com/api/v1`）。

## 脚本

```bash
# Search active businesses
node {baseDir}/scripts/search-businesses.mjs --limit 10

# Create an intention (structured need)
node {baseDir}/scripts/create-intention.mjs --content "Need a fine-tuned Chinese NLP model for sentiment analysis" [--locale zh]

# List your intentions
node {baseDir}/scripts/list-intentions.mjs [--limit N]

# Get intention details
node {baseDir}/scripts/get-intention.mjs <intention-id>

# Publish a draft intention
node {baseDir}/scripts/publish-intention.mjs <intention-id>

# Cancel an intention
node {baseDir}/scripts/cancel-intention.mjs <intention-id>

# One-shot search (create + profile + match + return results)
node {baseDir}/scripts/quick-search.mjs --content "Need an NLP model for sentiment analysis"

# Trigger multi-path matching (rules + BM25 + vector + RRF fusion)
node {baseDir}/scripts/trigger-match.mjs <intention-id>

# Check matching status (pending/running/completed/failed)
node {baseDir}/scripts/match-status.mjs <intention-id>

# Get matched business candidates
node {baseDir}/scripts/get-matches.mjs <intention-id>

# Start negotiations with matched businesses
node {baseDir}/scripts/start-negotiation.mjs --intention <id> --businesses <id1,id2,...>

# List your negotiation sessions
node {baseDir}/scripts/list-negotiations.mjs [--intention <id>]

# View/send messages in a negotiation
node {baseDir}/scripts/negotiation-messages.mjs <session-id> [--send "message text"]

# Accept a final_deal proposal (creates order)
node {baseDir}/scripts/accept-deal.mjs <session-id>

# Reject a proposal
node {baseDir}/scripts/reject-deal.mjs <session-id>

# Cancel a negotiation session
node {baseDir}/scripts/cancel-negotiation.mjs <session-id>

# Check order status
node {baseDir}/scripts/order-status.mjs <order-id>

# List all your orders
node {baseDir}/scripts/list-orders.mjs [--limit N]

# Cancel an order (before payment)
node {baseDir}/scripts/cancel-order.mjs <order-id>

# Pay for an order (escrow)
node {baseDir}/scripts/pay-order.mjs <order-id> [--currency USD|USDC]

# View order messages
node {baseDir}/scripts/get-messages.mjs <order-id>

# Send a message in an order
node {baseDir}/scripts/send-message.mjs <order-id> --content "message text"

# Accept delivery (releases escrow, moves to pending_rating)
node {baseDir}/scripts/accept-delivery.mjs <order-id>

# Request revision (sends order back to business for rework)
node {baseDir}/scripts/request-revision.mjs <order-id> --feedback "Please fix..."

# Submit a review
node {baseDir}/scripts/submit-review.mjs --order <id> --rating <1-5> [--comment "..."]

# Check wallet balances
node {baseDir}/scripts/get-wallet.mjs
```

## 个人工作流程

1. **注册并充值** — 创建账户，完成身份验证（KYC），为钱包充值。
2. **发布交易意向** — 通过 `--content` 参数描述您的需求。
3. **匹配企业** — 触发多路径的企业匹配过程。
4. **审核候选企业** — 检查匹配结果、企业声誉以及信用记录。
5. **谈判** — 与候选企业开始谈判，交换信息，审核提案。
6. **接受交易** — 接受 `final_deal` 提案，系统会生成合同和订单。
7. **付款** — 从您的钱包中扣除资金用于支付（支持 USD 或 USDC）。
8. **沟通** — 通过订单聊天功能与企业联系。
9. **接受交付** — 审查交付物，决定是否接受（释放托管资金）或要求修改。
10. **评价** — 在评价窗口期内对企业进行评分。

## 代理行为指南

### 参数自主处理级别

有三个级别定义了代理如何处理各种参数：

- **AUTO** — 代理可以直接推断参数的值（如 ID、语言设置、分页参数）。
- **CONFIRM** — 代理可以草拟参数值，但必须在提交前显示给用户确认。
- **ASK** — 代理必须直接询问用户，不得自行猜测或生成参数值。

| 操作 | 参数 | 处理级别 | 备注 |
|---|---|---|---|
| `create_intention` | `content` | CONFIRM | 代理可以根据对话内容草拟参数；提交前需展示草稿 |
| `create_intention` | `locale` | AUTO | 从内容语言（中文/英文）中自动检测语言设置 |
| `quick_search` | `content` | CONFIRM | 与 `create_intention` 的参数处理方式相同 |
| `publish_intention` | `intention_id` | AUTO | 使用上一步创建操作中的 ID |
| `update_intention` | `title`, `description` | CONFIRM | 代理可以建议修改内容 |
| `redescribe_intention` | `content` | CONFIRM | 代理可以草拟修改后的内容；需先提醒用户可能的副作用 |
| `redescribe_intention` | `locale` | AUTO | 从内容语言中自动检测语言设置 |
| `delete_intention` | `intention_id` | ASK | 必须确认是否真的要删除该意向 |
| `trigger_matching` | `intention_id` | AUTO | 使用当前工作流程中的 ID |
| `start_negotiations` | `business_ids` | ASK | 显示匹配到的企业列表；用户进行选择 |
| `send_negotiation_message` | `content` | CONFIRM | 代理可以草拟消息；用户确认内容 |
| `accept_deal` | `session_id` | ASK | 必须解释操作后果并得到用户确认 |
| `reject_deal` | `session_id` | ASK | 必须确认是否拒绝交易 |
| `cancel_negotiation` | `session_id` | ASK | 必须确认是否取消谈判 |
| `pay_order` | `currency` | ASK | 必须询问用户使用哪种货币（USD 或 USDC） |
| `pay_order` | `order_id` | AUTO | 使用交易接受时的 ID |
| `send_message` | `content` | CONFIRM | 代理可以草拟消息；用户确认内容 |
| `accept_delivery` | `order_id` | ASK | 必须解释释放托管资金的规则并得到用户确认 |
| `submit_review` | `rating` | ASK | 代理不能自动生成评价内容；用户确认评价 |
| `submit_review` | `comment` | CONFIRM | 代理可以建议评价内容；用户最终确认 |
| `cancel_order` | `order_id` | ASK | 必须确认是否取消订单 |
| `cancel_intention` | `intention_id` | ASK | 必须确认是否取消该意向 |

### 具有破坏性影响的操作

这些操作可能会产生严重的后果。代理在执行前必须警告用户并获取明确的确认。

| 操作 | 可能的后果 | 必需的确认 |
|---|---|---|
| `accept_delivery` | ⚠️ 不可逆操作。会将托管资金释放给企业，并将订单状态改为“待评价”状态。除非通过争议解决，否则无法撤销。 | “您确定要接受交付并将 [金额] [货币] 释放给 [企业] 吗？” |
| `accept_deal` | ⚠️ 不可逆操作。会创建具有约束力的合同和订单，并取消与该意向相关的所有其他谈判。 | “接受该提议将创建一个金额为 [金额] 的订单，并取消所有其他谈判。您确定要继续吗？” |
| `pay_order` | 会从用户的钱包中扣除资金用于支付。资金将一直被扣留，直到交付完成或争议解决。 | “这将从您的钱包中扣除 [金额] [货币]。您使用 USD 或 USDC 支付吗？” |
| `redescribe_intention` | ⚠️ 该操作会取消所有当前的谈判，并重新开始匹配过程。之前的谈判记录将丢失。 | “这将取消所有当前的谈判并重新开始。您确定要继续吗？” |
| `delete_intention` | ⚠️ 该操作会永久删除该意向及其所有相关数据。操作不可撤销。 | “这将永久删除该意向。您确定要删除它吗？” |
| `cancel_order` | 取消订单，但不会对用户的财务造成影响。 | “您确定要取消这个订单吗？” |
| `cancel_negotiation` | 结束谈判会话。谈判历史会被保留，但不会再有进一步的交互。 | “您确定要取消与 [企业] 的谈判吗？” |
| `reject_deal` | 拒绝提案。企业可以发送修改后的提议。 | “您拒绝这个提议吗？企业可以发送修改后的报价。” |
| `cancel_intention` | 取消该意向，可能会影响相关的谈判。 | “您确定要取消这个意向吗？” |

### 状态机参考

#### 意向生命周期

```
draft → published → matching → matched → negotiating → contracted
  ↓         ↓                      ↓           ↓
cancelled cancelled              cancelled   gated → expired
```

| 状态 | 允许的操作 |
|---|---|
| `draft` | `update_intention`, `publish_intention`, `delete_intention`, `cancel_intention` |
| `published` | `trigger_matching`, `redescribe_intention`, `cancel_intention` |
| `matching` | （等待匹配完成 — 通过 `get_match_status` 检查进度） |
| `matched` | `get_matches`, `start_negotiations`, `redescribe_intention`, `cancel_intention` |
| `negotiating` | `send_negotiation_message`, `accept_deal`, `reject_deal`, `cancel_negotiation`, `redescribe_intention` |
| `contracted` | （订单已创建 — 通过订单工具进行管理） |
| `gated` | （等待平台审核） |
| `cancelled` | `delete_intention` |
| `expired` | `delete_intention` |

#### 订单生命周期

```
pending_payment → delivering → pending_review → pending_rating → completed
       ↓                           ↕ revision_requested
   cancelled                    disputed
                                   ↓
                                refunded
```

| 状态 | 个人用户允许的操作 |
|---|---|
| `pending_payment` | `pay_order`, `cancel_order` |
| `delivering` | `send_message`, （等待交付） |
| `pending_review` | `accept_delivery`, `request_revision`, `dispute`, `send_message` |
| `revision_requested` | `send_message`, （等待企业重新提交） |
| `pending_rating` | `submit_review` |
| `completed` | （最终状态） |
| `disputed` | `get_dispute_votes`（查看争议结果） |
| `cancelled` | （最终状态） |
| `refunded` | （最终状态） |

#### 谈判生命周期

```
active → contracted (creates contract + order)
  ↓  ↑
  ↓  rejected (stays active, can re-propose)
  ↓
cancelled (terminal)
closed (terminal — order completed or cancelled)
```

| 状态 | 个人用户允许的操作 |
|---|---|
| `active` | `send_negotiation_message`, `accept_deal`, `reject_deal`, `cancel_negotiation` |
| `contracted` | （订单已创建 — 通过订单工具进行管理） |
| `rejected` | （针对该提案的谈判状态；会话可能仍然处于活跃状态） |
| `cancelled` | （最终状态） |
| `closed` | （最终状态） |

### 异步流程模式

#### 标准匹配流程

```
create_intention(content) → publish_intention(id)
  → trigger_matching(id)
  → poll get_match_status(id) until 'completed'
  → get_matches(id) → present candidates to user
  → start_negotiations(id, user_selected_ids)
```

#### 快速搜索快捷方式

```
quick_search(content) → returns matches directly (synchronous)
```

该方式结合了创建意向、查看企业资料和匹配企业的功能。适用于用户希望快速获得结果且不想管理意向生命周期的情况。

#### 谈判 → 订单流程

```
(in active negotiation)
  → business sends proposal (send_proposal with status='final_deal')
  → user reviews proposal
  → accept_deal(session_id) → creates contract + order
  → pay_order(order_id, currency)
  → (wait for delivery)
  → accept_delivery(order_id) → releases escrow, moves to pending_rating
  → submit_review(order_id, rating)
```

## API 概述

认证方式：`Authorization: Bearer <TMR_API_KEY>`。所有 API 路径前缀为 `/api/v1`。所有 ID 使用 UUID 格式。双语字段的文件名后缀为 `_zh`/`_en`。分页通过 `offset` 和 `limit` 参数实现。

主要涉及的领域包括：认证（auth）、钱包（wallet）、意向（intentions）、企业（businesses）、订单（orders）、合同（contracts）、信用（credit）、评价（reviews）、争议（disputes）、消息（messages）、通知（notifications）和设备（apparatus）。

详细请求/响应格式请参考 `references/` 目录。

## 错误代码说明

| 状态 | 含义 |
|--------|---------|
| 400 | 请求无效 — 验证失败 |
| 401 | 未经授权 — 令牌无效或丢失 |
| 403 | 禁止访问 — 权限不足 |
| 404 | 未找到 |
| 409 | 状态转换冲突 — 数据重复或无效 |
| 422 | 实体无法处理 — 数据格式错误 |
| 500 | 服务器内部错误 |