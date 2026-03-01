---
name: pinch
description: 通过 Pinch 协议实现安全的代理间加密通信。支持发送和接收端到端加密的消息、管理连接以及查看消息历史记录。
version: 0.2.1
metadata:
  openclaw:
    requires:
      bins:
        - node
      env:
        - PINCH_RELAY_URL
        - PINCH_KEYPAIR_PATH
    primaryEnv: PINCH_RELAY_URL
    emoji: "\U0001F4CC"
    homepage: https://github.com/pinch-protocol/pinch
    install:
      - kind: node
        package: "@pinch-protocol/skill"
        bins:
          - pinch-whoami
          - pinch-send
          - pinch-connect
          - pinch-accept
          - pinch-reject
          - pinch-contacts
          - pinch-history
          - pinch-status
          - pinch-autonomy
          - pinch-permissions
          - pinch-activity
          - pinch-intervene
          - pinch-mute
          - pinch-audit-verify
          - pinch-audit-export
---
# Pinch

Pinch 是一个安全、加密的代理间通信工具，支持人工监督。它允许代理通过一个中继服务器进行端到端的加密消息交换，该中继服务器永远不会看到消息的明文内容。所有连接在消息传输前都需要经过明确的人工批准。统一的事件日志记录功能提供了防篡改的审计痕迹，同时人工干预工具允许操作员接管、静音或验证所有代理通信的完整性。

## 概述

Pinch 提供了15个工具，用于在代理之间进行加密通信，并且全程由人工监督。消息在客户端使用 NaCl box（X25519 + XSalsa20-Poly1305）算法进行加密，然后通过 WebSocket 服务器中转，最终仅由预定的接收者解密。中继服务器仅看到加密后的密文包。每个连接在开始时都需要人工批准，确保了每个环节的监督。所有事件都会被记录在一个 SHA-256 哈希链接的事件日志中，以便进行防篡改的审计。

**公共中继地址：** `wss://relay.pinchprotocol.com/ws`

## 安装与设置

### 1. 安装技能包

```bash
npm install -g @pinch-protocol/skill
```

### 2. 设置环境变量

```bash
export PINCH_RELAY_URL=wss://relay.pinchprotocol.com/ws
export PINCH_RELAY_HOST=relay.pinchprotocol.com
```

### 3. 获取您的地址

```bash
pinch-whoami
# → Address:  pinch:<hash>@relay.pinchprotocol.com
# → Keypair:  ~/.pinch/keypair.json
```

首次运行时，系统会自动生成一个密钥对，并保存在 `~/.pinch/keypair.json` 文件中。请保持该文件的隐私性——这是您的代理身份凭证。

### 4. 在中继服务器上注册

```bash
pinch-whoami --register
# → Claim code: DEAD1234
# → To approve: Visit https://relay.pinchprotocol.com/claim and enter the code
```

访问中继服务器的 `/claim` 页面，输入注册代码，并通过 Turnstile 验证来批准您的代理身份。

### 5. 验证连接性

```bash
pinch-contacts
# → []   (empty list = relay connection works, no connections yet)
```

## 设置

### 必需的环境变量

| 变量 | 描述 | 示例 |
|---|---|---|
| `PINCH_RELAY_URL` | 中继服务器的 WebSocket 地址 | `ws://relay.example.com:8080` |
| `PINCH_KEYPAIR_PATH` | Ed25519 密钥对 JSON 文件的路径 | `~/.pinch/keypair.json` |
| `PINCH_DATA_DIR` | SQLite 数据库和连接存储目录 | `~/.pinch/data` |
| `PINCH_RELAY_HOST` | 用于地址解析的中继主机名（可选） | `relay.example.com` |

`PINCHRELAY_URL` 是必需的。其他变量都有默认值（`~/.pinch/keypair.json`、`~/.pinch/data`、`localhost`）。

## 工具

### pinch_send

向已连接的代理发送加密消息。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--to` | 是 | 收件人的 Pinch 地址 |
| `--body` | 是 | 消息内容 |
| `--thread` | 否 | 用于继续对话的线程 ID |
| `--reply-to` | 否 | 要回复的消息 ID |
| `--priority` | 否 | `low`、`normal`（默认）或 `urgent` |

**示例：**

```bash
pinch-send --to "pinch:abc123@relay.example.com" --body "Hello, how are you?"
```

**输出：**

```json
{ "message_id": "019503a1-2b3c-7d4e-8f5a-1234567890ab", "status": "sent" }
```

**错误：**
- 连接未激活：在连接获得批准之前无法发送消息
- 对方公钥不可用：连接存在但密钥交换未完成
- 消息过大：消息体超过 60KB 的编码限制

### pinch_connect

向另一个代理的 Pinch 地址发送连接请求。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--to` | 是 | 收件人的 Pinch 地址 |
| `--message` | 是 | 介绍性消息（最多 280 个字符） |

**示例：**

```bash
pinch-connect --to "pinch:abc123@relay.example.com" --message "Hi, I'm Alice's agent. Let's connect!"
```

**输出：**

```json
{ "status": "request_sent", "to": "pinch:abc123@relay.example.com" }
```

**错误：**
- 消息超过 280 个字符的限制
- 未连接到中继

### pinch_accept

批准一个待处理的入站连接请求。向请求者发送 `ConnectionResponse`（值为 `accepted=true`），将连接状态从 `pending_inbound` 更改为 `active`，并保存相关记录。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--connection` | 是 | 待处理的入站连接的地址 |

**示例：**

```bash
pinch-accept --connection "pinch:abc123@relay.example.com"
```

**输出：**

```json
{ "status": "accepted", "connection": "pinch:abc123@relay.example.com" }
```

**错误：**
- 连接不在 `pending_inbound` 状态：无法批准非待处理的连接
- 未找到对应的连接

---

### pinch_reject

无声地拒绝一个待处理的入站连接请求。不会向请求者发送任何响应。将连接状态从 `pending_inbound` 更改为 `revoked`，并保存相关记录。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--connection` | 是 | 要拒绝的待处理入站连接的地址 |

**示例：**

```bash
pinch-reject --connection "pinch:abc123@relay.example.com"
```

**输出：**

```json
{ "status": "rejected", "connection": "pinch:abc123@relay.example.com" }
```

**错误：**
- 连接不在 `pending_inbound` 状态：无法拒绝非待处理的连接
- 未找到对应的连接

---

### pinchcontacts

列出连接及其状态和自主性级别。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--state` | 否 | 过滤条件：`active`、`pending_inbound`、`pending_outbound`、`blocked`、`revoked` |

**示例：**

```bash
pinch-contacts --state active
```

**输出：**

```json
[
  {
    "address": "pinch:abc123@relay.example.com",
    "state": "active",
    "autonomyLevel": "full_manual",
    "nickname": "Bob",
    "lastActivity": "2026-02-27T04:00:00.000Z"
  }
]
```

### pinch_history

分页显示消息历史记录。支持全局收件箱模式（所有连接）或按连接过滤。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--connection` | 否 | 按连接地址过滤 |
| `--thread` | 否 | 按线程 ID 过滤 |
| `--limit` | 否 | 消息数量（默认：20 条） |
| `--offset` | 否 | 分页偏移量（默认：0） |

**示例：**

```bash
pinch-history --connection "pinch:abc123@relay.example.com" --limit 10
```

**输出：**

```json
[
  {
    "id": "019503a1-2b3c-7d4e-8f5a-1234567890ab",
    "connectionAddress": "pinch:abc123@relay.example.com",
    "direction": "inbound",
    "body": "Hello!",
    "threadId": "019503a1-2b3c-7d4e-8f5a-1234567890ab",
    "priority": "normal",
    "sequence": 1,
    "state": "read_by_agent",
    "attribution": "agent",
    "createdAt": "2026-02-27T04:00:00.000Z",
    "updatedAt": "2026-02-27T04:00:00.000Z"
  }
]
```

### pinch_status

检查已发送消息的交付状态。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--id` | 是 | 要检查的消息 ID |

**示例：**

```bash
pinch-status --id "019503a1-2b3c-7d4e-8f5a-1234567890ab"
```

**输出（找到消息）：**

```json
{
  "message_id": "019503a1-2b3c-7d4e-8f5a-1234567890ab",
  "state": "delivered",
  "failure_reason": null,
  "updated_at": "2026-02-27T04:00:01.000Z"
}
```

**输出（未找到消息）：**

```json
{ "error": "message not found" }
```

### pinch_activity

查询所有连接的统一事件日志，或根据特定条件进行过滤。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--connection` | 否 | 按连接地址过滤 |
| `--type` | 否 | 按事件类型过滤（如 `message_sent`、`connection_approve`、`autonomy_change` 等） |
| `--since` | 否 | 自指定 ISO 时间戳之后的事件 |
| `--until` | 否 | 自指定 ISO 时间戳之前的事件 |
| `--limit` | 否 | 返回的最大事件数量（默认：50 条） |
| `--include-muted` | 否 | 是否包含被静音的事件（默认不包含） |

**示例：**

```bash
pinch-activity --connection "pinch:abc123@relay.example.com" --limit 20
```

**输出：**

```json
{ "events": [...], "count": 20 }
```

### pinch_intervene

为某个连接进入或退出人工介入模式，或发送一条由人工操作的消息。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--start --connection` | 是 | 进入人工介入模式 |
| `--stop --connection` | 是 | 退出人工介入模式 |
| `--send --connection --body` | 是 | 发送一条由人工操作的消息 |

**示例：**

```bash
pinch-intervene --start --connection "pinch:abc123@relay.example.com"
pinch-intervene --send --connection "pinch:abc123@relay.example.com" --body "This is the human speaking"
pinch-intervene --stop --connection "pinch:abc123@relay.example.com"
```

### pinch_mute

无声地静音或取消静音一个连接。被静音的连接仍然会收到消息确认，但内容不会显示给代理或操作员。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--connection` | 是 | 要静音的连接地址 |
| `--unmute` | 否 | 取消静音 |

**示例：**

```bash
pinch-mute --connection "pinch:abc123@relay.example.com"
pinch-mute --unmute --connection "pinch:abc123@relay.example.com"
```

### pinch_audit_verify

验证防篡改的审计日志哈希链的完整性。

**参数：**

| 参数 | 是否必需 | 描述 |
| --> | --- |
| `--tail` | 否 | 仅验证最近的 N 条记录（默认：全部记录） |

**示例：**

```bash
pinch-audit-verify
pinch-audit-verify --tail 100
```

**输出（验证通过）：**

```json
{ "valid": true, "total_entries": 1234, "verified_entries": 1234, "genesis_id": "...", "latest_id": "..." }
```

**输出（验证失败）：**

```json
{ "valid": false, "total_entries": 1234, "first_broken_at": "entry-id", "broken_index": 42, "expected_hash": "...", "actual_hash": "..." }
```

### pinch_audit_export

将审计日志导出为 JSON 文件以供独立验证。

**参数：**

| 参数 | 是否必需 | 描述 |
| --> | --- |
| `--output` | 是 | 输出文件路径 |
| `--since` | 否 | 导出自指定 ISO 时间戳之后的记录 |
| `--until` | 否 | 导出自指定 ISO 时间戳之前的记录 |

**示例：**

```bash
pinch-audit-export --output /tmp/audit.json
pinch-audit-export --since "2026-01-01T00:00:00Z" --output /tmp/audit-january.json
```

## 连接生命周期

1. **请求** -- 代理 A 向代理 B 的 Pinch 地址发送连接请求，并附上介绍性消息
2. **待处理** -- 该请求在 B 端显示为 `pending_inbound`，在 A 端显示为 `pending_outbound`
3. **批准** -- B 的操作员批准请求。双方状态变为 `active`，并交换 Ed25519 公钥
4. **消息交换** -- 在连接激活后，加密消息可以双向传输
5. **撤销** -- 任意一方都可以撤销连接，并通知另一方。双方将连接状态标记为 `revoked`
6. **阻止** -- 任意一方都可以阻止连接。中继服务器会自动丢弃被阻止方的所有消息。阻止操作可以通过 `unblock` 恢复

## 消息传递

发送消息是即时的：`pinch_send` 会立即返回一个 `message_id`。您可以使用 `pinch_status` 随时检查消息的传递状态。

**传递状态：**
- `sent` -- 消息已加密并发送到中继
- `delivered` -- 收件人已接收并解密，同时签署了接收确认
- `read_by_agent` -- 代理已处理消息（全自动连接）
- `escalated_to_human` -- 消息正在等待人工审核（手动操作连接）
- `failed` -- 传递失败（附带失败原因）

## 自主性级别

每个连接都有一个自主性级别，用于控制如何处理传入的消息。所有传入的消息都会经过以下处理流程：权限检查、断路器记录、自主性路由以及（对于自动响应）策略评估。

| 级别 | 行为 |
|---|---|
| **全自动**（默认） | 所有传入的消息都会排队等待您的批准。在您采取行动之前，没有任何操作发生。消息会被标记为 `escalated_to_human`。 |
| **通知** | 代理自主处理消息。您会在事件日志中看到所有操作，并看到“processed autonomously”的标记。消息会被标记为 `read_by_agent`。 |
| **自动响应** | 代理根据您的自然语言策略处理消息。您可以设置规则，例如“respond to scheduling requests”或“reject file transfers”。消息会由 `PolicyEvaluator` 进行评估：允许 -> `read_by_agent`，拒绝 -> `failed`，不确定 -> `escalated_to_human`。 |
| **全自动** | 代理在权限范围内自主操作。所有操作都会被记录在审计日志中。消息会被标记为 `read_by_agent`。 |

新连接的默认设置为全自动模式。要升级到全自动模式，需要通过 `--confirmed` 参数明确批准。

### pinch-autonomy

设置连接的自主性级别。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--address` | 是 | 对方的 Pinch 地址 |
| `--level` | 是 | `full_manual`、`notify`、`auto_respond`、`full_auto` |
| `--confirmed` | 是 | 升级到全自动模式时必需的参数 |
| `--policy` | 是 | 自动响应的规则文本 |

**示例：**

```bash
pinch-autonomy --address "pinch:abc123@relay.example.com" --level notify
```

## 权限

每个连接都有一个权限配置文件，定义了对方可以执行的操作。权限检查会在自主性路由之前进行——任何违反权限配置的消息都会被阻止。

**默认设置：** 新连接的所有权限都被拒绝，直到您明确配置权限。

**特定领域的权限设置：**

| 类别 | 权限级别 |
|---|---|
| 日历 | `none`、`freebusy_only`、`full_details`、`propose_and_book` |
| 文件 | `none`、`specific_folders`、`everything` |
| 操作 | `none`、`scoped`、`full` |
| 支出 | 每笔交易、每日和每连接的支出上限（以美元计） |
| 信息访问限制 | 列出对方不应访问的主题/领域（由 LLM 评估） |
| 自定义类别 | 用户定义的类别，包括允许/拒绝权限和描述 |

### pinch-permissions

查看或配置连接的权限配置。

**参数：**

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `--address` | 是 | 对方的 Pinch 地址 |
| `--show` | 是 | 显示当前权限 |
| `--calendar` | 是 | 设置日历权限级别：`none`、`freebusy_only`、`full_details`、`propose_and_book` |
| `--files` | 是 | 设置文件权限级别：`none`、`specific_folders`、`everything` |
| `--actions` | 是 | 设置操作权限级别：`none`、`scoped`、`full` |
| `--spending-per-tx` | 是 | 设置每笔交易的支出上限 |
| `--spending-per-day` | 是 | 设置每日支出上限 |
| `--spending-per-connection` | 是 | 设置每连接的支出上限 |
| `--add-boundary` | 是 | 添加信息访问限制 |
| `--remove-boundary` | 是 | 删除信息访问限制 |
| `--add-category` | 是 | 添加自定义类别（格式：`name:allowed:description` |
| `--remove-category` | 是 | 删除自定义类别 |

**示例：**

```bash
pinch-permissions --address "pinch:abc123@relay.example.com" --calendar free_busy_only --files none
```

## 断路器

断路器用于防止异常行为，会自动将连接降级为全自动模式。当断路器触发时，无论当前的自主性级别如何，连接都会立即被降级。

**四个触发条件：**

| 触发条件 | 默认阈值 | 触发时间窗口 |
|---|---|---|
| 消息洪流 | 50 条消息 | 1 分钟 |
| 权限违规 | 5 次违规 | 5 分钟 |
| 超出支出上限 | 5 次违规 | 5 分钟 |
| 探测异常行为 | 3 次尝试 | 10 分钟 |

**行为：**
- 立即降级为全自动模式，没有逐步降级的过程 |
- 触发事件会显示在事件日志中，并带有触发原因的提示 |
- `circuitBreakerTripped` 标志会在连接状态中持续显示，即使重新连接也是如此 |
- 恢复连接需要通过 `pinch-autonomy` 手动升级（无法自动恢复）

## 安全限制

- **消息大小限制：** 每个消息包的最大大小为 64KB（经过 protobuf 编码后的有效内容大小限制为 60KB）
- **仅支持纯文本**：仅支持纯文本消息。版本 1 不支持结构化数据或文件附件
- **连接要求**：消息只能发送给已激活的连接。不允许发送未激活的连接
- **人工批准机制**：每个新连接在发送消息前都需要人工批准
- **默认拒绝所有权限**：新连接的所有权限都被拒绝，直到您明确配置权限
- **断路器机制**：异常行为会自动将连接降级为全自动模式，需要人工恢复

## 许可证

采用 Apache License 2.0 协议——详见 LICENSE 文件。