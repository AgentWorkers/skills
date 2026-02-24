---
name: bailian-knowledgebase-retrieve
description: Bailian KnowledgeBase（由 Alibaba ModelStdio 提供）能够检索托管知识库中已向量化处理的任何专有数据。它为大型语言模型（LLMs）返回多文档形式的、简洁的知识库检索结果。
homepage: https://bailian.console.aliyun.com/cn-beijing?tab=app#/knowledge-base
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY","KNOWLEDGEBASE_ID"]},"primaryEnv":"DASHSCOPE_API_KEY"}}
---
# Bailian KnowledgeBase 检索

这是一个基于向量的托管式知识库，支持 Bailian 嵌入（Embedding）和重新排序（Rerank）API。专为 AI 代理和聊天机器人设计，能够将清晰、相关的内容返回到您的专有数据中心中。

## 检索（Retrieve）

```bash
python3 {baseDir}/scripts/retrieve.py "query"
python3 {baseDir}/scripts/retrieve.py "query" 3
```

## 选项（Options）

- `<count>`：返回的结果数量（默认值：5，最大值：20）
- `<query>`：用于知识库检索的用户查询语句