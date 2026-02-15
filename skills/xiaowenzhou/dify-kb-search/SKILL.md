---
name: dify-kb-search
description: 在 Dify 知识库（数据集）中搜索，以获取用于 RAG（Retrieval-Augmented Generation）增强型答案的准确上下文信息。
metadata:
  openclaw:
    requires:
      env:
        - DIFY_API_KEY
        - DIFY_BASE_URL
    install:
      - id: python
        kind: node
        package: python3
        bins:
          - python3
      - id: requests
        kind: node
        package: requests
        bins: []
        label: Install Python requests library
commandDispatch: tool
commandTool: exec
commandArgMode: json
---

# Dify知识库搜索技能

🔍 **在Dify知识库中搜索，以获得准确、上下文相关的答案**

此技能使AI代理能够查询Dify数据集，以实现RAG（检索增强生成，Retrieval-Augmented Generation）功能，从而获取上下文相关的信息。非常适合用于知识库问答、文档搜索以及提供上下文相关的AI响应。

![Dify知识库](https://dify.ai/favicon.ico)

## ✨ 特点

- **列出知识库** - 查找所有可用的Dify数据集
- **智能搜索** - 通过混合搜索、语义搜索或关键词搜索来查询数据集
- **自动发现** - 如果未提供ID，会自动查找可用的数据集
- **可配置的结果** - 可调整返回结果的数量（top-k）、搜索方法和重新排序规则
- **错误处理** - 提供友好的错误信息以便调试
- **零编码** - 所有配置均通过环境变量完成

## 🚀 快速入门

### 1. 配置环境变量

在`openclaw.json`中设置：

```json
{
  "env": {
    "vars": {
      "DIFY_API_KEY": "${DIFY_API_KEY}",
      "DIFY_BASE_URL": "https://dify.example.com/v1"
    }
  }
}
```

**环境变量：**

| 变量 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `DIFY_API_KEY` | ✅ 是 | - | 你的Dify API密钥（来自“设置” → “API”） |
| `DIFY_BASE_URL` | ❌ 否 | `http://localhost/v1` | 你的Dify实例基础URL |

### 2. 安装依赖项

```bash
pip3 install requests
```

## 🛠️ 工具

### dify_list

列出你的Dify实例中所有可用的知识库（数据集）。

**调用方式：`dify_list` 工具**

**示例响应：**
```json
{
  "status": "success",
  "count": 2,
  "datasets": [
    {
      "id": "dataset-abc123",
      "name": "Product Documentation",
      "doc_count": 42,
      "description": "All product guides and tutorials"
    },
    {
      "id": "dataset-xyz789",
      "name": "API Reference",
      "doc_count": 156,
      "description": "REST API documentation"
    }
  ]
}
```

**使用方法：**
```json
{}
```

### dify_search

在Dify数据集中搜索相关的上下文片段。

**调用方式：`dify_search` 工具（映射到 `python3 scripts/search.py`）

**参数：**

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `query` | 字符串 | ✅ 是 | - | 搜索查询或问题 |
| `dataset_id` | 字符串 | ❌ 否 | 自动发现 | 要搜索的特定数据集ID |
| `top_k` | 整数 | ❌ 否 | 3 | 返回的结果数量 |
| `search_method` | 字符串 | ❌ 否 | `hybrid_search` | 搜索策略 |
| `reranking_enable` | 布尔值 | ❌ 否 | `false` | 启用重新排序以获得更好的结果 |

**搜索方法：**

- `hybrid_search` - 结合语义搜索和关键词搜索（推荐）
- `semantic_search` - 基于意义的相似性搜索
- `keyword_search` - 精确的关键词匹配

**示例用法：**
```json
{
  "query": "How do I configure OpenClaw?",
  "top_k": 5
}
```

```json
{
  "query": "API authentication methods",
  "dataset_id": "dataset-xyz789",
  "search_method": "semantic_search",
  "reranking_enable": true
}
```

**示例响应：**
```json
{
  "status": "success",
  "query": "How do I configure OpenClaw?",
  "dataset_id": "dataset-abc123",
  "count": 3,
  "results": [
    {
      "content": "To configure OpenClaw, edit the openclaw.json file...",
      "score": 0.8923,
      "title": "Installation Guide",
      "document_id": "doc-001"
    },
    {
      "content": "OpenClaw supports environment variables via...",
      "score": 0.8451,
      "title": "Configuration Options",
      "document_id": "doc-002"
    }
  ]
}
```

## 📋 完整工作流程示例

```json
[
  {
    "tool": "dify_list",
    "parameters": {}
  },
  {
    "tool": "dify_search",
    "parameters": {
      "query": "What are the system requirements?",
      "top_k": 5,
      "search_method": "hybrid_search"
    }
  }
]
```

## 🔧 故障排除

### 常见错误

| 错误 | 解决方案 |
|-------|----------|
| `缺少DIFY_API_KEY` | 在环境变量中设置 `DIFY_API_KEY` |
| `连接被拒绝` | 检查 `DIFY_BASE_URL` 是否正确且可访问 |
| 未找到数据集 | 验证数据集是否存在于你的Dify工作空间中 |
| API请求失败 | 检查网络连接和API密钥权限 |

### 调试模式

手动运行以查看详细错误信息：

```bash
DIFY_API_KEY=your-key python3 scripts/search.py <<< '{"query":"test"}'
```

## 📚 集成技巧

### RAG流程集成

```python
# Example: Use search results in AI response
results = dify_search(query, top_k=5)
context = "\n".join([r["content"] for r in results["results"]])
final_prompt = f"Answer based on context:\n\n{context}\n\nQuestion: {query}"
```

### 多个数据集

要跨多个数据集进行搜索，可以循环遍历它们：

```json
{
  "query": "Find information about authentication",
  "dataset_id": "dataset-api-docs"
}
```

然后分别查询另一个数据集。

## 🔒 安全性

- **切勿直接存储API密钥** - 使用环境变量或`.env`文件
- **定期轮换密钥** - 在Dify设置中生成新的密钥
- **限制访问** - 在可能的情况下限制API密钥的权限

## 📖 实现细节

此技能使用Dify数据集API：

- **列出数据集：`GET /v1/datasets`
- **搜索：`POST /v1/datasets/{id}/retrieve`

有关API的详细文档，请参阅：https://docs.dify.ai/reference/api-reference

## 📝 更新日志

**v1.1.0** (2026-02-08)：
- ✅ 添加了搜索方法选择（混合搜索/语义搜索/关键词搜索）
- ✅ 添加了重新排序支持
- ✅ 自动发现数据集
- ✅ 改进了错误处理
- ✅ 移除了硬编码的URL（完全可配置）
- ✅ 添加了详细的日志记录

**v1.0.0** (2026-02-06)：
- 初始版本
- 基本的列表和搜索功能