---
name: orchata-rag
description: 知识管理及RAG（Research, Access, and Governance）平台，具备基于树的文档索引功能。利用该技能，可通过MCP（Knowledge Management Platform）工具搜索、浏览和管理Orchata知识库中的内容。
metadata:
  version: 1.0.0
  author: Orchata AI
---

# Orchata 技能指南

本文档介绍了如何高效使用 Orchata——这是一个基于树形索引的 RAG（检索增强生成）平台。请将此文档加载到您的环境中，以便与 Orchata 知识库进行交互。

## 什么是 Orchata？

Orchata 是一个知识管理平台，具有以下特点：

- **将文档组织到“空间”中**：这些空间是包含相关内容的逻辑容器。
- **使用基于树的索引**：文档被解析为包含章节、摘要和页面范围的分层结构。
- **提供语义搜索**：可以使用自然语言查询找到相关内容。
- **支持 MCP 工具**：AI 助手可以直接管理和查询知识库。

## 核心概念

### 空间（Spaces）

**空间** 是用于存放相关文档的容器。可以将其视为具有语义搜索功能的文件夹。

- 每个空间都有一个 `名称`、`描述` 和可选的 `图标`。
- `描述` 被 `smart_query` 功能用来推荐相关的空间。
- 空间可以被归档（即软删除）。

### 文档（Documents）

**文档** 是空间内的内容。支持的格式包括：
- PDF（基于文本的文档和通过 OCR 扫描的文档）
- Word 文档（.docx）
- Excel 电子表格（.xlsx）
- PowerPoint 演示文稿（.pptx）
- Markdown 文件（.md）
- 普通文本文件（.txt）
- 图片（PNG、JPG 等）

**文档状态：**

| 状态 | 描述 |
| ------ | ----------- |
| `PENDING` | 已上传，等待处理 |
| `PROCESSING` | 正在解析和索引 |
| `COMPLETED` | 可以查询 |
| `FAILED` | 处理过程中出现错误 |

**注意：** 仅查询状态为 `COMPLETED` 的文档。其他状态的文档将不会返回结果。

### 文档树（Document Trees）

文档被索引成 **分层树结构**：

- 每棵树都有表示章节/部分的节点。
- 节点包含：`title`（标题）、`summary`（摘要）、`startPage`（起始页码）、`endPage`（结束页码）、`textContent`（文本内容）。
- 这种结构使得大型文档的导航更加方便。

### 查询（Queries）

有两种类型的查询：

1. **`query_spaces`**：使用基于树的推理来搜索文档内容。
2. **`smart_query`**：发现与查询相关的空间。

---

## MCP 工具参考

### 空间管理（Space Management）

#### `list_spaces`

列出组织中的所有知识空间。

**参数：**
- `page`（数字，可选）：页码（默认值：1）
- `pageSize`（数字，可选）：每页显示的条目数量（默认值：10）
- `status`（字符串，可选）：按 `active`、`archived` 或 `all` 进行过滤

---

#### `manage_space`

创建、获取、更新或删除空间。

**参数：**
- `action`（字符串，必填）：`create`、`get`、`update` 或 `delete`
- `id`（字符串）：空间 ID（获取/更新/删除时必需）
- `name`（字符串）：空间名称（创建时必需）
- `description`（字符串，可选）：空间描述
- `icon`（字符串，可选）：图标名称。默认值为 “folder”
- `slug`（字符串，可选）：适合 URL 的标识符
- `isArchived`（布尔值，可选）：归档状态（用于更新）

**有效的图标：**
`folder`、`book`、`file-text`、`database`、`package`、`archive`、`briefcase`、`inbox`、`layers`、`box`

如果提供了无效的图标，工具会返回一个错误，并列出有效的选项。

---

### 文档管理（Document Management）

#### `list_documents`

列出空间中的文档。

**参数：**
- `spaceId`（字符串，必需）：空间 ID
- `page`（数字，可选）：页码
- `pageSize`（数字，可选）：每页显示的条目数量（最大值：100）
- `status`（字符串，可选）：按状态过滤。可选值：`pending`、`processing`、`completed`、`failed` 或 `all`。省略该参数将返回所有文档。

**注意：** 状态值不区分大小写（`completed` 和 `COMPLETED` 都有效）。

---

#### `save_document`

上传或更新文档（单个或批量）。

**单个文档：**

**批量上传：**

---

#### `get_document`

通过 ID 或文件名获取文档内容。返回处理后的 Markdown 文本。

**参数：**
- `spaceId`（字符串，必需）：空间 ID；或使用 `*` 来搜索所有空间（需要提供文件名）
- `id`（字符串，可选）：文档 ID
- `filename`（字符串，可选）：文件名

**注意：**
- 必须提供 `id` 或 `filename` 中的一个。
- 如果知道文件名但不知道空间名称，可以使用 `spaceId="*"` 来搜索所有空间。
- 对于已完成的文档，返回提取的 Markdown 文本（而不是原始的 PDF 二进制文件）。
- 使用 `*` 时，响应中会包含文档所在的 `spaceId`。

---

#### `update_document`

更新文档内容或元数据。

**参数：**
- `spaceId`（字符串，必需）：空间 ID
- `id`（字符串，必需）：文档 ID
- `content`（字符串，可选）：新内容
- `metadata`（对象，可选）：自定义键值对

---

#### `delete_document`

永久删除文档。

---

### 查询工具（Query Tools）

#### `query_spaces`

使用基于树的推理在一个或多个空间中搜索文档。

**参数：**
- `query`（字符串，必需）：自然语言搜索查询
- `spaceIds`（字符串或数组，可选）：要搜索的空间 ID。省略或使用 `*` 来搜索所有空间
- `topK`（数字，可选）：最大返回结果数量（默认值：10）
- `compact`（布尔值，可选）：是否使用紧凑格式（默认值：false）。详见下文 **何时使用紧凑格式**。

**何时使用紧凑格式：**

| 模式 | 适用场景 | 返回内容 |
| ---- | ----------- | ------------ |
| `compact=false`（默认）**大多数查询**。当您需要文档的实际数据、事实、数字、日期或详细信息时。** | 包含完整结果、文档元数据、树结构、页面范围和全部内容。 |
| `compact=true` | 在需要了解哪些文档相关（而不需要具体内容）时。** | 返回最少的结果：仅包含内容片段、源文件名和评分。 |

**经验法则：** 默认使用 `compact=false`。仅在浏览/调查时且不需要具体内容时使用 `compact=true`。

**紧凑格式下的响应：**

---

#### `smart_query`

使用 LLM（大型语言模型）推理来发现与查询相关的空间。

**参数：**
- `query`（字符串，必需）：用于查找相关空间的查询
- `maxSpaces`（数字，可选）：返回的最大空间数量（默认值：5）

**响应：**

---

**使用场景：** 当不知道从哪个空间开始搜索时，先使用 `smart_query` 来发现相关空间，然后使用这些空间 ID 来执行 `query_spaces`。

### 树结构探索工具（Tree Structure Exploration Tools）

这些工具允许您探索索引文档的分层结构。

#### `get_document_tree`

获取文档的树结构，显示章节、摘要和页面范围。

**参数：**
- `spaceId`（字符串，必需）：空间 ID
- `documentId`（字符串，必需）：文档 ID

**响应：**

---

**使用场景：** 在深入查看特定章节之前，先使用此功能了解文档的结构。

---

#### `get_tree_node`

获取特定树节点/部分的完整文本内容。

**参数：**
- `documentId`（字符串，必需）：文档 ID
- `nodeId`（字符串，必需）：树结构中的节点 ID

**响应：**

---

## 工作流程模式（Workflow Patterns）

### 模式 1：搜索信息（默认方法）

**对于大多数问题，只需调用一次 `query_spaces` 即可**。在尝试多步骤工作流程之前，请先从这里开始。

**如果需要缩小搜索范围：**

---

**如果您真的不知道存在哪些空间：**

---

> **避免过度搜索**。多步骤工作流程（`smart_query` -> `query_spaces` -> `get_document_tree` -> `get_tree_node`）很少是必要的。对于大多数问题，一次 `query_spaces` 调用即可直接得到答案。只有在结果不足时才需要进一步使用树结构探索。

### 模式 2：查找特定数据**

当需要查找特定的事实、数字、日期、名称或详细信息时：

**直接查询即可——只需一次调用：**

---

默认的 `compact=false` 会返回包含文档元数据的完整内容，因此您可以一步获取所需的数据。**不要** 在数据查找时使用 `compact=true`，因为它会省略所需的详细信息。

### 模式 3：浏览大型文档**

当需要导航大型文档的结构时：

1. **获取文档结构：**

2. **从节点标题和摘要中识别相关章节**

3. **阅读特定章节：**

---

### 模式 4：添加新内容**

在向知识库中添加文档时：

1. **找到或创建合适的空间：**

2. **上传内容：**

3. **等待处理**（状态会从 `PENDING` 变为 `PROCESSING` 再变为 `COMPLETED`）

4. **验证是否已完成：**

---

## `manage_space` - 有效图标

在创建或更新空间时，可以使用以下图标之一：

- `folder`（默认）
- `book`
- `file-text`
- `database`
- `package`
- `archive`
- `briefcase`
- `inbox`
- `layers`
- `box`

如果提供了无效的图标，工具会返回一个错误信息，并列出有效的选项。

---

## `list_documents` - 状态参数

`status` 参数接受以下值（不区分大小写）：

- `"all"`：返回所有状态的文档（COMPLETED、FAILED、PENDING、PROCESSING）
- `"completed"`：仅返回已成功处理的文档
- `"failed"`：仅返回处理失败的文档（包含 `errorMessage` 字段）
- `"pending"`：返回等待处理的文档
- `"processing"`：返回正在处理的文档

状态为 `FAILED` 的文档会包含一个 `errorMessage` 字段，说明处理过程中出现了什么问题。

---

## `save_document` - 处理流程

文档是异步处理的：

1. `save_document` 会立即返回 `status="PROCESSING"` 的状态。
2. 后台任务会生成文档的嵌入信息并对其进行索引（通常需要 1-3 秒）。
3. 当索引完成后，状态会变为 `"COMPLETED"`。
4. 文档可以通过 `query_spaces` 进行搜索。

**检查完成状态：**

- 使用 `get_document` 来检查特定文档的状态。
- 使用 `list_documents` 且 `status="processing"` 来查看所有正在处理的文档。
- 使用 `list_documents` 且 `status="failed"` 来查看所有处理失败的文档。

**示例：**

---

## `get_tree_node` - 内容可用性

`get_tree_node` 可能会返回 `"No text content cached for this node"`（此节点没有缓存文本内容）。这种情况发生在以下情况：

- 没有关联文本内容的结构/组织节点
- 作为树结构中章节标题的节点

**这是正常现象。**

**要读取实际的文档内容：**

- 使用 `get_document` 来获取完整的处理后的 Markdown 文本。
- 使用 `query_spaces` 来搜索并获取相关的内容片段。

通过 `get_document_tree` 可以始终获取文档的结构，包括章节和页面范围。

## 最佳实践（Best Practices）

### 应该做的（What to Do）

- **从一次 `query_spaces` 调用开始**——通常一步即可得到答案。
- **对于大多数查询，使用 `compact=false`（默认设置）**——这样可以获取完整的内容和上下文。
- **在查询之前检查文档状态**——只有状态为 `COMPLETED` 的文档才能被搜索。
- **使用描述性强的查询**——自然语言查询效果最佳。
- **对于大型文档，使用树结构工具**——通过结构进行导航，而不是阅读所有内容。
- **编写详细的空间描述**——这些描述会被 `smart_query` 用于推荐相关空间。

### 不应该做的（What not to Do）

- **不要过度搜索**——当一次 `query_spaces` 调用就足够时，避免使用多步骤工作流程（`smart_query` -> `query_spaces` -> `get_document_tree` -> `get_tree_node`）。
- **不要在数据查找时使用 `compact=true`——它会省略所需的详细信息；仅在需要广泛搜索时使用。
- **不要查询 `PENDING`/`PROCESSING` 状态的文档**——这些文档不会返回结果。
- **不要使用过短的查询**——更多的上下文有助于获得更好的搜索结果。
- **上传新文档后不要忘记检查处理状态**。

---

## 错误处理（Error Handling）

常见错误及其解决方法：

| 错误 | 原因 | 解决方法 |
| ----- | ----- | -------- |
| “Document not found” | 文档 ID 错误或无法访问 | 使用 `list_documents` 验证文档 ID |
| “Space not found” | 文档 ID 错误或空间已被归档 | 使用 `list_spaces` 查找有效的空间 ID |
| 空搜索结果 | 文档未完成处理或没有匹配项 | 检查文档状态；尝试使用更宽泛的查询 |
| “Tree not found” | 文档使用向量索引或未处理 | 检查文档的状态是否为 `COMPLETED` |
| “Invalid icon” | 图标名称不在允许的列表中 | 使用以下图标之一：folder、book、file-text、database、package、archive、briefcase、inbox、layers、box |
| “No text content cached” | 树节点没有缓存文本内容 | 对于结构节点，这是正常现象；使用 `get_document` 来获取完整内容 |

### 故障排除提示（Troubleshooting Tips）

**如果 `save_document` 失败：**

1. 使用 `manage_space with action="get" id="..."` 验证空间是否存在。
2. 确保内容是有效的文本/Markdown 格式。
3. 检查空间是否已被归档。

**如果 `list_documents` 返回 0 个结果：**

1. 尝试使用 `status="all"` 或完全省略 `status` 参数。
2. 使用 `list_spaces` 验证 `spaceId` 是否正确。
3. 检查文档是否仍在处理中（状态是否为 `processing`）。

**如果 `get_tree_node` 返回无内容：**

- 有些节点是结构性的节点，没有缓存文本内容。
- 使用 `get_document` 来获取完整的处理后的文档文本。
- 或者使用 `query_spaces` 来搜索特定内容。

---

## 快速参考（Quick Reference）

| 任务 | 工具 | 示例 |
| ---- | ---- | ------- |
| 列出所有空间 | `list_spaces` | `list_spaces with status="active"` |
| 创建空间 | `manage_space` | `manage_space with action="create" name="Docs"` |
| 列出文档 | `list_documents` | `list_documents with spaceId="..."` |
| 上传内容 | `save_document` | `save_document with spaceId="..." content="..."` |
| 获取文档文本 | `get_document` | `get_document with spaceId="..." id="..."` |
| 搜索内容 | `query_spaces` | `query_spaces with query="..."` |
| 查找相关空间 | `smart_query` | `smart_query with query="..."` |
| 查看文档结构 | `get_document_tree` | `get_document_tree with spaceId="..." documentId="..."` |
| 阅读章节 | `get_tree_node` | `get_tree_node with documentId="..." nodeId="..."` |