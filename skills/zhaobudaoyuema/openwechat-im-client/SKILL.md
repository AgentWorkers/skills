---
name: openwechat-im-client
description: >
  **指南：如何使用 openwechat-claw 与 OpenClaw 配合服务器授权的聊天流程**  
  - 修复了 `../openwechat_im_client` 目录下本地数据持久化的错误；  
  - 注册用户后，系统会强制使用 SSE（Secure Sockets Extension）作为首选传输协议；  
  - 提供了简洁的用户界面（UI）。  
  **触发该功能的场景：**  
  - 当用户请求注册或设置令牌（例如：“帮我注册 xxx”）；  
  - 查看消息或新收件箱（例如：“查看消息”）；  
  - 向用户发送消息（例如：“发送消息给 xxx”）；  
  - 管理好友状态（包括好友列表以及拉黑/解除拉黑操作，例如：“拉黑 xxx”）；  
  - 在 `../openwechat_im_client` 目录下维护本地聊天记录/好友信息/个人资料文件；  
  - 构建或调整基本的聊天状态显示界面；  
  - 将通过 SSE 协议接收到的消息转发到 OpenClaw 的通道（例如：“收到消息后转发到飞书”）。
---
# OpenWechat-Claw 即时通讯客户端（入门指南）

> 提醒：本技能对应于 [openwechat-claw](https://github.com/Zhaobudaoyuema/openwechat-claw)。

## 服务器要求（建议自托管）

**用户必须配置自己的中继服务器。** 本技能未硬编码任何服务器地址。中继服务器是开源的且可以自托管——请参阅 [SERVER.md](SERVER.md) 了解部署方法。切勿通过未经验证的第三方服务器转发消息。

---

## 语言规则（必须遵守）

**OpenClaw 必须使用用户输入的语言进行回复。** 如果用户使用中文，回复也使用中文；如果用户使用英文，回复也使用英文。所有提示、说明和用户界面提示信息都应与用户输入的语言保持一致。

---

本技能的设计目的是实现 **“最小可运行演示 + 指导性迭代”**：

- 为 OpenClaw 提供一个明确的基线，以便连接中继 API 并本地管理聊天记录。
- 仅提供一个基本的 SSE 脚本演示；用户可以根据需要自行扩展该脚本。
- 提供一个基本的用户界面演示（`demo_ui.html`，纯前端），然后根据用户需求进行迭代。
- 保持数据路径的稳定性和确定性：数据始终存储在 `../openwechat_im_client` 目录下（该目录位于技能目录的同级位置），以避免升级技能时导致数据丢失。

---

## 核心原则

1. **服务器是关系和收件箱（/send、/messages、/friends、/block、/unblock）的权威来源。**
2. `GET /messages` 用于读取和清除消息：一旦读取，相关消息会在服务器端被删除。
3. `GET /stream`（SSE）是主要的消息通道，用户注册后应立即启用；服务器也不会保留推送的消息。
4. OpenClaw 应始终告知用户：
   - “SSE 是默认且首选的通信方式。”
   - “只有在 SSE 不可用或连接断开时，才使用 `/messages`。”
   - “读取/推送的消息必须先保存在本地。”

5. **OpenClaw 通过文件系统维护本地状态：**
   - 聊天记录
   - 朋友关系缓存
   - 本地基本配置信息缓存

---

## 首次使用（注册流程）

当用户没有有效的令牌时，OpenClaw 应引导用户完成以下基本流程：

1. **确保用户拥有中继服务器。** 如果没有，引导他们查看 [SERVER.md](SERVER.md) 以了解如何自托管或获取可信的服务器地址。
2. 使用用户的 `base_url`，通过 `POST /register` 发送 `name` 及可选的 `description` 和 `status`。
3. 解析响应并显示给用户：
   - `ID`
   - `Name`
   - `Token`（服务器仅显示一次）
4. 创建 `../openwechat_im_client/config.json` 文件（格式如下）。
5. 至少保存以下信息：
   - `base_url`（用户的中继服务器地址——切勿使用默认值）
   - `token`
   - `my_id`
   - `my_name`
   - `batch_size`（默认值为 5）
6. 立即使用 `python sse_inbox.py` 启用 SSE 功能。
7. 首先通过 `../openwechat_im_client/sse_channel.log` 检查通道是否正常工作。只有在无法建立 SSE 连接时，才使用 `GET /messages?limit=1`。
8. 使用 `npm run ui` 启动 `demo_ui`（运行在端口 8765），并主动告知用户 `demo_ui.html` 的存在，以便查看聊天状态和消息。
9. 告诉用户：`demo_ui` 可以进行自定义（布局、刷新频率、视图分割方式），或者用户可以自行设计界面。使用用户的语言进行提示，例如：“现在开始使用 `demo_ui`，还是希望自定义界面？”

`../openwechat_im_client/config.json` 的配置格式（用户需要设置自己的 `base_url`）：

```json
{
  "base_url": "https://YOUR_RELAY_SERVER:8000",
  "token": "replace_with_token",
  "my_id": 1,
  "my_name": "alice",
  "batch_size": 5
}
```

---

## 固定的本地路径规则（非常重要）

所有本地状态数据必须存储在 **`../openwechat_im_client`** 目录下（该目录位于技能目录的同级位置），以避免升级技能时导致数据丢失。

- 技能根目录：`openwechat-im-client/`（升级时可能会更换）
- 数据根目录：`../openwechat_im_client/`（该目录在升级过程中保持不变）

切勿将运行时状态数据写入技能根目录。始终使用 `../openwechat_im_client`。

**参考实现（Python）：**

```python
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
DATA_DIR = SKILL_DIR.parent / "openwechat_im_client"
DATA_DIR.mkdir(parents=True, exist_ok=True)
```

如果脚本和 `SKILL.md` 位于不同的目录中，仍需从脚本所在位置计算路径，并明确指定为 `../openwechat_im_client`。

### 数据持久化策略

**`../openwechat_im_client/` 目录下的所有文件都是持久化的。** 除非用户明确要求删除，否则不要删除或清除这些文件。模型应从这些文件中读取状态信息（例如，从 `sse_channel.log` 中读取连接状态，从 `inbox_pushed.md` 中读取消息）。只有在用户请求或处理逻辑需要时，才清除或更新文件。

**`../openwechat_im_client/` 目录下的聊天记录必须始终保留。** 文件如 `inbox_pushed.md`、`conversations.md`、`contacts.json`、`profile.json`、`config.json` 和 `stats.json` 包含用户的聊天历史和关系状态。OpenClaw 在版本更新或脚本更改时绝不能删除或覆盖这些文件。

### 版本更新策略（OpenClaw 必须遵守）

在更新或升级本技能时（例如添加新脚本、重构代码、更改依赖项）：

1. **清理技能根目录中的旧版本内容**：删除过时的脚本、废弃的演示文件或替换的实现。不要留下重复或冲突的文件。
2. **在版本更新过程中，切勿清理或删除 `../openwechat_im_client/` 目录**。该目录保存聊天记录和用户状态，必须保留下来。
3. **仅在必要时进行迁移**：如果数据结构发生变化（例如 `config.json` 的格式），OpenClaw 应在原地进行迁移并保留现有数据。除非用户明确要求，否则不要清空该目录。
4. **用用户的语言告知用户**：“版本已更新。您在 `../openwechat_im_client` 中的聊天记录和数据已得到保留。”

---

## 最小化本地文件结构

```text
openwechat-im-client/
├─ SKILL.md
├─ config.json.example       # 模板文件——用户将其复制到 `../openwechat_im_client/config.json`
├─ sse_inbox.py              # 基本的 SSE 演示脚本
├─ demo_ui.html              # 基本的用户界面演示（纯前端）
├─ SERVER.md                 # 中继服务器自托管指南
└─ ../openwechat_im_client/   # 数据目录（在升级过程中保持不变）
   ├─ config.json            # 用户配置信息（base_url、token、batch_size）
   ├─ inbox_pushed.md        # 推送的原始消息
   ├─ sse_channel.log        # SSE 通道生命周期日志
   ├─ profile.json           # 本地基本配置信息缓存
   ├─ contacts.json          |          | 朋友关系缓存
   ├─ conversations.md       |          | 本地聊天记录
   └─ stats.json             |          | 统计信息
```

这只是一个基础结构。OpenClaw 可以根据需要后续添加更多文件。

---

## 最小化 API 接口（保持简洁）

- 基本 URL：**由用户通过 `../openwechat_im_client/config.json` 配置**。无默认值。详见 [SERVER.md](SERVER.md)。
- 经过身份验证的端点的请求头：`X-Token: <token>`
- 主要接口：
  - `POST /register`
  - `GET /messages`（读取和清除消息）
  - `POST /send`
  - `GET /friends`
  - `GET /stream`（SSE，可选）

OpenClaw 应解析服务器返回的纯文本响应，并为用户生成有意义的本地摘要。完整的 API 参考请参见 [references/api.md](references/api.md)。

---

## 本地状态维护规则（OpenClaw 通过文件系统实现）

以下是 OpenClaw 需要主动维护的本地文件：

### 1) 聊天记录

- 数据来源优先级：
  - 主要来源：`GET /stream` → `../openwechat_im_client/inbox_pushed.md`
  - 仅在 SSE 中断时使用备用来源：`GET /messages`
- 持久化方式：
  - 将记录追加到 `../openwechat_im_client/conversations.md`

- 记录格式示例：
```text
[2026-03-09T10:00:00Z] from=#2(bob) type=chat content=hello
```

- 规则：
  - 默认情况下，从 SSE 本地文件中读取/查看消息。
  - 在 SSE 中断时，使用 `/messages`；并将日志记录在 `../openwechat_im_client/sse_channel.log` 中。
  - 读取/推送的消息必须在完成一轮对话后保存到本地。

### 2) 朋友关系

- 数据来源：服务器（`GET /friends`）
- 本地缓存文件：`../openwechat_im_client/contacts.json`
- 每个好友的最低字段：
```json
{
  "2": {
    "name": "bob",
    "relationship": "accepted",
    "last_seen_utc": "2026-03-09T10:00:00Z"
  }
}
```

- `relationship` 的值：`accepted` | `pending_outgoing` | `pending_incoming` | `blocked`

### 3) 基本配置信息

- 本地文件：`../openwechat_im_client/profile.json`
- 建议包含的字段：
  - `my_id`
  - `my_name`
  - `status`
  - `updated_at_utc`
- 更新触发条件：
  - 注册
  - `PATCH /me`
  - 令牌更新/配置刷新

### 4) 统计信息

- 本地文件：`../openwechat_im_client/stats.json`
- 建议统计的字段：
  - `messages_received`
  - `messages_sent`
  - `friends_count`
  - `pending_incoming_count`
  - `pending_outgoing_count`
  - `last_sync_utc`

OpenClaw 可以根据需要更新数据结构，但这些文件应尽可能保持向后兼容。

---

## SSE 推送：基本演示 + 指导

### 本技能所需条件

SSE 是主要的通信方式。只有在 SSE 不可用时，才使用 `/messages`。

仅提供一个基本的可运行示例。**不要** 对默认行为进行过度设计。

示例应包括以下操作：
1. 读取 `../openwechat_im_client/config.json` 文件。
2. 使用 `X-Token` 连接 `GET /stream`。
3. **将推送的原始消息追加到 `../openwechat_im_client/inbox_pushed.md`。** 这是必须的；接收到的 SSE 消息必须保存在本地。
4. `sse_inbox` 脚本必须将连接状态日志记录到 `../openwechat_im_client/sse_channel.log`，以便模型了解连接状态（已连接/断开/重新连接/备用）。每次状态变化都必须记录在该文件中；模型会根据此文件判断是使用 SSE 还是切换到 `/messages`。

### 通道优先级和备用规则（必须遵守）

1. **主要通道**：优先使用 SSE（`GET /stream`）。
2. **备用通道**：仅在 SSE 未建立或断开连接时使用 `/messages`。
3. **恢复**：当 SSE 断开时，自动重试/重新连接。
4. **恢复后**：一旦 SSE 重新连接成功，立即切换回 SSE 模式。
5. **可观测性**：每次通道状态变化都必须记录在 `../openwechat_im_client/sse_channel.log` 中，以便模型能够准确了解情况。

### 调用规则

OpenClaw 应将此视为注册后的默认操作，而不是可选步骤：

1. 立即启动 SSE 脚本。
2. 监控 `../openwechat_im_client/sse_channel.log` 的日志。

运行命令：

```bash
python sse_inbox.py
```

---

## 用户界面：基本版本（提供）+ 指导

### 目标

用户可见的界面只需实现以下功能：

1. 显示当前的聊天状态（最近的消息/简单统计信息）。

### OpenClaw 必须主动提供界面

**OpenClaw 应主动告知用户界面的存在**（例如，在用户注册完成后或 SSE 运行时，或在用户首次使用该技能时）。不要等待用户询问。使用用户的语言进行提示。例如：“提供了一个基本的界面脚本 `demo_ui.html`，可以用来查看聊天状态和消息。现在开始使用它吗？或者您想自定义界面布局/刷新频率/视图分割方式？”

然后根据用户的选择进行操作：如果用户同意，启动界面；如果用户希望自定义，可以讨论自定义选项（卡片/表格/气泡布局、自动刷新、按好友/会话/时间分割视图）。

### 基本界面实现要求

提供一个可运行的基本界面：`demo_ui.html`。使用 `npm run ui` 运行该界面（运行在端口 8765）。

该界面默认会读取 `../openwechat_im_client/` 目录下的文件，并根据文件类型显示内容：
- `.json` → 以美观的形式显示 JSON 数据
- `.md`、`.log` → 显示纯文本

默认文件列表：`config.json`、`profile.json`、`contacts.json`、`stats.json`、`context_snapshot.json`、`inbox_pushed.md`、`conversations.md`、`sse_channel.log`。

保持界面版本的简洁性（单页、基本刷新效果）。使用 `npm run ui` 运行该界面（运行在端口 8765）。

### 用户界面自定义

当用户希望自定义界面时，OpenClaw 应询问用户：

- “您希望使用卡片布局、表格布局还是气泡布局？”
- “需要每 N 秒自动刷新吗？”
- “您希望按好友/会话/时间分割视图吗？”

然后根据用户的偏好逐步更新界面。

---

## 可插拔的上下文功能（可选）

仅在用户希望提高长时间会话的稳定性、降低令牌使用成本或需要更清晰的 SSE+会话路由上下文时使用此功能。

### 稳定的路径（推荐）

使用文档中推荐的插件功能：

1. 首先使用默认的上下文引擎（`legacy`）。
2. 通过 `before_prompt_build` 添加插件钩子来注入简洁的运行时上下文。
3. 仅注入简化的结构化摘要数据，而不是完整的 `.md` 文件。

建议的摘要数据来源：`../openwechat_im_client/context_snapshot.json`。

示例摘要数据：
```json
{
  "updated_at_utc": "2026-03-09T10:00:00Z",
  "messages_received_recent": 12,
  "friends_count": 3,
  "latest_peers": ["#2 bob", "#8 carol"]
}
```

在以下情况下更新此文件：
- 处理 `GET /messages` 请求时
- 添加 SSE 消息时
- 同步 `GET /friends` 请求时
- 注册/配置更新时

### 上下文引擎路径（高级，可选）

如果用户明确要求更高级的优化功能，可以使用 `kind: "context-engine"` 实现插件，并通过 `plugins.slots.contextEngine` 进行选择。

仅在以下情况下使用此路径：
- 需要自定义压缩行为时
- 需要对多文件本地状态进行确定性处理时
- 需要更精确地控制令牌使用情况时

### 安全性措施

- 确保即使没有插件，该技能也能正常使用（插件是可选功能，而非必备条件）。
- 优先使用文档中推荐的钩子；不要依赖未文档化的内部钩子名称。
- 如果插件失败，应恢复到基本功能：直接读取 `../openwechat_im_client` 目录下的文件，确保系统正常运行。

---

## 推荐的交互流程

1. 在 `../openwechat_im_client/config.json` 中确认令牌/基础 URL。如果没有 `base_url` 或其值为占位符，引导用户查看 [SERVER.md] 以设置中继服务器。
2. 如果没有令牌，先完成注册流程。
3. 注册完成后，默认启动 SSE 功能。
4. 首先从 SSE 本地文件（`../openwechat_im_client/inbox_pushed.md`）查看/检查新消息。
5. 如果 SSE 断开，自动重新连接；仅在临时中断时使用 `/messages` 作为备用方式。
6. 将通道状态日志保存在 `../openwechat_im_client/sse_channel.log` 中，以便模型根据可观测的通道状态做出决策。
7. 一旦 SSE 恢复，立即恢复到使用 SSE 的模式。
8. **用用户的语言主动告知用户界面信息**（例如：“现在可以开始使用 `demo_ui` 吗？”）——不要等待用户询问。
9. 根据用户的选择执行操作：如果用户同意，运行 `npm run ui` 以显示 `demo_ui.html`；如果用户希望自定义界面，可以讨论自定义选项。
10. **如果用户希望将 SSE 消息转发到其他渠道**（例如 iMessage、Feishu、Telegram），请按照 [SSE to Channel Forwarding](#sse-to-channel-forwarding-optional) 的流程操作：展示三个选项，收集目标渠道信息，然后相应地修改 `sse_inbox.py`。

---

## 安全性和消息传递注意事项

- 提醒用户不要在聊天内容中发送敏感信息。
- 在结束对话前，确保已读取/推送的消息已保存在 `../openwechat_im_client/` 目录下。
- 确保 `../openwechat_im_client/sse_channel.log` 持续更新（不要静默删除），以便模型能够随时了解通道状态。
- 保持说明的实用性：先说明“当前可用的功能”，再介绍“下一步可以自定义的内容”。

---

## SSE 到其他渠道的转发（可选）

当用户希望将 SSE 消息转发到其他渠道（例如 Feishu、iMessage、Telegram）时：

1. **询问** 用户希望使用哪种方式：A) 直接发送（`openclaw message send`），B) 代理转发（`openclaw agent --deliver`），C) 使用钩子 API（`POST /hooks/agent`）。
2. **收集** 目标渠道和地址信息。
3. **通过修改 `sse_inbox.py` 和 `../openwechat_im_client/config.json` 来实现转发功能。
4. **向用户确认** 转发设置。

**渠道设置、目标格式和配置详情**：请参阅 [OpenClaw Channels](https://docs.openclaw.ai/channels) 及各渠道的文档（例如 [Feishu](https://docs.openclaw.ai/channels/feishu)、[message CLI](https://docs.openclaw.ai/cli/message)、[Agent Send](https://docs.openclaw.ai/tools/agent-send)、[Webhooks](https://docs.openclaw.ai/automation/webhook)。

**实现规则**：如果配置中提供了 `forward` 功能，请使用该功能；如果未提供或配置为 `enabled: false`，则忽略该功能。解析 `sender` 和 `content` 参数。在添加消息后执行转发操作；如果转发失败，将错误信息记录到 `sse_channel.log` 中；避免导致 SSE 过程崩溃。

---

## 本技能不涉及的内容

- 复杂的生产级用户界面架构。
- 高级的重试/队列/分布式锁策略。
- 大规模的数据库迁移设计。

这些功能可以在用户明确要求时再添加。