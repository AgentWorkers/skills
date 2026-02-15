# Feishu RSS 功能

允许用户订阅 RSS/Atom 源，并将更新内容以富卡片的形式推送到 Feishu 组中。

## 主要功能

- **添加订阅源：** 可以订阅任何 RSS/Atom URL。
- **查看订阅源：** 查看所有已激活的订阅源。
- **检查更新：** 检查是否有新内容（过去 24 小时内），并发送通知。
- **取消订阅：** 可以通过 ID 取消订阅。
- **导入/导出：** 支持 OPML 格式（计划中实现）。

## 使用方法

```bash
# Add a feed
node skills/feishu-rss/index.js add "https://news.ycombinator.com/rss" --name "Hacker News" --target "oc_xxx"

# List feeds
node skills/feishu-rss/index.js list

# Check for updates (run via cron)
node skills/feishu-rss/index.js check

# Remove a feed
node skills/feishu-rss/index.js remove <id>
```

## 配置方式

订阅源信息存储在 `skills/feishu-rss/feeds.json` 文件中。
处理后的更新内容会记录在 `memory/rss_history.json` 文件中，以避免重复。

## 所需依赖库

- `rss-parser`（npm 包）
- `feishu-card`（用于发送更新内容）