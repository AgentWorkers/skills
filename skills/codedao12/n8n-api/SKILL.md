---
name: n8n-api
description: 通过 OpenClaw 的公共 REST API 来操作 n8n。该 API 可用于工作流管理、执行以及自动化任务，例如列出、创建、发布、触发或故障排除等。支持自托管的 n8n 以及 n8n Cloud 两种部署方式。
---

# n8n 公共 REST API

当您需要通过编程方式操作 n8n 时，请使用此 API。它涵盖了与用户界面中相同的核心功能：工作流、执行任务、标签、凭证、项目等。

## 可用性
- 免费试用期间，公共 API 不可用。
- 请升级您的计划以启用 API 访问权限。

## 配置

推荐的环境变量（或存储在 `.n8n-api-config` 文件中）：

```bash
export N8N_API_BASE_URL="https://your-instance.app.n8n.cloud/api/v1"  # or http://localhost:5678/api/v1
export N8N_API_KEY="your-api-key-here"
```

在 n8n 的设置 → n8n API → 创建 API 密钥 中生成 API 密钥。

## 认证头

所有请求都需要包含以下认证头：

```
X-N8N-API-KEY: $N8N_API_KEY
```

## 测试环境

API 测试环境仅适用于自行托管的 n8n 实例，并且会使用真实数据。为了安全地进行实验，请使用测试工作流或单独的测试实例。

## 常用操作

### 列出工作流
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_BASE_URL/workflows" \
  | jq '.data[] | {id, name, active}'
```

### 查看工作流详情
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_API_BASE_URL/workflows/{id}"
```

### 激活或停用工作流
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

### 触发 Webhook
```bash
# Production webhook
curl -s -X POST "$N8N_API_BASE_URL/../webhook/{webhook-path}" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# Test webhook
curl -s -X POST "$N8N_API_BASE_URL/../webhook-test/{webhook-path}" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'
```

### 列出执行任务
```bash
# Recent executions
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/executions?limit=10" \
  | jq '.data[] | {id, workflowId, status, startedAt}'

# Failed only
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/executions?status=error&limit=5"
```

### 重试执行任务
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"loadWorkflow":true}' \
  "$N8N_API_BASE_URL/executions/{id}/retry"
```

## 常见操作流程

### 健康检查
- 统计活跃的工作流数量及最近的失败记录：
```bash
ACTIVE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/workflows?active=true" | jq '.data | length')

FAILED=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_API_BASE_URL/executions?status=error&limit=100" \
  | jq '[.data[] | select(.startedAt > (now - 86400 | todate))] | length')

echo "Active workflows: $ACTIVE | Failed (24h): $FAILED"
```

### 调试失败的执行任务
1. 列出失败的执行任务以获取其 ID。
2. 获取执行任务的详细信息并确定出问题的节点。
3. 查看节点参数和输入数据。
4. 根据错误信息提供修复建议。

## 端点索引

完整的端点列表请参见 `assets/n8n-api.endpoints.md` 文件。

## REST 基础知识（可选）
如果您需要复习相关知识，可以参考以下资源：
- KnowledgeOwl：API 使用指南（入门）
- IBM Cloud Learn Hub：API 与 REST API 的概念
- MDN：HTTP 简介

## 注意事项与提示
- n8n 的节点可以在工作流内部调用公共 API。
- Webhook 的 URL 与 API 的 URL 不同，且不需要使用 API 密钥认证头。
- 根据实例的保留策略，执行记录可能会被删除。