---
name: sergei-mikhailov-tg-channel-reader
description: 通过 MTProto（Pyrogram 或 Telethon）读取并总结 Telegram 频道的帖子。可以根据时间窗口获取公共频道或私人频道中的最新消息。
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["tg-reader"]
      python: ["pyrogram", "tgcrypto", "telethon"]
---
# tg-channel-reader

该技能允许您的代理使用 MTProto（Pyrogram 或 Telethon）从 Telegram 频道中读取帖子。支持用户订阅的任何公共频道和私人频道。

## 库选择

该技能支持两种 MTProto 实现方式：
- **Pyrogram**（默认）——现代且维护活跃
- **Telethon**——作为备用方案，当 Pyrogram 出现问题时可以使用

用户可以通过以下方式选择库：
1. **环境变量**（永久生效）：
   ```bash
   export TG_USE_TELETHON=true
   ```
2. **命令参数**（仅限一次使用）：
   ```bash
   tg-reader fetch @channel --since 24h --telethon
   ```

此外，还提供以下直接命令：
- `tg-reader-pyrogram` — 强制使用 Pyrogram
- `tg-reader-telethon` — 强制使用 Telethon

## 适用场景

当用户需要执行以下操作时，可以使用此技能：
- 查看、阅读或监控 Telegram 频道的动态
- 获取频道的最新帖子摘要
- 询问某个频道的最新动态（例如：“@channel 有什么新内容？”或“总结 @channel 过去 24 小时的内容”）
- 跟踪多个频道并比较它们的内容

## 运行前——检查凭据

**在获取数据之前，请务必检查凭据。** 执行以下命令：

```bash
tg-reader fetch @durov --since 1h --limit 1
```

如果出现 `{"error": "Missing credentials..."}` 的错误信息，请指导用户完成以下步骤：
1. 告知用户需要从 https://my.telegram.org 获取 Telegram API 密钥。
2. 指导用户按照以下步骤操作：
   - 访问 https://my.telegram.org 并使用手机号登录
   - 点击 “API 开发工具”
   - 填写 “应用名称”（任意名称）和 “应用简称”（任意简短词汇）
   - 点击 “创建应用”
   - 复制 “应用 API ID”（一个数字）和 “应用 API 哈希值”（32 个字符的字符串）
3. 要求用户设置凭据：
   ```bash
   echo 'export TG_API_ID=their_id' >> ~/.bashrc
   echo 'export TG_API_HASH=their_hash' >> ~/.bashrc
   source ~/.bashrc
   ```
4. 运行身份验证：
   ```bash
   python3 -m reader auth
   ```
   - 用户将在 Telegram 应用中收到一条验证码（来自 “Telegram” 服务的消息）
   - 如果未收到验证码，请检查所有打开 Telegram 的设备
5. 身份验证成功后，重新尝试原始请求

## 使用方法

```bash
# Fetch last 24h from one channel (default: Pyrogram)
tg-reader fetch @channel_name --since 24h --format json

# Use Telethon instead (one-time)
tg-reader fetch @channel_name --since 24h --telethon

# Fetch last 7 days, up to 200 posts
tg-reader fetch @channel_name --since 7d --limit 200

# Fetch multiple channels at once
tg-reader fetch @channel1 @channel2 @channel3 --since 24h

# Human-readable output
tg-reader fetch @channel_name --since 24h --format text

# Force specific library
tg-reader-pyrogram fetch @channel_name --since 24h
tg-reader-telethon fetch @channel_name --since 24h
```

如果找不到 `tg-reader` 命令，请使用以下命令：
```bash
python3 -m tg_reader_unified fetch @channel_name --since 24h
```

## 输出格式

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
      "link": "https://t.me/channel_name/1234"
    }
  ]
}
```

## 数据获取后

1. 解析 JSON 格式的输出内容
2. 如果用户要求提供文本摘要，过滤掉空帖子或仅包含媒体文件的帖子
3. 总结频道的主题、浏览量最高的帖子以及重要的链接
4. 如果用户希望长期跟踪频道动态，将摘要保存到 `memory/YYYY-MM-DD.md` 文件中

## 存储频道列表

将用户跟踪的频道信息保存在 `TOOLS.md` 文件中：
```markdown
## Telegram Channels
- @channel1 — why tracked
- @channel2 — why tracked
```

## 错误处理

- **凭据缺失** → 指导用户完成凭据设置（见上文）
- **FloodWait** → 告知用户等待 N 秒后重试
- **ChannelInvalid** → 频道不存在或用户未订阅该频道（针对私人频道）
- **tg-reader: command not found** → 请使用 `python3 -m reader` 代替该命令

## 安全提示

- 会话文件（`~/.tg-reader-session.session`）会授予用户完整的账户访问权限，请妥善保管
- 绝不要分享或提交 `TG_API_HASH` 或会话文件