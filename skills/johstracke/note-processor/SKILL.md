---
name: note-processor
description: **研究助理生成的研究笔记的汇总与分析工具**  
该工具具备以下核心功能：  
1. **生成笔记摘要**：能够自动提取研究笔记的关键内容，为用户提供简洁的笔记概要。  
2. **关键词提取**：从笔记中识别出高频出现的关键词，帮助用户快速理解笔记的主题。  
3. **主题搜索**：支持用户根据特定关键词或主题对笔记进行高效搜索。  
4. **完整主题列表**：系统会列出所有被记录的研究主题，便于用户进行分类和管理。  

该工具专为处理 `research_db.json` 格式的笔记文件设计，非常适合用于：  
- **发现研究中的规律与趋势**：通过分析大量笔记数据，帮助研究人员发现潜在的研究模式或趋势。  
- **监控研究进度**：用户可以随时查看已完成或正在进行的研究主题，确保研究工作的顺利进行。  
- **高效提取见解**：无需逐篇阅读所有笔记，即可快速获取关键信息，提升研究效率。
---

# 笔记处理器（Note Processor）

该工具用于分析和总结研究笔记，以便快速提取有价值的见解。

## 快速入门

```bash
note_processor.py summarize <topic>
note_processor.py keywords <topic>
note_processor.py extract <topic> <keyword>
note_processor.py list
```

**示例：**
```bash
# Get a summary of a research topic
note_processor.py summarize income-experiments

# Extract top keywords from notes
note_processor.py keywords security-incident

# Search for specific information
note_processor.py extract income-experiments skill

# List all research topics with stats
note_processor.py list
```

## 主要功能

- **摘要**：提供主题概览，包括统计数据、标签和关键点
- **关键词**：提取最常见的词汇（排除常用停用词）
- **搜索**：查找包含特定关键词的笔记
- **列表**：查看所有研究主题及其基本统计信息
- **集成**：支持与研究辅助工具（research-assistant）的数据库格式兼容

## 使用场景

### 研究会后
```bash
# Summarize what you learned
note_processor.py summarize new-research-topic

# Extract key themes
note_processor.py keywords new-research-topic
```

### 撰写报告前
```bash
# Find specific information
note_processor.py extract income-experiments monetization

# Get overview for introductions
note_processor.py summarize income-experiments
```

### 审查研究进展
```bash
# See all topics and their sizes
note_processor.py list

# Check what you've been working on
note_processor.py keywords income-experiments
```

## 命令详情

### `summarize <主题>`
- 显示：笔记数量、单词数量、创建日期和最后更新日期
- 前5个标签
- 关键点（包含重要词汇的句子）
- 最近3条笔记

**输出示例：**
```
📊 Summary: income-experiments
------------------------------------------------------------
Notes: 4
Words: 63
Created: 2026-02-07
Last update: 2026-02-07

🏷️  Top Tags:
   content: 2
   automation: 2
   experiment: 2

💡 Key Points:
   1. First experiment: create and publish skills...
   2. Second experiment: content automation pipeline...
```

### `keywords <主题>`
- 显示：所有独特的关键词
- 出现频率最高的20个关键词
- 过滤常用停用词（如“that”、“this”、“with”等）

**输出示例：**
```
🔤 Keywords: income-experiments
------------------------------------------------------------
Total unique keywords: 38

Top 20 Keywords:
  1. experiment           ( 4x)
  2. skill                ( 3x)
  3. clawhub              ( 2x)
  4. content              ( 2x)
```

### `extract <主题> <关键词>`
- 显示：所有包含该关键词的笔记
- 关键词会以大写字母显示
- 包含时间戳和标签
- 显示匹配内容的预览

**输出示例：**
```
🔍 Search Results: 'skill' in income-experiments
------------------------------------------------------------
Found 4 match(es)

1. [2026-02-07 19:09:51]
   Tags: ideas, autonomous
   First experiment: create and publish **SKILL**s to ClawHub...
```

### `list`
- 显示：所有研究主题
- 笔记数量和单词数量
- 最后更新日期
- 最新笔记的预览

**输出示例：**
```
📚 Research Topics (5)
------------------------------------------------------------

income-experiments
   Notes: 4 | Words: 63 | Updated: 2026-02-07
   Latest: Experiment 2 STARTING: Content automation...

security-incident
   Notes: 1 | Words: 45 | Updated: 2026-02-07
   Latest: Day 1: Security vulnerability found...
```

## 与研究辅助工具的集成

该工具使用与研究辅助工具相同的数据库（`research_db.json`）。

### 典型工作流程

```bash
# 1. Add research notes
research_organizer.py add "new-topic" "Research finding here" "tag1" "tag2"

# 2. Add more notes over time
research_organizer.py add "new-topic" "Another finding" "tag3"

# 3. Summarize when done
note_processor.py summarize new-topic

# 4. Find specific information
note_processor.py extract new-topic keyword

# 5. See all topics
note_processor.py list
```

### 两者结合使用

```bash
# Research phase
research_organizer.py add "experiment" "Test result 1" "testing"
research_organizer.py add "experiment" "Test result 2" "testing"
research_organizer.py add "experiment" "Conclusion: worked!" "results"

# Analysis phase
note_processor.py summarize experiment
note_processor.py keywords experiment

# Writing phase
note_processor.py extract experiment conclusion
# Now write report based on extracted notes
```

## 关键点检测

`summarize`命令通过识别包含重要词汇的句子来提取关键点：
- “important”、“key”、“critical”、“essential”
- “must”、“should”、“note”、“remember”
- “warning”、“priority”、“critical”

这有助于从研究中提取出可操作的见解。

## 关键词提取

`keywords`命令：
- 过滤长度小于4个字符的词汇
- 删除常用停用词
- 统计所有笔记中关键词的出现频率
- 显示出现频率最高的20个关键词

**被过滤的停用词：**
that, this, with, from, have, been, will, what, when, where, which, their, there, would, could, should, about, these, those, other, into, through

## 使用场景

### 撰写报告前
```bash
# Get overview
note_processor.py summarize research-topic

# Find specific data points
note_processor.py extract research-topic metrics

# Extract themes
note_processor.py keywords research-topic
```

### 审查研究进展
```bash
# See what you've been working on
note_processor.py list

# Check a specific topic's progress
note_processor.py summarize current-project

# Find patterns
note_processor.py keywords current-project
```

### 查找特定信息
```bash
# Search across a topic
note_processor.py extract income-experiments monetization

# Find references to specific tools
note_processor.py extract security-incident path-validation

# Locate conclusions
note_processor.py extract experiment conclusion
```

## 最佳实践

1. **使用摘要**：在深入细节之前先获取整体概览
2. **先搜索**：在阅读所有笔记之前使用`extract`功能
3. **检查关键词**：发现可能遗漏的主题
4. **定期整理列表**：定期查看所有主题以发现遗漏的内容
5. **一致地添加标签**：使关键词更具意义

## 数据存储位置

数据库：`~/.openclaw/workspace/research_db.json`
格式：与研究辅助工具（research-assistant）兼容

## 限制

- **简单的关键词提取**：基于频率统计，而非语义分析
- **无自然语言处理**：仅进行基本文本处理（不使用机器学习/人工智能）
- **停用词列表**：以英语为主，可针对其他语言进行自定义
- **关键点检测**：基于模式识别，而非深度理解

## 提示

### 提高关键词质量

- 在笔记中使用统一的术语
- 避免使用缩写或同义词来表示相同概念
- 为笔记添加相关标签
- 定期检查关键词，确保重要术语被正确标记

### 提高摘要质量

- 在笔记中书写完整的句子
- 包含重要词汇（如“key”、“critical”、“must”等）
- 为笔记添加主题标签
- 定期生成摘要以跟踪研究进展

### 提高搜索效果

- 在`extract`命令中使用具体的关键词
- 搜索相关词汇（使用同义词）
- 查看搜索结果中的标签
- 利用摘要来定位相关主题

## 常见问题及解决方法

### “找不到该主题”
**解决方法：**检查主题名称的拼写。可以使用`note_processor.py list`查看所有主题。

### “未找到匹配结果”
**解决方法：**尝试使用不同的关键词，检查拼写，或使用`note_processor.py keywords`查找相关术语。

### 关键词提取效果不佳
**解决方法：**
- 在笔记中使用更具体的词汇
- 为笔记添加重要标签
- 可以在代码中自定义停用词过滤规则

## 按使用场景划分的示例

### 项目回顾
```bash
# What have I been working on?
note_processor.py list

# Tell me about this project
note_processor.py summarize project-x

# What are the main themes?
note_processor.py keywords project-x
```

### 编写文档
```bash
# Find specific details
note_processor.py extract security-incident vulnerability

# Get overview for introduction
note_processor.py summarize security-incident

# What's important?
note_processor.py keywords security-incident
```

### 准备报告
```bash
# Find all relevant information
note_processor.py extract income-experiments monetization

# Get summary
note_processor.py summarize income-experiments

# Extract key points
note_processor.py summarize income-experiments
# Key points are in the output
```

## 与其他工具的集成

### 与研究辅助工具（research-assistant）集成
- `research-assistant`：添加笔记
- `note-processor`：分析笔记
- 顺序使用：添加 → 分析 → 撰写报告

### 与任务执行工具（task-runner）集成
```bash
# Add task to summarize research
task_runner.py add "Summarize experiment results" "documentation"

# When complete
note_processor.py summarize experiment

# Mark done
task_runner.py complete 1
```

### 与其他工具集成
```bash
# Extract research notes
note_processor.py extract research-topic important

# Export for sharing
research_organizer.py export research-topic ~/shared/summary.md

# Or export summary output to file
note_processor.py summarize research-topic > ~/shared/summary.txt
```

## 无成本优势

该工具无需额外费用，具备以下要求：
- ✅ 支持Python 3（已包含）
- ✅ 无需API密钥
- ✅ 无需外部依赖
- ✅ 无需付费服务
- ✅ 可与研究辅助工具（research-assistant）免费结合使用

非常适合无需额外成本的自主研究工作流程。