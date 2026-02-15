---
name: deck-tracker
version: 0.1.1
description: 在 NextCloud Deck 平板上跟踪 OpenClaw 任务。自动将任务添加到队列中，并跟踪任务的状态变化。
metadata:
  openclaw:
    emoji: "📋"
---

# Deck Tracker v1.0.0

用于在 NextCloud Deck 平板上跟踪任务。

## 板块结构

本技能假设板上有 4 个堆栈（列）：

| 堆栈 | 默认 ID | 用途 |
|-------|------------|---------|
| 队列 | 1 | 新到来的任务 |
| 进行中 | 2 | 当前正在处理的任务 |
| 等待 | 3 | 被阻塞/等待用户处理 |
| 今日已完成 | 4 | 已完成的任务 |

## 配置

设置以下环境变量（例如在您的 `.bashrc` 或 OpenClaw 配置文件中）：

```bash
export DECK_URL="https://your-nextcloud.com/index.php/apps/deck/api/v1.0"
export DECK_USER="your_username"
export DECK_PASS="your_app_password" # Use an App Password!
export BOARD_ID=1
```

如果您的堆栈 ID 与默认值（1、2、3、4）不同，请自行修改它们：

```bash
export STACK_QUEUE=10
export STACK_PROGRESS=11
export STACK_WAITING=12
export STACK_DONE=13
```

## 命令

### 列出板上的所有卡片

```bash
deck list
```

### 向队列中添加新任务

```bash
deck add "Task title" "Optional description"
```
**选项：**
- `--progress`：立即将新卡片移动到“进行中”状态。
- `--stack <id>`：将卡片创建到指定的堆栈中（默认：队列）。

示例（包含自动启动功能）：
```bash
deck add "Urgent Fix" "Fixing production bug" --progress
```

### 将卡片移动到另一个堆栈

```bash
deck move <card_id> <queue|progress|waiting|done>
```

### 获取卡片详情

```bash
deck get <card_id>
```

### 更新卡片标题/描述

```bash
deck update <card_id> [--title "New title"] [--description "New desc"]
```

### 向卡片记录状态更新

```bash
deck log <card_id> <status> "Message"
```
**状态：** `progress`、`success`、`error`、`warning`、`info`。

### 启动自动心跳监控

```bash
deck monitor <card_id> [target_id]
```
该命令会启动一个后台进程，每 60 秒在卡片上添加“仍在处理中...”的日志记录。此外，它还会每 120 秒向指定的 `target_id`（默认为 Skander）发送聊天通知。当卡片从“进行中”堆栈移动到“已完成”或“等待”堆栈时，该进程会自动终止。适用于预计耗时超过 2 分钟的任务。

### 将所有已完成的任务导出为 JSON 格式

```bash
deck dump-done
```
输出所有“今日已完成”状态卡片的 JSON 数据。有助于记忆整理。

### 归档所有已完成的卡片

```bash
deck archive-done
```

将所有“今日已完成”状态的卡片移动到归档状态。便于通过 cron 任务进行日常清理。

### 删除卡片

```bash
deck delete <card_id>
```

## 工作流程与记忆协议

1. **新任务到达** → `deck add "标题" "详细的初始描述"`（使用 `--progress` 选项立即开始处理）。
2. **详细描述**：描述应包括**目标**、**计划**和**约束条件**。
3. **记录更新** → `deck log <id> progress "完成第一步"`。
4. **完成任务**：使用 `deck update <id> --description "详细的总结"`，包括**技术总结**、**执行的操作**和**结果**。
5. **记忆整理**：在归档之前，使用 `deck dump-done` 来整理当天的工作内容，以增强长期记忆。
6. **日常清理** → `deck archive-done`。

### 🚨 AI 协议：复杂描述

在更新包含多行 Markdown 描述的卡片时，务必使用**临时文件方法**，以防止 shell 解释错误：

```bash
# 1. Write rich description to temp file
cat > /tmp/deck_desc_<id>.txt << 'EOF'
[Rich Markdown]
EOF

# 2. Update deck using the temp file
deck update <id> --description "$(cat /tmp/deck_desc_<id>.txt)"
```