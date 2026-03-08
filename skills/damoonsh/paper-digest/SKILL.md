---
name: paper-digest
description: "给定一个 arXiv ID 或 URL，获取该论文，派生子代理来阅读其关键引用，并在其下方撰写一份执行摘要。"
user-invocable: true
author: Damoon
version: 0.0.1
---# 论文摘要

## 输入参数

- `arxiv_id`: 以 `2305.11206` 这样的简短 ID 或 `https://arxiv.org/abs/2305.11206` 这样的完整 URL 形式提供（处理规则：去除 URL 前缀，仅保留 ID 部分。）

## 第一步 — 获取论文正文

首先尝试使用 HTML 格式获取论文内容：`web.fetch https://arxiv.org/html/<arxiv_id>`  
- 如果请求返回 HTTP 200 状态码，则将获取到的内容作为 `paper_text` 使用。  
- 如果请求失败，则在 URL 后添加 `v1`，然后重新尝试：`web.fetch https://arxiv.org/html/<arxiv_id>v1`  
- 如果所有尝试都失败，则直接终止流程！

如果成功获取到 `paper_text`，将其内容写入文件 `~/.openclaw/workspace/papers/<arxiv-id>.md`。

## 第二步 — 提取引用文献

**注意**：此步骤必须在主代理（main agent）中执行，且不得在子代理（sub-agents）中执行。  
从 `paper_text` 中识别出该论文直接引用的文献（最多 5 篇）。优先考虑以下类型的文献：  
- 被该论文明确扩展或改进的文献；  
- 作为比较基准的文献；  
- 为该论文提供核心架构的文献；  
- 被多次引用（而不仅仅是简单提及）或提供关键背景信息的文献。  

对于每篇引用的文献，提取其 `arXiv ID` 或 **标题**，然后尝试获取其对应的 URL：  
- 如果引用的文献有 `arXiv ID`，则直接使用 `https://arxiv.org/html/<id>`；  
- 否则，在 `https://arxiv.org/search/?query=<title>&searchtype=all` 中进行搜索，并选择第一个匹配结果。

## 第三步 — 为每篇引用文献创建子代理（sub-agent）

**注意**：确保子代理的任务描述精确且简洁，以避免重复读取已处理的 SKILL 和文件。  
对于每篇成功获取引用的文献：  
- 检查对应的引用文件（`~/.openclaw/workspace/papers/<arxiv-id>.md`）是否存在；如果存在，则跳过当前步骤。  
- 如果前一步骤失败，则创建一个新的子代理，并向其传递以下指令：  
  - 获取该引用文献的 HTML 内容（`https://arxiv.org/html/<citation_id>`；如果无法获取，则在 URL 后添加 `v1`，然后重新尝试：`web.fetch https://arxiv.org/html/<arxiv_id>v1`。如果仍然无法获取，则跳过当前步骤。如果成功获取到内容，将其摘要写入文件 `~/.openclaw/workspace/papers/<arxiv-id>.md`。

## 第四步 — 编写执行摘要

查看 `~/.openclaw/workspace/papers/` 目录下的引用文献摘要，结合主论文内容，使用流畅的 prose（非列表格式）编写一个 markdown 文档，保存到 `~/.openclaw/workspace/digest/report_<arxiv-id>`。文档结构如下：

```markdown
# <Title>

<What problem this solves and why it matters. Context and related references summary>

<What prior work missed and how this paper addresses that gap. Cite inline as [Author et al., YEAR](<arxiv_link>).

<Core method in plain terms>

<Headline result. How it differs from previous work.

<One limitation and one future direction>

<Detailed Ablations, benchmarks if present in this paper or cited references>
```

## 规则说明：  
- 每条引用文献都必须以 markdown 格式表示，格式为：`[作者等人, 年份](<arxiv_or_url>)`  
- 输出内容必须为纯 prose（无列表格式）。  
- 如果论文中缺少某些部分（例如实验结果、指标或作者声明），则直接跳过相关内容。  
- 不得伪造任何数据、指标或作者的陈述。  
- **引用文献的获取尝试**：如果尝试多次后仍无法获取引用文献的 URL，则将其以纯文本形式显示（不添加链接），格式为：`[作者等人, 年份]`。