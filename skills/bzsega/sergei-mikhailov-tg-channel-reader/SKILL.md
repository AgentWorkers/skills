---
name: sergei-mikhailov-tg-channel-reader
description: 通过 MTProto（Pyrogram 或 Telethon）读取并总结 Telegram 频道的帖子。可以根据时间窗口获取公共频道或私人频道中的最新消息。
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["tg-reader", "tg-reader-check"], "env": ["TG_API_ID", "TG_API_HASH"]}, "primaryEnv": "TG_API_HASH"}}
---
# tg-channel-reader  
使用 MTProto（Pyrogram 或 Telethon）从 Telegram 频道读取帖子。  
支持用户订阅的任何公共频道和私人频道。  

> **安全提示：** 此功能需要从 [myTelegram.org](https://myTelegram.org) 获取的 `TG_API_ID` 和 `TG_API_HASH`。会话文件会授予对 Telegram 账户的完整访问权限——请妥善保管，切勿共享。  

---

## 执行权限  
OpenClaw 可能要求用户在运行 `tg-reader` 或 `tg-reader-check` 命令前进行 **权限批准**。如果命令卡住或用户没有收到任何反馈：  
1. 告诉用户打开 `http://localhost:18789/` 上的 **[控制界面](https://docs.openclaw.ai/web/control-ui)`——在“执行权限”面板中应能看到待处理的批准请求。点击“始终允许”将命令添加到允许列表中。  
2. 如果用户通过消息应用（Telegram、Slack、Discord）操作，OpenClaw 机器人可能会在聊天中发送批准请求。用户可以回复 `/approve <id> allow-always`（机器人会提供 `<id>`）。其他选项包括：`/approve <id> allow-once` 或 `/approve <id> deny`。  
注意：批准提示会出现在 **控制界面** 或机器人消息中，而非代理程序的对话中。这可能是造成混淆的常见原因。  

---

## 使用场景  
- 用户请求“检查”、“阅读”或“监控”某个 Telegram 频道  
- 需要最近帖子的摘要或汇总  
- 询问“@channel 有什么新内容”或“总结 @channel 过去 24 小时的动态”  
- 需要跟踪或比较多个频道  
- 需要频道信息（标题、描述、订阅者数量）——使用 `tg-reader info`  

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
返回 JSON 格式，内容包含 `"status": "ok"` 或 `"status": "error"` 以及一个 `problems` 数组。  
检查：  
- 是否有有效的凭证（环境变量或 `~/.tg-reader.json` 文件）  
- 磁盘上是否存在会话文件（包括文件大小和修改时间）  
- 是否安装了至少一个 MTProto 后端（Pyrogram 或 Telethon）  
- 是否存在过时的会话文件（配置指向旧文件，而实际上存在新文件）  

### `tg-reader info` — 频道信息  
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
```  

### `tg-reader auth` — 首次身份验证  
```bash
tg-reader auth
```  
创建会话文件。此操作只需执行一次。  

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

### `fetch` with `--comments`  
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
- `comments_available: false` 表示该频道没有关联的讨论组（因此无法显示评论）  
- `comments_error` 表示该帖子的评论已达到速率限制  
- 对于匿名评论，`from_user` 可能为 `null`  
- 评论中的图片/视频不会被分析——仅捕获文本  
- 当使用 `--comments` 时，默认帖子数量限制为 30 条（可通过 `--limit` 参数调整）  

---

## 数据获取后的处理  
1. 解析 JSON 输出  
2. 包含图片/视频的帖子会有 `has_media: true` 和 `media_type` 字段。其文本内容位于 `text` 字段中（来自图片/视频的标题）。**不要因为帖子包含媒体内容就忽略它们**——这些内容可能很重要。  
3. 评论中的图片/视频不会被分析（不使用 OCR/视觉识别技术），仅返回文本/标题  
4. 概括主要主题、浏览量最高的帖子以及重要链接  
5. 如果 `commentsenabled: true`，则分析评论情感和主要帖子的主题  
6. 如果用户希望长期跟踪数据，可将摘要保存到 `memory/YYYY-MM-DD.md` 文件中  

### 保存到文件（基于令牌机制）  
当数据量较大（尤其是使用 `--comments` 时）且无需立即分析时，可以使用 `--output` 参数。所有数据会保存到文件中，标准输出仅返回简短确认信息——这样可以节省令牌。  
**定期更新方案：** 设置定时任务 `tg-reader fetch @channel --comments --output comments.json`。文件会定期更新。当用户需要分析评论时，直接读取文件即可，避免每次请求都消耗令牌。  
如果未指定文件名，默认保存路径为 `tg-output.json`。标准输出确认信息如下：  
```json
{"status": "ok", "output_file": "/absolute/path/to/tg-output.json", "count": 12}
```  

### 保存频道列表  
将跟踪的频道信息保存到 `TOOLS.md` 文件中：  
```markdown
## Telegram Channels
- @channel1 — why tracked
- @channel2 — why tracked
```  

---

## 错误处理  
错误信息包含 `error_type` 和 `action` 字段，帮助代理程序自动决定如何处理：  

### 频道相关错误  
| `error_type` | 含义 | `action` |  
|--------------|---------|----------|  
| `access_denied` | 频道为私密频道、您被踢出或访问受限 | `remove_from_list_or_rejoin` — 询问用户是否仍有权访问；若无权限，则从列表中移除该频道 |  
| `banned` | 您被禁止访问该频道 | `remove_from_list` — 从列表中移除该频道，并通知用户 |  
| `not_found` | 频道不存在或用户名错误 | `check_username` — 核实用户提供的 `@username` 是否正确 |  
| `invite_expired` | 邀请链接过期或无效 | `request_new_invite` — 请用户重新发送邀请链接 |  
| `flood_wait` | 达到 Telegram 的速率限制 | `wait_Ns` — 自动重试，等待时间不超过 60 秒；超时则显示此错误 |  
| `comments_multi_channel` | 同时为多个频道使用 `--comments` 参数 | `remove_extra_channels_or_drop_comments` — 每次只处理一个频道 |  

### 系统错误  
| 错误类型 | 处理方式 |  
|-------|--------|  
| `Session file not found` | 运行 `tg-reader-check` 并根据输出提示操作 |  
| `Missing credentials` | 指导用户完成设置（步骤 1-2） |  
| `tg-reader: command not found` | 使用 `python3 -m tg_reader_unified` 替代该命令 |  
| `AUTH_KEY_UNREGISTERED` | 会话已过期——删除会话并重新认证（详见下文） |  

### 会话过期  
```bash
rm -f ~/.tg-reader-session.session
tg-reader auth
```  

### 认证代码未收到  
使用详细的调试脚本（`debug_auth.py`）获取完整的 MTProto 级别日志：  
```bash
python3 debug_auth.py
```  
> **警告：** `debug_auth.py` 会在重新认证前删除现有的会话文件。系统会先请求用户确认。  

---

## 库选择  
支持两种 MTProto 后端：  
| 后端 | 命令 | 备注 |  
|---------|---------|-------|  
| **Pyrogram**（默认） | `tg-reader` 或 `tg-reader-pyrogram` | 现代版本，维护活跃 |  
| **Telethon** | `tg-reader-telethon` | 如果 Pyrogram 出现问题时的替代方案 |  
**切换方式：**  
  - 持久切换：`export TG_USE_TELETHON=true`  
  - 一次性切换：`tg-reader fetch @channel --since 24h --telethon`  

---

## 设置与安装  
详细信息请参阅 [README.md](./README.md)。  

### 第 1 步 — 获取 API 凭证  
访问 https://myTelegram.org → **API 开发工具** → 创建一个应用 → 复制 `api_id` 和 `api_hash`。  

### 第 2 步 — 保存凭证  
**推荐方式**（适用于代理程序和服务器）：  
```bash
cat > ~/.tg-reader.json << 'EOF'
{
  "api_id": YOUR_ID,
  "api_hash": "YOUR_HASH"
}
EOF
chmod 600 ~/.tg-reader.json
```  
**替代方式**（仅适用于交互式环境）：将 `export TG_API_ID=...` 和 `export TG_API_HASH=...` 添加到 `~/.bashrc` 或 `~/.zshrc` 中。  
> **注意：** 代理程序和服务器通常不加载 shell 配置文件。如果设置环境变量后仍找不到凭证，请使用 `~/.tg-reader.json`。  

### 第 3 步 — 安装  
```bash
npx clawhub@latest install sergei-mikhailov-tg-channel-reader
cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader
pip install pyrogram tgcrypto telethon && pip install .
```  
在 Linux 系统（Ubuntu/Debian）上使用虚拟环境（venv）：  
```bash
python3 -m venv ~/.venv/tg-reader
~/.venv/tg-reader/bin/pip install pyrogram tgcrypto telethon && ~/.venv/tg-reader/bin/pip install .
echo 'export PATH="$HOME/.venv/tg-reader/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```  

### 第 4 步 — 进行身份验证  
Pyrogram 会要求用户确认电话号码——回答 “y”。验证码会通过 Telegram 应用发送（而非短信）。  

### 第 5 步 — 保护会话安全  
```bash
chmod 600 ~/.tg-reader-session.session
```  

---

## 定时任务与 Cron  
此功能需要网络连接（与 Telegram 服务器的 MTProto 连接）和会话文件。配置 OpenClaw 的 Cron 任务方式取决于会话文件的位置。  
> **重要提示：** 在设置定时任务时，务必告知用户所使用的方法及其含义，以便他们做出明智的选择。  

### 选项 A — `sessionTarget: "main"`（推荐）  
Cron 任务会向主代理程序的会话发送提醒。代理程序会在主环境中运行 `tg-reader`，此时技能、凭证和会话文件都已准备好。  
**优点：** 无需额外配置，一切均可自动运行。  
**缺点：** 不完全自主——任务会触发系统事件，由代理程序接收并执行。需要设置 `payload.kind: "systemEvent"`（OpenClaw Cron API 的限制）。  
**设置方法：**  
1. 创建一个定时任务，设置 `sessionTarget: "main"` 和 `payload.kind: "systemEvent"`  
2. 在任务描述中指定要执行的 `tg-reader` 命令  
3. 代理程序接收到提醒后，在主会话中执行该命令  

### 选项 B — `sessionTarget: "isolated"`（完全自主，设置复杂）  
Cron 任务在 **Docker 容器** 中运行——完全自主，无需代理程序参与。但容器启动时为空（无技能、无凭证、无会话文件）。  
**优点：** 完全自主，按计划自动执行。**缺点：** 需要 Docker 配置；会话文件必须挂载到容器中（可能不稳定——不同环境可能导致会话失效）。  
**在 `~/.openclaw/openclaw.json` 中需要配置：**  
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
**会话文件注意事项：** Telegram 会话文件（`~/.tg-reader-session.session`）也必须存在于容器中。可能需要使用 Docker 卷挂载，且在不同环境中可能会遇到问题（例如会话失效）。如果在隔离模式下遇到 `AUTH_KEY_UNREGISTERED` 错误，请切换到选项 A。  

### 显式路径（两种选项均适用）  
当 `~/` 路径不可用或指向其他位置时，可使用显式路径：  
```bash
tg-reader-check \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session

tg-reader fetch @channel --since 6h \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session
```  
这两个选项适用于所有子命令和后端。  

---

## 安全性  
- 会话文件（`~/.tg-reader-session.session`）会授予对账户的完整访问权限——请妥善保管  
- 严禁共享或提交 `TG_API_HASH` 和会话文件  
- `TG_API_HASH` 是敏感信息——请将其存储在环境变量或配置文件中，切勿放入 Git 仓库