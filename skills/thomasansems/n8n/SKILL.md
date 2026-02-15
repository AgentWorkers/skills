---
name: n8n
description: 通过 API 管理 n8n 工作流和自动化任务。在处理 n8n 工作流、执行过程或自动化任务时可以使用该功能，包括列出工作流、激活/停用工作流、检查执行状态、手动触发工作流以及调试自动化问题。
metadata: {"openclaw":{"emoji":"\u2699\ufe0f","requires":{"env":["N8N_API_KEY","N8N_BASE_URL"]},"primaryEnv":"N8N_API_KEY"}}
---

# n8n 工作流管理

n8n 平台提供全面的工作流自动化管理功能，包括工作流的创建、测试、执行监控以及性能优化。

## ⚠️ 重要提示：工作流创建规则

**在创建 n8n 工作流时，务必：**

1. ✅ **生成完整的工作流**，包含所有功能节点。
2. ✅ **添加实际的 HTTP 请求节点** 以进行 API 调用（例如 ImageFX、Gemini、Veo、Suno 等）。
3. ✅ **添加代码节点** 以处理数据转换和逻辑操作。
4. ✅ **正确连接所有节点**。
5. ✅ **使用真实的节点类型**（如 n8n-nodes-base.httpRequest、n8n-nodes-base.code、n8n-nodes-base.set）。

**严禁：**
- ❌ 创建仅包含“设置说明”的占位符节点。
- ❌ 仅使用 TODO 注释来生成工作流。
- ❌ 创建需要手动添加节点的不完整工作流。
- ❌ 用纯文本节点替代实际的功能节点。

**示例（正确的工作流）：**
```
Manual Trigger → Set Config → HTTP Request (API call) → Code (parse) → Response
```

**示例（错误的工作流）：**
```
Manual Trigger → Code ("Add HTTP nodes here, configure APIs...")
```

务必构建完整且功能齐全的工作流，确保所有必要的节点都已配置并正确连接。

## 设置

**所需环境变量：**
- `N8N_API_KEY` — 你的 n8n API 密钥（在 n8n 用户界面中的“设置” → “API”中设置）。
- `N8N_BASE_URL` — 你的 n8n 实例 URL。

**通过 OpenClaw 设置配置凭据：**

将以下内容添加到 `~/.config/openclaw/settings.json` 文件中：
```json
{
  "skills": {
    "n8n": {
      "env": {
        "N8N_API_KEY": "your-api-key-here",
        "N8N_BASE_URL": "your-n8n-url-here"
      }
    }
  }
}
```

或者设置为会话级凭据（**不要** 将敏感信息保存在 shell 配置文件中）：
```bash
export N8N_API_KEY="your-api-key-here"
export N8N_BASE_URL="your-n8n-url-here"
```

**验证连接：**
```bash
python3 scripts/n8n_api.py list-workflows --pretty
```

> **安全提示：** **切勿** 将 API 密钥以明文形式保存在 shell 配置文件（如 `~/.bashrc`、`~/.zshrc`）中。请使用 OpenClaw 设置文件或安全的密钥管理工具。

## 快速参考

### 工作流管理

#### 列出工作流
```bash
python3 scripts/n8n_api.py list-workflows --pretty
python3 scripts/n8n_api.py list-workflows --active true --pretty
```

#### 获取工作流详情
```bash
python3 scripts/n8n_api.py get-workflow --id <workflow-id> --pretty
```

#### 创建工作流
```bash
# From JSON file
python3 scripts/n8n_api.py create --from-file workflow.json
```

#### 激活/停用工作流
```bash
python3 scripts/n8n_api.py activate --id <workflow-id>
python3 scripts/n8n_api.py deactivate --id <workflow-id>
```

### 测试与验证

#### 验证工作流结构
```bash
# Validate existing workflow
python3 scripts/n8n_tester.py validate --id <workflow-id>

# Validate from file
python3 scripts/n8n_tester.py validate --file workflow.json --pretty

# Generate validation report
python3 scripts/n8n_tester.py report --id <workflow-id>
```

#### 干运行测试
```bash
# Test with data
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data '{"email": "test@example.com"}'

# Test with data file
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data-file test-data.json

# Full test report (validation + dry run)
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data-file test.json --report
```

#### 测试套件
```bash
# Run multiple test cases
python3 scripts/n8n_tester.py test-suite --id <workflow-id> --test-suite test-cases.json
```

### 执行监控

#### 列出执行记录
```bash
# Recent executions (all workflows)
python3 scripts/n8n_api.py list-executions --limit 10 --pretty

# Specific workflow executions
python3 scripts/n8n_api.py list-executions --id <workflow-id> --limit 20 --pretty
```

#### 获取执行详情
```bash
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty
```

#### 手动执行
```bash
# Trigger workflow
python3 scripts/n8n_api.py execute --id <workflow-id>

# Execute with data
python3 scripts/n8n_api.py execute --id <workflow-id> --data '{"key": "value"}'
```

### 性能优化

#### 分析性能
```bash
# Full performance analysis
python3 scripts/n8n_optimizer.py analyze --id <workflow-id> --pretty

# Analyze specific period
python3 scripts/n8n_optimizer.py analyze --id <workflow-id> --days 30 --pretty
```

#### 获取优化建议
```bash
# Priority-ranked suggestions
python3 scripts/n8n_optimizer.py suggest --id <workflow-id> --pretty
```

#### 生成优化报告
```bash
# Human-readable report with metrics, bottlenecks, and suggestions
python3 scripts/n8n_optimizer.py report --id <workflow-id>
```

#### 获取工作流统计信息
```bash
# Execution statistics
python3 scripts/n8n_api.py stats --id <workflow-id> --days 7 --pretty
```

## Python API

### 基本用法
```python
from scripts.n8n_api import N8nClient

client = N8nClient()

# List workflows
workflows = client.list_workflows(active=True)

# Get workflow
workflow = client.get_workflow('workflow-id')

# Create workflow
new_workflow = client.create_workflow({
    'name': 'My Workflow',
    'nodes': [...],
    'connections': {...}
})

# Activate/deactivate
client.activate_workflow('workflow-id')
client.deactivate_workflow('workflow-id')

# Executions
executions = client.list_executions(workflow_id='workflow-id', limit=10)
execution = client.get_execution('execution-id')

# Execute workflow
result = client.execute_workflow('workflow-id', data={'key': 'value'})
```

### 验证与测试
```python
from scripts.n8n_api import N8nClient
from scripts.n8n_tester import WorkflowTester

client = N8nClient()
tester = WorkflowTester(client)

# Validate workflow
validation = tester.validate_workflow(workflow_id='123')
print(f"Valid: {validation['valid']}")
print(f"Errors: {validation['errors']}")
print(f"Warnings: {validation['warnings']}")

# Dry run
result = tester.dry_run(
    workflow_id='123',
    test_data={'email': 'test@example.com'}
)
print(f"Status: {result['status']}")

# Test suite
test_cases = [
    {'name': 'Test 1', 'input': {...}, 'expected': {...}},
    {'name': 'Test 2', 'input': {...}, 'expected': {...}}
]
results = tester.test_suite('123', test_cases)
print(f"Passed: {results['passed']}/{results['total_tests']}")

# Generate report
report = tester.generate_test_report(validation, result)
print(report)
```

### 性能优化
```python
from scripts.n8n_optimizer import WorkflowOptimizer

optimizer = WorkflowOptimizer()

# Analyze performance
analysis = optimizer.analyze_performance('workflow-id', days=7)
print(f"Performance Score: {analysis['performance_score']}/100")
print(f"Health: {analysis['execution_metrics']['health']}")

# Get suggestions
suggestions = optimizer.suggest_optimizations('workflow-id')
print(f"Priority Actions: {len(suggestions['priority_actions'])}")
print(f"Quick Wins: {len(suggestions['quick_wins'])}")

# Generate report
report = optimizer.generate_optimization_report(analysis)
print(report)
```

## 常见工作流

### 1. 验证和测试工作流
```bash
# Validate workflow structure
python3 scripts/n8n_tester.py validate --id <workflow-id> --pretty

# Test with sample data
python3 scripts/n8n_tester.py dry-run --id <workflow-id> \
  --data '{"email": "test@example.com", "name": "Test User"}'

# If tests pass, activate
python3 scripts/n8n_api.py activate --id <workflow-id>
```

### 2. 调试失败的工作流
```bash
# Check recent executions
python3 scripts/n8n_api.py list-executions --id <workflow-id> --limit 10 --pretty

# Get specific execution details
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty

# Validate workflow structure
python3 scripts/n8n_tester.py validate --id <workflow-id>

# Generate test report
python3 scripts/n8n_tester.py report --id <workflow-id>

# Check for optimization issues
python3 scripts/n8n_optimizer.py report --id <workflow-id>
```

### 3. 优化工作流性能
```bash
# Analyze current performance
python3 scripts/n8n_optimizer.py analyze --id <workflow-id> --days 30 --pretty

# Get actionable suggestions
python3 scripts/n8n_optimizer.py suggest --id <workflow-id> --pretty

# Generate comprehensive report
python3 scripts/n8n_optimizer.py report --id <workflow-id>

# Review execution statistics
python3 scripts/n8n_api.py stats --id <workflow-id> --days 30 --pretty

# Test optimizations with dry run
python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data-file test-data.json
```

### 4. 监控工作流运行状态
```bash
# Check active workflows
python3 scripts/n8n_api.py list-workflows --active true --pretty

# Review recent execution status
python3 scripts/n8n_api.py list-executions --limit 20 --pretty

# Get statistics for each critical workflow
python3 scripts/n8n_api.py stats --id <workflow-id> --pretty

# Generate health reports
python3 scripts/n8n_optimizer.py report --id <workflow-id>
```

## 验证检查

测试模块执行全面的验证：

### 结构验证
- ✓ 必需字段齐全（节点、连接）
- ✓ 所有节点都有名称和类型
- ✓ 连接目标存在
- ✓ 无断开的节点（警告）

### 配置验证
- ✓ 需要凭据的节点已配置
- ✓ 必需的参数已设置
- ✓ HTTP 节点有 URL
- ✓ Webhook 节点有路径
- ✓ Email 节点有内容

### 流程验证
- ✓ 工作流包含触发节点
- ✓ 执行流程正确
- ✓ 无循环依赖
- ✓ 有结束节点

## 优化分析

优化器从多个维度进行分析：

### 执行指标
- 总执行次数
- 成功/失败率
- 运行状态（优秀/良好/一般/较差）
- 错误模式

### 性能指标
- 节点数量和复杂性
- 连接方式
- 耗时操作（API 调用、数据库查询）
- 并行执行机会

### 瓶颈检测
- 顺序执行的耗时操作
- 高失败率
- 缺乏错误处理
- 速率限制问题

### 优化建议
- **并行执行：** 确定可以同时运行的节点。
- **缓存：** 建议对重复的 API 调用进行缓存。
- **批量处理：** 对于大型数据集建议使用批量处理。
- **错误处理：** 添加错误恢复机制。
- **降低复杂性：** 分解复杂的工作流。
- **设置超时：** 配置执行时间限制。

## 性能评分

工作流会根据以下指标获得性能评分（0-100 分）：

- **成功率：** 成功率越高越好（权重 50%）。
- **复杂性：** 复杂度越低越好（权重 30%）。
- **瓶颈：** 瓶颈越少越好（严重问题扣 20 分，高问题扣 10 分，一般问题扣 5 分）。
- **优化措施：** 实施了最佳实践（每项加 5 分）。

评分解读：
- **90-100 分：** 优秀 - 优化得很好。
- **70-89 分：** 良好 - 需要进一步改进。
- **50-69 分：** 一般 - 建议进行优化。
- **0-49 分：** 较差 - 存在重大问题。

## 最佳实践

### 开发
1. **规划结构：** 在构建之前设计工作流节点和连接。
2. **先进行验证：** 部署前务必进行验证。
3. **彻底测试：** 使用多个测试用例进行干运行测试。
4. **错误处理：** 添加错误处理节点以确保可靠性。
5. **文档说明：** 在代码节点中注释复杂逻辑。

### 测试
1. **创建真实的数据文件：** 生成符合实际的测试数据。
2. **测试边界条件：** 测试边界情况和错误情况。
3. **逐步测试：** 每添加一个节点都进行测试。
4. **回归测试：** 修改后重新测试。
5. **模拟生产环境：** 使用与生产环境相似的测试环境。

### 部署
1. **先进行非生产环境测试：** 先在非生产环境中部署工作流。
2. **逐步推广：** 初始阶段使用有限的流量进行测试。
3. **密切监控：** 仔细观察首次执行情况。
4. **快速回滚：** 准备好在出现问题时立即停用工作流。
5. **记录变更：** 保留修改日志。

### 优化
1. **基准测试：** 在修改前记录性能数据。
2. **一次只进行一项优化：** 分析每次优化的效果。
3. **测量结果：** 比较修改前后的指标。
4. **定期审查：** 定期进行性能优化审查。
5. **成本意识：** 监控 API 使用情况和执行成本。

### 维护
1. **定期检查：** 每周查看执行统计信息。
2. **错误分析：** 调查失败原因。
3. **性能监控：** 跟踪执行时间。
4. **定期更新凭据：** 定期更新凭据。
5. **清理：** 存档或删除不再使用的工作流。

## 故障排除

### 认证错误
```
Error: N8N_API_KEY not found in environment
```
**解决方法：** 设置环境变量：
```bash
export N8N_API_KEY="your-api-key"
```

### 连接错误
```
Error: HTTP 401: Unauthorized
```
**解决方法：**
1. 确认 API 密钥正确。
2. 检查 `N8N_BASE_URL` 是否设置正确。
3. 确保 n8n 已启用 API 访问功能。

### 验证错误
```
Validation failed: Node missing 'name' field
```
**解决方法：** 检查工作流的 JSON 结构，确保所有必需字段都存在。

### 执行超时
```
Status: timeout - Execution did not complete
```
**解决方法：**
1. 检查工作流中是否存在无限循环。
2. 减小测试数据集的大小。
3. 优化耗时操作。
4. 在工作流设置中设置执行超时。

### 速率限制
```
Error: HTTP 429: Too Many Requests
```
**解决方法：**
1. 在 API 调用之间添加等待节点。
2. 实现指数级退避策略。
3. 使用批量处理。
4. 检查 API 的速率限制。

### 凭据丢失
```
Warning: Node 'HTTP_Request' may require credentials
```
**解决方法：**
1. 在 n8n 用户界面中配置凭据。
2. 为节点分配凭据。
3. 在激活前测试连接是否正常。

## 文件结构
```
~/clawd/skills/n8n/
├── SKILL.md                    # This file
├── scripts/
│   ├── n8n_api.py             # Core API client (extended)
│   ├── n8n_tester.py          # Testing & validation
│   └── n8n_optimizer.py       # Performance optimization
└── references/
    └── api.md                 # n8n API reference
```

## API 参考

有关 n8n REST API 的详细文档，请参阅 [references/api.md](references/api.md) 或访问：
https://docs.n8n.io/api/

## 支持

**文档：**
- n8n 官方文档：https://docs.n8n.io
- n8n 社区论坛：https://community.n8n.io
- n8n API 参考：https://docs.n8n.io/api/

**调试：**
1. 使用验证工具：`python3 scripts/n8n_tester.py validate --id <workflow-id>`
2. 查看执行日志：`python3 scripts/n8n_api.py get-execution --id <execution-id>`
3. 查看优化报告：`python3 scripts/n8n_optimizer.py report --id <workflow-id>`
4. 进行干运行测试：`python3 scripts/n8n_tester.py dry-run --id <workflow-id> --data-file test.json`