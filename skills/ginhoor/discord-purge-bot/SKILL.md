---
name: discord-purge-bot
description: "使用官方的 Discord 机器人令牌和 Discord HTTP API 来操作消息清理工作流程。适用于以下场景：根据请求清除公会频道的历史记录、按用户、关键词或时间范围删除消息、进行预测试（dry-run）、执行受保护的批量删除操作，或快速重建频道以清除所有内容。请勿将其用于清理自身机器人的消息或个人私信记录。"
---
# Discord 清理工具

该工具可在 Discord 公会频道中执行受控的清理操作，同时具备安全防护机制和便于审计的输出功能。

## 安全规范

- 仅使用指定的机器人令牌（`DISCORD_BOT_TOKEN` 或 `--token`）。
- 禁止接收用户账户令牌或执行自我操作（即禁止机器人自我删除频道）。
- 在执行任何删除操作之前，必须先运行 `purge-preview.mjs` 脚本以预览清理结果。
- 删除操作前需要用户明确确认。
- 如果目标频道不是公会频道，则立即终止操作。
- 每次执行清理操作后都会生成日志及 JSON 格式的总结报告。

## 工作流程

1. 收集清理范围：`channel-id`（必填），可选参数 `author-id`、`contains`、`regex`、`after`、`before`。
2. 在执行删除操作前，请阅读 `references/discord-limits.md` 文件以了解使用限制。
3. 运行 `purge-preview.mjs` 脚本预览清理效果，并获取用户的确认代码。
4. 使用确认代码执行删除操作。
5. 分享清理结果：显示已扫描的消息数量、匹配到的消息数量、被删除的消息数量、操作失败的情况，以及旧消息与最新消息的分割情况。

## 命令

### 预览清理结果

```bash
node scripts/purge-preview.mjs \
  --channel-id 123456789012345678 \
  --author-id 987654321098765432 \
  --contains "error" \
  --after "2026-03-01T00:00:00Z" \
  --max-scan 5000 \
  --out ./tmp/purge-preview.json
```

### 执行清理操作

```bash
node scripts/purge-runner.mjs \
  --channel-id 123456789012345678 \
  --author-id 987654321098765432 \
  --contains "error" \
  --after "2026-03-01T00:00:00Z" \
  --confirm "PURGE-XXXXXXXX" \
  --state-file ./tmp/purge-state.json \
  --out ./tmp/purge-result.json
```

### 进行模拟测试（Dry Run）

```bash
node scripts/purge-runner.mjs --channel-id 123456789012345678 --confirm "PURGE-XXXXXXXX" --dry-run
```

### 复制或彻底删除频道

```bash
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --out ./tmp/nuke.json
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --delete-old --out ./tmp/nuke.json
```

## 脚本角色

- `scripts/purge-preview.mjs`：扫描频道消息，应用过滤规则，返回统计结果及用户确认代码。
- `scripts/purge-runner.mjs`：执行删除操作，支持分批删除（`bulk-delete`）或单条消息删除的备用方案。
- `scripts/purge-nuke.mjs`：创建替换频道；可选择性地删除原始频道。
- `scripts/scan-filter.mjs`：可重用的消息扫描与过滤逻辑。
- `scripts/discord-api.mjs`：封装了 Discord API 的调用逻辑，并实现了速率限制和重试机制。
- `scripts/job-code.mjs`：提供用于生成确认代码的辅助函数。

## 操作员注意事项

- 对于包含大量消息的频道，请设置合理的 `max-scan` 限制。
- 对于耗时较长的清理任务，请使用 `--state-file` 参数保存操作状态。
- 尽量使用内容、用户或时间作为过滤条件，而非直接删除整个频道。
- 仅在无需保留频道历史记录时才使用彻底删除（`purge-nuke`）模式。
- 除非设置了 `--include-pinned` 参数，否则系统会自动保护已固定的消息。

## 常见问题解决方法

- 401/403 错误：请检查机器人令牌和频道权限。
- 预览结果为空但实际存在历史记录：请确保已启用 `READ_MESSAGE_HISTORY` 功能。
- 遭到 429 错误（请求过多）：降低并发请求量并保持重试机制的启用状态。
- `bulk-delete` 操作失败：可能是由于消息超过 14 天的保留期限，此时系统会切换为单条消息删除模式。
- 如果无法通过代理访问 Discord，请设置 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量（建议使用大写），并通过 `NODE_USE_ENV_PROXY=1` 参数运行脚本；或使用支持 `setGlobalProxyFromEnv()` 方法的 Node.js 版本。
- 如果代理工具同时提供 HTTP 和 SOCKS 端口，请将 `HTTP_PROXY`/`HTTPS_PROXY` 设置为 HTTP 端口；仅设置 `ALL_PROXY=socks5://...` 是不够的。

### 代理配置示例

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export NODE_USE_ENV_PROXY=1

node scripts/purge-preview.mjs --channel-id 123456789012345678 --max-scan 200
```