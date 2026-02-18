---
name: reasoning-answer
description: Current Date: $DATE$. Default language: keep the same with user's language, unless the user explicitly specifies a language. If answering based on search results, add a citation mark immediately after the relevant sentence or phrase. 2. The citation mark MUST be a clickable numbered footnote in the format `[[Number]](URL)`,for example [[1]](https://link-to-source-1.com). At the end, there shoul...
---

# 推理回答（Reasoning Answer）

## 概述

该技能提供了用于生成推理回答的专门功能。

## 使用说明

- 当前日期：$DATE$。默认语言与用户的语言相同，除非用户明确指定了其他语言。如果回答内容基于搜索结果，则需要在相关句子或短语后立即添加引号。  
- 引号必须采用可点击的编号脚注格式，例如 `[[数字]](链接)`，例如 `[[1]](https://link-to-source-1.com)`。  
- 在回答的末尾，需要提供完整的参考文献列表，确保引用编号从 [1] 开始依次递增。

## 使用注意事项

- 该技能基于 `Reasoning_Answer` 代理的配置进行工作。  
- 模板变量（如 `$DATE`、`$SESSION_GROUP_ID`）可能需要在使用时进行动态替换。  
- 请严格遵循上述内容中提供的说明和指南。