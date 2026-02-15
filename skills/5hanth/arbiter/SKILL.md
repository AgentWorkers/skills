---
name: arbiter
description: 将决策提交给仲裁者 Zebu 进行异步人工审核。当您需要在计划、架构选择或继续执行之前获得人工输入或批准时，请使用此方法。
metadata: {"openclaw":{"requires":{"bins":["arbiter-push"]}}}
---

# Arbiter 技能

将决策推送到 Arbiter Zebu 进行异步人工审核。当您需要对计划、架构选择或在继续执行前需要获得人工批准时，请使用此功能。

## 安装

**通过 ClawHub 快速安装：**
```bash
clawhub install arbiter
```

**或通过 bun（使 CLI 命令全局可用）：**
```bash
bun add -g arbiter-skill
```

**或手动安装：**
```bash
git clone https://github.com/5hanth/arbiter-skill.git
cd arbiter-skill && npm install && npm run build
ln -s $(pwd) ~/.clawdbot/skills/arbiter
```

### 先决条件

- [Arbiter Zebu](https://github.com/5hanth/arbiter-zebu) 机器人正在运行（或只需运行 `bunx arbiter-zebu`）
- `~/.arbiter/queue/` 目录（由机器人自动创建）

## 环境变量

在您的代理环境中设置以下变量，以便自动检测代理/会话：

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `CLAWDBOT_AGENT` | 代理 ID | `ceo`, `swe1` |
| `CLAWDBOT_SESSION` | 会话密钥 | `agent:ceo:main` |

## 使用场景

- 在实施前审查计划
- 需要权衡的各种架构决策
- 任何需要人工判断的阻碍性事项
- 多个相关决策的批量处理

**请勿用于：**
- 无需解释的简单“是/否”问题
- 紧急的实时决策（请使用直接消息）
- 可以自行研究的技术问题

## 工具

### arbiter_push

创建一个决策计划以供人工审核。

**CLI：`arbiter-push '<json>'`** — 接受一个包含所有字段的 JSON 参数。

```bash
arbiter-push '{
  "title": "API Design Decisions",
  "tag": "nft-marketplace",
  "context": "SWE2 needs these decided before API work",
  "priority": "normal",
  "notify": "agent:swe2:main",
  "decisions": [
    {
      "id": "auth-strategy",
      "title": "Auth Strategy", 
      "context": "How to authenticate admin users",
      "options": [
        {"key": "jwt", "label": "JWT tokens", "note": "Stateless"},
        {"key": "session", "label": "Sessions", "note": "More control"},
        {"key": "oauth", "label": "OAuth", "note": "External provider"}
      ]
    },
    {
      "id": "database",
      "title": "Database Choice",
      "context": "Primary datastore",
      "options": [
        {"key": "postgresql", "label": "PostgreSQL + JSONB"},
        {"key": "mongodb", "label": "MongoDB"}
      ],
      "allowCustom": true
    }
  ]
}'
```

**JSON 字段：**

| 字段 | 是否必填 | 描述 |
|-------|----------|-------------|
| `title` | 是 | 计划标题 |
| `tag` | 否 | 用于过滤的标签（例如，项目名称） |
| `context` | 否 | 供审核者参考的背景信息 |
| `priority` | 否 | `low`, `normal`, `high`, `urgent`（默认：normal） |
| `notify` | 否 | 完成后通知的会话 |
| `agent` | 否 | 代理 ID（从 `CLAWDBOT_AGENT` 环境变量自动检测） |
| `session` | 否 | 会话密钥（从 `CLAWDBOT_SESSION` 环境变量自动检测） |
| `decisions` | 是 | 决策数组 |

**决策对象：**

| 字段 | 是否必填 | 描述 |
|-------|----------|-------------|
| `id` | 是 | 计划内的唯一 ID |
| `title` | 是 | 决策标题 |
| `context` | 否 | 供审核者参考的说明 |
| `options` | 是 | `{key, label, note?}` 的数组 |
| `allowCustom` | 否 | 是否允许自由文本回答（默认：false） |
| `default` | 否 | 建议的选项键 |

**返回值：**
```json
{
  "planId": "abc123",
  "file": "~/.arbiter/queue/pending/ceo-api-design-abc123.md",
  "total": 2,
  "status": "pending"
}
```

### arbiter_status

检查决策计划的状态。

**CLI：`arbiter-status <plan-id>` 或 `arbiter-status --tag <tag>`

```bash
arbiter-status abc12345
# or
arbiter-status --tag nft-marketplace
```

**返回值：**
```json
{
  "planId": "abc123",
  "title": "API Design Decisions",
  "status": "in_progress",
  "total": 3,
  "answered": 1,
  "remaining": 2,
  "decisions": {
    "auth-strategy": {"status": "answered", "answer": "jwt"},
    "database": {"status": "pending", "answer": null},
    "caching": {"status": "pending", "answer": null}
  }
}
```

### arbiter_get

获取已完成计划的答案。

**CLI：`arbiter-get <plan-id>` 或 `arbiter-get --tag <tag>`

```bash
arbiter-get abc12345
# or
arbiter-get --tag nft-marketplace
```

**返回值：**
```json
{
  "planId": "abc123",
  "status": "completed",
  "completedAt": "2026-01-30T01:45:00Z",
  "answers": {
    "auth-strategy": "jwt",
    "database": "postgresql",
    "caching": "redis"
  }
}
```

**如果未完成：**
```json
{
  "error": "Plan not complete",
  "status": "in_progress",
  "remaining": 2
}
```

### arbiter_await

阻塞直到计划完成（带有超时设置）。

```bash
arbiter-await abc12345 --timeout 3600
```

每 30 秒检查一次，直到计划完成或超时。

**返回值：** 完成后与 `arbiter_get` 的返回值相同。

## 使用示例

### 示例 1：计划审查
```bash
# Push plan decisions (single JSON argument)
RESULT=$(arbiter-push '{"title":"Clean IT i18n Plan","tag":"clean-it","priority":"high","notify":"agent:swe3:main","decisions":[{"id":"library","title":"i18n Library","options":[{"key":"i18next","label":"i18next"},{"key":"formatjs","label":"FormatJS"}]},{"id":"keys","title":"Key Structure","options":[{"key":"flat","label":"Flat (login.button)"},{"key":"nested","label":"Nested ({login:{button}})"}]}]}')

PLAN_ID=$(echo $RESULT | jq -r '.planId')
echo "Pushed plan $PLAN_ID — waiting for human review"
```

### 示例 2：检查后继续执行
```bash
# Check if decisions are ready
STATUS=$(arbiter-status --tag nft-marketplace)

if [ "$(echo $STATUS | jq -r '.status')" == "completed" ]; then
  ANSWERS=$(arbiter-get --tag nft-marketplace)
  AUTH=$(echo $ANSWERS | jq -r '.answers["auth-strategy"]')
  echo "Using auth strategy: $AUTH"
  # Proceed with implementation
else
  echo "Still waiting for $(echo $STATUS | jq -r '.remaining') decisions"
fi
```

### 示例 3：等待结果
```bash
# Wait up to 1 hour for decisions
ANSWERS=$(arbiter-await abc12345 --timeout 3600)

if [ $? -eq 0 ]; then
  # Got answers, proceed
  echo "Decisions ready: $ANSWERS"
else
  echo "Timeout waiting for decisions"
fi
```

## 最佳实践

1. **批量处理相关决策** — 不要一次只推送一个决策
2. **提供背景信息** — 人工审核者需要了解各种权衡因素
3. **使用标签** — 便于过滤（例如：`--tag project-name`）
4. **设置通知** — 以便被阻塞的代理能够收到通知
5. **谨慎使用优先级** — 将 `urgent` 状态保留给真正需要紧急处理的决策

## 文件位置

| 路径 | 用途 |
|------|---------|
| `~/.arbiter/queue/pending/` | 待审核的计划 |
| `~/.arbiter/queue/completed/` | 已回答的计划（存档） |
| `~/.arbiter/queue/notify/` | 代理通知 |

## 检查通知（代理心跳）

在您的 HEARTBEAT.md 文件中添加以下内容：
```markdown
## Check Arbiter Notifications

1. Check if `~/.arbiter/queue/notify/` has files for my session
2. If yes, read answers and proceed with blocked work
3. Delete notification file after processing
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 计划未显示在 Arbiter 中 | 确保文件具有有效的 YAML 标头信息 |
| 回答未显示 | 检查 `arbiter_status`，可能计划尚未完成 |
| 未收到通知 | 确保正确设置了 `--notify` 参数 |

## 参见

- [Arbiter Zebu 架构](https://github.com/5hanth/arbiter-zebu/blob/main/ARCHITECTURE.md)
- [Arbiter Zebu 机器人](https://github.com/5hanth/arbiter-zebu)