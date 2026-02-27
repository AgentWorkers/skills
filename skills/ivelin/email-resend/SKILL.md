---
license: Apache-2.0
name: email-resend
version: "1.0.14"
metadata:
  clawdbot:
    requires:
      env:
        - RESEND_API_KEY
      bins:
        - python3
        - openclaw
      python:
        - requests
        - pyyaml
triggers:
  - "send email"
  - "check emails"
  - "email me"
  - "email notification"
  - "download attachment"
description: >
  使用 Resend API 发送和接收电子邮件。该 API 可用于：  
  (1) 直接通过 Resend API 发送电子邮件；  
  (2) 通过 cron 任务接收电子邮件通知；  
  (3) 撰写带有正确线程结构的回复邮件；  
  (4) 从传入的电子邮件中下载附件。  
  **必需的环境变量：** RESEND_API_KEY（API 密钥）  
  **可选的环境变量：** DEFAULT_FROM_EMAIL、DEFAULT_FROM_NAME（如果未设置，则使用偏好设置文件中的值）  
  **许可证：** Apache-2.0 — 详细信息请参阅 LICENSE 文件。
---
## 许可证

本工具采用 **Apache License 2.0**。完整许可协议请参阅 `LICENSE` 文件。

### 通过 Resend API 发送和接收电子邮件

您可以使用 Resend API 来发送和接收电子邮件。

## 配置

**无需配置文件。** 该工具会自动从以下来源获取配置信息：

1. **环境变量**：`RESEND_API_KEY`（必需）、`DEFAULT_FROM_EMAIL/NAME`（可选）
2. **偏好设置文件**：`memory/email-preferences.md`（`from_email`、`from_name`、`telegram_target`）
3. **OpenClaw 环境**：`channel`、`chat_id`、`thread_id`（用于定时任务）

### 必需的环境变量

### 偏好设置文件

该工具会从 `memory/email-preferences.md` 文件中读取发送者的相关信息：

脚本会首先检查环境变量，如果环境变量不存在，则会从偏好设置文件中获取信息。

### 首次设置

当该工具首次被调用时，子代理应执行以下操作：

1. **检查 OpenClaw 环境**：已有的信息包括：
   - `context.user.email`（来自 `USER.md`）
   - `context.channel`（来自当前会话）
   - `context.chat_id`
   - `context.thread_id`（用于主题）

2. **检查内存**：使用 `memory_get` 工具：
   - 尝试读取：`memory_get path="memory/email-preferences.md"`
   - 如果文件不存在，提示用户创建 `memory/email-preferences.md`（不会回退到其他文件进行扫描）

3. **如果信息缺失，询问用户**：通过聊天消息询问用户以下内容：
   - “应该使用哪个电子邮件地址发送？”（`from_email`）
   - “发送邮件时使用的显示名称是什么？”（`from_name`）
   - “应该通过哪个频道/主题通知您？”（`telegram_target` 和 `thread_id`）

4. **根据用户的回答创建 `memory/email-preferences.md` 文件**。

5. **将配置信息保存到内存中**：将偏好设置写入内存，以便在后续会话中使用。请使用包含 YAML 前言的 Markdown 格式。

**Markdown 格式（包含 YAML 前言）：**
请将配置信息保存在 `memory/email-preferences.md` 文件中（而非 `MEMORY.md` 文件），因为独立的定时任务只能通过 `memory_get` 读取该文件。

### OpenClaw 环境字段（子代理中可用）

| 字段 | 来源 | 示例 |
|-------|--------|---------|
| `user.email` | USER.md | `you@company.com` |
| `user.name` | USER.md | `Your Name` |
| `channel` | OpenClaw | 来自 OpenClaw 环境 |
| `chat_id` | OpenClaw | `123456789` |
| `thread_id` | OpenClaw | `334` |

该工具会直接使用 OpenClaw 环境中的这些字段，无需额外解析。

## 使用方法

### 接收邮件（Inbound）

### 定时任务配置

有两种方式可以配置定时任务：

#### 选项 1：静态目标（硬编码）

如果您希望始终使用相同的发送目标，请使用此方法：

#### 选项 2：动态目标（来自偏好设置）——推荐使用

此方法会从 `memory/email-preferences.md` 文件中读取您的通知偏好设置，并自动配置定时任务。

运行命令：
```
```
```
```

**功能说明：**
1. 从 `memory/email-preferences.md` 文件中读取您的 Telegram 发送目标/主题 ID。
2. 删除现有的 `email-resend-inbound` 定时任务。
3. 创建一个新的定时任务，使用您指定的发送目标。

**首次设置：** 如果偏好设置文件不存在，系统会提示您需要配置的内容。

**参数：**
- `--schedule "cron */15 * * * *"` — 每 15 分钟运行一次
- `--session isolated` — 用于代理任务的数据传输
- `--announce` — 启用将结果发送到聊天频道
- `--channel telegram` — 发送渠道
- `--to` — Telegram 发送目标（格式：`chat_id:topic:thread_id`

**注意：** 定时任务配置会从 `memory/email-preferences.md` 文件中读取通知偏好设置。首次运行时，如果文件不存在，系统会询问您以下信息：
- 通知应发送到哪个频道（例如 Telegram、Discord 等）
- 聊天 ID 和主题 ID

### 手动检查

### 通知格式

每封新收到的邮件都会触发通知，内容包括：
- 发件人、主题、日期
- 正文预览（约 2000 个字符）
- 附件列表（如果有）
- 重要性级别：🔥 高度重要 / 📅 会议 / 📬 普通

### 确认流程（非常重要）

**切勿自动确认邮件。** 只有用户才能通过以下方式确认邮件：
- 回复通知消息
- 输入 `done` 或 `ack`

邮件必须保持未确认状态，直到用户明确确认。

请使用 `draft-reply.py` 脚本来编写回复，并确保使用正确的引用格式（`[[reply_to_current]]`）。

**重要提示：** 始终使用内联回复（`[[reply_to_current]]`），以保持消息在聊天线程中的关联性。这样可以：
- 正确追踪消息的流转过程
- 确保回复能够关联到原始邮件
- 保持对话的连贯性

**重要提示：** 当通过 OpenClaw 消息工具回复时，请使用 `replyTo` 参数（而不是 `[[reply_to_current]]` 标签）：

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `inbound.py` | 检查邮件并发送通知 |
| `draft-reply.py` | 使用引用格式起草回复 |
| `outbound.py` | 直接发送邮件 |
| `download_attachment.py` | 从收到的邮件中下载附件 |

### 下载附件

要从收到的邮件中下载附件，请使用以下脚本：

**注意：** API 路径是 `/emails/receiving/{email_id}/attachments`（而非标准的 `/emails/` 路径）。

## 状态文件

- `memory/email-resend-inbound-notified.json` — 未确认/已确认的邮件
- `memory/email-message-map.json` — 通知消息 ID 到邮件 ID 的映射关系（旧版本）
- `memory/email-custody-chain.json` — 邮件 → 通知 → 操作的完整有向无环图（DAG）
- `memory/email-msg-to-chain.json` — 通知消息 ID 到操作链的映射关系
- `memory/email-draft-state.json` — 待发送邮件的状态（邮件 ID、状态、回复内容）

有关有向无环图（DAG）的设计，请参阅 `docs/custody-chain.md`。

## 发送邮件（Outbound）

### ⚠️ 非常重要：邮件回复规则（2026-02-22）

**必须使用 `draft-reply.py` 来回复邮件。** 这是一条不可更改的规则。违反此规则会导致 Gmail 的回复线程出现问题。

### 为什么这很重要？
- Gmail 根据 `In-Reply-To` 和 `References` 标头来组织邮件线程
- 如果使用错误的标头，回复邮件会创建新的线程，导致上下文丢失
- 发送后无法更改这一设置

### 正确的工作流程（务必遵循）

### ⚠️ 非常重要：审批执行规则（2026-02-22）

**当用户批准回复草稿时，必须立即执行发送命令。**

**避免的错误操作：**
- ❌ 先展示草稿供用户审批 → 用户点击“发送”后仅确认，不执行发送操作
- ✅ 先展示草稿供用户审批 → 用户点击“发送”后，执行 `draft-reply.py send` 命令

**正确的流程：**
**切勿：**
- 仅确认审批而不执行发送操作
- 在用户批准后再次请求确认
- 等待用户确认后再发送邮件

### 绝对禁止的操作：
- **切勿使用 `outbound.py` 来回复邮件：**
**切勿手动设置 `--reply-to` 标签：**
**切勿在主题以 “Re:” 开头时跳过处理流程：**

`outbound.py` 仅用于 **新邮件**（而非回复邮件）：
- 首次联系时的邮件
- 需要创建新线程的邮件

对于任何可能被视为回复的邮件，请使用 `draft-reply.py` 脚本。

## 必需条件

- 确保设置了 `RESEND_API_KEY` 环境变量
- 需要 `requests` Python 库

### 草稿回复的最佳实践

使用 `draft-reply.py` 起草回复时，请遵循以下规则：
1. **始终引用原始邮件**：在回复中加上 `>` 前缀，以便接收者知道您是在回复哪封邮件
2. **正确设置线程信息**：使用原始邮件的 Message-ID 设置 `In-Reply-To` 和 `References` 标头
3. **保留主题行**：回复时以 `Re: ` 开头，以保持线程的连续性（但避免使用 “Re: Re:”）
4. **回复结构：**
   （具体结构见代码示例）
5. **支持多次回复**：发送回复后，草稿会被标记为“已发送”，您可以继续在同一线程中回复
6. **避免重复使用 “Re:”**：如果原始邮件的主题已经以 “Re:” 开头，不要再次添加 “Re:”
7. **追踪消息流转**：确保完整的消息流转记录：
   - 邮件 → 通知 → 所有回复/操作
   - 使用有向无环图（DAG）来记录消息的流转路径

## 草稿回复命令

| 命令 | 功能 |
|---------|---------|
| `start <email_id>` | 开始回复某封邮件 |
| `resume` | 继续已发送的邮件进行回复 |
| `content "text"` | 设置回复内容 |
| `send` | 发送回复 |
| `cancel` | 取消草稿 |
| `status` | 查看当前草稿的状态 |

发送回复后，可以使用 `resume` 命令在同一线程中继续回复。回复时，回复的线程信息会保持不变。

**测试说明：** 总共需要运行 43 个测试（`test_inbound.py`：37 个，`test_threading.py`：6 个，`test_attachments.py`：数量不定）。

如果测试失败，请：
1. 查明哪个测试失败及其原因
2. 修复相关功能或代码，使其符合预期行为
3. 如果功能有变更，请更新测试用例。

## 隐私与安全注意事项

### 必需的凭据
- **RESEND_API_KEY**：必需。请从 https://resend.com 的 API 设置中获取。创建此密钥时请使用最低权限。
- **DEFAULT_FROM_EMAIL** / **DEFAULT_FROM_NAME**：可选。如果未设置，将从 `memory/email-preferences.md` 文件中读取。

### 内存文件访问

该工具仅从指定的偏好设置文件中读取数据：
- `memory/email-preferences.md`：用于存储 Telegram 发送目标/主题 ID
**不会扫描 `MEMORY.md`、`USER.md`、`TOOLS.md` 或 `memory/*.md` 文件**

这种限制性的访问方式可以防止敏感信息泄露。

### 定时任务

`configure-cron.py` 脚本会通过 OpenClaw CLI 创建或删除名为 `email-resend-inbound` 的定时任务。

### 建议：
- 在生产环境中启用该工具之前，请使用虚拟的 `RESEND_API_KEY` 进行测试
- 如果您只需要发送邮件，无需启用接收邮件/定时任务功能
- 审查 `memory/email-preferences.md` 文件，确保其中仅包含必要的字段
- 保持偏好设置文件简洁——仅包含必需的字段（如发送目标、主题 ID）