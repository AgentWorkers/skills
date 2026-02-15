---
name: clawdbot-release-check
description: 监控 `clawdbot` 的新版本发布，并在每个新版本发布时发送通知。
homepage: https://github.com/clawdbot/clawdbot
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["curl","jq"]}}}
---

# Clawdbot 版本检查工具

该工具会定期从 GitHub 检查 Clawdbot 的新版本，并在每次有新版本发布时通知您。不会频繁打扰您。

## 安装

```bash
clawdhub install clawdbot-release-check
```

## 快速设置（使用 cron 任务）

```bash
# Add daily update check at 9am, notify via Telegram
{baseDir}/scripts/setup.sh --telegram YOUR_TELEGRAM_ID

# Custom hour (e.g., 8am)
{baseDir}/scripts/setup.sh --hour 8 --telegram YOUR_TELEGRAM_ID

# Remove cron job
{baseDir}/scripts/setup.sh --uninstall
```

设置完成后，请重启网关：
```bash
launchctl kickstart -k gui/$(id -u)/com.clawdis.gateway
```

## 手动使用方法

```bash
# Check for updates (silent if up-to-date or already notified)
{baseDir}/scripts/check.sh

# Show version info
{baseDir}/scripts/check.sh --status

# Force notification (bypass "already notified" state)
{baseDir}/scripts/check.sh --force

# Show highlights from ALL missed releases
{baseDir}/scripts/check.sh --all-highlights

# Clear state (will notify again on next check)
{baseDir}/scripts/check.sh --reset

# Help
{baseDir}/scripts/check.sh --help
```

## 工作原理

1. 从 `github.com/clawdbot/clawdbot/releases` 获取最新版本信息。
2. 与您已安装的版本（存储在 `package.json` 中）进行比较。
3. 如果发现版本更新，会显示版本更新说明中的重点内容。
4. 保存检查状态信息，以避免重复通知。

## 示例输出

```
🔄 **Clawdbot Update Available!**

Current: `2.0.0-beta5`
Latest:  `2026.1.5-3`

_(3 versions behind)_

**Highlights:**
- Models: add image-specific model config
- Agent tools: new `image` tool
- Config: default model shorthands

🔗 https://github.com/clawdbot/clawdbot/releases/tag/v2026.1.5-3

To update: `cd /path/to/clawdis && git pull && pnpm install && pnpm build`
```

## 相关文件

**状态文件** — `~/.clawdbot/clawdbot-release-check-state.json`：
```json
{
  "lastNotifiedVersion": "v2026.1.5-3",
  "lastCheckMs": 1704567890123
}
```

**缓存文件** — `~/.clawdbot/clawdbot-release-check-cache.json`：
- 版本信息缓存有效期为 24 小时（可减少 API 调用次数）。
- 每次版本更新后，仅提取重点内容进行缓存（节省存储空间）。
- 可使用 `--clear-cache` 命令强制刷新缓存。

## 配置参数

环境变量：
- `CLAWDBOT_DIR` — Clawdbot 源代码的路径（系统会自动从 `~/dev/clawdis`、`~/clawdbot` 或 npm 全局目录中检测该路径）。
- `CACHE_MAX_AGE_HOURS` — 缓存的有效时间（以小时为单位，默认值为 24 小时）。