---
name: webhook-promo-scheduler
description: 使用反垃圾邮件机制，将促销/提醒消息安排发送到 Discord Webhook URL。
---
## webhook-promo-scheduler

该工具用于定时向 Discord 的 webhook URL 发送促销/提醒信息，并通过 JSONL （JavaScript Object Notation with Logging） ledger 来控制发送频率。

### 功能概述：
- 向 Discord webhook 发送 JSON 格式的消息（包含 `content` 字段）。
- 使用 JSONL ledger 确保每个频道每天最多只能成功发送一条消息。
- 支持循环发送消息的功能，可以自动切换不同的消息内容。
- 提供 `--dry-run` 参数，允许在正式发送前验证发送频率和日志记录的正确性。

### 使用场景（最佳实践）：
- 以合适的频率发送更新内容，同时避免被视为垃圾信息或泄露 webhook 的地址：通过严格的发送频率控制及详细的日志记录来实现。

### 相关文件：
- `scripts/post_webhook.py`：用于向 Discord webhook 发送消息的辅助脚本（仅依赖标准库）。
- `scripts/ledger.py`：用于管理 JSONL ledger 的辅助脚本（仅依赖标准库）。
- `scripts/promo_scheduler.py`：命令行工具（CLI），用于执行发送任务（仅依赖标准库）。

### ledger 的配置：
- 默认路径：`~/.openclaw/webhook-promo-ledger.jsonl`
- 可通过 `--ledger-path` 参数自定义 ledger 的路径。
- JSONL 格式的记录包含以下字段：`date`（日期）、`channel`（频道名称）、`status`（发送状态）、`hash`（消息的哈希值）。

### 安全性：
- 命令行工具会**禁止**显示 webhook 的地址。
- 如果日志中出现了 webhook 的地址，会对其进行隐藏处理。
- 建议将 webhook 放置在私密频道中；如果地址被泄露，应立即更换，并在正式启用发送功能前使用 `--dry-run` 参数进行测试。

### 常见问题（关于安全性）：
**问：这个工具会暴露 Discord 的 webhook 地址，这安全吗？**
**答：** 应将其视为敏感信息。该工具不会显示 webhook 地址，支持使用秘密参数进行配置，并提供了 `--dry-run` 功能以便在正式使用前验证行为。如果希望完全避免直接暴露 webhook 地址，可以在前端使用代理服务（如 Cloudflare Worker 或 Supabase Edge Function），并将真实的 webhook 保持私密。

### 使用方法：

**一次性发送消息：**
```bash
python3 {baseDir}/scripts/promo_scheduler.py post \
  --webhook-url <URL> \
  --channel openclaw-discord \
  --message "Hello from OpenClaw!"
```

**消息轮播功能：**
```bash
python3 {baseDir}/scripts/promo_scheduler.py rotate \
  --webhook-url <URL> \
  --channel openclaw-discord \
  --messages-file messages.txt
```

**`messages.txt` 文件格式：**
- 每行包含一条消息内容。
- 以 `#` 开头的行会被忽略。