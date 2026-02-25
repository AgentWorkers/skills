---
name: ragie-rag
description: |
  Execute Retrieval-Augmented Generation (RAG) using Ragie.ai.
  Use this skill whenever the user wants to:
  - Search their knowledge base
  - Ask questions about uploaded documents
  - Upload documents to Ragie
  - Retrieve context from Ragie
  - Perform grounded answering using stored documents
  - List, check status, or delete Ragie documents

  This skill manages the full Ragie.ai API lifecycle including ingestion,
  retrieval, and grounded answer construction.
metadata:
{
    "openclaw":
      {
        "requires":
          {
            "bins": ["python3"],
            "env": ["RAGIE_API_KEY"],
            "python": ["requests", "python-dotenv"]
          },
        "credentials":
          {
            "primary": "RAGIE_API_KEY",
            "description": "API key from https://app.ragie.ai"
          }
      }
  }
---

# Ragie.ai RAG 技能（基于 OpenClaw 优化）

该技能利用 Ragie.ai 作为 RAG（Retrieval-Augmented Question Answering，检索增强型问答）的后端，实现基于事实的问答功能。

Ragie 负责以下任务：
- 文档分块处理
- 文本嵌入
- 向量索引
- 数据检索
- 可选的重排序功能

代理（agent）则负责：
- 决定何时开始数据摄入
- 触发数据检索
- 构建问题提示
- 生成最终答案

---

# 核心原则
1. 未经检索，绝不给出任何答案。
2. 绝不编造检索结果中不存在的信息。
3. 在引用具体事实时，必须标注文档名称。
4. 如果检索结果中没有任何相关内容，应明确说明：“当前知识库中不存在该信息。”
5. 最终答案中不得泄露 API 密钥或原始 API 请求数据。

---

# 确定性工作流程

## 情况 A：用户提供文件或 URL
如果用户提供了：
- 一个文件
- 一个文档路径
- 一个 PDF 文件或 URL 链接

则执行以下步骤：
1. 开始数据摄入：
   ```bash
   python `skills/scripts/ingest.py` --file <path> --name "<document_name>"
   ```
   或
   ```bash
   python `skills/scripts/ingest.py` --url "<url>" --name "<document_name>"
   ```

2. 获取返回的 `document_id`。
3. 检查文档状态：
   ```bash
   python `skills/scripts/manage.py` status --id <document_id>
   ```
   重复此步骤，直到文档状态变为 `ready`。

4. 进入检索阶段（情况 C）。

---

## 情况 B：用户请求文档管理
- 列出所有文档：
   ```bash
python `skills/scripts/manage.py` list
```

- 检查文档状态：
   ```bash
python `skills/scripts/manage.py` status --id <document_id>
```

- 删除文档：
   ```bash
python `skills/scripts/manage.py` delete --id <document_id>
```

将结构化结果返回给用户。

---

## 情况 C：检索（基于事实的问答）
执行以下操作：
```bash
python `skills/scripts/retrieve.py` \
  --query "<user_question>" \
  --top-k 6 \
  --rerank
```

可选参数：
- `--partition <名称>`：用于划分数据分区
- `--filter '{"key":"value"}`：用于设置过滤条件

---

# 检索输出格式
预期输出格式如下：
```json
[
  {
    "text": "...",
    "score": 0.87,
    "document_name": "Policy Handbook",
    "document_id": "doc_abc123"
  }
]
```

---

# 问题提示的构建
在完成检索后：
1. 提取所有文本片段。
2. 使用指定的分隔符将这些片段连接起来。
3. 构建问题提示：
```
SYSTEM:
You are a helpful assistant.
Answer using ONLY the context provided below.
If the context does not contain the answer, say:
"I don't have that information in the current knowledge base."

CONTEXT:
[chunk 1 text]
---
[chunk 2 text]
---
...

USER QUESTION:
{original user question}
```

4. 生成最终答案。
5. 在引用具体信息时，必须标注文档名称。

---

# 输出规范
最终答案必须满足以下要求：
- 仅基于检索到的数据生成；
- 对于事实性内容，必须标注文档名称；
- 避免编造信息；
- 避免透露内部处理细节；
- 不得泄露 API 密钥或原始检索结果；
- 明确说明信息是否缺失。

如果检索结果为空：
```
I don't have that information in the current knowledge base.
```

---

# API 参考
基础 URL：
```
https://api.ragie.ai
```

| 操作                | 方法                | API 端点                          |
|------------------|------------------|----------------------------------|
| 归入文件              | POST                | /documents                         |
| 归入 URL              | POST                | /documents/url                        |
| 检索文档片段          | POST                | /retrievals                        |
| 列出所有文档          | GET                | /documents                         |
| 获取文档详情          | GET                | /documents/{id}                        |
| 删除文档              | DELETE               | /documents/{id}                        |

---

# 错误处理
| HTTP 状态码 | 错误原因                | 处理措施                          |
|-----------|------------------|----------------------------------|
| 404       | 文档未找到             | 重新验证 `document_id`                    |
| 422       | 请求数据无效             | 验证请求格式                        |
| 429       | 请求频率受限             | 请稍后重试                         |
| 5xx       | 服务器错误             | 重试或检查 Ragie 的运行状态                   |

如果数据摄入失败：
- 明确报告错误原因，并停止后续操作。
如果检索失败：
- 重试一次；
- 如果仍然失败，通知用户。

---

# 决策规则总结
1. 如果用户上传了文件，则先进行数据摄入，待数据准备就绪后再进行检索。
2. 如果用户提出问题，立即开始检索。
3. 如果检索结果为空，应说明知识库中缺乏相关内容。
4. 除非明确禁用，否则始终使用重排序功能。
5. 未经检索，绝不给出任何答案。

---

# 高级用法
- 使用 `filter` 参数来缩小检索范围。
- 通过 `partition` 参数区分不同租户的数据。
- 仅在时间相关性重要的情况下使用 `recency_bias`（时间相关性权重）。
- 根据查询的复杂性调整 `top_k`（返回的文档数量）。

---

# 安全性
- API 密钥必须从环境变量中获取。
- 禁止将 `.env` 文件提交到代码仓库中。
- 不要记录敏感的请求头部信息。

---

# 总结
该技能具备以下特点：
- 数据摄入和检索过程具有确定性；
- 严格遵循基于事实的问答原则；
- 完整管理 Ragie 的生命周期；
- 提供安全、可靠的 RAG（检索增强型问答）功能。

技能介绍结束。