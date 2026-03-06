---
name: sergei-mikhailov-tg-channel-reader
description: 通过 MTProto（Pyrogram 或 Telethon）读取 Telegram 频道的帖子和评论。可以根据时间窗口获取公共或私人频道中的最新消息及讨论回复。
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["tg-reader", "tg-reader-check"], "env": ["TG_API_ID", "TG_API_HASH"]}, "primaryEnv": "TG_API_HASH"}}
---
# tg-channel-reader

该技能使用MTProto（Pyrogram或Telethon）从Telegram频道中读取帖子和评论。它可以处理任何公开频道以及用户已订阅的私人频道，并支持获取单个帖子的评论。

> **安全提示：** 使用此技能需要从[myTelegram.org](https://myTelegram.org)获取`TG_API_ID`和`TG_API_HASH`。会话文件会授予对Telegram账户的完全访问权限——请妥善保管，切勿共享。

---

## 执行权限审批

> **是通过`clawhub install`安装的吗？** 首先完成设置和安装（见下文）——在执行权限审批之前，该技能需要`pip install`、凭证以及会话文件。

OpenClaw默认会阻止未知的CLI命令。用户必须先批准`tg-reader`命令才能执行它们。如果命令卡住或用户没有收到任何反馈，很可能是因为权限审批尚未完成。

### 快速设置（推荐）

从技能目录运行该命令——它会检查先决条件，如有需要会安装pip包，并打印出需要执行的审批命令：

```bash
cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader
bash setup-tg-reader.sh
```

### 手动CLI审批

```bash
openclaw approvals allowlist add --gateway "$(which tg-reader)"
openclaw approvals allowlist add --gateway "$(which tg-reader-check)"
openclaw approvals allowlist add --gateway "$(which tg-reader-telethon)"
```

### 或者：首次使用时进行审批

1. **控制界面**——打开`http://localhost:18789/`，找到`tg-reader`的待审批请求，点击“始终允许”。[文档](https://docs.openclaw.ai/web/control-ui)
2. **消息机器人**（Telegram、Slack、Discord）——机器人会发送一个包含`<id>`的审批请求。回复：`/approve <id> allow-always`。其他选项：`allow-once`、`deny`。

审批提示会显示在**控制界面或机器人消息中**——不会出现在代理的对话中。这是常见的混淆来源。

---

## 适用场景

- 用户请求“查看”、“阅读”或“监控”Telegram频道
- 需要最近帖子的摘要或总结
- 询问“@channel有什么新内容”或“总结@channel过去24小时的内容”
- 需要跟踪或比较多个频道
- 需要频道信息（标题、描述、订阅者数量）——使用`tg-reader info`

---

## 快速入门

```bash
# 1. Run pre-flight diagnostic (fast, no Telegram connection)
tg-reader-check

# 2. Get channel info
tg-reader info @channel_name

# 3. Fetch recent posts
tg-reader fetch @channel_name --since 24h
```

> **`tg-reader: 命令未找到`？** 从技能目录运行`bash setup-tg-reader.sh`（它会安装相关包），或者手动运行：`cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader && pip install .`

---

## 命令

### `tg-reader-check` — 预检

**在获取数据之前务必运行。** 快速的离线检查——无需连接Telegram。

```bash
tg-reader-check
tg-reader-check --config-file /path/to/config.json
tg-reader-check --session-file /path/to/session
```

返回JSON，其中包含`"status": "ok"`或`"status": "error"`以及一个`problems`数组。

检查以下内容：
- 凭证是否可用（环境变量或`~/.tg-reader.json`）
- 磁盘上是否存在会话文件（包括文件大小和修改日期）
- 是否至少安装了一个MTProto后端（Pyrogram或Telethon）
- 检测到过时的会话（配置指向旧文件，而实际上存在更新后的文件）

### `tg-reader info` — 频道信息

```bash
tg-reader info @channel_name
```

返回频道的标题、描述、订阅者数量和链接。

### `tg-reader fetch` — 读取帖子

```bash
# Last 24 hours (default)
tg-reader fetch @channel_name --since 24h

# Last 7 days, up to 200 posts
tg-reader fetch @channel_name --since 7d --limit 200

# Multiple channels (fetched sequentially with 10s delay between each)
tg-reader fetch @channel1 @channel2 @channel3 --since 24h

# Custom delay between channels (seconds)
tg-reader fetch @channel1 @channel2 @channel3 --since 24h --delay 5

# Fetch posts with comments (single channel only, limit auto-drops to 30)
tg-reader fetch @channel_name --since 7d --comments

# More comments per post, custom delay between posts
tg-reader fetch @channel_name --since 24h --comments --comment-limit 20 --comment-delay 5

# Skip posts without text (media-only, no caption)
tg-reader fetch @channel_name --since 24h --text-only

# Human-readable output
tg-reader fetch @channel_name --since 24h --format text

# Write output to file instead of stdout (saves tokens)
tg-reader fetch @channel_name --since 24h --output
tg-reader fetch @channel_name --since 24h --comments --output comments.json

# Use Telethon instead of Pyrogram (one-time)
tg-reader fetch @channel_name --since 24h --telethon

# Read unread mode — only fetch new (unread) posts, no --since needed
# Requires "read_unread": true in ~/.tg-reader.json
tg-reader fetch @channel_name

# Override read_unread mode (fetch everything, don't update state)
tg-reader fetch @channel_name --since 7d --all

# Custom state file location
tg-reader fetch @channel_name --since 24h --state-file /path/to/state.json
```

### `tg-reader auth` — 首次认证

```bash
tg-reader auth
```

创建一个会话文件。只需执行一次。

---

## 未读帖子模式

仅返回新的（未读的）帖子——该技能会记住您已经看过的帖子。适用于每日摘要和监控工作流程。

### 设置

**选项A — 配置文件**（`~/.tg-reader.json`）：

```json
{
  "api_id": 12345,
  "api_hash": "...",
  "read_unread": true
}
```

**选项B — 环境变量**（与`~/.openclaw/openclaw.json`配合使用）：

```bash
export TG_READ_UNREAD=true
```

环境变量的优先级高于配置文件。这样您可以通过`openclaw.json`的Docker `env`以及`TG_API_ID`/`TG_API_HASH`来启用`read_unread`功能。

状态信息存储在`~/.tg-reader-state.json`中（可以通过配置文件中的`"state_file"`、`TG_STATE_FILE`环境变量或`--state-file`标志进行配置）。

### 行为

- 当启用`read_unread`模式时，不需要`--since`参数——该技能会自动返回所有未读帖子
- **首次运行**（频道没有之前的状态）：`--since`参数按默认值（24小时）生效；会创建状态文件
- **后续运行**：仅返回比上次阅读更新的帖子；`--since`参数会被忽略
- **`--all`标志**：绕过未读帖子模式——根据`--since`参数获取所有帖子，同时不更新状态
- **新频道**：行为类似于首次运行（没有之前的状态）
- **没有新帖子**：状态不变，返回`count: 0`

### 示例

```bash
# With read_unread enabled — just fetch, no --since needed
tg-reader fetch @channel_name

# First run for a new channel — --since determines initial window
tg-reader fetch @new_channel --since 7d

# Override: fetch everything, don't update tracking state
tg-reader fetch @channel_name --since 7d --all
```

### 输出

当启用未读帖子模式时，JSON输出会包含`read_unread`字段：

```json
{
  "channel": "@channel_name",
  "read_unread": {"enabled": true},
  "count": 5,
  "messages": [...]
}
```

使用`--all`参数时：`"read_unread": {"enabled": true, "overridden": true}`

### 限制

- 跟踪仅针对帖子级别——已读帖子上的新评论不会被捕获
- 如果频道更改了用户名，跟踪信息会重置（状态是根据用户名来区分的）
- 对同一频道的多次并发请求是安全的，但最后一次操作的请求会优先处理

### 诊断

`tg-reader-check`用于报告跟踪状态：

```json
{
  "tracking": {
    "read_unread": true,
    "state_file": "~/.tg-reader-state.json",
    "state_file_exists": true,
    "tracked_channels": 3
  }
}
```

---

## 输出格式

### `info`

```json
{
  "id": -1001234567890,
  "title": "Channel Name",
  "username": "channel_name",
  "description": "About this channel...",
  "members_count": 42000,
  "link": "https://t.me/channel_name"
}
```

### `fetch`

```json
{
  "channel": "@channel_name",
  "fetched_at": "2026-02-22T10:00:00Z",
  "since": "2026-02-21T10:00:00Z",
  "count": 12,
  "messages": [
    {
      "id": 1234,
      "date": "2026-02-22T09:30:00Z",
      "text": "Post content...",
      "views": 5200,
      "forwards": 34,
      "link": "https://t.me/channel_name/1234",
      "has_media": true,
      "media_type": "MessageMediaType.PHOTO"
    }
  ]
}
```

### 带`--comments`参数的`fetch`

```json
{
  "channel": "@channel_name",
  "fetched_at": "2026-02-28T10:00:00Z",
  "since": "2026-02-27T10:00:00Z",
  "count": 5,
  "comments_enabled": true,
  "comments_available": true,
  "messages": [
    {
      "id": 1234,
      "text": "Post content...",
      "has_media": false,
      "comment_count": 2,
      "comments": [
        {
          "id": 5678,
          "date": "2026-02-28T09:35:00Z",
          "text": "Great post!",
          "from_user": "username123"
        }
      ]
    }
  ]
}
```

**注意：**
- `comments_available: false`——频道没有关联的讨论组（因此无法获取评论）
- 如果消息显示`comments_error`，则表示该帖子的评论数量达到了限制
- 对于匿名评论，`from_user`可能为`null`
- 评论中的图片/视频不会被分析——只捕获文本
- 当`--comments`参数启用时，默认的帖子数量限制会降至30条（可以通过`--limit`参数进行调整）

---

## 获取数据后的处理

1. 解析JSON输出
2. 包含图片/视频的帖子会有`has_media: true`和`media_type`字段。它们的文本位于`text`字段中（来自图片的标题）。**不要因为帖子包含媒体内容就跳过它们**——这些内容通常也包含重要信息。
3. 图片和视频不会被分析（没有使用OCR/视觉识别技术）——只返回文本/标题。
4. 概括主要主题、浏览量最高的帖子、重要的链接
5. 如果`comments_enabled: true`，则会分析评论的情绪和主要主题
6. 如果用户希望长期跟踪数据，可以将摘要保存到`memory/YYYY-MM-DD.md`文件中

### 保存到文件（基于令牌的经济模型）

当数据量较大（尤其是使用`--comments`参数时）且不需要立即分析数据时，可以使用`--output`参数。所有数据会被保存到文件中，而标准输出只返回简短的确认信息——这样可以节省令牌。

**定期更新方案：** 设置一个定时任务，定期运行`tg-reader fetch @channel --comments --output comments.json`。文件会定期更新。当用户请求分析评论时，直接读取文件即可，无需再次获取数据。这样可以避免每次获取数据时消耗令牌。

当使用`--output`参数且未指定文件名时，默认文件名为`tg-output.json`。标准输出确认信息如下：
```json
{"status": "ok", "output_file": "/absolute/path/to/tg-output.json", "count": 12}
```

### 保存频道列表

将跟踪的频道信息保存在`TOOLS.md`文件中：

```markdown
## Telegram Channels
- @channel1 — why tracked
- @channel2 — why tracked
```

---

## 错误处理

错误信息包含`error_type`和`action`字段，以帮助代理自动决定如何处理。

### 频道相关错误

| `error_type` | 含义 | `action` |
|--------------|---------|----------|
| `access_denied` | 频道是私有的，您被踢出了频道，或者访问权限受到限制 | `remove_from_list_or_rejoin` — 询问用户是否仍有权访问；如果没有权限，则从列表中移除该频道 |
| `banned` | 您被禁止访问该频道 | `remove_from_list` — 从列表中移除该频道，并通知用户 |
| `not_found` | 频道不存在或用户名错误 | `check_username` — 与用户确认`@username`是否正确 |
| `invite_expired` | 邀请链接已过期或无效 | `request_new_invite` — 请求用户提供新的邀请链接 |
| `flood_wait` | 违反了Telegram的发送频率限制 | `wait_Ns` — 如果等待时间小于60秒，则自动重试；超过这个时间限制则会显示此错误 |
| `comments_multi_channel` | 在多个频道上同时使用`--comments`参数 | `remove_extra_channels_or_drop_comments` — 每次只处理一个频道 |

### 系统错误

| 错误 | 处理方式 |
|-------|--------|
| `Session file not found` | 运行`tg-reader-check`——根据输出中的建议进行处理 |
| `Missing credentials` | 指导用户完成设置（见步骤1-2） |
| `tg-reader: 命令未找到` | 从技能目录运行`bash setup-tg-reader.sh`，或者手动运行：`pip install .`。备用方案：`python3 -m tg_reader_unified` |
| `AUTH_KEY_UNREGISTERED` | 会话已过期——删除会话并重新认证（见下文） |

### 会话过期

```bash
rm -f ~/.tg-reader-session.session
tg-reader auth
```

### 认证代码未收到

使用详细的调试脚本来获取完整的MTProto级别日志：

```bash
python3 debug_auth.py
```

> **警告：** `debug_auth.py`在重新认证之前会删除现有的会话文件。它会先请求用户的确认。

---

## 库选择

支持两种MTProto后端：

| 后端 | 命令 | 备注 |
|---------|---------|-------|
| **Pyrogram**（默认） | `tg-reader`或`tg-reader-pyrogram` | 最新版本，维护活跃 |
| **Telethon** | `tg-reader-telethon` | 如果Pyrogram出现问题时的替代方案 |

**永久切换后端：** `export TG_USE_TELETHON=true`
**一次性切换后端：** `tg-reader fetch @channel --since 24h --telethon`

---

## 设置与安装

详细信息请参阅[README.md](./README.md)。

### 第1步 — 获取API凭证

访问https://myTelegram.org → **API开发工具** → 创建一个应用 → 复制`api_id`和`api_hash`。

### 第2步 — 保存凭证

**推荐方法**（适用于代理和服务器）：
```bash
cat > ~/.tg-reader.json << 'EOF'
{
  "api_id": YOUR_ID,
  "api_hash": "YOUR_HASH"
}
EOF
chmod 600 ~/.tg-reader.json
```

**替代方法**（仅适用于交互式shell）：
```bash
export TG_API_ID=YOUR_ID
export TG_API_HASH="YOUR_HASH"
```
将这些凭证设置到当前的shell会话中。避免将`TG_API_HASH`写入shell配置文件（`~/.bashrc`）——建议使用`~/.tg-reader.json`进行持久化存储。

> **注意：** 代理和服务器不会加载shell配置文件。在非交互式环境中，请使用`~/.tg-reader.json`（上述推荐方法）。

### 第3步 — 安装与配置

```bash
npx clawhub@latest install sergei-mikhailov-tg-channel-reader
cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader
bash setup-tg-reader.sh
```

设置脚本会安装Python包（`pip install .`），检查凭证和会话信息，然后运行`tg-reader-check`，并打印出需要手动执行的审批命令。

在具有管理权限的Python环境（Ubuntu/Debian）中，建议在运行设置脚本之前创建一个虚拟环境（`venv`）：

```bash
python3 -m venv ~/.venv/tg-reader
echo 'export PATH="$HOME/.venv/tg-reader/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

<details>
<summary>手动安装（无需设置脚本）</summary>

```bash
cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader
pip install pyrogram tgcrypto telethon && pip install .
openclaw approvals allowlist add --gateway "$(which tg-reader)"
openclaw approvals allowlist add --gateway "$(which tg-reader-check)"
```
</details>

### 第4步 — 认证

```bash
tg-reader auth
```

Pyrogram会要求您确认电话号码——回答“y”。验证码会通过Telegram应用发送（不会通过短信）。

### 第5步 — 验证

```bash
tg-reader-check
```

应该返回`"status": "ok"`。如果返回其他结果，请解决报告的问题，然后重新运行`bash setup-tg-reader.sh`。

---

## 定时任务与Cron

该技能需要网络访问权限（与Telegram服务器的MTProto连接）以及会话文件。您如何配置OpenClaw的Cron任务取决于会话的目标。

> **重要提示：** 在设置使用`tg-reader`的定时任务时，务必告知用户您使用的具体方法及其含义——以便他们能够做出明智的选择。

### 选项A — `sessionTarget: "main"`（推荐）

定时任务会向主代理会话发送一个提醒。代理随后会在已经准备好技能、凭证和会话文件的主环境中运行`tg-reader`。

**优点：** 无需额外配置——一切都能立即使用。
**缺点：** 不完全自主——任务会触发系统事件，由代理接收并执行。需要设置`payload.kind: "systemEvent"`（这是OpenClaw Cron API的限制）。

**设置方法：**
1. 创建一个定时任务，设置`sessionTarget: "main"`和`payload.kind: "systemEvent"`
2. 在任务描述中指定要运行的`tg-reader`命令
3. 代理接收到提醒后，在其主环境中执行该命令

### 选项B — `sessionTarget: "isolated"`（完全自主，设置复杂）

定时任务在**Docker容器**中运行——完全自主，无需代理参与。但是，容器启动时没有任何预设内容：没有技能、没有凭证、没有会话文件。

**优点：** 完全自主——按计划自动运行，无需代理干预。
**缺点：** 需要Docker环境；会话文件必须挂载到容器中（可能无法可靠地工作——因为不同环境可能会导致会话失效）。`

**在`~/.openclaw/openclaw.json`中需要配置的参数：**

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "clawhub install sergei-mikhailov-tg-channel-reader && cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader && pip install pyrogram tgcrypto telethon && pip install .",
          "env": {
            "TG_API_ID": "YOUR_ID",
            "TG_API_HASH": "YOUR_HASH",
            "TG_READ_UNREAD": "true"
          }
        }
      }
    }
  }
}
```

**关于会话文件的注意事项：** Telegram会话文件（`~/.tg-reader-session.session`）也必须存在于容器中。这可能需要使用Docker卷挂载，而且在不同环境中可能会遇到问题（例如，新的环境可能会导致会话失效）。如果在隔离模式下遇到`AUTH_KEY_UNREGISTERED`错误，请切换到选项A。

### 显式路径（两种选项都适用）

当`~/`路径不可用或指向其他位置时，可以使用显式路径：

```bash
tg-reader-check \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session

tg-reader fetch @channel --since 6h \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session
```

这两个选项都适用于所有子命令和两种后端。

---

## 安全性

- 会话文件（`~/.tg-reader-session.session`）会授予**对账户的完全访问权限**——请妥善保管
- 绝不要共享或提交`TG_API_HASH`或会话文件
- `TG_API_HASH`是敏感信息——请将其存储在环境变量或配置文件中，切勿将其放入git仓库