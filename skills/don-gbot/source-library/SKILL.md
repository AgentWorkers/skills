---
name: source-library
description: 这是一个可搜索的知识库，能够捕获并关联用户分享的所有内容。当用户分享任何URL（文章、推文、帖子、仓库、视频或论文）时，系统会自动触发更新。该知识库会保存结构化的摘要，包括关键观点、引用内容、分析结果、标签以及内容更新的时间记录。它还能实现来源之间的关联、冲突检测，并管理用户的阅读队列。触发更新的场景包括：分享的URL、用户查询的“参考资料库”、“我读过的内容”、“查找相关文章”、“回忆我何时分享过某内容”等。请注意：该系统不适用于一般的网络浏览、书签管理，也不适用于仅获取页面内容而无需保存的情况。
allowed-tools: "Bash(node:*)"
compatibility: >
  Requires Node.js 18+. Uses local markdown search for retrieval.
  No API keys needed. No external dependencies. Works on Linux/macOS.
metadata:
  author: DaDefiDon
  version: 2.0.0
  category: knowledge-management
  tags: [sources, research, knowledge-base, cross-reference]
---
# 源代码库（Source Library）

这是一个基于用户分享的所有内容的持久化、可搜索的知识库。它不是一个书签管理工具，而是一个具备关联映射、冲突检测和内容时效性管理功能的跨引用知识管理系统。

## 快速入门

1. 运行 `node scripts/source-library.js setup` 命令以创建所需目录。
2. 在聊天中分享任何 URL，系统会自动处理并保存该内容。
3. 使用 `node scripts/source-library.js search "查询内容"` 来查找之前的相关资源。

## 自动触发机制

当用户分享 **任何 URL** 时，系统会自动执行以下操作：

1. **先进行搜索**：使用本地搜索功能查找相关的现有资源，并展示具体的关联关系。
2. **结合上下文进行分析**：将新资源与现有的知识体系结合进行讨论。
3. **有针对性地保存内容**：使用 ````bash
   node scripts/source-library.js save --name "Title" --url "https://..." --author "Name" --type "article" --tags "topic1, topic2" --claims "Claim 1. Claim 2." --analysis "Why this matters" --context "How it came up"
   ```` 代码块来保存资源信息。
4. 确保每个保存的条目在数月后仍然具有参考价值，无需重新阅读原始内容。

## 命令参考

所有命令均通过 `node scripts/source-library.js <命令>` 来执行：

| 命令          | 描述                                      |
|-----------------|--------------------------------------------|
| `setup`        | 创建目录并显示首次使用的欢迎信息                   |
| `save --name "..." --url "..." [--author --type --tags --summary --claims --analysis --context --slug --related --decay --date --force]` | 保存资源                         |
| `list [--type tweet] [--tag crypto] [--decay]` | 根据可选条件列出资源                         |
| `search "查询内容" [--limit 10]` | 根据相关性对本地资源摘要进行搜索                   |
| `stats`        | 显示库的统计信息（总数、类型、标签、磁盘使用情况）           |
| `connections [--clusters\|--orphans]` | 显示资源之间的关联关系                         |
| `conflicts`      | 通过情感分析检测内容中的矛盾之处                   |
| `queue add "url" [--note "..."]` | 将 URL 添加到阅读队列                         |
| `queue list`       | 显示队列中的所有项目                         |
| `queue next`       | 显示队列中最旧的未处理项目                         |
| `queue done "url-or-index"` | 从队列中移除项目                         |
| `teach "主题" [--limit 20]` | 从相关资源中提取并整合知识                         |
| `import file.json`     | 从 JSON 文件（包含完整对象或 URL 列表）批量导入资源           |

## 资源格式

每个资源的存储路径为 `life/source/{slug}/summary.md`：

```markdown
# Title

**Source:** URL
**Author:** Name (@handle)
**Date:** YYYY-MM-DD
**Type:** tweet|thread|article|repo|video|paper
**Tags:** comma-separated
**Decay:** fast|normal|slow

## Key Claims
- Actual arguments, mechanics, data points
- Specific enough to be useful without re-reading original

## Notable Quotes
- Direct quotes worth remembering verbatim

## Analysis
What matters. Connections to other knowledge. Why it's significant.

## Context
Why it was shared. Decisions made based on this.

## Related Sources
- [[other-source-slug]]
```

## 质量要求

1. **避免泛泛而谈**。仅仅描述“有趣的见解”是没有价值的。必须捕捉具体的观点、机制和数据。
2. **记录推理过程**：保存分析的逻辑，而不仅仅是最终结论。
3. **使用引文**：直接引用原文能提高信息的准确性。
4. **合理使用标签**：标签有助于未来的资源查找，应包含主题、作者、领域和相关实体。
5. **记录决策过程**：如果某个资源引发了用户的行动，务必在相关记录中体现这一点。
6. **建立关联**：相互关联的资源才是真正的知识；孤立存在的资源只是书签而已。

## 不适用场景

- 用于一般的网页浏览或无保存需求的页面获取。
- 不能用于书签管理（不能仅为了“稍后查看”而保存内容）。
- 不能用于总结用户未要求保存的页面。
- 不能用于存储用户知识库之外的信息。