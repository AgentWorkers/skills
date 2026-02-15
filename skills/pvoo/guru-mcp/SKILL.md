---
name: guru-mcp
description: 通过 MCP 访问 Guru 知识库：您可以提出 AI 相关问题、搜索文档、创建草稿以及更新卡片。该工具能够连接到您所有的 Guru 数据源，包括 Slack、Drive、Confluence 和 SharePoint。
homepage: https://www.getguru.com
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["mcporter"],"env":["GURU_API_TOKEN"]}}}
---

# Guru MCP

您可以通过官方的MCP服务器访问Guru知识库。您可以提出由AI驱动的问题、搜索文档、创建文档草稿以及更新卡片内容。

## 主要功能

- **AI驱动的答案**：从知识代理那里获得全面的答案。
- **文档搜索**：在整个知识库中查找卡片和内容。
- **创建草稿**：利用AI工具生成新的卡片草稿。
- **更新卡片**：直接修改现有的卡片。
- **集成外部资源**：通过Guru访问Salesforce、Slack、Google Drive、Confluence和SharePoint。
- **权限管理**：严格遵守现有的Guru权限设置。
- **数据分析**：所有查询都会被记录在AI代理中心。

## 设置流程

### 1. 获取API令牌

1. 登录Guru管理界面，选择“API Tokens”。
2. 创建一个新的API令牌。
3. 记下您的电子邮件地址和令牌值。

### 2. 配置环境

将以下配置添加到`~/.clawdbot/.env`文件中：
```bash
GURU_API_TOKEN=your.email@company.com:your-api-token
```

### 3. 配置mcporter

将以下配置添加到`config/mcporter.json`文件中：
```json
{
  "mcpServers": {
    "guru": {
      "baseUrl": "https://mcp.api.getguru.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GURU_API_TOKEN}"
      }
    }
  }
}
```

### 4. 验证配置

```bash
mcporter list guru
```

## 可用的工具

### `guru_list_knowledgeAgents`

列出您工作空间中的所有知识代理。在使用其他工具之前，请务必先调用此命令以获取代理的ID。
```bash
mcporter call 'guru.guru_list_knowledge_agents()'
```

返回结果：
```json
[
  {"id": "08de66e8-...", "name": "Guru"},
  {"id": "abc123...", "name": "Engineering Docs"}
]
```

### `guru_answer_generation`

从知识代理那里获取AI驱动的答案。适用于诸如“X是什么？”或“我该如何做Y？”之类的具体问题。
```bash
mcporter call 'guru.guru_answer_generation(
  agentId: "YOUR_AGENT_ID",
  question: "How do I submit expenses?"
)'
```

可选参数：
- `collectionIds`：仅搜索特定集合中的内容。
- `sourceIds`：仅搜索来自特定来源的文档。

返回包含来源信息的完整答案。

### `guru_search_documents`

用于查找文档、卡片和资源。适用于诸如“查找关于X的文档”或“我们有关于Y的卡片吗？”之类的查询。
```bash
mcporter call 'guru.guru_search_documents(
  agentId: "YOUR_AGENT_ID",
  query: "onboarding process"
)'
```

返回匹配的文档列表，并附有文档片段。

### `guru_get_card_by_id`

以HTML格式获取卡片的完整内容。
```bash
mcporter call 'guru.guru_get_card_by_id(id: "CARD_ID")'
```

返回卡片的ID、标题和HTML内容。

### `guru_create_draft`

创建一个新的卡片草稿。
```bash
mcporter call 'guru.guru_create_draft(
  title: "New Process Guide",
  content: "<h2>Overview</h2><p>This guide covers...</p>"
)'
```

返回草稿的ID和URL。

### `guru_update_card`

更新现有的卡片。首先使用`guru_get_card_by_id`获取当前卡片内容，然后进行修改。
**注意：**在更新时请保持HTML结构的完整性，避免破坏现有的DOM结构。

## 使用方式

### 提出问题
```bash
# 1. Get agent ID
mcporter call 'guru.guru_list_knowledge_agents()'

# 2. Ask question
mcporter call 'guru.guru_answer_generation(
  agentId: "08de66e8-...",
  question: "What is the PTO policy?"
)'
```

### 查找并阅读卡片
```bash
# 1. Search for cards
mcporter call 'guru.guru_search_documents(
  agentId: "08de66e8-...",
  query: "expense report"
)'

# 2. Get full content
mcporter call 'guru.guru_get_card_by_id(id: "CARD_ID_FROM_SEARCH")'
```

### 创建新文档
```bash
mcporter call 'guru.guru_create_draft(
  title: "API Authentication Guide",
  content: "<h2>Overview</h2><p>This guide explains how to authenticate with our API.</p><h2>Steps</h2><ol><li>Generate API key</li><li>Add to headers</li></ol>"
)'
```

## 选择合适的工具

| 使用场景 | 所需工具 |
|---------|--------|
| “X是什么？” / “我该如何做Y？” | `guru_answer_generation` |
| “查找关于X的文档” | `guru_search_documents` |
| “显示卡片XYZ” | `guru_get_card_by_id` |
| “为X创建新的指南” | `guru_create_draft` |
| “用……更新这张卡片” | `guru_update_card` |

## 令牌格式

`GURU_API_TOKEN`的格式应为`email:token`：
```
your.email@company.com:a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## 注意事项

- 提出的问题会显示在Guru的**AI代理中心**的统计报告中。
- 系统会严格遵循用户的权限设置（用户只能查看他们有权访问的内容）。
- 知识代理可以是针对特定领域的——请根据您的问题选择合适的代理。
- 卡片内容采用HTML格式——在更新时请保持其结构不变。

## 参考资源

- [Guru MCP文档](https://help.getguru.com/docs/connecting-gurus-mcp-server)
- [Guru API参考文档](https://developer.getguru.com)
- [AI代理中心](https://app.getguru.com/ai-agent-center)
- [MCP反馈渠道](https://help.getguru.com/docs/connecting-gurus-mcp-server#feedback)