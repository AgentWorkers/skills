---
name: calendly
description: Calendly 调度集成：通过 Calendly API 列出事件、检查可用性以及管理会议。
---

# Calendly 技能

通过 MCP 生成的 CLI 与 Calendly 进行日程安排交互。

> **注意：** 日程安排 API 功能（如 `list-event-types`、`get-event-type-availability`、`schedule-event`）将在 `calendly-mcp-server v2.0.0` 发布到 npm 时可用。当前使用的 CLI 仍基于 v1.0.0 版本，以确保兼容性。

## 快速入门

```bash
# Get your Calendly profile (returns user URI)
calendly get-current-user

# List RECENT events (always use --min-start-time for recent queries!)
calendly list-events --user-uri "<YOUR_USER_URI>" --min-start-time "2026-01-20T00:00:00Z"

# Get event details
calendly get-event --event-uuid <UUID>

# Cancel an event
calendly cancel-event --event-uuid <UUID> --reason "Rescheduling needed"
```

## 可用命令

### 用户信息
- `get-current-user` - 获取已认证用户的详细信息

### 事件
- `list-events` - 列出已安排的事件（需要指定 `--user-uri`）
- `get-event` - 获取事件详情（需要指定 `--event-uuid`）
- `cancel-event` - 取消事件（需要指定 `--event-uuid`，可选参数 `--reason`）

### 参与者
- `list-event-invitees` - 列出事件的参与者（需要指定 `--event-uuid`）

### 组织
- `list-organization-memberships` - 列出用户所属的组织成员信息

## 配置

API 密钥可以存储在环境变量或 `.env` 文件中：
```bash
export CALENDLY_API_KEY="<your-pat-token>"
# Or in ~/.moltbot/.env or ~/.clawdbot/.env
```

请从以下链接获取您的个人访问令牌：https://calendly.com/integrations/api_webhooks

## 在 Moltbot 中的使用

当用户询问以下内容时：
- “我有哪些会议？” → 使用 `list-events` 并添加 `--min-start-time` 参数（查询最近的事件！）
- “取消我下午 2 点的会议” → 先使用 `list-events` 进行筛选，然后使用 `cancel-event` 取消会议
- “谁参加了 X 会议？” → 使用 `list-event-invitees` 查看参与者

**注意：** 首次使用前，请运行 `calendly get-current-user` 以获取您的用户 URI。

## 获取用户 URI

运行 `calendly get-current-user` 以获取您的用户 URI。示例：
```json
{
  "resource": {
    "uri": "https://api.calendly.com/users/<YOUR_USER_UUID>",
    "scheduling_url": "https://calendly.com/<your-username>"
  }
}
```

## 示例

```bash
# List next 10 events
calendly list-events \
  --user-uri "<YOUR_USER_URI>" \
  -o json | jq .

# Get event details
calendly get-event \
  --event-uuid "<EVENT_UUID>" \
  -o json

# Cancel with reason
calendly cancel-event \
  --event-uuid "<EVENT_UUID>" \
  --reason "Rescheduling due to conflict"
```

## 即将推出：日程安排 API（v2.0）

一旦 `calendly-mcp-server v2.0.0` 发布，以下命令将可用：

### 日程安排工作流程
```bash
# 1. List available event types
calendly list-event-types

# 2. Check availability for a specific event type
calendly get-event-type-availability --event-type "<EVENT_TYPE_URI>"

# 3. Schedule a meeting (requires paid Calendly plan)
calendly schedule-event \
  --event-type "<EVENT_TYPE_URI>" \
  --start-time "2026-01-25T19:00:00Z" \
  --invitee-email "client@company.com" \
  --invitee-name "John Smith" \
  --invitee-timezone "America/New_York"
```

**日程安排 API 的要求：**
- 使用 `calendly-mcp-server v2.0.0` 或更高版本（截至 2026-01-21 为止尚未发布）
- 拥有付费的 Calendly 计划（Standard 或更高级别）

当 v2.0 版本发布后，您需要升级您的应用程序：

```bash
cd ~/clawd/skills/calendly
MCPORTER_CONFIG=./mcporter.json npx mcporter@latest generate-cli --server calendly --output calendly
```

## 重要提示：时间筛选

**查询最近的事件时，请务必使用 `--min-start-time` 参数！**

API 默认按事件发生时间从旧到新返回结果，并且不支持 CLI 分页功能。如果不使用时间筛选，您可能会收到多年前的事件信息。

```bash
# Last 7 days
calendly list-events --user-uri "<URI>" --min-start-time "$(date -u -d '7 days ago' +%Y-%m-%dT00:00:00Z)"

# This week
calendly list-events --user-uri "<URI>" --min-start-time "2026-01-20T00:00:00Z" --max-start-time "2026-01-27T23:59:59Z"

# Future events only
calendly list-events --user-uri "<URI>" --min-start-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## 其他说明：
- API 响应中的所有时间均为 UTC 格式（显示时需转换为太平洋标准时间）
- 事件 UUID 可在 `list-events` 的输出结果中找到
- 虽然提供了 OAuth 选项，但使用个人访问令牌即可完成所有操作
- CLI 不支持分页功能，请使用时间筛选来限制查询结果

---

**生成时间：** 2026-01-20  
**更新时间：** 2026-01-21（CLI 保持与 npm v1.0.0 的兼容性；日程安排 API 功能待上游发布）  
**来源：** meAmitPatil/calendly-mcp-server（通过 mcporter 工具生成）