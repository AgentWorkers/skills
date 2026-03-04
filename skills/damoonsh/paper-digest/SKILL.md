---
name: paper-digest
description: "给定一个 arXiv ID 或 URL，获取该论文，派生出子代理来阅读其关键引用，并在下方撰写一份执行摘要。"
user-invocable: true
author: Damoon
version: 0.0.1
metadata:
  openclaw:
    emoji: "📄"
    always: true
    requires:
      skills: ["arxiv-paper-processor"]
---
# 论文摘要

## 输入参数

- `arxiv_id`: 仅包含数字的ID（例如 `2305.11206`），或完整的URL（例如 `https://arxiv.org/abs/2305.11206`）；处理方式：去除URL前缀，仅保留ID部分。

## 第一步：获取论文正文

- 首先尝试使用HTML方式获取论文内容：`web.fetch https://arxiv.org/html/ <arxiv_id>`（限制获取的字符数为70000个）。
- 如果请求返回HTTP 200状态码，则将获取到的内容作为`paper_text`。
- 否则，使用`arxiv-paper-processor`处理`arxiv_id`，并将其输出结果作为`paper_text`。

## 第二步：提取引用文献

从`paper_text`中找出论文直接引用的文献（最多5篇）。这些文献可能是论文扩展、借鉴其基础或架构的来源。具体来说，需要提取这些文献的`arXiv ID`或标题。

- 对于每篇引用的文献，解析其对应的`arXiv`链接：
  - 如果引用文献的`arXiv ID`已经提供，则直接使用链接 `https://arxiv.org/abs/<id>`。
  - 否则，在`https://arxiv.org/search/?query=<title>&searchtype=all` 中进行搜索，并选择第一个搜索结果。

## 第三步：为每篇引用文献创建子代理

对于每篇解析出的引用文献，创建一个子代理，让其执行以下操作：

“获取https://arxiv.org/html/<citation_id> 的内容。如果无法获取该内容，请使用`arxiv-paper-processor`处理`<citation_id>`，并返回一篇总结报告，内容包括该文献的贡献、实验方法、使用的数据以及所有相关信息。”

在继续下一步之前，收集所有子代理的响应。如果某篇引用文献无法获取，请将其标记为“不可用”，并继续处理其他文献。

## 第四步：撰写执行摘要

使用Markdown格式撰写一篇完整的文档，采用流畅的叙述方式（不要使用项目符号列表）。文档结构如下：

    # <论文标题>
    *<作者> · <发表年份> · [arXiv链接](<arxiv_link>)*

    ---

    <该论文解决的问题及其重要性。相关背景和参考文献的概述>

    <前人研究的不足之处以及本文如何填补这些空白（引用格式：[作者等, 发表年份](<arxiv_link>)>

    <论文的核心方法（用通俗语言解释）>

    <主要成果及其与以往研究的区别>

    <论文的局限性及未来研究方向>

    <实验方法、基准测试结果（来自本文或引用文献）>

## 规则：

- 所有引用文献都必须以Markdown链接的形式呈现：`[作者等, 发表年份](<arxiv_or_url>)`
- 文档中不得使用项目符号列表，只能使用纯文本。
- 如果论文中某个部分缺失（例如没有实验方法），则直接跳过该部分。
- 不得伪造实验结果、指标或作者的声明。
- 如果在尝试一次后仍无法解析引用链接，则将引用内容以纯文本形式呈现（不添加链接）：`[作者等, 发表年份]`