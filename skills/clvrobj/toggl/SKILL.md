---
name: toggl
description: 通过 `toggl CLI` 来记录工作时间。当用户需要开始/停止时间跟踪、查看当前计时器状态、查看今日或周报、列出最近的记录条目，或管理时间记录时，可以使用该命令。该命令会在以下关键词被输入时触发：`toggl`、`time tracking`、`timer`、`track time`、`what am I working on`、`log time`、`timesheet`。
---

# Toggl 时间跟踪

使用 `toggl` CLI（@beauraines/toggl-cli）来实现与 Toggl 的集成。

## 先决条件

安装 CLI：
```bash
npm install -g @beauraines/toggl-cli
```

配置身份验证（创建 `~/.toggl-cli.json` 文件）：
```json
{
  "api_token": "YOUR_TOGGL_API_TOKEN",
  "default_workspace_id": "YOUR_WORKSPACE_ID",
  "timezone": "Your/Timezone"
}
```

从以下地址获取您的 API 令牌：https://track.toggl.com/profile
从您的 Toggl 网址获取您的工作区 ID：`https://track.toggl.com/{workspace_id}/...`

设置权限：`chmod 600 ~/.toggl-cli.json`

## 命令

### 查看状态
```bash
toggl now                    # Show running timer
toggl me                     # Show user info
```

### 启动/停止时间跟踪
```bash
toggl start                  # Start timer (interactive)
toggl start -d "Task name"   # Start with description
toggl start -d "Task" -p "Project"  # With project
toggl stop                   # Stop current timer
```

### 继续之前的操作
```bash
toggl continue               # Restart most recent entry
toggl continue "keyword"     # Restart entry matching keyword
```

### 生成报告
```bash
toggl today                  # Today's time by project
toggl week                   # Weekly summary by day
```

### 列出所有记录
```bash
toggl ls                     # Last 14 days
toggl ls -d 7                # Last 7 days
toggl ls --today             # Today only
toggl ls "search term"       # Search entries
```

### 添加已完成的任务
```bash
toggl add "9:00AM" "10:30AM" "Meeting notes"
```

### 编辑当前任务
```bash
toggl edit -s "10:00AM"      # Change start time
toggl edit -d "New desc"     # Change description
toggl edit -p "Project"      # Change project
```

### 删除任务
```bash
toggl rm <id>                # Remove entry by ID
```

### 管理项目
```bash
toggl project ls             # List projects
```

### 其他功能
```bash
toggl web                    # Open Toggl in browser
toggl create-config          # Generate config template
```

## 注意事项

- 时间格式必须符合 dayjs 的解析规则（例如：`4:50PM`、`12:00 AM`、`9:00`）
- 配置文件：`~/.toggl-cli.json`
- 环境变量可以覆盖配置文件中的设置：`TOGGL_API_TOKEN`、`TOGGL_DEFAULT_WORKSPACE_ID`、`TOGGL_TIMEZONE`