---
name: timesheet
description: 使用 timesheet.io 的 CLI 工具来记录工作时间、管理项目和任务。
user-invocable: true
homepage: https://timesheet.io
metadata: {"requires": {"bins": ["timesheet"]}}
---

# Timesheet CLI 功能

通过命令行控制 timesheet.io 的时间跟踪功能。所有命令均可使用 `--json` 标志来获取结构化输出。

## 认证

在使用其他命令之前，请先检查认证状态：
```bash
timesheet auth status --json
```

如果未认证，请引导用户运行以下命令：
```bash
timesheet auth login
```

或者，为了实现自动化操作，请设置 API 密钥：
```bash
export TIMESHEET_API_KEY=ts_your.apikey
```

## 计时器操作

### 启动计时器
```bash
# List projects first to get project ID
timesheet projects list --json

# Start timer for a project
timesheet timer start <project-id>
```

### 检查计时器状态
```bash
timesheet timer status --json
```

返回信息包括：状态（运行中/暂停/已停止）、项目名称、持续时间以及开始时间。

### 控制计时器
```bash
timesheet timer pause
timesheet timer resume
timesheet timer stop  # Creates a task from the timer
```

### 更新正在运行的计时器
```bash
timesheet timer update --description "Working on feature X"
timesheet timer update --billable
```

## 项目管理

### 列出项目
```bash
timesheet projects list --json
```

### 创建项目
```bash
timesheet projects create "Project Name" --json
timesheet projects create "Client Project" --billable --json
```

### 显示/更新/删除项目
```bash
timesheet projects show <id> --json
timesheet projects update <id> --title "New Name"
timesheet projects delete <id>
```

## 任务管理

### 列出任务
```bash
timesheet tasks list --json           # Recent tasks
timesheet tasks list --today --json   # Today's tasks
timesheet tasks list --this-week --json
```

### 手动创建任务
```bash
timesheet tasks create -p <project-id> -s "2024-01-15 09:00" -e "2024-01-15 17:00" --json
timesheet tasks create -p <project-id> -s "09:00" -e "17:00" -d "Task description" --json
```

### 更新任务
```bash
timesheet tasks update <id> --description "Updated description"
timesheet tasks update <id> --billable
timesheet tasks update <id> --start "10:00" --end "12:00"
```

### 删除任务
```bash
timesheet tasks delete <id>
```

## 团队与标签

### 团队
```bash
timesheet teams list --json
```

### 标签
```bash
timesheet tags list --json
timesheet tags create "Urgent" --color 1
timesheet tags delete <id>
```

## 报告

### 时间统计
```bash
timesheet reports summary --today --json
timesheet reports summary --this-week --json
timesheet reports summary --this-month --json
timesheet reports summary --from 2024-01-01 --to 2024-01-31 --json
```

### 导出数据
```bash
timesheet reports export -f xlsx -s 2024-01-01 -e 2024-01-31
timesheet reports export -f csv --this-month
```

## 用户配置

```bash
timesheet profile show --json
timesheet profile settings --json

timesheet config show
timesheet config set defaultProjectId <id>
```

## 常见工作流程

### 为当前工作记录时间
1. 检查计时器是否正在运行：`timesheet timer status --json`
2. 如果未运行，请启动计时器：`timesheet timer start <project-id>`
3. 完成工作后，停止计时器：`timesheet timer stop`

### 快速记录时间
```bash
# Create a completed task directly
timesheet tasks create -p <project-id> -s "09:00" -e "12:00" -d "Morning standup and dev work" --json
```

### 按名称查找项目
```bash
timesheet projects list --json | jq '.[] | select(.title | contains("ProjectName"))'
```

## 错误处理

退出代码：
- 0：成功
- 1：一般错误
- 2：使用错误（参数无效）
- 3：认证错误 - 运行 `timesheet auth login`
- 4：API 错误
- 5：超出请求频率限制 - 等待片刻后重试
- 6：网络错误

## 提示

- 始终使用 `--json` 标志以便程序化解析输出结果
- 使用 `--quiet` 或 `-q` 选项来抑制非必要的输出信息
- 在配置文件中设置 `defaultProjectId` 可以避免在选择项目时出现错误
- 当不在终端环境中时，系统会自动生成适合管道传输的输出格式