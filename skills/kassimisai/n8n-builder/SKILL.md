---
name: n8n-builder
description: 这是一个专业的 n8n 工作流构建工具，能够通过 n8n 的 REST API 以编程方式创建、部署和管理 n8n 工作流。适用于需要创建 n8n 工作流、自动化任务、构建自动化流程、通过 n8n 连接服务或管理现有 n8n 工作流的场景。该工具支持处理 Webhook 流、定时任务、AI 代理、数据库同步、条件逻辑、错误处理以及任何 n8n 节点配置。
---

# n8n 工作流构建器

## 设置

需要两个环境变量：
- `N8N_URL` — n8n 实例的 URL（例如：`https://your-n8n.example.com`）
- `N8N_API_KEY` — n8n API 密钥（在“设置” → “API” → “创建 API 密钥”中获取）

## 工作流创建流程

1. **理解自动化需求**：明确触发方式（Webhook/计划任务/手动触发）、数据来源、处理逻辑、输出结果以及错误处理方式。
2. **设计工作流 JSON**：根据 `references/workflow-schema.md` 中的架构构建有效的工作流 JSON 文件。可以参考 `references/workflow-patterns.md` 中提供的模板。
3. **通过 API 部署工作流**：使用 `scripts/n8n-api.sh create <文件名>` 命令，或将 JSON 数据通过管道传递给 `scripts/n8n-api.sh create-stdin` 命令进行部署。
4. **激活工作流**：对于基于触发器的工作流，使用 `scripts/n8n-api.sh activate <工作流 ID>` 命令进行激活。
5. **验证工作流**：使用 `scripts/n8n-api.sh list` 命令查看已部署的工作流列表。

## API 脚本参考

```bash
# List all workflows
scripts/n8n-api.sh list

# Create workflow from JSON file
scripts/n8n-api.sh create /tmp/workflow.json

# Create from stdin
echo '{"name":"Test",...}' | scripts/n8n-api.sh create-stdin

# Get, activate, deactivate, delete, execute
scripts/n8n-api.sh get <id>
scripts/n8n-api.sh activate <id>
scripts/n8n-api.sh deactivate <id>
scripts/n8n-api.sh delete <id>
scripts/n8n-api.sh execute <id>

# List credentials and tags
scripts/n8n-api.sh credentials
scripts/n8n-api.sh tags
```

## 构建工作流 JSON

每个工作流都需要包含以下内容：
- `name`（工作流名称）
- `nodes[]`（节点数组）
- `connections{}`（连接信息）

每个节点需要包含以下内容：
- `id`（节点 ID）
- `name`（节点名称）
- `type`（节点类型）
- `typeVersion`（节点版本）
- `position`（节点在工作流中的位置）
- `parameters`（节点参数）

连接信息使用源节点的显示名称作为键，将输出结果映射到目标节点。

有关完整的架构、节点类型和表达式语法，请参阅 `references/workflow-schema.md`；
有关完整的工作流示例（Webhook、计划任务、AI 代理、数据库同步、错误处理等），请参阅 `references/workflow-patterns.md`。

## 重要规则：

- **务必在设置中设置 `"executionOrder": "v1"`**。
- **工作流内的节点名称必须唯一**。
- **节点 ID 也必须唯一**，建议使用描述性的名称，例如 `webhook1`、`code1` 等。
- **节点的位置应从 `[250, 300]` 开始，水平间距约为 200 像素**。
- **IF 节点** 有两个输出：索引 0 表示条件为真，索引 1 表示条件为假。
- **对于基于 Webhook 的工作流**，如果 `responseMode` 为 `responseNode`，则需要添加 `respondToWebhook` 节点。
- **在激活工作流之前，确保 n8n 中已配置相应的凭据**（使用 `scripts/n8n-api.sh credentials` 命令进行检查）。
- **在激活前进行测试**：对于手动触发的工作流，可以使用 `scripts/n8n-api.sh execute <ID>` 命令进行测试。
- **对于涉及高风险操作的 HTTP/API 节点，建议将 `continueOnFail` 设置为 `true`，以便在失败后继续执行后续步骤并检查错误。

## 常见房地产相关的工作流示例：

- **潜在客户信息收集**：通过 Webhook 收集信息 → 验证数据 → 去重 → 存储到数据库 → 通知相关人员（Slack/SMS）。
- **回电跟进**：根据计划任务查询数据库中的已完成通话记录 → 根据结果发送 SMS 或电子邮件。
- **持续营销活动**：根据计划任务按阶段查询潜在客户 → 发送相应的电子邮件或短信。
- **CRM 数据同步**：通过 Webhook 将数据传输到 HubSpot/Salesforce 并更新内部数据库。
- **房产信息提醒**：根据计划任务抓取房产列表 → 筛选新信息 → 通知相关人员。
- **智能分类**：通过 Webhook 将潜在客户信息传递给 AI 代理进行分类 → 将客户分配到相应的工作流程中。