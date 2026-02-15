---
name: task-status
description: 对于长时间运行的任务，应在聊天中发送简短的状态描述。当需要在多步骤操作过程中提供定期更新、确认任务完成情况或通知任务失败时，可以使用这种方法。该方案包括自动化的定期监控功能（每5秒发送一次更新）、状态消息模板，以及一个用于统一状态报告的辅助函数。
---

# 任务状态管理技能

## 快速入门

### 手动状态更新
```bash
python scripts/send_status.py "Starting data fetch..." "progress" "step1"
python scripts/send_status.py "Processing complete" "success" "final"
python scripts/send_status.py "Error: Missing API key" "error" "auth"
```

### 自动周期性监控（每5秒一次）
```bash
# Start monitoring a long-running task
python scripts/monitor_task.py start "My Long Task" "processing"

# Monitor will send "Still working..." updates every 5 seconds
# When task completes, report final status
python scripts/monitor_task.py stop "My Long Task" "success" "Completed successfully!"
```

## 状态类型

- **进行中**：任务正在执行中（显示为 🔄 或 ->）
- **成功**：任务已完成（显示为 ✅ 或 OK）
- **失败**：任务失败（显示为 ❌ 或 !）
- **警告**：存在问题但仍在继续（显示为 ⚠️ 或 ?）

## 周期性监控

`monitor_task.py` 脚本提供自动状态更新功能：

### 启动监控
```bash
python scripts/monitor_task.py start "<task_name>" "<status_type>" [--interval <seconds>]
```

- 每5秒自动发送“仍在处理中...”的更新信息
- 在后台运行，直到手动停止
- 可以通过配置不同的时间间隔来调整监控频率

### 停止监控
```bash
python scripts/monitor_task.py stop "<task_name>" "<final_status>" "<final_message>"
```

### 示例：处理大文件
```bash
# Start monitoring
python scripts/monitor_task.py start "video_processing" "progress"

# ... long processing happens here ...

# Stop with final status
python scripts/monitor_task.py stop "video_processing" "success" "Processing complete!"
```

## 手动更新（快速状态显示）

对于不需要周期性监控的单次状态更新，可以使用手动更新方式：
```bash
python scripts/send_status.py "Still fetching data..." "progress" "fetch"
python scripts/send_status.py "Processing records: 250/1000" "progress" "process"
python scripts/send_status.py "Complete! 3 files ready" "success" "final"
python scripts/send_status.py "Error: Connection timeout" "error" "api"
```

## 各种方法的适用场景

### 何时使用手动更新：
- 任务执行时间较短（少于30秒）
- 您希望控制更新发送的时间
- 任务有明确的、可量化的里程碑

### 何时使用周期性监控：
- 任务运行时间较长（超过1分钟）
- 您希望每5秒接收一次状态更新
- 任务在某些阶段没有明显进展
- 您希望让用户知道任务仍在继续进行中

## 消息提示规范

状态消息的长度应控制在140个字符以内。示例：
- **进行中**：“仍在获取数据中...” 或 “正在处理记录：250/1000”
- **成功**：“任务完成！3个文件已准备好” 或 “任务成功完成”
- **失败**：“错误：连接超时” 或 “失败：缺少API密钥”
- **警告**：“尽管出现超时，但仍继续执行” 或 “部分成功：5/10个文件”

## 高级用法

### 添加更多详细信息
```bash
python scripts/send_status.py "Uploading..." "progress" "upload" --details "File: report.pdf (2.4MB)"
```

### 配置不同的监控间隔
```bash
python scripts/monitor_task.py start "data_sync" "progress" --interval 10
```

### 在Python脚本中导入该功能
```python
from send_status import send_status

def long_task():
    send_status("Starting...", "progress", "step1")
    # ... work
    send_status("Step complete", "success", "step1")
```

## 使用Clawdbot的Cron功能实现自动化

对于需要定时更新的任务，可以利用Clawdbot的Cron功能：
```python
# In a script or session
from cron import add

# Every 5 seconds, check status
job = {
    "text": "Check status update",
    "interval": "5s",
    "enabled": True
}
add(job)
```

这样即使您没有实时监控，系统也能自动发送状态更新。

## 安装方法

要使用此技能，请将 `task-status` 文件夹复制到您的Clawdbot技能目录中：
```
C:\Users\Luffy\AppData\Roaming\npm\node_modules\clawdbot\skills\task-status
```

或者将其添加到您的工作空间中，并在 `AGENTS.md` 或 `TOOLS.md` 文件中引用它。

安装完成后，该技能将可用于任何需要周期性状态更新的任务。