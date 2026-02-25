---
name: sergei-mikhailov-tg-channel-reader
description: 通过 MTProto（Pyrogram 或 Telethon）读取并汇总 Telegram 频道的帖子。可以根据时间窗口获取公共频道或私人频道中的最新消息。
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["tg-reader"], "env": ["TG_API_ID", "TG_API_HASH"]}, "primaryEnv": "TG_API_HASH"}}
---
# tg-channel-reader

该技能允许您的代理通过 MTProto（Pyrogram 或 Telethon）从 Telegram 频道中读取帖子。它支持用户订阅的任何公共频道和私人频道。

> ⚠️ **安全提示：** 该技能需要从 [myTelegram.org](https://myTelegram.org) 获取的 `TG_API_ID` 和 `TG_API_HASH` 凭据。生成的会话文件会授予对 Telegram 账户的完全访问权限——请妥善保管这些凭证，切勿共享。

## 库选择

该技能支持两种 MTProto 实现方式：
- **Pyrogram**（默认）——现代且维护良好
- **Telethon**——作为备用方案，当 Pyrogram 出现问题时可以使用

用户可以通过以下方式选择所需的库：
1. **环境变量**（永久生效）：
   ```bash
   export TG_USE_TELETHON=true
   ```
2. **命令参数**（仅限一次使用）：
   ```bash
   tg-reader fetch @channel --since 24h --telethon
   ```

此外，还提供了以下直接命令：
- `tg-reader-pyrogram` — 强制使用 Pyrogram
- `tg-reader-telethon` — 强制使用 Telethon

## 设置与安装

完整的设置说明请参阅 [README.md](./README.md)。简要步骤如下：
1. 从 https://myTelegram.org 获取 Telegram API 凭据（API 开发工具）
2. 将 `TG_API_ID` 和 `TG_API_HASH` 设置为环境变量
3. 安装该技能及其 Python 依赖项：
   ```bash
   npx clawhub@latest install sergei-mikhailov-tg-channel-reader
   cd ~/.openclaw/workspace/skills/sergei-mikhailov-tg-channel-reader
   pip install pyrogram tgcrypto telethon && pip install -e .
   ```
   在使用托管 Python 的 Linux 系统（Ubuntu/Debian）上，建议使用 `venv`：
   ```bash
   python3 -m venv ~/.venv/tg-reader
   ~/.venv/tg-reader/bin/pip install pyrogram tgcrypto telethon && ~/.venv/tg-reader/bin/pip install -e .
   echo 'export PATH="$HOME/.venv/tg-reader/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
   ```
4. 进行一次身份验证：`tg-reader auth`
5. 设置会话文件的权限：`chmod 600 ~/.tg-reader-session.session`

> 如果用户需要设置帮助，请引导他们查看 README.md 以获取完整的信息（包括环境变量、direnv 等设置方法）。

## 使用场景

当用户需要执行以下操作时，可以使用该技能：
- 查看、阅读或监控 Telegram 频道的帖子
- 获取频道的最新帖子摘要或汇总
- 了解某个频道的最新动态（例如：“@channel 的最新内容”或“@channel 过去 24 小时的总结”）
- 跟踪多个频道并比较其内容
- 了解频道的详细信息（使用 `info` 命令获取频道标题、描述和订阅者数量）

## 运行前请检查凭证

**在获取数据之前，请务必检查凭证。** 执行以下命令：
```bash
tg-reader fetch @durov --since 1h --limit 1
```

如果出现 `{"error": "Missing credentials..."}` 的错误，请指导用户按照以下步骤操作：
1. 告知用户需要从 https://myTelegram.org 获取 Telegram API 密钥。
2. 指导用户完成以下步骤：
   - 访问 https://myTelegram.org 并使用手机号登录
   - 点击 “API 开发工具”
   - 填写 “应用名称”（任意名称）和 “简称”（任意简短词汇）
   - 点击 “创建应用”
   - 复制 “应用 API ID”（一个数字）和 “应用 API 哈希值”（32 个字符的字符串）
3. 告诉用户将凭证保存到 `~/.tg-reader.json` 文件中。该文件在所有环境中都能可靠地使用，包括不加载 `.bashrc`/`.zshrc` 的代理和服务器：
   ```bash
   cat > ~/.tg-reader.json << 'EOF'
   {
     "api_id": their_id,
     "api_hash": "their_hash"
   }
   EOF
   chmod 600 ~/.tg-reader.json
   ```
   或者，也可以通过环境变量设置凭证（仅限在 shell 中交互式运行时使用）：
   ```bash
   # macOS (zsh)
   echo 'export TG_API_ID=their_id' >> ~/.zshrc
   echo 'export TG_API_HASH=their_hash' >> ~/.zshrc
   source ~/.zshrc

   # Linux (bash)
   echo 'export TG_API_ID=their_id' >> ~/.bashrc
   echo 'export TG_API_HASH=their_hash' >> ~/.bashrc
   source ~/.bashrc
   ```
   > **注意：** 代理和服务器通常不加载 `.bashrc`/`.zshrc` 文件。如果设置环境变量后仍找不到凭证，请使用 `~/.tg-reader.json`。
4. 执行身份验证：`tg-reader auth`
5. Pyrogram 会要求用户确认手机号码——回答 “y”
6. 用户会在 Telegram 应用中收到验证码（来自 “Telegram” 服务的消息）
7. 如果未收到验证码，请检查所有打开 Telegram 的设备。
8. 为会话文件设置安全权限：`chmod 600 ~/.tg-reader-session.session`
9. 身份验证成功后，可以重新尝试原始请求。

## 使用方法

```bash
# Get channel title, description and subscriber count
tg-reader info @channel_name

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

# Explicit config and session paths (for isolated agents / cron jobs)
tg-reader fetch @channel_name --since 6h \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session
```

如果找不到 `tg-reader` 命令，请使用以下命令：
```bash
python3 -m tg_reader_unified fetch @channel_name --since 24h
```

## 隔离代理与 Cron 作业

当该技能在隔离的子代理中运行时（例如，在 OpenClaw 的 cron 作业中设置 `sessionTarget: "isolated"`），它可能无法访问用户的 home 目录。此时可以使用 `--config-file` 和 `--session-file` 参数传递明确的路径：
```bash
tg-reader fetch @channel --since 6h \
  --config-file /home/user/.tg-reader.json \
  --session-file /home/user/.tg-reader-session
```

这两个参数适用于所有子命令（`fetch`、`info`、`auth`）以及 Pyrogram 和 Telethon 两种后端。

## 输出格式

### info
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

### fetch
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

1. 解析 JSON 格式的输出
2. 如果需要文本摘要，过滤掉空内容或仅包含媒体文件的帖子
3. 概述主要主题、浏览量最高的帖子以及重要的链接
4. 如果用户希望记录数据变化，可将摘要保存到 `memory/YYYY-MM-DD.md` 文件中

## 存储频道列表

用户跟踪的频道信息会保存在 `TOOLS.md` 文件中：
```markdown
## Telegram Channels
- @channel1 — why tracked
- @channel2 — why tracked
```

## 错误处理

- **凭证缺失** → 指导用户完成设置（参见上述步骤）
- **FloodWait** → 告知用户等待 N 秒后重试
- **ChannelInvalid** → 频道不存在或用户未订阅（针对私人频道）
- **tg-reader: command not found** → 请改用 `python3 -m tg_reader_unified`
- **AUTH_KEY_UNREGISTERED** → 会话过期或无效；删除会话文件并重新进行身份验证：
  ```bash
  rm -f ~/.tg-reader-session.session
  tg-reader auth
  ```
- 验证码未收到或连接出现问题 → 使用详细的调试脚本：
  ```bash
  python3 debug_auth.py
  ```
  该脚本会显示完整的 MTProto 级日志，以便您能够准确判断连接失败的原因。

## 安全注意事项

- 会话文件（`~/.tg-reader-session.session`）会授予对账户的完全访问权限——请确保其安全
- 严禁共享或提交 `TG_API_HASH` 或会话文件
- `TG_API_HASH` 应被视为机密信息——请将其存储在环境变量中，而非通过 git 追踪的文件中