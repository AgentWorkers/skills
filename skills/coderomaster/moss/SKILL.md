---
name: moss-docs
description: Moss语义搜索的文档与功能参考。
  Use for understanding Moss APIs, SDKs, and integration patterns.
metadata:
  author: usemoss
  version: "1.0"
  docs-url: https://docs.usemoss.dev
  mintlify-proj: moss
---

# Moss Agent Skills

## 功能概述

Moss 是一款用于对话式人工智能的实时语义搜索引擎。它支持在浏览器、设备端或云端进行搜索，查询响应时间低于 10 毫秒，并能即时更新索引——无论您的代理程序运行在何处。代理程序无需管理基础设施即可创建索引、嵌入文档、执行语义搜索或混合搜索，以及管理文档的生命周期。该平台负责处理文档的嵌入生成、索引持久化以及可选的云端同步，使代理程序能够专注于检索逻辑而非基础设施的配置。

## 主要功能

### 索引管理

- **创建索引**：使用指定的文档和嵌入模型创建新的语义索引。
- **加载索引**：从持久化存储中加载现有索引以供查询使用。
- **获取索引元数据**：检索特定索引的元数据（如文档数量、使用的模型等）。
- **列出所有索引**：列出项目下的所有索引。
- **删除索引**：删除索引及其所有关联数据。

### 文档操作

- **添加文档**：将文档插入或更新现有索引（可选择是否附加元数据）。
- **获取文档**：通过 ID 检索存储的文档，或获取所有文档。
- **删除文档**：根据 ID 从索引中删除特定文档。

### 搜索与检索

- **语义搜索**：使用自然语言进行查询，并通过向量相似度进行匹配。
- **关键词搜索**：基于 BM25 的关键词匹配技术进行精确匹配。
- **混合搜索**：可配置权重比例，结合语义搜索和关键词搜索结果。
- **元数据过滤**：根据文档元数据（如类别、语言、标签）筛选搜索结果。
- **返回最佳结果**：返回排名前 k 位的匹配文档及其得分。

### 嵌入模型

- **moss-minilm**：专为边缘设备/离线环境设计的快速轻量级模型（默认模型）。
- **moss-mediumlm**：精度更高的模型，适用于对准确性要求较高的场景。

### SDK 方法

| 语言        | 语言        | 描述                                      |
|-------------|-------------|----------------------------------------|
| JavaScript    | Python       | 创建索引的方法                               |
| `createIndex()`    | `create_index()`    | 创建包含文档的索引                         |
| `loadIndex()`    | `load_index()`    | 从存储中加载索引                         |
| `getIndex()`    | `get_index()`    | 获取索引元数据                           |
| `listIndexes()`   | `list_indexes()`   | 列出所有索引                             |
| `deleteIndex()`   | `delete_index()`   | 删除索引                                 |
| `addDocs()`     | `add_docs()`     | 向索引中添加/更新文档                         |
| `getDocs()`     | `get_docs()`     | 获取文档                                 |
| `deleteDocs()`    | `delete_docs()`    | 从索引中删除文档                         |
| `query()`      | `query()`      | 执行语义搜索                             |

### API 操作

所有 REST API 操作都通过 `POST /manage` 路径进行，需要指定 `action` 参数：

- `createIndex`：使用示例文档创建索引。
- `getIndex`：获取单个索引的元数据。
- `listIndexes`：列出项目中的所有索引。
- `deleteIndex`：删除索引及其相关资源。
- `addDocs`：将文档添加到索引中。
- `getDocs`：检索存储的文档。
- `deleteDocs`：根据 ID 删除文档。

## 工作流程

### 基本语义搜索流程

1. 使用项目凭据初始化 MossClient。
2. 调用 `createIndex()` 方法，传入文档和模型（`moss-minilm` 或 `moss-mediumlm`）。
3. 调用 `loadIndex()` 方法准备索引以供查询。
4. 调用 `query()` 方法，传入搜索文本和 `top_k` 参数。
5. 处理返回的文档及其得分结果。

### 混合搜索流程

1. 如上所述创建并加载索引。
2. 调用 `query()` 方法，并设置 `alpha` 参数以平衡语义搜索和关键词搜索的结果。
- `alpha: 1.0` 表示纯语义搜索；`alpha: 0.0` 表示纯关键词搜索；`alpha: 0.6` 表示两者各占 60% 的权重。
- 对于对话式应用，默认设置为以语义搜索为主（权重约为 80%）。

### 文档更新流程

1. 初始化客户端并确保索引存在。
2. 调用 `addDocs()` 方法，传入新文档并设置 `upsert: true` 选项。
- 系统会更新具有相同 ID 的现有文档，并插入新文档。
3. 调用 `deleteDocs()` 方法根据 ID 删除过时的文档。

### 语音代理上下文注入流程

1. 在代理程序启动时初始化 MossClient 并加载索引。
2. 对于每个用户输入的消息，自动向 Moss 发起搜索以获取相关上下文。
3. 在生成响应前将搜索结果注入大型语言模型（LLM）的上下文中。
4. 以基于知识的答案形式返回结果（无工具调用延迟）。

### 离线优先搜索流程

1. 使用本地嵌入模型创建索引。
2. 从本地存储中加载索引。
3. 搜索完全在设备端完成，响应时间低于 10 毫秒。
- 可选择将结果同步到云端以进行备份和共享。

## 集成

### 语音代理框架

- **LiveKit**：通过 `inferedge-moss` SDK 将搜索结果注入语音代理流程。
- **Pipecat**：通过 `pipecat-moss` 包实现管道处理，自动将搜索结果注入代理流程。

### 认证

SDK 需要项目凭据：

- `MOSS_PROJECT_ID`：来自 Moss Portal 的项目标识符。
- `MOSSPROJECT_KEY`：来自 Moss Portal 的项目访问密钥。

```bash
theme={null}
export MOSS_PROJECT_ID=your_project_id
export MOSS_PROJECT_KEY=your_project_key
```

REST API requires headers:

- `x-project-key`: Project access key
- `x-service-version: v1`: API version header
- `projectId` in JSON body

### Package Installation

| Language              | Package           | Install Command               |
| --------------------- | ----------------- | ----------------------------- |
| JavaScript/TypeScript | `@inferedge/moss` | `npm install @inferedge/moss` |
| Python                | `inferedge-moss`  | `pip install inferedge-moss`  |
| Pipecat Integration   | `pipecat-moss`    | `pip install pipecat-moss`    |

### Document Schema

```typescript theme={null}
interface DocumentInfo {
  id: string;      // 必填：唯一标识符
  text: string;      // 必填：用于嵌入和搜索的内容
  metadata?: object;   // 可选：用于过滤的键值对
}
```

### Query Parameters

| Parameter        | Type   | Default | Description                                 |
| ---------------- | ------ | ------- | ------------------------------------------- |
| `indexName`      | string | -       | Target index name (required)                |
| `query`          | string | -       | Natural language search text (required)     |
| `top_k` / `topK` | number | 5       | Max results to return                       |
| `alpha`          | float  | \~0.8   | Hybrid weighting: 0.0=keyword, 1.0=semantic |
| `filters`        | object | -       | Metadata constraints                        |

### Model Selection

| Model           | Use Case                            | Tradeoff          |
| --------------- | ----------------------------------- | ----------------- |
| `moss-minilm`   | Edge, offline, browser, speed-first | Fast, lightweight |
| `moss-mediumlm` | Precision-critical, higher accuracy | Slightly slower   |

### Performance Expectations

- Sub-10ms local queries (hardware-dependent)
- Instant index updates without reindexing entire corpus
- Sync is optional; compute stays on-device
- No infrastructure to manage

### Chunking Best Practices

- Aim for \~200–500 tokens per chunk
- Overlap 10–20% to preserve context
- Normalize whitespace and strip boilerplate

### Common Errors

| Error                      | Cause               | Fix                                          |
| -------------------------- | ------------------- | -------------------------------------------- |
| Unauthorized               | Missing credentials | Set `MOSS_PROJECT_ID` and `MOSS_PROJECT_KEY` |
| Index not found            | Query before create | Call `createIndex()` first                   |
| Index not loaded           | Query before load   | Call `loadIndex()` before `query()`          |
| Missing embeddings runtime | Invalid model       | Use `moss-minilm` or `moss-mediumlm`         |

### Async Pattern

All SDK methods are async - always use `await`:

```typescript theme={null}
// JavaScript
await client.createIndex("faqs", docs, "moss-minilm");
await client.loadIndex("faqs");
const results = await client.query("faqs", "search text", 5);
```

```python theme={null}
# Python
await client.create_index("faqs", docs, "moss-minilm")
await client.load_index("faqs")
results = await client.query("faqs", "search text", top_k=5)
```

---

> 更多文档和导航信息，请参阅：[https://docs.usemoss.dev/llms.txt](https://docs.usemoss.dev/llms.txt)