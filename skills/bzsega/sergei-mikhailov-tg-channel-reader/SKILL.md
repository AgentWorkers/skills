---
name: sergei-mikhailov-tg-channel-reader
description: 通过 MTProto（Pyrogram 或 Telethon）读取并总结 Telegram 频道的帖子。可以根据时间窗口获取公共频道或私人频道中的最新消息。
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["tg-reader", "tg-reader-check"], "env": ["TG_API_ID", "TG_API_HASH"]}, "primaryEnv": "TG_API_HASH"}}
---
# tg-channel-reader

该工具使用 MTProto（通过 Pyrogram 或 Telethon）从 Telegram 频道读取帖子，支持用户订阅的任何公共频道和私人频道。

> **安全提示：** 该工具需要从 [myTelegram.org](https://myTelegram.org) 获取的 `TG_API_ID` 和 `TG_API_HASH`。会话文件会授予对 Telegram 账户的完整访问权限——请妥善保管这些信息，切勿共享。

---

## 使用场景

- 用户需要“查看”、“阅读”或“监控”某个 Telegram 频道的内容
- 用户希望获取最近帖子的摘要或总结
- 用户询问“@channel 有什么新内容”或“总结 @channel 过去 24 小时的动态”
- 用户希望跟踪或比较多个频道
- 用户需要获取频道信息（如标题、描述和订阅者数量）——可使用 `tg-reader info` 命令

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

---

## 命令

### `tg-reader-check` — 预检

**在获取数据前务必运行此命令。** 这是一个快速的离线检查，无需连接 Telegram。

```bash
tg-reader-check
tg-reader-check --config-file /path/to/config.json
tg-reader-check --session-file /path/to/session
```

返回一个 JSON 对象，其中包含 `"status": "ok"` 或 `"status": "error"` 以及一个 `problems` 数组。
该命令会验证：
- 是否有有效的凭据（环境变量或 `~/.tg-reader.json` 文件）
- 磁盘上是否存在会话文件（包括文件大小和修改时间）
- 是否安装了至少一个 MTProto 后端（Pyrogram 或 Telethon）
- 检查会话文件是否过期（配置文件指向的文件版本较旧，而实际存在更新的版本）

### `tg-reader info` — 获取频道信息

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

# Use Telethon instead of Pyrogram (one-time)
tg-reader fetch @channel_name --since 24h --telethon
```

### `tg-reader auth` — 首次认证

```bash
tg-reader auth
```

创建会话文件。此操作只需执行一次。

---

## 设置与安装

详细安装说明请参阅 [README.md](./README.md)。

### 第一步 — 获取 API 凭据

1. 访问 https://myTelegram.org 并使用手机号登录
2. 点击 “API 开发工具”
3. 填写 “应用名称”（任意名称）和 “简称”（任意简短词汇）
4. 点击 “创建应用”
5. 复制 “应用 API ID”（一个数字）和 “应用 API 哈希值”（一个 32 位的字符串）

### 第二步 — 保存凭据

**推荐方式：** 将凭据保存在 `~/.tg-reader.json` 文件中——该文件在所有环境中都有效，包括不加载 `.bashrc`/`.zshrc` 的代理程序和服务器：

```bash
cat > ~/.tg-reader.json << 'EOF'
{
  "api_id": YOUR_ID,
  "api_hash": "YOUR_HASH"
}
EOF
chmod 600 ~/.tg-reader.json
```

**备用方式：** 通过环境变量设置凭据（仅适用于交互式运行环境）：

```bash
# macOS
echo 'export TG_API_ID=YOUR_ID' >> ~/.zshrc
echo 'export TG_API_HASH=YOUR_HASH' >> ~/.zshrc
source ~/.zshrc

# Linux
echo 'export TG_API_ID=YOUR_ID' >> ~/.bashrc
echo 'export TG_API_HASH=YOUR_HASH' >> ~/.bashrc
source ~/.bashrc
```

> **注意：** 代理程序和服务器通常不会加载 shell 配置文件。如果设置环境变量后仍无法获取凭据，请使用 `~/.tg-reader.json` 文件。

### 第三步 — 安装

#### 在使用管理 Python 的 Linux 系统（Ubuntu/Debian）上安装

```bash
python3 -m venv ~/.venv/tg-reader
~/.venv/tg-reader/bin/pip install pyrogram tgcrypto telethon && ~/.venv/tg-reader/bin/pip install .
echo 'export PATH="$HOME/.venv/tg-reader/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

---

### 第四步 — 进行认证

#### 使用 Pyrogram 时

Pyrogram 会要求用户确认手机号码——输入 “y”
用户会在 Telegram 应用中收到验证码。
如果未收到验证码，请检查所有打开 Telegram 的设备。

#### 使用 Telethon 时

---

## 库选择

支持两种 MTProto 后端：

| 后端 | 命令 | 备注 |
|---------|---------|-------|
| **Pyrogram**（默认） | `tg-reader` 或 `tg-reader-pyrogram` | 最新的、维护良好的版本 |
| **Telethon** | `tg-reader-telethon` | 当 Pyrogram 出现问题时的替代方案 |

**建议：** 持续使用 Telethon。

---

## 定时任务与 Cron

该工具需要网络连接（与 Telegram 服务器的 MTProto 连接）和会话文件。配置 OpenClaw 的 Cron 任务的方式取决于会话文件的位置。

> **重要提示：** 在设置定时任务时，务必告知用户所使用的方法及其含义，以便他们做出明智的选择。

### 选项 A — `sessionTarget: "main"`（推荐）

Cron 任务会向主代理会话发送提醒，代理会在已配置好技能、凭据和会话文件的主环境中运行 `tg-reader`。

**优点：** 无需额外配置，一切均可自动运行。
**缺点：** 不完全自主——任务会触发系统事件，由代理来处理和执行。需要设置 `payload.kind: "systemEvent"`（OpenClaw Cron API 的限制）。

**设置方法：**
1. 创建一个 `sessionTarget: "main"` 且 `payload.kind: "systemEvent"` 的 Cron 任务。
2. 在任务描述中指定要运行的 `tg-reader` 命令。
3. 代理接收到提醒后会在主会话中执行该命令。

### 选项 B — `sessionTarget: "isolated"`（完全自主，设置较为复杂）

Cron 任务在 Docker 容器中运行——完全自主，无需代理参与。但容器启动时为空（没有技能、凭据或会话文件）。

**优点：** 完全自主，按计划自动执行，无需代理介入。
**缺点：** 需要 Docker 配置；会话文件必须挂载到容器中（可能不稳定——不同环境可能导致会话失效）。

**在 `~/.openclaw/openclaw.json` 中需要的配置：**

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "clawhub install sergei-mikhailov-tg-channel-reader && cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader && pip install pyrogram tgcrypto telethon && pip install .",
          "env": {
            "TG_API_ID": "YOUR_ID",
            "TG_API_HASH": "YOUR_HASH"
          }
        }
      }
    }
  }
}
```

**⚠️ 会话文件注意事项：** Telegram 会话文件（`~/.tg-reader-session.session`）也必须在容器中可用。可能需要使用 Docker 卷挂载，且可能存在不稳定问题——不同环境可能导致会话失效。如果在隔离模式下遇到 `AUTH_KEY_UNREGISTERED` 错误，请切换到选项 A。**

### 显式路径（两种选项均适用）

当 `~/` 路径不可用或指向其他位置时，可以使用显式路径：

```bash
tg-reader-check \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session

tg-reader fetch @channel --since 6h \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session
```

这两个选项都适用于所有子命令和后端。

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

### `fetch` 带 `--comments` 选项

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

**说明：**
- `comments_available: false` 表示频道没有关联的讨论组（无法查看评论）
- `comments_error` 表示某条帖子的评论数量达到了限制
- `from_user` 可能为 `null`，表示评论来自匿名用户
- 评论中的图片/视频不会被解析——仅捕获文本
- 当使用 `--comments` 选项时，帖子的默认数量限制为 30 条（可通过 `--limit` 参数调整）

---

## 数据获取后的处理

1. 解析 JSON 输出
2. 包含图片/视频的帖子会有 `has_media: true` 和 `media_type` 字段。图片/视频的文本信息存储在 `text` 字段中（来自图片说明）。**不要因为帖子包含媒体内容就忽略它们**——这些内容通常也很重要。
3. 图片和视频不会被解析（不使用 OCR/视觉识别技术）——仅返回文本/图片说明。
4. 概括主要主题、浏览量最高的帖子以及重要的链接。
5. 如果 `commentsenabled: true`，则同时分析评论情感和主要帖子的主题。
6. 如果用户希望长期跟踪数据，可将摘要保存到 `memory/YYYY-MM-DD.md` 文件中。

### 保存频道列表

将跟踪的频道信息保存在 `TOOLS.md` 文件中：

```markdown
## Telegram Channels
- @channel1 — why tracked
- @channel2 — why tracked
```

---

## 错误处理

错误信息包含 `error_type` 和 `action` 字段，帮助代理程序自动决定如何处理。

### 常见错误及其处理方式

| `error_type` | 含义 | 处理方式 |
|--------------|---------|----------|
| `access_denied` | 频道为私密频道、您被踢出或访问受限 | `remove_from_list_or_rejoin` — 询问用户是否仍有权访问；如果没有权限，则从列表中移除该频道 |
| `banned` | 您被禁止访问该频道 | `remove_from_list` — 从列表中移除该频道，并通知用户 |
| `not_found` | 频道不存在或用户名错误 | `check_username` — 核实用户名是否正确 |
| `invite_expired` | 邀请链接过期或无效 | `request_new_invite` — 请求用户提供新的邀请链接 |
| `flood_wait` | 违反了 Telegram 的评论发送频率限制 | `wait_Ns` — 自动重试，等待时间不超过 60 秒；超过此时间则返回此错误 |
| `comments_multi_channel` | 在多个频道上同时使用 `--comments` 选项 | `remove_extra_channels_or_drop_comments` — 每次只处理一个频道 |

### 系统错误

| 错误类型 | 处理方式 |
|-------|--------|
| `Session file not found` | 运行 `tg-reader-check` 命令——根据输出中的提示进行处理 |
| `Missing credentials` | 指导用户完成设置（步骤 1-2） |
| `tg-reader: command not found` | 使用 `python3 -m tg_reader_unified` 替代该命令 |
| `AUTH_KEY_UNREGISTERED` | 会话过期——删除现有会话并重新认证（见下文） |

### 会话过期

```bash
rm -f ~/.tg-reader-session.session
tg-reader auth
```

### 未收到认证码

使用 `debug_auth.py` 脚本获取详细的 MTProto 级日志：

```bash
python3 debug_auth.py
```

> **警告：** `debug_auth.py` 会在重新认证前删除现有的会话文件。执行此命令前会先请求用户确认。

---

## 安全性

- 会话文件（`~/.tg-reader-session.session`）会授予对 Telegram 账户的完整访问权限——请妥善保管。
- 严禁共享或提交 `TG_API_HASH` 和会话文件。
- `TG_API_HASH` 是敏感信息——请将其存储在环境变量或配置文件中，切勿放入 Git 仓库。