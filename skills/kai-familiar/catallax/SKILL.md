---
name: catallax
description: >
  Interact with the Catallax decentralized contract work protocol on Nostr.
  Use when the user mentions tasks, bounties, contract work, arbiters, escrow,
  labor market, gigs, or Catallax. Supports browsing open tasks, creating task
  proposals, discovering arbiter services, submitting work deliveries, and
  managing the full task lifecycle (kinds 33400, 33401, 3402).
---

# Catallax 技能

Catallax 是一个基于 Nostr 的去中心化合约工作协议，支持 Lightning/Cashu 支付方式，并采用可信的第三方仲裁机构来处理交易。

## 协议概述

请参阅 `references/NIP-3400.md` 以获取完整的协议规范。主要概念包括：

- **赞助者（Patron）**：创建任务、设立资金托管、分配工作给工作者。
- **仲裁者（Arbiter）**：负责评估工作质量并处理支付的第三方机构。
- **自由工作者（Free Agent）**：申请任务、完成任务并获取报酬。
- **事件类型（Kinds）**：33400（仲裁服务）、33401（任务提案）、3402（任务完成）。
- **状态流转**：提案（proposed）→ 资金募集（funded）→ 进行中（in_progress）→ 提交（submitted）→ 完成（concluded）。

## 查询任务

使用 `nak` 命令从相关中继（relays）查询类型为 33401 的事件：

```bash
# List all task proposals (limit 50)
nak req -k 33401 -l 50 wss://relay.damus.io

# Filter by tag (e.g. tasks tagged "development")
nak req -k 33401 -t development -l 50 wss://relay.damus.io

# Filter by status (open tasks only)
nak req -k 33401 -l 100 wss://relay.damus.io | \
  while read -r event; do
    status=$(echo "$event" | jq -r '.tags[] | select(.[0]=="status") | .[1]')
    if [ "$status" = "proposed" ] || [ "$status" = "funded" ]; then
      echo "$event"
    fi
  done
```

将 `content` 字段解析为 JSON 格式，以获取任务的标题、描述和需求信息。同时解析 `tags` 标签以获取金额、状态和分类信息。

### 显示格式

向用户展示任务时，应包括以下内容：
- **标题**（来自 `content.title`）
- **赏金**（来自 `amount` 标签，单位为 sats；若缺失则显示“?”）
- **状态**（来自 `status` 标签）
- **创建时间**（来自 `created_at`）
- **分类**（来自 `t` 标签）
- **描述**（来自 `content.description`，部分内容会被截断显示）
- **资金来源**（来自 `funding_type` 标签：“patron”表示由赞助者资助，“crowdfunding”表示通过众筹获得）

## 查询仲裁者

```bash
# List arbiter services
nak req -k 33400 -l 50 wss://relay.damus.io
```

解析仲裁者的相关信息，包括姓名（name）、简介（about）和收费标准（policy）。同时解析 `tags` 标签以获取费用类型（fee_type）、费用金额（fee_amount）以及费用的下限/上限（min/max_amount）和分类（categories）。

### 显示格式

展示仲裁者信息时，应包括：
- **姓名**（来自 `content.name`）
- **费用**（费用类型 + 费用金额，例如“5%”或“1000 sats”）
- **费用范围**（来自 `min_amount/max_amount` 标签）
- **简介**（来自 `content.about`）

## 创建任务提案

作为赞助者，需要发布类型为 33401 的事件来创建新任务：

```bash
# Build and publish task proposal
nak event -k 33401 \
  --tag d="<unique-slug>" \
  --tag p="<your-pubkey>" \
  --tag amount="<bounty-in-sats>" \
  --tag t="<category>" \
  --tag status="proposed" \
  --tag funding_type="patron" \
  -c '{"title":"Task Title","description":"Detailed description...","requirements":"What must be delivered"}' \
  --sec "<nsec>" \
  wss://relay.damus.io wss://nos.lol wss://relay.primal.net
```

根据任务标题生成一个唯一的 d-tag（小写、使用连字符连接，并添加随机后缀）。

**重要提示**：`content` 字段必须包含有效的 JSON 数据，其中必须包含任务标题、描述，以及可选的需求和截止日期。

## 更新任务状态

由于类型为 33401 的事件可以被替换，因此需要发布一个新的事件来更新任务状态。新事件应包含所有原有的标签以及更改的内容：

```bash
# Update to funded (add zap receipt reference)
nak event -k 33401 \
  --tag d="<same-d-tag>" \
  --tag status="funded" \
  --tag e="<zap-receipt-event-id>" \
  # ... all other original tags ...
  --sec "<nsec>" \
  wss://relay.damus.io
```

## 提交工作（作为自由工作者）

工作交付过程由协议另行规定。不过，工作者也可以使用类型为 951 的事件来表示工作已完成：

```bash
nak event -k 951 \
  --tag e="<task-event-id>" \
  --tag p="<patron-pubkey>" \
  -c '{"delivery":"Description of completed work","evidence":"Link or proof"}' \
  --sec "<nsec>" \
  wss://relay.damus.io
```

## 完成任务（仅限仲裁者操作）

```bash
nak event -k 3402 \
  --tag e="<payout-zap-receipt-id>" \
  --tag e="<task-event-id>" \
  --tag p="<patron-pubkey>" \
  --tag p="<arbiter-pubkey>" \
  --tag p="<worker-pubkey>" \
  --tag resolution="successful" \
  --tag a="33401:<patron-pubkey>:<task-d-tag>" \
  -c '{"resolution_details":"Work met all requirements"}' \
  --sec "<nsec>" \
  wss://relay.damus.io
```

## 常见操作

| 用户操作 | 对应动作 |
|-----------|--------|
| “查找赏金” / “显示任务” | 查询类型为 33401 的任务，筛选状态为“proposed”或“funded”的任务 |
| “创建任务” / “发布赏金” | 创建并发布类型为 33401 的任务提案 |
| “查找仲裁者” | 查询类型为 33400 的仲裁者信息 |
| “提交工作” | 发布类型为 951 的事件以表示工作已完成 |
| “查看我的任务” | 根据用户的公钥（pubkey）筛选类型为 33401 的任务 |
| “查询任务状态” | 根据 d-tag 查询特定任务的状态 |

## 参考客户端

用于可视化浏览任务信息的客户端：https://catallax-reference-client.netlify.app/catallax

## 主要中继节点

为了获得更全面的查询结果，请同时查询以下中继节点：
- wss://relay.damus.io
- wss://nos.lol
- wss://relay.primal.net

**注意**：某些中继节点可能因过滤规则而无法返回类型为 33401 的事件。如果 `nak` 命令返回空结果，可以尝试使用 WebSocket 脚本：打开 WebSocket 连接，发送请求 `{“kinds”:[33401],“limit”:50}`，并持续接收响应直到接收完所有事件。

## 特殊情况处理：

- **缺少金额信息**：部分任务采用众筹方式（`funding_type=crowdfunding`），此时赏金信息会显示为“crowdfunded”。
- **内容格式**：任务内容应为 JSON 格式，但早期的一些任务可能使用纯文本格式。首先尝试使用 `JSON.parse` 进行解析，如果解析失败则将其视为普通描述信息处理。
- **过期的任务**：状态为“proposed”且创建时间超过 30 天的任务可能被视为已放弃。在显示任务信息时需注明其状态。
- **多中继查询**：为确保任务能被更多用户发现，请将任务信息发布到至少 3 个中继节点，并通过事件 ID 进行去重处理。