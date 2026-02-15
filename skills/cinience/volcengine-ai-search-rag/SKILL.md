---
name: volcengine-ai-search-rag
description: 在 Volcengine AI 堆栈中，提供了检索（Retrieval）和 RAG（Retrieval with Answer Generation）工作流程。这些功能适用于用户需要实现嵌入式搜索、文档索引、Top-k 检索、生成相关答案（Grounding Prompts）或调整搜索相关性（Search Relevance Tuning）的场景。
---

# volcengine-ai-search-rag

实现基于显式索引的检索优先型问答系统，包括检索和知识链接（grounding）两个阶段。

## 执行检查清单

1. 确认语料库的来源及分块策略。
2. 生成嵌入向量并构建/更新索引。
3. 使用过滤器检索前 k 个相关上下文片段。
4. 根据检索到的上下文片段生成带有引用信息的答案。

## 质量标准

- 将检索提示与生成提示分开。
- 保留每个上下文片段的元数据（来源、时间戳、ID）。
- 如果没有找到匹配结果，返回置信度信息及备用路径。

## 参考资料

- `references/sources.md`