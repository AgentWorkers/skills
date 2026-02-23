# 本地任务运行器

该功能提供了一种在主机上本地执行 Node.js 代码片段或完整脚本的机制。
当无法使用子代理（subagent）或使用子代理效率低下时，这是**默认的执行方式**。

## 目的

- **替代子代理**：对于简单的任务，可以直接使用该功能来运行代码，而无需创建完整的子代理。
- **安全性**：能够隔离执行逻辑，处理清理工作，并强制执行超时。
- **便捷性**：无需手动管理文件（无需执行 `write`、`exec` 和 `rm` 等操作）。

## 使用方法

当您需要执行计算、检查系统状态或运行实用工具脚本时，请按照以下步骤操作：

1. 将 Node.js 代码转换为字符串格式。
2. 调用 `run_task` 函数（或通过命令行界面执行）并传入代码。

### 命令行界面

```bash
# Execute a task
node skills/local-task-runner/index.js run --code "console.log('Hello World')"

# Execute with timeout (ms)
node skills/local-task-runner/index.js run --code "while(true){}" --timeout 5000
```

### 响应格式

成功：
```
[TASK: <id>] Completed in 123ms
--- STDOUT ---
...
```

错误：
```
[TASK: <id>] Failed in 123ms
Error: ...
--- STDERR ---
...
```