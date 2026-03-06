---
name: discord-purge-bot
description: "使用官方的 Discord 机器人令牌和 Discord HTTP API 来操作消息清理工作流程。适用于以下场景：根据请求清除公会频道的历史记录、按用户、关键词或时间范围删除消息、运行预测试用例、执行受保护的大规模删除操作，或快速清理频道内容。请勿将其用于自我清理或个人私信历史的删除。"
---
# Discord 清理机器人

在 Discord 公会频道中执行受控的清理操作，同时具备安全机制和便于审计的输出功能。

## 安全规范

- 仅使用机器人令牌（`DISCORD_BOT_TOKEN` 或 `--token`）。
- 拒绝用户账户令牌的传递以及自我操作行为（即机器人自我删除）。
- 在执行任何删除操作前，先运行 `purge-preview.mjs` 脚本进行预览。
- 在执行删除操作前，必须获得用户的明确确认代码。
- 如果目标频道不是公会频道，则立即终止操作。
- 保留每次操作的执行日志和 JSON 总结。

## 工作流程

1. 收集操作范围：`channel-id`（可选），`author-id`，`contains`，`regex`，`after`，`before`。
2. 在执行删除操作前，先阅读 `references/discord-limits.md` 文件以了解相关限制。
3. 运行 `purge-preview.mjs` 脚本进行预览，评估操作影响并获取用户的确认代码。
4. 使用确认代码执行删除操作。
5. 分享操作结果：显示已扫描的消息数量、匹配到的消息数量、被删除的消息数量、操作失败的情况，以及旧消息与最新消息的对比情况。

## 命令

### 预览

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

### 干运行（无实际删除操作）

```bash
node scripts/purge-runner.mjs --channel-id 123456789012345678 --confirm "PURGE-XXXXXXXX" --dry-run
```

### 复制或彻底删除频道

```bash
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --out ./tmp/nuke.json
node scripts/purge-nuke.mjs --channel-id 123456789012345678 --confirm "NUKE-XXXXXXXX" --delete-old --out ./tmp/nuke.json
```

## 脚本角色

- `scripts/purge-preview.mjs`：扫描频道消息，应用过滤规则，返回统计结果和用户的确认代码。
- `scripts/purge-runner.mjs`：执行删除操作，采用分批删除（`bulk-delete`）的方式；如果批量删除失败，则切换为单条消息删除。
- `scripts/purge-nuke.mjs`：创建替换频道；可选择性地删除原始频道。
- `scripts/scan-filter.mjs`：可重用的扫描和过滤逻辑。
- `scripts/discord-api.mjs`：封装 Discord API，实现速率限制和重试机制。
- `scripts/job-code.mjs`：提供用于生成确认代码的辅助工具。

## 操作员规则

- 对于大型频道，限制扫描次数（`max-scan`）。
- 对于耗时较长的任务，使用 `--state-file` 参数保存操作状态。
- 在可能的情况下，优先使用内容、用户或时间过滤方式，而非直接删除整个频道。
- 除非设置了 `--include-pinned` 参数，否则将置顶消息视为受保护内容，不予删除。

## 故障排除

- 如果出现 401/403 错误，请检查机器人令牌和频道权限。
- 如果预览结果显示消息历史为空，请检查 `READ_MESSAGE_HISTORY` 功能是否正常工作。
- 如果遇到频繁的 429 错误（请求被拒绝），请降低操作并行度并保持重试机制的启用状态。
- 如果 `bulk-delete` 操作失败，可能是由于消息创建时间超过 14 天，此时系统会切换为单条消息删除方式。