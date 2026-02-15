---
name: github-mentions
description: 监控并追踪您在所在组织中GitHub上的提及情况。查询新的提及记录，跟踪其状态（待处理/进行中/已完成），以避免重复工作。该工具可用于查看新的提及记录，或将已处理的提及标记为已解决。
version: 1.0.0
metadata:
  clawdhub:
    emoji: "🔔"
    requires:
      bins: ["gh", "jq"]
    dependencies:
      - github
---

# GitHub 提及监控

该技能用于跟踪和管理您在所有组织中收到的 GitHub 提及。通过维护状态信息，可避免重复查询和重复工作。

## 先决条件

- 已使用 `gh` CLI 进行身份验证（`gh auth login`）
- 需要 `jq` 工具来处理 JSON 数据
- 必须安装 `github` 技能（作为依赖项）

## 配置

### 配置文件

运行时配置信息存储在 `config.json` 文件中（默认路径：`skills/github-mentions/config.json`）：

```json
{
  "orgOnly": true,           // Only track mentions from within your orgs
  "orgMembersOnly": true,    // Only track mentions from org members (not external users)
  "memberCacheHours": 1,     // Refresh org member list every N hours
  "checkIntervalMinutes": 5  // Intended check frequency (for reference)
}
```

**配置选项：**
- `orgOnly=true`（默认值）：仅跟踪来自您所在组织的仓库的提及
- `orgOnly=false`：跟踪所有提及（包括来自外部组织的仓库）
- `orgMembersOnly=true`（默认值）：仅跟踪来自组织成员的提及
- `orgMembersOnly=false`：跟踪来自任何人的提及（包括外部贡献者和机器人）
- `memberCacheHours`：组织成员列表的刷新频率（默认值：1 小时）

**通过 CLI 设置配置：**
```bash
github-mentions config orgOnly false           # Track all mentions
github-mentions config orgMembersOnly false    # Include non-org-members
github-mentions config memberCacheHours 2      # Refresh members every 2 hours
```

### 环境变量（可选）

- `GITHUB_MENTIONS_STATE`：状态文件的路径（默认值：`~/.openclaw/workspace/memory/github-mentions-state.json`）
- `GITHUB_MENTIONS_CONFIG`：配置文件的路径（默认值：`skills/github-mentions/config.json`）

## 状态文件

该技能将状态信息保存在 JSON 文件中：

```json
{
  "lastChecked": "2026-02-02T00:00:00Z",
  "username": "gigi-trifle",
  "orgs": ["trifle-labs"],
  "mentions": {
    "trifle-labs/repo#123": {
      "type": "issue",
      "status": "pending",
      "title": "Issue title",
      "url": "https://github.com/...",
      "mentionedAt": "2026-02-02T00:00:00Z",
      "mentionedBy": "okwme"
    }
  }
}
```

## 命令

### 检查新提及

```bash
github-mentions check
```

查询自上次检查以来收到的新提及，并将新提及标记为“待处理”状态。返回新提及和待处理提及的汇总信息。

**查询策略：**
1. 在您被提及的每个组织中搜索问题/拉取请求（issues/PRs）。
2. 过滤掉来自同一组织成员的提及（排除自我提及）。
3. 与当前状态信息进行比较，找出新的提及。

### 列出当前提及

```bash
github-mentions list [--status <pending|in_progress|completed>]
```

显示所有被跟踪的提及，可根据需要按状态进行筛选。

### 开始处理提及

```bash
github-mentions start <mention-id>
```

将某个提及标记为“进行中”状态。提及的格式为 `owner/repo#number`。

### 完成提及

```bash
github-mentions done <mention-id>
```

将某个提及标记为“已完成”状态。

### 查看提及详情

```bash
github-mentions view <mention-id>
```

显示提及的详细信息，包括问题/拉取请求的内容以及最近的评论。

## 工作流程

1. **检查提及**：`github-mentions check`
2. **查看待处理的提及**：`github-mentions list --status pending`
3. **开始处理提及**：`github-mentions start trifle-labs/repo#123`
4. **处理提及**（回复、修复问题等）
5. **标记为已完成**：`github-mentions done trifle-labs/repo#123`

## 示例用法

```bash
# Check for new mentions across your orgs
github-mentions check

# Output:
# Last checked: 2026-02-01T23:00:00Z
# Found 2 new mentions:
#   - trifle-labs/clawdbot#456 (issue) by @okwme: "Need help with..."
#   - trifle-labs/webapp#789 (pr) by @teammate: "Review requested..."
#
# Pending mentions: 3
# In progress: 1

# Start working on one
github-mentions start trifle-labs/clawdbot#456

# View full context
github-mentions view trifle-labs/clawdbot#456

# Mark as done after addressing
github-mentions done trifle-labs/clawdbot#456
```

## 实现说明

**检测提及：**
```bash
# Search for issues/PRs mentioning you in an org
gh search issues "org:<org> mentions:<username>" --json number,repository,title,author,createdAt,url --limit 50

# Search for PR review requests
gh search prs "org:<org> review-requested:<username>" --json number,repository,title,author,createdAt,url --limit 50
```

**仅过滤组织成员的提及：**
```bash
# Get org members
gh api orgs/<org>/members --jq '.[].login'
```

仅跟踪此列表中用户的提及（排除自我提及）。

**避免重复查询：**
- 存储 `lastChecked` 时间戳
- 在搜索中使用 `created:>YYYY-MM-DD` 来限制结果范围
- 跳过状态文件中已记录的提及

## Cron 任务设置

将此技能设置为 OpenClaw 的 Cron 任务以自动执行。在 OpenClaw 的网关界面（Cron 标签）中创建一个新的任务：
- **名称：** GitHub 提及监控
- **调度时间：** `*/5 * * * *`（每 5 分钟执行一次）
- **会话模式：** 孤立会话
- **唤醒模式：** 下一次心跳时触发
- **负载（agentTurn）：**
  ```
  Run the GitHub mentions check and process any results:
  1. Run: bash ~/.openclaw/workspace/skills/github-mentions/github-mentions.sh check
  2. If there are NEW pending mentions, read the issue/PR details using gh api
  3. ALWAYS respond directly on GitHub first (post review or comment)
  4. Then notify via Telegram with a summary
  5. Mark the mention as completed
  6. If no new mentions, do nothing
  ```

这样确保代理直接在 GitHub 上作出响应，然后通过 Telegram 发送通知。