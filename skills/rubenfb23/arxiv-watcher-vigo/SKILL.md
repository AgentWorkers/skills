---
name: arxiv-watcher
description: 从 ArXiv 中搜索并汇总论文。当用户需要了解最新的研究动态、特定主题的论文，或每日的人工智能论文摘要时，可以使用该功能。
---

# ArXiv Watcher

该技能通过调用ArXiv API来查找并汇总最新的研究论文。

## 功能

- **搜索**：根据关键词、作者或类别查找论文。
- **摘要生成**：获取论文的摘要并提供简洁的总结。
- **保存到内存**：自动将汇总的论文信息记录到`memory/RESEARCH_LOG.md`文件中，以便长期跟踪。
- **深入分析**：根据需要，使用`web_fetch`函数从PDF链接中提取更多详细信息。

## 工作流程

1. 使用`scripts/search_arxiv.sh "<query>"`命令获取XML格式的搜索结果。
2. 解析XML数据（查找`<entry>`、`<title>`、`<summary>`以及`<link title="pdf">`元素）。
3. 向用户展示搜索结果。
4. **必选操作**：将找到的论文的标题、作者、日期和摘要添加到`memory/RESEARCH_LOG.md`文件中。格式如下：
   ```markdown
   ### [YYYY-MM-DD] TITLE_OF_PAPER
   - **Authors**: Author List
   - **Link**: ArXiv Link
   - **Summary**: Brief summary of the paper and its relevance.
   ```

## 示例

- “在ArXiv上搜索关于大语言模型（LLM）推理的最新论文。”
- “告诉我ID为2512.08769的论文是关于什么的。”
- “为我总结一下ArXiv上关于智能体的最新研究动态。”

## 资源

- `scripts/search_arxiv.sh`：用于直接调用ArXiv API的脚本。