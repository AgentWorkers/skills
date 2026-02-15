---
name: n8n
description: 通过 API 管理 n8n 工作流和自动化任务。适用于处理 n8n 工作流、执行过程或自动化任务时，包括列出工作流、激活/停用工作流、检查执行状态、手动触发工作流以及调试自动化问题等操作。
---

# n8n 工作流管理

通过 REST API 与 n8n 自动化平台进行交互。

## 设置

**首次设置：**

1. API 密钥必须存储在环境变量中：
```bash
export N8N_API_KEY="your-api-key-here"
```

2. 验证连接是否成功：
```bash
python3 scripts/n8n_api.py list-workflows --pretty
```

为了实现持久化存储，可以将配置添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：
```bash
echo 'export N8N_API_KEY="your-key"' >> ~/.bashrc
```

## 快速参考

### 列出工作流
```bash
python3 scripts/n8n_api.py list-workflows --pretty
python3 scripts/n8n_api.py list-workflows --active true --pretty
```

### 获取工作流详情
```bash
python3 scripts/n8n_api.py get-workflow --id <workflow-id> --pretty
```

### 激活/停用工作流
```bash
python3 scripts/n8n_api.py activate --id <workflow-id>
python3 scripts/n8n_api.py deactivate --id <workflow-id>
```

### 执行工作流
```bash
# List recent executions
python3 scripts/n8n_api.py list-executions --limit 10 --pretty

# Get execution details
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty

# Filter by workflow
python3 scripts/n8n_api.py list-executions --id <workflow-id> --limit 20 --pretty
```

### 手动执行工作流
```bash
# Trigger workflow
python3 scripts/n8n_api.py execute --id <workflow-id>

# With data
python3 scripts/n8n_api.py execute --id <workflow-id> --data '{"key": "value"}'
```

## Python API

用于程序化访问：
```python
from scripts.n8n_api import N8nClient

client = N8nClient()

# List workflows
workflows = client.list_workflows(active=True)

# Get workflow
workflow = client.get_workflow('workflow-id')

# Activate/deactivate
client.activate_workflow('workflow-id')
client.deactivate_workflow('workflow-id')

# Executions
executions = client.list_executions(workflow_id='workflow-id', limit=10)
execution = client.get_execution('execution-id')

# Execute workflow
result = client.execute_workflow('workflow-id', data={'key': 'value'})
```

## 常见任务

### 调试失败的工作流
1. 列出最近失败的执行记录
2. 查看执行详情以找出错误原因
3. 检查工作流配置
4. 如有需要，停用相关工作流

### 监控工作流状态
1. 列出当前正在运行的工作流
2. 查看最近的执行状态
3. 分析错误模式

### 工作流管理
1. 列出所有工作流
2. 查看工作流的活跃/停用状态
3. 根据需要激活或停用工作流
4. 删除旧的工作流

## API 参考

有关详细的 API 文档，请参阅 [references/api.md](references/api.md)。

## 故障排除

**认证错误：**
- 确保已设置 `N8N_API_KEY`：`echo $N8N_API_KEY`
- 在 n8n 用户界面中验证 API 密钥的有效性

**连接错误：**
- 如果使用自定义 URL，请检查 `N8N_BASE_URL` 是否正确

**命令错误：**
- 使用 `--pretty` 标志以获得更易读的输出
- 确保在需要时提供了 `--id` 参数
- 验证 `--data` 参数的 JSON 格式是否正确