# 任务规划与验证工具 - 技能指南

本工具为AI代理提供了一个安全、循序渐进的任务管理系统。

## 快速安装

```bash
# Clone the repository
git clone https://github.com/cerbug45/task-planner-validator.git
cd task-planner-validator

# That's it! No dependencies needed - pure Python standard library
```

## 验证安装

```bash
# Run tests
python test_basic.py

# Run examples
python examples.py
```

## 基本使用

### 1. 导入并初始化

```python
from task_planner import TaskPlanner

# Create planner
planner = TaskPlanner(auto_approve=False)
```

### 2. 定义执行器

```python
def my_executor(action: str, parameters: dict):
    """Your custom execution logic"""
    if action == "fetch_data":
        # Fetch data from API, database, etc.
        return {"data": [1, 2, 3]}
    elif action == "process_data":
        # Process the data
        return {"processed": True}
    else:
        return {"status": "completed"}
```

### 3. 创建计划

```python
steps = [
    {
        "description": "Fetch user data",
        "action": "fetch_data",
        "parameters": {"source": "database"},
        "expected_output": "List of users"
    },
    {
        "description": "Process users",
        "action": "process_data",
        "parameters": {"validation": True},
        "expected_output": "Processed data"
    }
]

plan = planner.create_plan(
    title="Data Processing Pipeline",
    description="Fetch and process user data",
    steps=steps
)
```

### 4. 验证并执行

```python
# Validate
is_valid, warnings = planner.validate_plan(plan)
if warnings:
    print("Warnings:", warnings)

# Approve
planner.approve_plan(plan, approved_by="admin")

# Execute
success, results = planner.execute_plan(plan, my_executor)

# Get summary
summary = planner.get_execution_summary(plan)
print(f"Progress: {summary['progress_percentage']}%")
```

## 主要特性

### 安全验证

自动检测危险操作：

```python
steps = [
    {
        "description": "Delete old files",
        "action": "delete_files",  # ⚠️ Dangerous!
        "parameters": {"path": "/data/old"},
        "safety_check": True,  # System will warn
        "rollback_possible": False  # Cannot undo
    }
]
```

### 干运行模式

无需执行即可进行测试：

```python
success, results = planner.execute_plan(
    plan, 
    my_executor, 
    dry_run=True  # Simulate only
)
```

### 保存和加载计划

持久化计划以便重复使用：

```python
# Save
planner.save_plan(plan, "my_plan.json")

# Load later
loaded_plan = planner.load_plan("my_plan.json")

# Verify integrity
if loaded_plan.verify_integrity():
    planner.execute_plan(loaded_plan, my_executor)
```

### 错误处理

控制错误行为：

```python
success, results = planner.execute_plan(
    plan,
    my_executor,
    stop_on_error=False  # Continue on failures
)

# Check results
for result in results:
    if not result['success']:
        print(f"Step {result['order']} failed: {result['error']}")
```

## 步骤配置

每个步骤都支持以下参数：

```python
{
    "description": str,          # Required: Human-readable description
    "action": str,               # Required: Action identifier
    "parameters": dict,          # Required: Action parameters
    "expected_output": str,      # Required: Expected result
    "safety_check": bool,        # Optional: Enable validation (default: True)
    "rollback_possible": bool,   # Optional: Can be rolled back (default: True)
    "max_retries": int          # Optional: Retry attempts (default: 3)
}
```

## 常见使用场景

### API编排

```python
steps = [
    {
        "description": "Authenticate",
        "action": "api_auth",
        "parameters": {"service": "github"},
        "expected_output": "Auth token"
    },
    {
        "description": "Fetch data",
        "action": "api_fetch",
        "parameters": {"endpoint": "/repos"},
        "expected_output": "Repository list"
    }
]
```

### 数据管道

```python
steps = [
    {
        "description": "Extract data",
        "action": "extract",
        "parameters": {"source": "database"},
        "expected_output": "Raw data"
    },
    {
        "description": "Transform data",
        "action": "transform",
        "parameters": {"rules": ["normalize", "validate"]},
        "expected_output": "Clean data"
    },
    {
        "description": "Load data",
        "action": "load",
        "parameters": {"destination": "warehouse"},
        "expected_output": "Success confirmation"
    }
]
```

### 系统自动化

```python
steps = [
    {
        "description": "Backup database",
        "action": "backup",
        "parameters": {"target": "postgres"},
        "expected_output": "Backup file path",
        "rollback_possible": True
    },
    {
        "description": "Update schema",
        "action": "migrate",
        "parameters": {"version": "2.0"},
        "expected_output": "Migration complete",
        "rollback_possible": True
    },
    {
        "description": "Verify integrity",
        "action": "verify",
        "parameters": {"checks": ["all"]},
        "expected_output": "All checks passed"
    }
]
```

## 最佳实践

### 1. 必须先进行验证

```python
is_valid, warnings = planner.validate_plan(plan)
if not is_valid:
    print("Plan validation failed!")
    for warning in warnings:
        print(f"  - {warning}")
    exit(1)
```

### 使用描述性名称

```python
# Good ✅
{
    "description": "Fetch active users from PostgreSQL production database",
    "action": "fetch_active_users_postgres_prod",
    ...
}

# Bad ❌
{
    "description": "Get data",
    "action": "get",
    ...
}
```

### 标记危险操作

```python
{
    "description": "Delete temporary files older than 30 days",
    "action": "cleanup_temp_files",
    "parameters": {"age_days": 30, "path": "/tmp"},
    "safety_check": True,      # ⚠️ Will trigger warnings
    "rollback_possible": False  # ⚠️ Cannot undo!
}
```

### 使用干运行模式进行测试

```python
# Always test first
success, results = planner.execute_plan(plan, my_executor, dry_run=True)

if success:
    # Now run for real
    success, results = planner.execute_plan(plan, my_executor, dry_run=False)
```

### 优雅地处理错误

```python
def safe_executor(action: str, parameters: dict):
    try:
        result = execute_action(action, parameters)
        return result
    except Exception as e:
        logging.error(f"Failed to execute {action}: {e}")
        raise  # Re-raise to let planner handle it
```

## 高级特性

### 自动批准自动化任务

```python
# Skip manual approval for automated workflows
planner = TaskPlanner(auto_approve=True)
```

### 检查点系统

```python
# Checkpoints are automatically created for rollback-capable steps
# Access checkpoint history
checkpoints = planner.executor.checkpoint_stack
```

### 执行历史记录

```python
# View execution history
history = planner.executor.execution_history
for entry in history:
    print(f"{entry['timestamp']}: {entry['step_id']} - {entry['status']}")
```

### 自定义验证规则

```python
# Add custom validation to SafetyValidator
planner.safety_validator.dangerous_operations.append('my_dangerous_op')
planner.safety_validator.sensitive_paths.append('/my/sensitive/path')
```

## 故障排除

### “执行前必须先批准计划”

```python
# Solution: Approve the plan first
planner.approve_plan(plan, approved_by="admin")
# Or use auto-approve mode
planner = TaskPlanner(auto_approve=True)
```

### 安全验证警告

```python
# Review warnings and ensure operations are intentional
is_valid, warnings = planner.validate_plan(plan)
for warning in warnings:
    print(warning)

# If operations are safe, approve anyway
if is_valid:  # Still valid, just warnings
    planner.approve_plan(plan)
```

### 步骤执行顺序错误

```python
# Ensure order values are sequential
steps[0]['order'] = 1
steps[1]['order'] = 2
steps[2]['order'] = 3
```

## 文件结构

```
task-planner-validator/
├── task_planner.py      # Main library
├── examples.py          # Usage examples
├── test_basic.py        # Test suite
├── README.md            # Full documentation
├── QUICKSTART.md        # Quick start guide
├── API.md              # API reference
├── SKILL.md            # This file
└── LICENSE              # MIT License
```

## 系统要求

- Python 3.8或更高版本
- 无需外部依赖！

## 测试

```bash
# Run basic tests
python test_basic.py

# Run examples
python examples.py

# Both should show "✅ ALL TESTS PASSED"
```

## 获取帮助

- 📖 阅读[README.md]以获取完整文档
- 🚀 查看[QUICKSTART.md]以获取快速使用示例
- 📚 查阅[API.md]以获取完整的API参考
- 💡 浏览[examples.py]以查看实际代码示例
- 🐛 在GitHub上报告问题

## 许可证

MIT许可证 - 详见[LICENSE]文件

## 作者

**cerbug45**
- GitHub: [@cerbug45](https://github.com/cerbug45)

---

⭐ 如果您觉得这个工具有用，请在GitHub上给仓库点赞！