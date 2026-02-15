---
name: Chat with PDF
description: **功能概述：**  
- **回答问题关于PDF内容：** 用户可以针对PDF文件中的具体内容提出问题，系统会提供相应的答案或解释。  
- **总结PDF内容：** 系统能够对PDF文件进行自动总结，提取关键信息或主题。  
- **提取信息：** 用户可以指定从PDF文件中提取特定的数据或文本片段。  

**技术实现：**  
- **自然语言处理（NLP）：** 使用先进的自然语言处理技术来理解用户的查询和PDF文件的内容。  
- **文本分析：** 对PDF文件进行深度文本分析，提取关键词、句子和段落结构。  
- **数据提取：** 根据用户的需求，从PDF文件中提取所需的信息或数据。  

**示例：**  
1. 用户提问：“PDF文件的第3页第5行是什么内容？”  
   - 系统会返回：“PDF文件的第3页第5行是：‘This is an example sentence.’”  
2. 用户请求：“总结这篇PDF文章的主要观点。”  
   - 系统会输出：“本文主要讨论了……（总结文章的核心观点）。”  
3. 用户指定：“提取PDF文件中所有与‘人工智能’相关的文本。”  
   - 系统会提取出所有包含“人工智能”一词的文本片段。
author: claude-office-skills
version: "1.0"
tags: [pdf, document-ai, qa, summarization, extraction]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# 与PDF文档进行智能对话

您可以就PDF文档提出问题、获取摘要或提取特定信息。

## 概述

此功能允许您：
- 提出关于PDF内容的问题
- 获取不同详细程度的摘要
- 提取具体数据点
- 比较多个PDF文件中的信息
- 快速找到相关部分

## 使用方法

### 基本操作
1. 共享或上传PDF文档
2. 提出您的问题或请求
3. 获取带有引用信息的答案

### 问题类型

**事实性问题**
```
"What is the contract value mentioned in this document?"
"Who are the parties involved in this agreement?"
"What are the key dates mentioned?"
```

**摘要**
```
"Summarize this document in 3 bullet points"
"Give me an executive summary"
"What are the main topics covered?"
```

**提取**
```
"Extract all names and titles mentioned"
"List all financial figures in the document"
"Find all action items or deliverables"
```

**分析**
```
"What are the risks mentioned in this contract?"
"Are there any ambiguous terms?"
"What obligations does Party A have?"
```

## 输出格式

### 问答格式
```markdown
**Question**: [Your question]

**Answer**: [Direct answer to your question]

**Source**: Page [X], Section [Y]
> "[Relevant quote from document]"

**Confidence**: [High/Medium/Low]
```

### 摘要格式
```markdown
## Document Summary

**Type**: [Contract/Report/Manual/etc.]
**Pages**: [X]
**Date**: [If mentioned]

### Key Points
1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

### Important Details
- [Detail 1]
- [Detail 2]
```

### 提取格式
```markdown
## Extracted Information

### [Category 1]
| Item | Value | Location |
|------|-------|----------|
| [Item 1] | [Value] | Page X |
| [Item 2] | [Value] | Page Y |

### [Category 2]
...
```

## 最佳实践

### 为了获得更好的答案
1. **具体说明**：例如，“终止条款是什么？”而不是“请介绍一下合同内容”
2. **引用相关章节**：例如，“第5.2节关于责任的部分是怎么规定的？”
3. **提出后续问题**：基于之前的答案进行更深入的探讨

### 为了更准确地提取信息
1. **指定格式**：例如，“以表格形式提取”或“以项目符号列表的形式呈现”
2. **明确字段名称**：例如，“提取的字段包括：名称、日期、金额、描述”
3. **设置筛选条件**：例如，“仅提取金额超过10,000美元的记录”

### 为了获得更好的摘要
1. **指定长度**：例如，“用100个字概括”或“列出3个要点”
2. **明确目标受众**：例如，“为法律团队总结”或“为高管总结”

## 示例工作流程

### 合同审核
```
1. "What type of contract is this?"
2. "Who are the parties and what are their roles?"
3. "What are the key obligations for each party?"
4. "What is the term and renewal process?"
5. "What are the termination conditions?"
6. "Are there any unusual or concerning clauses?"
```

### 研究论文分析
```
1. "What is the main thesis or hypothesis?"
2. "What methodology was used?"
3. "What are the key findings?"
4. "What are the limitations mentioned?"
5. "What future research do they suggest?"
```

### 财务报告分析
```
1. "What is the total revenue reported?"
2. "How does this compare to last year?"
3. "What are the main expense categories?"
4. "What guidance is given for next quarter?"
5. "Extract all financial metrics into a table"
```

## 多文档支持

当处理多个PDF文件时：
```
"Compare the terms in Contract A vs Contract B"
"Which document mentions [topic]?"
"Create a summary table comparing key points across all documents"
```

### 对比结果
```markdown
## Document Comparison

| Aspect | Document A | Document B |
|--------|------------|------------|
| Term Length | 2 years | 3 years |
| Value | $50,000 | $75,000 |
| Termination | 30 days notice | 60 days notice |

### Key Differences
1. [Difference 1]
2. [Difference 2]

### Similarities
1. [Similarity 1]
2. [Similarity 2]
```

## 面临的挑战

### 扫描的PDF文件（基于图像）
- 系统会自动应用OCR技术
- 文本质量取决于扫描效果
- 可能存在识别错误

### 复杂的布局
- 表格可能需要重新格式化
- 多列文本会按从左到右的顺序处理
- 脚注会单独处理

### 长文档
- 为确保准确性，请询问特定章节的内容
- 如需概览，可以请求逐页摘要
- 请提出具体、针对性的问题，而非笼统的问题

## 限制

- 无法执行PDF中嵌入的代码
- 需要密码保护的PDF文件需要输入密码
- 非常大的PDF文件（500页以上）可能需要分部分处理
- 手写内容的识别能力有限
- 无法保证扫描文档的100%准确性
- 图表和图片只能进行描述，无法进行数值分析

## 隐私声明

文档内容将按照AI提供商的隐私政策进行处理。对于敏感文档，请考虑：
- 使用本地解决方案
- 先删除敏感信息
- 查阅数据保留政策