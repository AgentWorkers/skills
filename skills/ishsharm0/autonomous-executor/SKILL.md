# 自主执行器（Autonomous Executor）

具备自我修复和错误恢复能力，能够完全自主地执行任务。

## 主要特性

- **自动错误恢复**：对错误进行分类，并采取针对性的恢复策略。
- **指数级重试机制**：智能的重试时机控制，支持配置重试次数上限。
- **自我修复功能**：自动安装缺失的依赖项，创建缺失的资源。
- **检查点/恢复功能**：为需要隔夜执行的任务保存进度，以便后续继续执行。
- **MongoDB 日志记录**：生成持久的执行日志，便于监控。
- **工具识别能力**：全面了解所有 OpenClaw 工具和技能的使用情况。
- **隔夜批量处理**：在用户睡眠期间自动执行任务队列中的任务。

## 错误分类与恢复策略

| 错误类型 | 恢复方式 |
|---------|---------|
| 网络问题 | 等待并尝试重新连接；使用指数级重试策略。 |
| 认证问题 | 刷新凭据，提示用户重新认证。 |
| 速率限制问题 | 使用 `Retry-After` 头部信息进行重试；采用指数级重试策略。 |
| 资源问题 | 自动创建缺失的文件/目录，清理临时文件。 |
| 验证问题 | 自动修复输入数据；使用默认值。 |
- 依赖项问题 | 使用 `pip` 安装缺失的模块。 |
- 浏览器问题 | 重启 Playwright 运行环境，减少并发请求。 |
- API 问题 | 使用指数级重试策略；尝试其他 API 端点。 |

## 快速使用方法

```python
from autonomous_executor.executor import AutoExec

# Deploy a project autonomously
result = AutoExec.deploy("my-portfolio", "portfolio", "My awesome portfolio")

# Run any function with auto-recovery
result = AutoExec.run(my_function, arg1, arg2, _max_retries=5)

# Check overnight report
report = AutoExec.report()

# List all capabilities
print(AutoExec.caps())
```

## 隔夜批量执行任务

```python
from autonomous_executor.overnight import Overnight

# Queue tasks to run overnight
Overnight.deploy("my-portfolio", "portfolio", description="Overnight deploy")
Overnight.deploy("client-site", "landing", description="Client landing page")
Overnight.research("AI trends 2025")

# Queue custom functions
Overnight.run(my_backup_function, "/data", _name="Backup Data")

# Start overnight run
summary = Overnight.start()

# Next morning, check report
print(Overnight.report())
```

## 装饰器使用方法

```python
from autonomous_executor.executor import autonomous

@autonomous(max_retries=5, task_name="Critical Task")
def my_critical_function():
    # This will auto-recover from errors
    return do_something()
```

## 完整的 API 文档

### AutonomousExecutor

```python
from autonomous_executor.executor import AutonomousExecutor

executor = AutonomousExecutor(user="ishaan")

# Execute any function
result = executor.execute(
    task_fn=my_function,
    args=(arg1, arg2),
    kwargs={"key": "value"},
    task_name="My Task",
    max_retries=5,
    timeout=300  # 5 minutes
)

# Run project pipeline
result = executor.run_project_pipeline({
    "name": "my-app",
    "type": "nextjs",
    "description": "My Next.js app",
    "extra": {"features": ["dark_mode", "auth"]}
})

# Run research
result = executor.run_research_pipeline("quantum computing", depth="deep")

# Get execution history
history = executor.get_execution_history(limit=20)

# Get overnight report
report = executor.get_overnight_report()
```

## 示例输出结果

```
[14:23:45] 🚀 Starting task: Deploy Portfolio
[14:23:45]    Max retries: 5, Timeout: 0s
[14:23:45]    Available capabilities: 15 skills
[14:23:45] ⚡ Attempt 1/5...
[14:23:47] ❌ Attempt 1 failed: ConnectionError: Network timeout
[14:23:47]    Error category: network
[14:23:47] 🔧 Trying recovery: wait_and_retry
[14:23:47] ⏳ Waiting 4.0s before retry...
[14:23:51] ⚡ Attempt 2/5...
[14:24:03] ✅ Task completed successfully in 12.1s
```

## MongoDB 数据库中的相关集合

- `task_records`：存储完整的任务执行记录。
- `task_checkpoints`：保存需要恢复执行的任务的检查点数据。
- `execution_logs`：实时生成的执行日志。