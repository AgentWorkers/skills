---
name: n8n-hub
description: 一个集中式的 n8n 中心，用于设计可靠的流程（具备幂等性、重试机制以及 HITL 功能），并通过公共 REST API 来执行这些流程。该中心支持流程规划、生成 JSON 格式的输出结果，以及执行诸如列表显示、发布、调试等生命周期相关操作。
---

# n8n Hub

该技能整合了两个核心功能：
1) **设计**：规划可靠的工作流程，并可选择生成 `workflow.json` 文件。
2) **操作**：通过公共 REST API 来管理和执行工作流程。

## 可用性
- 免费试用计划不支持公共 API 访问，需要升级计划才能使用 API。

## 配置

建议设置环境变量（或将其存储在 `.n8n-api-config` 文件中）：

```bash
export N8N_API_BASE_URL="https://your-instance.app.n8n.cloud/api/v1"  # or http://localhost:5678/api/v1
export N8N_API_KEY="your-api-key-here"
```

请在 n8n 设置 → n8n API → 创建 API 密钥中生成 API 密钥。

## 适用场景
- 当您需要构建具有幂等性、重试机制、日志记录以及审核队列功能的工作流程时。
- 当您需要可导入的 `workflow.json` 文件以及运行手册模板时。
- 当您希望通过 API 来列出、发布、停用或调试工作流程时。

## 不适用场景
- 当您仅需要纯代码自动化功能（不依赖 n8n 时）。
- 当您希望绕过安全控制或隐藏审计痕迹时。

## 输入参数
**必填**：
- 触发类型 + 时间表/时区
- 成功标准及目标地址（电子邮件/云端存储/数据库）

**可选**：
- 现有的工作流程 JSON 文件
- 示例数据/记录
- 去重键（用于确保运行结果的唯一性）

## 输出结果
- 默认输出：工作流程的设计规范（包括节点、数据契约、故障处理方式等）
- 根据请求：`workflow.json` 文件 + `workflow-lab.md` 文件（来自 `assets/workflow-lab.md`）

## 认证请求头
所有请求必须包含以下认证信息：

```
X-N8N-API-KEY: $N8N_API_KEY
```

## 快速操作（API）
### 列出所有工作流程
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_BASE_URL/workflows" \
  | jq '.data[] | {id, name, active}'
```

### 查看工作流程详情
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_BASE_URL/workflows/{id}"
```

### 激活或停用工作流程
```bash
# Activate (publish)
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"versionId":"","name":"","description":""}' \
  "$N8N_API_BASE_URL/workflows/{id}/activate"

# Deactivate
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/workflows/{id}/deactivate"
```

### 设置 Webhook 触发器
```bash
curl -s -X POST "$N8N_API_BASE_URL/../webhook/{webhook-path}" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'
```

### 列出所有执行记录
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/executions?limit=10" \
  | jq '.data[] | {id, workflowId, status, startedAt}'
```

### 重试执行任务
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"loadWorkflow":true}' \
  "$N8N_API_BASE_URL/executions/{id}/retry"
```

## 设计工作流程的步骤：
1. 确认触发类型和时间表/时区。
2. 定义输入参数、输出结果及验证规则。
3. 选择去重键以确保每次运行的唯一性。
4. 添加可观测性信息（如运行 ID、日志记录、状态信息）。
5. 设置重试策略和错误处理机制。
6. 将失败任务发送到审核队列。
7. 设置安全机制以防止故障被忽略。

## 端点列表
完整的端点列表请参见 `assets/endpoints-api.md`。

## 注意事项与提示：
- API 测试环境仅适用于自托管的 n8n 服务器，并使用真实数据。
- n8n API 节点可以在工作流程内部调用公共 API。
- Webhook URL 不需要包含 API 密钥。
- 执行数据可以通过配置保留策略进行筛选和删除。