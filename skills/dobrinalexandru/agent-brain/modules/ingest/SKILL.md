# 知识摄取 📥

**状态:** ✅ 正在运行 | **模块:** ingest | **所属部分:** Agent Brain（代理大脑）

该模块负责从外部来源摄取知识，包括URL、文章、论文和文档等，并对这些知识进行读取、处理和存储。

## 功能概述

- **获取内容（Fetch）**：从指定URL获取数据。
- **提取关键信息（Extract）**：从获取的内容中解析出核心概念、主要观点、支持性论据以及事实/数据。
- **存储数据（Store）**：将提取的信息以便于检索的格式保存起来。
- **建立知识链接（Link）**：将新获取的知识与现有的知识库进行关联。

## 使用场景

### 阅读论文
```
"Read https://paulgraham.com/ammers.html"
"Ingest this article: [URL]"
"Learn from this: [URL]"
```

### 处理文档
```
"Process this PDF"
"Extract knowledge from [URL]"
"Index this page"
```

### 构建知识库
```
"What do you know about X?"
"Summarize what you ingested from Y"
"Link these concepts"

## Processing Pipeline

```
1. 从URL获取内容。
2. 提取以下信息：
   - 核心概念
   - 主要观点
   - 支持性论据
   - 事实/数据
   - 来源元数据
3. 将提取的信息存储到知识库中。
4. 将新知识与现有知识建立关联。
5. 使这些信息能够被检索到。

示例代码：
```json
{
  "source": "https://paulgham.com/article.html",
  "title": "文章标题",
  "author": "Paul Graham",
  "date": "2026-01",
  "concepts": ["创业", "想法", "执行"],
  "key_points": ["观点1", "观点2"],
  "facts": ["事实A", "事实B"],
  "linked_concepts": ["现有概念"],
  "raw_summary": "..."
}
```

示例命令：
```
Ingest: [URL]
Learn from: [URL]
Read this: [URL]
"What did you learn from [source]?"
"What do you know about [topic]?"
```

示例代码（用于存储处理后的数据）：
```json
{
  "sources": [],
  "concepts": {},
  "extracted_knowledge": []
}
```

## 持续学习机制

- 标记需要重新检查的资料来源。
- 当有新内容时进行更新。
- 建立相关概念之间的链接。
- 构建一个相互关联的知识图谱。