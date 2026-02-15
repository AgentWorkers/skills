---
name: todoist
description: 在 Todoist 中管理任务和项目。当用户询问有关任务、待办事项、提醒或生产力方面的问题时，可以使用此内容进行解答。
homepage: https://todoist.com
metadata:
  clawdbot:
    emoji: "✅"
    requires:
      bins: ["todoist"]
      env: ["TODOIST_API_TOKEN"]
---

# Todoist CLI

这是一个用于管理Todoist任务的命令行工具（CLI），基于官方的TypeScript SDK开发。

## 安装

```bash
# Requires todoist-ts-cli >= 0.2.0 (for --top / --order)
npm install -g todoist-ts-cli@^0.2.0
```

## 设置

1. 从 [https://todoist.com/app/settings/integrations/developer](https://todoist.com/app/settings/integrations/developer) 获取API令牌。
2. 选择以下方法之一进行设置：
   ```bash
   todoist auth <your-token>
   # or
   export TODOIST_API_TOKEN="your-token"
   ```

## 命令

### 任务操作

```bash
todoist                    # Show today's tasks (default)
todoist today              # Same as above
todoist tasks              # List tasks (today + overdue)
todoist tasks --all        # All tasks
todoist tasks -p "Work"    # Tasks in project
todoist tasks -f "p1"      # Filter query (priority 1)
todoist tasks --json
```

### 添加任务

```bash
todoist add "Buy groceries"
todoist add "Meeting" --due "tomorrow 10am"
todoist add "Review PR" --due "today" --priority 1 --project "Work"
todoist add "Prep slides" --project "Work" --order 3  # add at a specific position (1-based)
todoist add "Triage inbox" --project "Work" --order top  # add to top (alternative to --top)
todoist add "Call mom" -d "sunday" -l "family"  # with label
```

### 管理任务

```bash
todoist view <id>          # View task details
todoist done <id>          # Complete task
todoist reopen <id>        # Reopen completed task
todoist update <id> --due "next week"
todoist move <id> -p "Personal"
todoist delete <id>
```

### 搜索

```bash
todoist search "meeting"
```

### 项目与标签

```bash
todoist projects           # List projects
todoist project-add "New Project"
todoist labels             # List labels
todoist label-add "urgent"
```

### 评论

```bash
todoist comments <task-id>
todoist comment <task-id> "Note about this task"
```

## 使用示例

**用户：“我今天需要做什么？”**
```bash
todoist today
```

**用户：“在我的任务列表中添加‘买牛奶’”**
```bash
todoist add "Buy milk" --due "today"
```

**用户：“提醒我明天去看牙医”**
```bash
todoist add "Call the dentist" --due "tomorrow"
```

**用户：“将‘购买杂货’的任务标记为已完成”**
```bash
todoist search "grocery"   # Find task ID
todoist done <id>
```

**用户：“我的工作项目里有哪些任务？”**
```bash
todoist tasks -p "Work"
```

**用户：“显示我的高优先级任务”**
```bash
todoist tasks -f "p1"
```

## 过滤语法

Todoist支持强大的过滤查询：
- `p1`, `p2`, `p3`, `p4` - 优先级级别
- `today`, `tomorrow`, `overdue` - 任务截止日期（支持自然语言表达，如“明天”、“下周一”、“1月15日”）
- `@label` - 带有特定标签的任务
- `#project` - 属于某个项目的任务
- `search: 关键词` - 搜索任务内容

## 注意事项

- 任务ID会在任务列表中显示。
- 截止日期支持自然语言表达（如“明天”、“下周一”、“1月15日”）。
- 优先级1表示最高优先级，4表示最低优先级。
- 可使用 `--order <n>`（基于1的顺序）或 `--order top` 将任务插入项目/部分的特定位置。