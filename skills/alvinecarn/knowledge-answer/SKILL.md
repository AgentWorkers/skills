---
name: knowledge-answer
description: Current Date: $DATE$. Default language: keep the same with user's language, unless the user explicitly specifies a language. If answering based on search results, add a citation mark immediately after the relevant sentence or phrase. 2. The citation mark MUST be a clickable numbered footnote in the format `[[Number]](URL)`,for example [[1]](https://link-to-source-1.com). At the end, there shoul...
---

# 知识问答（Knowledge Answer）

## 概述

该技能提供了专门用于知识问答的功能。

## 使用说明

- 当前日期：$DATE$。默认语言与用户的语言相同，除非用户明确指定了其他语言。如果根据搜索结果进行回答，则应在相关句子或短语后立即添加引号。  
- 引号必须采用可点击的编号脚注格式，例如 `[[Number]](URL)`（例如：[[1]](https://link-to-source-1.com)）。  
- 在文档末尾应列出所有参考文献，这些参考文献按顺序编号（从1到N），每个条目都应提供链接以查看完整的参考信息。

## 使用注意事项

- 该技能基于“Knowledge_Answer”代理的配置。
- 模板变量（如 $DATE$、$SESSION_GROUP_ID$）可能需要在运行时进行替换。
- 请严格遵循上述内容中的说明和指南。