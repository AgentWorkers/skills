---
name: ragflow
description: 通用 Ragflow API 客户端，用于 RAG（Retrieval, Adaptation, and Generation）操作。支持创建数据集、上传文档以及对知识库执行聊天式查询。同时支持与自托管的 RAG 平台进行集成。
version: 1.0.2
author: Ania
env:
  RAGFLOW_URL:
    description: Ragflow instance URL (e.g., https://rag.example.com)
    required: true
  RAGFLOW_API_KEY:
    description: Ragflow API key (use least-privilege key, can manage datasets/upload files)
    required: true
metadata:
  clawdbot:
    emoji: "📚"
    requires:
      bins: ["node"]
---

# Ragflow API 客户端

这是一个通用的 Ragflow 客户端，用于使用自托管的 RAG（Retrieval-Augmented Generation，检索增强生成）平台。

## 主要功能

- **数据集管理**：创建、列出和删除知识库
- **文档上传**：上传文件或文本内容
- **聊天查询**：对数据集执行 RAG 查询
- **数据块管理**：触发解析操作并列出数据块

## 使用方法

```bash
# List datasets
node {baseDir}/scripts/ragflow.js datasets

# Create dataset
node {baseDir}/scripts/ragflow.js create-dataset --name "My Knowledge Base"

# Upload document
node {baseDir}/scripts/ragflow.js upload --dataset DATASET_ID --file article.md

# Chat query
node {baseDir}/scripts/ragflow.js chat --dataset DATASET_ID --query "What is stroke?"

# List documents in dataset
node {baseDir}/scripts/ragflow.js documents --dataset DATASET_ID
```

## 配置

在您的 `.env` 文件中设置环境变量：

```bash
RAGFLOW_URL=https://your-ragflow-instance.com
RAGFLOW_API_KEY=your-api-key
```

## API 接口

该客户端支持 Ragflow 的 REST API 接口：

- `GET /api/v1/datasets` — 列出数据集
- `POST /api/v1/datasets` — 创建数据集
- `DELETE /api/v1/datasets/{id}` — 删除数据集
- `POST /api/v1/datasets/{id}/documents` — 上传文档
- `POST /api/v1/datasets/{id}/chunks` — 触发解析操作
- `POST /api/v1/datasets/{id}/retrieval` — 执行 RAG 查询

完整的 API 文档请参阅：https://ragflow.io/docs

## 使用示例

```javascript
// Programmatic usage
const ragflow = require('{baseDir}/lib/api.js');

// Upload and parse
await ragflow.uploadDocument(datasetId, './article.md', { filename: 'article.md' });
await ragflow.triggerParsing(datasetId, [documentId]);

// Query
const answer = await ragflow.chat(datasetId, 'What are the stroke guidelines?');
```