---
name: moss-docs
description: Moss语义搜索的文档与功能参考。用于了解Moss的API、SDK以及集成模式。
  Use for understanding Moss APIs, SDKs, and integration patterns.
metadata:
  author: usemoss
  version: "1.0"
  docs-url: https://docs.moss.dev
  mintlify-proj: moss
  primary-credential: MOSS_PROJECT_KEY
  required-env:
    - name: MOSS_PROJECT_ID
      description: Project identifier from the Moss Portal
    - name: MOSS_PROJECT_KEY
      description: Project access key from the Moss Portal (treat as a secret)
---
# Moss Agent技能

## 功能

Moss是一个用于对话式AI的实时语义搜索运行时引擎。它能够在浏览器、设备本地或云端（无论您的代理位于何处）提供低于10毫秒的查询响应和即时索引更新。代理可以创建索引、嵌入文档、执行语义/混合搜索，并管理文档的生命周期，而无需管理基础设施。该平台负责生成嵌入内容、维护索引以及可选的云端同步，使代理能够专注于检索逻辑而非基础设施的配置。

## 技能

### 索引管理

- **创建索引**：使用文档和嵌入模型选择来构建新的语义索引。
- **加载索引**：从持久化存储中加载现有索引以供查询使用。
- **获取索引信息**：检索特定索引的元数据（如文档数量、使用的模型等）。
- **列出索引**：枚举项目下的所有索引。
- **删除索引**：移除索引及其所有关联数据。

### 文档操作

- **添加文档**：将文档插入或更新到现有索引中（可选添加元数据）。
- **获取文档**：通过ID检索存储的文档或获取所有文档。
- **删除文档**：通过ID从索引中删除特定文档。

### 搜索与检索

- **语义搜索**：使用自然语言进行查询，并通过向量相似度进行匹配。
- **关键词搜索**：使用基于BM25的关键词匹配进行精确术语查找。
- **混合搜索**：通过`QueryOptions`（Python SDK）配置混合使用语义搜索和关键词搜索。
- **元数据过滤**：根据文档元数据（类别、语言、标签）筛选结果。
- **返回前K个结果**：返回得分最高的K个匹配文档。

### 嵌入模型

- **moss-minilm**：一种快速、轻量级的模型，专为边缘设备/离线使用优化（默认值）。
- **moss-mediumlm**：一种精度要求较高的模型，性能适中。

### SDK方法

| JavaScript        | Python             | 描述                    |
| ----------------- | ------------------ | ------------------------------ |
| `createIndex()`   | `create_index()`   | 创建索引并添加文档                    |
| `loadIndex()`     | `load_index()`     | 从存储中加载索引                        |
| `getIndex()`      | `get_index()`      | 获取索引元数据                        |
| `listIndexes()`   | `list_indexes()`   | 列出所有索引                        |
| `deleteIndex()`   | `delete_index()`   | 删除索引                          |
| `addDocs()`       | `add_docs()`       | 向索引中添加/更新文档                    |
| `getDocs()`       | `get_docs()`       | 检索文档                          |
| `deleteDocs()`    | `delete_docs()`    | 从索引中删除文档                      |
| `query()`         | `query()`          | 执行语义/混合搜索                      |

### API操作

所有REST API操作都通过`POST /v1/manage`（基础URL：`https://service.usemoss.dev/v1`）进行，需要提供`action`字段：

| 操作            | 目的                                      | 需要的额外字段                          |
| ------------------ | -------------------------------------- | ------------------------------------------- |
| `initUpload`       | 获取用于上传索引数据的预签名URL                   | `indexName`, `modelId`, `docCount`, `dimension`         |
| `startBuild`       | 上传数据后触发索引构建                         | `jobId`                          |
| `getJobStatus`     | 检查异步构建作业的状态                        | `jobId`                          |
| `getIndex`        | 获取单个索引的元数据                         | `indexName`                          |
| `listIndexes`       | 列出项目下的所有索引                         |                                |
| `deleteIndex`       | 删除索引记录及其相关资源                         | `indexName`                          |
| `getIndexUrl`       | 获取已构建索引的下载URL                         | `indexName`                          |
| `addDocs`        | 向现有索引中添加文档                         | `indexName`, `docs`                        |
| `deleteDocs`       | 通过ID删除文档                         | `indexName`, `docIds`                        |
| `getDocs`        | 检索存储的文档（不包括嵌入内容）                   | `indexName`                          |

## 工作流程

### 基本语义搜索工作流程

1. 使用项目凭据初始化MossClient。
2. 调用`createIndex()`方法，传入文档和模型选项（JavaScript中使用`{ modelId: 'moss-minilm' }`；Python中使用`"moss-minilm"`字符串）。
3. 调用`loadIndex()`方法准备索引以供查询。
4. 调用`query()`方法，传入搜索文本和`topK`参数（JavaScript）或`QueryOptions(top_k=...)`（Python）。
5. 处理返回的文档及其得分结果。

### 混合搜索工作流程（Python）

在Python SDK中，可以通过`QueryOptions`配置混合搜索：

1. 如上所述创建并加载索引。
2. 调用`query()`方法，并传入指定`alpha`值的`QueryOptions`对象。
- `alpha=1.0`：纯语义搜索。
- `alpha=0.0`：纯关键词搜索。
- `alpha=0.6`：60/40的比例混合搜索。
- 对于对话式应用，默认采用以语义搜索为主的方式。

### 文档更新工作流程

1. 初始化客户端并确保索引存在。
2. 调用`addDocs()`方法添加新文档（默认情况下会更新现有文档的ID）。
3. 调用`deleteDocs()`方法通过ID删除过时的文档。

### 语音代理上下文注入工作流程

这是一种可选的集成方式，用于语音代理流程——并非该技能的自动行为：

1. 在代理启动时初始化MossClient并加载索引。
2. 在应用程序代码中，对每个用户消息调用`query()`方法以获取相关上下文。
3. 在生成响应之前将搜索结果注入大型语言模型（LLM）的上下文中。
4. 以基于知识的答案进行响应（无工具调用延迟）。

### 离线优先搜索工作流程

1. 使用本地嵌入模型创建索引并加载文档。
2. 从本地存储中加载索引。
3. 查询完全在设备本地进行，延迟低于10毫秒。
4. 可选地将结果同步到云端以进行备份和共享。

## 集成

### 语音代理框架

- **LiveKit**：通过`inferedge-moss` SDK将上下文注入语音代理流程。
- **Pipecat**：通过`pipecat-moss`包处理流程，并自动注入检索结果。

## 上下文

### 认证

SDK需要项目凭据：

- `MOSS_PROJECT_ID`：来自Moss门户的项目标识符。
- `MOSS PROJECT_KEY`：来自Moss门户的项目访问密钥。

```bash
theme={null}
export MOSS_Project_ID=your_project_id
export MOSS PROJECT_KEY=your_project_key
```

REST API requires the following on every request:

- `x-project-key` header: project access key
- `x-service-version: v1` header: API version
- `projectId` field in the JSON body

```
curl -X POST "https://service.usemoss.dev/v1/manage" \
  -H "Content-Type: application/json" \
  -H "x-service-version: v1" \
  -H "x-project-key: moss_access_key_xxxxx" \
  -d '{"action": "listIndexes", "projectId": "project_123"}'
```

### Package Installation

| Language              | Package           | Install Command               |
| --------------------- | ----------------- | ----------------------------- |
| JavaScript/TypeScript | `@inferedge/moss` | `npm install @inferedge/moss` |
| Python                | `inferedge-moss`  | `pip install inferedge-moss`  |
| Pipecat Integration   | `pipecat-moss`    | `pip install pipecat-moss`    |

### Document Schema

```
interface DocumentInfo {
  id: string;        // 必填：唯一标识符
  text: string;      // 必填：要嵌入和搜索的内容
  metadata?: object; // 可选：用于过滤的键值对
}
```

### Query Parameters

| Parameter   | SDK         | Type   | Default  | Description                                  |
| ----------- | ----------- | ------ | -------- | -------------------------------------------- |
| `indexName` | JS + Python | string | —        | Target index name (required)                 |
| `query`     | JS + Python | string | —        | Natural language search text (required)      |
| `topK`      | JS          | number | 5        | Max results to return                        |
| `top_k`     | Python      | int    | 5        | Max results to return                        |
| `alpha`     | Python only | float  | ~0.8     | Hybrid weighting: 0.0=keyword, 1.0=semantic  |
| `filters`   | JS + Python | object | —        | Metadata constraints                         |

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

- Aim for ~200–500 tokens per chunk
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

All SDK methods are async — always use `await`:

```
// JavaScript
import { MossClient, DocumentInfo } from '@inferedge/moss'
const client = new MossClient(process.env.MOSS_PROJECT_ID!, process.env.MOSS_Project_KEY!)
await client.createIndex('faqs', docs, { modelId: 'moss-minilm' })
await client.loadIndex('faqs')
const results = await client.query('faqs', 'search text', { topK: 5 })
```

```
# Python
import os
from inferedge_moss import MossClient, QueryOptions
client = MossClient(os.getenv('MOSS_PROJECT_ID'), os.getenv('MOSSPROJECT_KEY'))
await client.create_index('faqs', docs, 'moss-minilm')
await client.load_index('faqs')
results = await client.query('faqs', 'search text', QueryOptions(top_k=5, alpha=0.6))
```

---

> 有关更多文档和导航信息，请访问：[https://docs.moss.dev/llms.txt](https://docs.moss.dev/llms.txt)