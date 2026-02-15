---
name: mission-claw
description: 将代理活动记录到 Mission Claw 仪表板，并跟踪令牌的使用情况。适用于完成重要任务、子代理工作或任何值得在活动日志中记录的操作。该功能会在任务完成、活动被记录或代理工作被跟踪时触发。
binaries: [mclaw]
install: npm install -g mission-claw
homepage: https://github.com/tsangwailam/mcclaw
repository: https://github.com/tsangwailam/mcclaw
---

# Mission Claw 活动日志记录

将重要的任务记录到 Mission Claw 活动日志中，以便跟踪代理的工作情况、令牌使用情况以及项目进度。

## 先决条件

- **Mission Claw CLI**：必须在主机系统上安装 `mclaw` 可执行文件。
- **OpenClaw 内置功能**：依赖于 `session_status` 工具来获取当前的令牌使用情况。

## CLI 使用方法

```bash
mclaw log "Task description" \
  --agent "AgentName" \
  --project "ProjectName" \
  --status completed \
  --duration "Xm Ys" \
  --input-tokens N \
  --output-tokens N \
  --total-tokens N
```

### 必填字段
- `action` - 任务简述（位置参数）
- `--agent` - 代理名称（例如：“J”、“mission-claw”、“type-alchemy”）
- `--total-tokens` - 使用的令牌总数（**必须包含**）

### 可选字段
- `--details` - 任务完成的详细说明
- `--project` - 项目名称
- `--status` - `completed`（默认）、`in_progress` 或 `failed`
- `--duration` - 所用时间（例如：“5m”、“1h 30m”）
- `--input-tokens` / `--output-tokens` - 令牌使用明细

## 何时记录日志

在完成以下操作后记录日志：
- 重要的开发任务
- 错误修复或功能实现
- 研究或调查工作
- 配置更改
- 任何值得跟踪的任务

## 获取令牌使用情况

在记录日志之前，请检查您的会话令牌使用情况：
- 使用内置的 `session_status` 工具查看当前令牌数量
- 对于子代理，令牌信息会包含在完成通知中

## 示例

```bash
# Feature implementation
mclaw log "Added date-time filter to dashboard" \
  --agent "mission-claw" \
  --project "Mission Claw" \
  --status completed \
  --duration "10m" \
  --total-tokens 15000

# Quick fix
mclaw log "Fixed timezone bug" \
  --agent "J" \
  --project "ContentMorph" \
  --duration "2m" \
  --total-tokens 3500

# In-progress work
mclaw log "Implementing payment flow" \
  --agent "J" \
  --project "TypeAlchemy" \
  --status in_progress
```

## 其他命令

```bash
mclaw list                    # Recent activities
mclaw list --agent J          # Filter by agent
mclaw status                  # Quick stats and service status
mclaw dashboard start         # Start web dashboard (localhost:3101 by default)
```

## API 替代方案

CLI 会将日志记录到本地守护进程（默认为 `http://localhost:3100`）。您也可以直接通过 API 进行记录：

POST `http://localhost:3100/api/activity`
```json
{
  "action": "Task name",
  "agent": "J",
  "project": "Project",
  "status": "completed",
  "totalTokens": 5000,
  "inputTokens": 4000,
  "outputTokens": 1000
}
```