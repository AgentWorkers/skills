---
name: alchemyst-mcp
description: 每当您需要使用 Alchemyst AI MCP 服务器（地址：mcp.getalchemystai.com/mcp/sse）来存储、检索、搜索或查看持久化的数据时，请使用此技能。适用场景包括：在不同会话之间“记住”或“恢复”信息、存储文档/笔记/决策以供后续查阅、搜索项目相关知识，以及任何涉及从 Alchemyst 的数据存储系统中读取或写入数据的操作。
---
# Alchemyst AI MCP — 上下文引擎

## 概述

Alchemyst AI 是一个用于 AI 应用的 **持久化上下文层**。它将文档、对话和结构化知识存储在外部，以便在需要时跨会话、工具和环境进行检索。

MCP 服务器作为一个 SSE（Server-Sent Events）端点提供接口：

```
https://mcp.getalchemystai.com/mcp/sse
```

身份验证通过 **Bearer 令牌**（您的 Alchemyst API 密钥）在请求头中传递来完成。

---

## 先决条件

| 条件 | 详情 |
|---|---|
| **Alchemyst API 密钥** | 从 [platform.getalchemystai.com](https://platform.getalchemystai.com) 获取 |
| **兼容 MCP 的客户端** | Claude Desktop、Cursor、VS Code + MCP 扩展程序或自定义代理 |
| **传输协议** | SSE (`https://mcp.getalchemystai.com/mcp/sse`) |
| **认证头** | `Authorization: Bearer <YOUR_API_KEY>` |

---

## Claude Desktop 配置

在您的 `claude_desktop_config.json` 中添加以下内容：

```json
{
  "mcpServers": {
    "alchemyst": {
      "url": "https://mcp.getalchemystai.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_ALCHEMYST_API_KEY"
      }
    }
  }
}
```

> **切勿泄露您的 API 密钥。** 在生产环境中使用环境变量或密钥管理工具。

---

## 工具

该服务器提供了以下四种工具：

---

### `alchemyst_ai_search_context` — 语义搜索

使用自然语言查询在上下文存储中搜索。返回按语义相似度排序的文档。

**使用场景：** 在回答可能依赖于存储知识的问题的之前；无需手动查找即可检索之前的决策、文档或指令。

#### 输入格式

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `query` | `string` | ✅ | 自然语言搜索查询 |
| `similarity_threshold` | `number` (0–1) | ✅ | 最大相似度阈值——返回得分等于或低于此阈值的结果 |
| `minimum_similarity_threshold` | `number` (0–1) | ✅ | 最小相似度阈值——低于此得分的结果将被排除 |
| `scope` | `"internal"` \| `"external"` | ❌ | 搜索范围；默认为 `"internal"` |
| `metadata` | `object` \| `null` | ❌ | 可选的文件元数据过滤条件；默认为 `null` |

**元数据过滤字段**（如果提供了元数据对象，则所有字段均为必填）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `fileName` | `string` | 要过滤的文件名 |
| `fileSize` | `number` | 文件大小（字节） |
| `fileType` | `string` | MIME 类型 |
| `lastModified` | `string` | ISO 8601 日期时间字符串 |
| `groupName` | `string[]` | 标签组；默认为 `["default"]` |

> **注意：** 在搜索工具中，元数据字段名使用 **驼峰式命名法**（`fileName`、`fileSize`、`fileType`、`lastModified`、`groupName`）。

#### 阈值建议

- `similarity_threshold: 0.8` + `minimum_similarity_threshold: 0.5` → 结果精确且严格 |
- `similarity_threshold: 0.7` + `minimum_similarity_threshold: 0.4` → 结果更广泛且更宽松 |
- 始终将 `minimum_similarity_threshold` 设置得低于 `similarity_threshold`。

#### 示例调用

```json
{
  "query": "authentication token expiry policy",
  "similarity_threshold": 0.8,
  "minimum_similarity_threshold": 0.5,
  "scope": "internal",
  "metadata": null
}
```

---

### `alchemyst_ai_add_context` — 存储上下文

将一个或多个文档添加到 Alchemyst 上下文存储中。

**使用场景：** 保存项目需求、架构决策、入职文档、会议记录、代码规范或任何希望持久化并稍后检索的知识。

#### 输入格式

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `user_id` | `string` | ✅ | 提交上下文的用户的唯一标识符 |
| `organization_id` | `string` \| `null` | ✅ | 组织 ID；如不适用则传递 `null` |
| `documents` | `array` | ✅ | 文档对象数组，每个对象包含 `content` 字段（以及可选的额外字符串字段） |
| `source` | `string` | ✅ | 描述上下文来源的标签（例如，`"project.auth.decisions"`） |
| `context_type` | `"resource"` \| `"conversation"` \| `"instruction"` | ✅ | 要存储的上下文类型 |
| `metadata` | `object` | ✅ | 文件元数据——所有四个字段均为必填 |
| `scope` | `"internal"` \| `"external"` | ❌ | 默认为 `"internal"` |

**元数据字段**（所有字段均为必填；注意这里的命名法为 **蛇形命名法**）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `file_name` | `string` | 文件或文档的名称 |
| `doc_type` | `string` | MIME 类型或文档类型（例如，`"text/markdown"`） |
| `modalities` | `string[]` | 存在的模态（例如，`["text"]`、`["text", "image"]`） |
| `size` | `number` | 大小（字节） |

> ⚠️ **关键点：** `add_context` 使用 **蛇形命名法** 的元数据字段（`file_name`、`doc_type`、`size`），而 `search_context` 使用 **驼峰式命名法**（`fileName`、`fileType`、`fileSize`）。请根据所使用的工具选择正确的命名法。

#### 上下文类型

| 值 | 用途 |
|---|---|
| `"resource"` | 文件、文档、参考资料、代码 |
| `"conversation"` | 聊天记录、会议记录、支持帖子 |
| `"instruction"` | 持久性规则、规范、代理指令 |

#### 来源命名规范

使用点分隔的层次化标签。这有助于审计：

```
project.auth.decisions
team.onboarding.v2
agent.instructions.sales
```

#### 示例调用

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz",
  "documents": [
    { "content": "All API routes use JWT auth with 15-minute token expiry." }
  ],
  "source": "project.auth.decisions",
  "context_type": "resource",
  "scope": "internal",
  "metadata": {
    "file_name": "auth-decisions.md",
    "doc_type": "text/markdown",
    "modalities": ["text"],
    "size": 64
  }
}
```

---

### `alchemyst_ai_context_mcp_view_context` — 查看上下文摘要

检索给定用户和组织的所有存储上下文的摘要。

**使用场景：** 审计上下文存储中的内容、调试缺失的上下文，或在会话前检查可用的知识。

#### 输入格式

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `user_id` | `string` | ✅ | 要获取上下文的用户 ID |
| `organization_id` | `string` \| `null` | ✅ | 组织 ID；如不适用则传递 `null` |

#### 示例调用

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz"
}
```

---

### `alchemyst_ai_context_mcp_view_docs` — 查看存储的文档

检索给定用户和组织的存储文档。

**使用场景：** 列出存储的文档、验证内容是否正确保存，或在决定添加新内容之前浏览可用的知识。

#### 输入格式

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `user_id` | `string` | ✅ | 要获取文档的用户 ID |
| `organization_id` | `string` \| `null` | ✅ | 组织 ID；如不适用则传递 `null` |

#### 示例调用

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz"
}
```

---

## 工作流程模式

### 存储 → 搜索（基本模式）

1. 调用 `alchemyst_ai_add_context` 存储文档
2. 稍后，使用相关查询调用 `alchemyst_ai_search_context` 来检索文档
3. 将检索到的内容作为上下文注入到提示中

### 添加前的审计

1. 调用 `alchemyst_ai_context_mcp_view_docs` 检查已存储的内容
2. 仅当知识不存在时才调用 `alchemyst_ai_add_context`
3. 这可以避免上下文重复并保持存储的整洁

### 回答前的检索

在回答任何可能依赖于项目特定知识的问题之前，先调用 `alchemyst_ai_search_context`。建议主动执行此操作——不要等到用户明确要求“检查上下文存储”。

---

## 最佳实践

**始终填充元数据。** `add_context` 需要 `metadata` 对象——每次都要填写所有四个字段。缺少元数据会显著降低检索质量。

**分块处理大文档。** 在添加之前将大文件分解为逻辑上独立的章节。每个部分都应该有独立的意义。不要在句子或概念中间分割文件。

**为来源添加版本号。** 当内容更新时，使用版本号标签（例如 `project.arch.v1`、`project.arch.v2`），而不是重新添加到相同的来源。这样可以保留历史记录。

**存储前进行搜索。** 在调用 `add_context` 之前先进行搜索，以检查是否存在相似的内容。避免累积重复项。

**注意驼峰式/蛇形命名法的区别。** 不同工具之间的元数据格式有所不同——这是当前 API 的一个特性。在构建请求体时请仔细检查字段名：
- `add_context` → `file_name`、`doc_type`、`size`（蛇形命名法）
- `search_context` → `fileName`、`fileType`、`fileSize`（驼峰式命名法）

**明确传递 `organization_id`。** 即使没有组织，也请传递 `null` 而不是省略该字段——因为这是规范所要求的。

---

## 错误处理

| 状态 | 含义 | 处理方式 |
|---|---|---|
| 400 | 请求错误 | 检查必填字段；验证 `documents` 是否为数组；检查元数据格式 |
| 401 | 身份验证失败 | 验证 API 密钥；确认请求头中是否包含 `Authorization: Bearer <key>` |
| 403 | 权限被拒绝 | 检查组织/用户的权限 |
| 404 | 未找到 | 确认 `user_id` 或 `organization_id` 是否有效 |
| 422 | 实体无法处理 | 架构验证失败——检查字段类型、必填字段以及驼峰式/蛇形命名法的使用 |
| 429 | 请求速率限制 | 按指数级延迟后重试 |
| 500+ | 服务器错误 | 重试两次并增加延迟；查看 [status.getalchemystai.com](https://status.getalchemystai.com) |

---

## 资源

- 文档：[getalchemystai.com/docs](https://getalchemystai.com/docs)
- MCP 概述：[getalchemystai.com/docs/mcps/introduction](https://getalchemystai.com/docs/mcps/introduction)
- Claude Desktop 设置：[getalchemystai.com/docs/mcps/claude-desktop](https://getalchemystai.com/docs/mcps/claude-desktop)
- API 状态：[status.getalchemystai.com](https://status.getalchemystai.com)
- Python SDK：`pip install alchemystai`
- 支持：anuran@getalchemystai.com