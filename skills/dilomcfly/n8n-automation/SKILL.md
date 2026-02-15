---
name: n8n-automation
description: 通过 OpenClaw 的 n8n REST API 来管理 n8n 工作流。当用户需要查询 n8n 工作流、自动化任务、执行情况，或者希望触发、列出、创建、激活或调试 n8n 工作流时，可以使用该 API。该 API 支持自托管的 n8n 实例以及 n8n Cloud 实例。
---

# n8n自动化

通过REST API控制n8n工作流自动化平台。

## 设置

请设置以下环境变量（或将其存储在`.n8n-api-config`文件中）：

```bash
export N8N_API_URL="https://your-instance.app.n8n.cloud/api/v1"  # or http://localhost:5678/api/v1
export N8N_API_KEY="your-api-key-here"
```

生成API密钥：进入n8n设置 → API选项 → 创建API密钥。

## 快速参考

所有请求都需要使用`X-N8N-API-KEY`作为认证头。

### 列出工作流
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/workflows" | jq '.data[] | {id, name, active}'
```

### 获取工作流详情
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/workflows/{id}"
```

### 激活/停用工作流
```bash
# Activate
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}' "$N8N_API_URL/workflows/{id}"

# Deactivate
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": false}' "$N8N_API_URL/workflows/{id}"
```

### 通过Webhook触发工作流
```bash
# Production webhook
curl -s -X POST "$N8N_API_URL/../webhook/{webhook-path}" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Test webhook
curl -s -X POST "$N8N_API_URL/../webhook-test/{webhook-path}" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### 列出执行记录
```bash
# All recent executions
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/executions?limit=10" | jq '.data[] | {id, workflowId, status, startedAt}'

# Failed executions only
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/executions?status=error&limit=5"

# Executions for specific workflow
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/executions?workflowId={id}&limit=10"
```

### 获取执行详情
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/executions/{id}"
```

### 从JSON创建工作流
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow.json "$N8N_API_URL/workflows"
```

### 删除工作流
```bash
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/workflows/{id}"
```

## 常见用法

### 健康检查（定期运行）
- 列出所有活跃的工作流
- 检查最近的执行记录是否有错误
- 报告工作流状态：
```bash
# Count active workflows
ACTIVE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/workflows?active=true" | jq '.data | length')

# Count failed executions (last 24h)
FAILED=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_URL/executions?status=error&limit=100" | jq '[.data[] | select(.startedAt > (now - 86400 | todate))] | length')

echo "Active workflows: $ACTIVE | Failed (24h): $FAILED"
```

### 调试失败的执行
1. 列出失败的执行记录 → 获取执行ID
2. 获取执行详情 → 查找出现问题的节点
3. 检查节点参数和输入数据
4. 根据错误信息提供修复建议

### 工作流摘要
解析工作流JSON数据以获取摘要信息：触发类型、连接的应用程序数量、调度计划等。

## API端点参考

请参阅[references/api-endpoints.md](references/api-endpoints.md)以获取完整的端点文档。

## 提示：
- API密钥在非企业版计划中具有完全访问权限
- 访问频率限制因计划（云服务）而异，或者对于自托管环境可能是无限制的
- Webhook地址与API地址不同（无需携带认证头）
- 可以使用`?active=true`或`?active=false`来过滤工作流列表
- 执行数据可能会根据n8n的保留策略被删除