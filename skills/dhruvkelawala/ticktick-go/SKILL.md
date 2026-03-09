---
name: ticktick-go
version: 1.0.1
description: "通过 `ttg` CLI（github.com/dhruvkelawala/ticktick-go）来管理 TickTick 任务和项目。该工具可用于以下操作：添加任务、查看任务列表、标记任务为已完成、编辑任务、管理项目，以及根据截止日期或优先级对任务进行筛选。使用前请确保已安装 `ttg` 并完成身份验证。"
metadata:
  openclaw:
    requires:
      bins:
        - ttg
    install:
      - id: ttg
        kind: shell
        label: "Build and install ttg CLI from source"
        script: "git clone https://github.com/dhruvkelawala/ticktick-go /tmp/ttg-install && cd /tmp/ttg-install && make install && rm -rf /tmp/ttg-install"
---
# TickTick CLI（`ttg`）

这是一个通过[`ticktick-go` CLI`](https://github.com/dhruvkelawala/ticktick-go)提供的[TickTick](https://ticktick.com)终端接口。

## 先决条件

安装`ttg`：
```bash
git clone https://github.com/dhruvkelawala/ticktick-go
cd ticktick-go && make install
```

创建`~/.config/ttg/config.json`文件，并填写您的TickTick API凭据（可在[developer.ticktick.com](https://developer.ticktick.com/manage)获取）：
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "timezone": "America/New_York"
}
```

进行身份验证：
```bash
ttg auth login      # opens browser OAuth2 flow
ttg auth status     # confirm you're logged in
```

## 任务命令

```bash
# List
ttg task list                              # Inbox (default)
ttg task list --all                        # Every task
ttg task list --project "Work"             # By project name
ttg task list --due today                  # Due today
ttg task list --due tomorrow               # Due tomorrow
ttg task list --priority high              # By priority
ttg task list --json                       # JSON output for scripting

# Add
ttg task add "Buy milk"
ttg task add "Review PR" --project "Work" --priority high --due "tomorrow 9am"

# Manage
ttg task get <id>                          # Full details
ttg task done <id>                         # Mark complete
ttg task delete <id>                       # Delete
ttg task edit <id> --title "Updated title" --priority medium --due "next monday"
```

## 项目命令

```bash
ttg project list                           # All projects
ttg project get <id>                       # Project details
ttg project create "Side Projects"         # Create new project
```

## 截止日期格式

| 输入 | 结果 |
|-------|--------|
| `today`, `tomorrow` | 当天的午夜 |
| `next monday` | 下一个周一 |
| `3pm`, `tomorrow 3pm` | 特定时间 |
| `in 2 days`, `in 3 hours` | 相对时间间隔 |
| `2026-03-20` | ISO日期格式 |
| `2026-03-20T15:00:00` | ISO日期时间格式 |

## 优先级

`none`（默认）· `low`· `medium`· `high`

## JSON/脚本支持

所有命令都支持`--json` / `-j`选项：
```bash
# Get all high-priority tasks as JSON
ttg task list --priority high --json

# Pipe into jq
ttg task list --all --json | jq '.[] | select(.dueDate != null) | .title'
```

## 常用模式

```bash
# Morning review — what's due today?
ttg task list --due today

# Quick capture while in flow
ttg task add "Follow up with Alex" --due "tomorrow 10am" --priority medium

# End-of-day — mark things done
ttg task list --json | jq '.[].id'   # get IDs
ttg task done <id>

# Weekly planning — see everything
ttg task list --all
```