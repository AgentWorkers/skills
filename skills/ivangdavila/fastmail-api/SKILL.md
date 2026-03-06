---
name: Fastmail API
slug: fastmail-api
version: 1.0.0
homepage: https://clawic.com/skills/fastmail-api
description: 通过 JMAP API 调用，可以安全地批量管理 Fastmail 的邮件、邮箱、身份信息、联系人和日历相关的工作流程，同时确保令牌的安全性（即防止令牌被滥用）。
changelog: Initial release with production-safe Fastmail JMAP API workflows for mail, mailbox, identity, and calendar automation.
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["curl","jq"],"env":["FASTMAIL_API_TOKEN"]},"os":["linux","darwin","win32"]}}
---
# Fastmail API 操作指南

## 设置

首次使用时，请阅读 `setup.md` 文件，以了解账户集成偏好、激活规则以及凭证处理方式。

## 使用场景

当用户需要通过 API 调用来自动化 Fastmail 的操作时（如邮箱管理、消息搜索、草稿/发送流程、身份设置、联系人操作或日历事件管理等），本技能可提供支持。代理会负责处理能力检测、安全请求的构建以及高影响操作的确认工作。

## 架构

所有相关数据存储在 `~/fastmail-api/` 目录下。具体结构请参考 `memory-template.md` 文件。

```text
~/fastmail-api/
├── memory.md         # Account context, IDs, and operating preferences
├── request-log.md    # High-impact API actions and outcomes
└── snapshots/        # Optional payload backups before bulk writes
```

## 快速参考

当您需要了解核心操作规则之外的详细信息时，请参考以下文件：

| 主题 | 文件名 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 会话与方法调用模式 | `jmap-patterns.md` |
| 邮箱与消息工作流程 | `mail-workflows.md` |
| 联系人与日历操作 | `calendar-contacts.md` |
| 错误处理与恢复 | `troubleshooting.md` |

## 所需工具

- `curl`
- `jq`
- `FASTMAIL_API_TOKEN`
- 可选：`FASTMAIL_API_BASE`（默认值为 `https://api.fastmail.com/jmap/api`）

**注意**：切勿将 bearer token 存储在仓库文件、shell 历史记录或共享日志中。

## 数据存储

- `~/fastmail-api/memory.md`：用于存储账户 ID、默认设置以及工作流程上下文信息。
- `~/fastmail-api/request-log.md`：用于记录高影响操作的历史记录。
- `~/fastmail-api/snapshots/`：用于在批量更新前备份数据。

## 核心规则

### 1. 在执行任何操作前先检测会话能力

- 首先调用 Fastmail 的 JMAP 会话端点，以确认 `apiUrl`、`primaryAccounts` 以及支持的功能。
- 将检测到的账户 ID 存储在内存中，以避免写入错误的账户。

```bash
curl -sS https://api.fastmail.com/jmap/session \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" | jq
```

### 2. 在方法调用中明确指定账户范围

- 在每次方法调用中，必须指定使用的功能（`using`）以及对应的账户 ID。
- 使用唯一的 `clientCallId` 值，以便能够安全地追踪重试操作。

```bash
curl -sS "${FASTMAIL_API_BASE:-https://api.fastmail.com/jmap/api}" \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "using": ["urn:ietf:params:jmap:mail", "urn:ietf:params:jmap:core"],
    "methodCalls": [
      ["Mailbox/get", {"accountId": "u123", "ids": null}, "c1"]
    ]
  }' | jq
```

### 3. 使用安全的分页和过滤机制

- 对于大型邮箱，请避免执行无限制的查询；务必设置查询范围和过滤条件。
- 相比于直接导出整个邮箱内容，建议使用 `Email/query` 或 `Email/get` 等方法。

### 4. 对高影响操作进行确认

- 在删除邮箱、移动多条消息、更新账户信息或批量修改日历事件之前，请务必进行确认。
- 对于高影响性的写入操作，请将操作前的数据备份到 `~/fastmail-api/snapshots/` 目录中。

### 5. 正视部分失败情况

- 每次写入操作完成后，检查 `notCreated`、`notUpdated` 等状态码以及方法级别的错误信息。
- 明确报告部分失败的情况，并提供回滚或重试的方案。

### 6. 保护输出数据中的敏感信息

- 在正常响应中，切勿打印原始的授权头信息或完整的 token 字符串。
- 在将日志共享到外部环境时，应隐藏地址和主题行内容。

### 7. 通过后续读取操作验证写入结果

- 写入操作完成后，通过 `Mailbox/get`、`Email/get`、`Contact/get`、`CalendarEvent/get` 等方法验证最终状态。
- 仅在确认状态正确后，才完成任务的执行。

## 安全检查清单

在进行批量更新、删除操作、发送消息或修改账户信息之前，请执行以下步骤：

1. 确认目标账户 ID 和操作环境。
2. 拍摄请求的快照，以便在需要时进行回滚。
3. 确认用户对不可逆操作的意图。
4. 先执行最小范围的、安全的批量操作。
5. 通过读取操作验证操作后的状态。

## Fastmail API 的潜在风险

- 如果跳过会话检测步骤，可能会导致数据被写入错误的账户。
- 如果在方法调用中未指定所需的功能，可能会导致方法失败（看似是身份验证问题）。
- 未经过滤的批量消息移动操作可能会意外地重新组织整个邮箱的内容。
- 如果在未检查 `notUpdated` 状态码的情况下假设所有操作都成功，可能会掩盖部分失败的情况。
- 在调试输出中记录 bearer token 会带来凭证泄露的风险。

## 外部端点

本技能仅使用 Fastmail 官方提供的 JMAP 端点：

| 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| `https://api.fastmail.com/jmap/session` | 包含 bearer token 的授权头信息 | 用于获取 API 端点地址、功能列表和账户 ID |
| `https://api.fastmail.com/jmap/api` | 用于执行邮箱、邮箱管理、身份信息、联系人和日历操作的 JMAP 方法请求 | 用于读写操作 |

**注意**：不会向外部发送任何其他类型的数据。

## 安全性与隐私

**离开您机器的数据：**
- 包含身份验证信息的 JMAP 请求数据（用于邮箱、消息、联系人和日历操作）
- 根据请求内容生成的元数据（用于查询和写入操作）

**保留在本地的数据：**
- 操作相关的上下文信息（存储在 `~/fastmail-api/memory.md` 中）
- 高影响操作的历史记录（存储在 `~/fastmail-api/request-log.md` 中）
- 可选的备份数据（存储在 `~/fastmail-api/snapshots/` 中）

**本技能不会：**
- 发送未声明的 API 请求数据
- 将 bearer token 存储在仓库文件中
- 在未经明确确认的情况下执行具有破坏性的写入操作

## 信任机制

使用本技能意味着您的邮箱和日历操作数据将被发送到 Fastmail 的服务器。请仅在您信任 Fastmail 并同意其处理这些数据的情况下安装本技能。

## 相关技能

如果用户需要，可以使用以下技能进行扩展安装：

- `clawhub install <slug>`：
  - `api`：用于构建复杂的 API 请求和响应处理流程。
  - `oauth`：用于管理 token 的生命周期并确保授权流程的安全性。
  - `mail`：用于规划高质量的电子邮件发送流程和格式。
  - `webhook`：用于根据 API 的变化触发自动化集成。

## 反馈建议

- 如果本技能对您有帮助，请使用 `clawhub star fastmail-api` 给予评分。
- 为了保持信息更新，请使用 `clawhub sync` 功能。