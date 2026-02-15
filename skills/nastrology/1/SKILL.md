---
name: second-brain
description: 这是一个由 Ensue 提供支持的个性化知识库，用于捕获和检索用户的学习内容。用户可以借助该知识库保存知识、回忆已学过的内容、管理自己的工具箱，或基于以往的学习成果进行进一步的学习。触发该知识库操作的关键词包括：“保存这个”、“记住”、“我对……了解多少”、“添加到工具箱中”、“我的笔记关于……”以及“存储这个概念”。
metadata: {"clawdbot":{"emoji":"🧠","requires":{"env":["ENSUE_API_KEY"]},"primaryEnv":"ENSUE_API_KEY","homepage":"https://ensue-network.ai"}}
---

# 第二大脑（Second Brain）

这是一个个人知识库，旨在帮助你逐步积累和深化对各种主题的理解。它不仅仅是一个简单的笔记集合，而是一个结构化系统，能够让你方便地检索和运用所学知识。

## 设计理念

你的“第二大脑”应该具备以下特点：
- **记录理解过程，而不仅仅是事实**：为你未来的自己编写内容——当你忘记相关背景信息时，这些记录能帮助你回忆。
- **易于检索**：内容需要经过合理组织，以便在需要时能够快速找到所需的信息。
- **保持内容的时效性**：避免保存私人信息、敏感数据或时效性强的内容。
- **反映真实的经验**：只保存你真正学到的或用到的知识。

在保存任何内容之前，请先问自己：“未来的我会感谢我这样做吗？”

## 命名空间结构

```
public/                           --> Shareable knowledge
  concepts/                       --> How things work
    [domain]/                     --> Organize by topic
      [concept-name]              --> Individual concepts
  toolbox/                        --> Tools and technologies
    _index                        --> Master index of tools
    [category]/                   --> Group by type
      [tool-name]                 --> Individual tools
  patterns/                       --> Reusable solutions
    [domain]/                     --> Design patterns, workflows
  references/                     --> Quick-reference material
    [topic]/                      --> Cheatsheets, syntax, APIs

private/                          --> Personal only
  notes/                          --> Scratchpad, drafts
  journal/                        --> Dated reflections
```

**示例命名空间：** `programming`（编程）、`devops`（DevOps）、`design`（设计）、`business`（商业）、`data`（数据）、`security`（安全）、`productivity`（生产力）

## 内容格式

### 概念（Concepts）
用于记录对某事物工作原理的理解：

```
CONCEPT NAME
============

What it is:
[One-line definition]

Why it matters:
[What problem it solves, when you'd need it]

How it works:
[Explanation with examples]
[ASCII diagrams for architecture/flows where helpful]

+----------+      +----------+
| Client   | ---> | Server   |
+----------+      +----------+

Key insight:
[The "aha" moment - what makes this click]

Related: [links to related concepts]
```

### 工具箱条目（Toolbox Entries）
用于记录你实际使用过的工具和技术：

```
TOOL NAME

Category: [category]
Website: [url]
Cost: [free/paid/freemium]

What it does:
[Brief description]

Why I use it:
[Personal experience - what problem it solved for you]

When to reach for it:
[Scenarios where this is the right choice]

Quick start:
[Minimal setup/usage to get going]

Gotchas:
[Things that tripped you up]
```

### 模式（Patterns）
用于保存可复用的解决方案：

```
PATTERN NAME

Problem:
[What situation triggers this pattern]

Solution:
[The approach, with code/pseudocode if relevant]

Trade-offs:
[Pros and cons, when NOT to use it]

Example:
[Concrete implementation]
```

### 参考资料（References）
用于提供快速查阅的资料：

```
REFERENCE: [TOPIC]

[Organized, scannable content]
[Tables, lists, code snippets]
[Minimal prose, maximum signal]
```

## 使用规则

### 保存知识
在保存任何内容之前，请务必确认：
1. “是否要将这些内容保存到我的‘第二大脑’中？”
2. 查看要保存内容的草稿。
3. 确认后进行保存。
4. 确认保存了哪些内容以及保存的位置。

### 检索知识
当遇到相关主题时：
- 搜索已有的知识。
- 提取相关的概念。
- 将新学到的知识与已有的理解联系起来。

### 保持内容质量
在保存之前，请验证：
- 内容是为未来的自己编写的（即考虑到你可能忘记背景信息的情况）。
- 包含“为什么”（即背后的原理），而不仅仅是“是什么”。
- 提供具体的例子。
- 避免保存敏感信息（如API密钥、凭证等）。
- 内容需要结构化，以便于检索。

## 避免的错误做法：
1. **不要自动保存**：每次保存前都请先确认。
2. **不要保存未使用的工具**：只保存实际使用过的工具。
3. **不要保存理解不深入的概念**：先彻底理解后再保存。
4. **不要包含敏感信息**：不要保存API密钥、密码或token。
5. **不要创建浅层次的内容**：如果无法清晰地解释某个内容，就不要保存它。
6. **不要重复保存**：先检查是否已有相同的内容，如有需要再更新。

## API使用
请使用以下脚本进行操作：

```bash
{baseDir}/scripts/ensue-api.sh <method> '<json_args>'
```

### 常用操作
- **搜索知识**：```bash
{baseDir}/scripts/ensue-api.sh discover_memories '{"query": "how does X work", "limit": 5}'
```
- **按命名空间列出内容**：```bash
{baseDir}/scripts/ensue-api.sh list_keys '{"prefix": "public/concepts/", "limit": 20}'
```
- **获取特定条目**：```bash
{baseDir}/scripts/ensue-api.sh get_memory '{"key_names": ["public/concepts/programming/recursion"]}'
```
- **创建新条目**：```bash
{baseDir}/scripts/ensue-api.sh create_memory '{"items":[
  {"key_name":"public/concepts/domain/name","description":"Short description","value":"Full content","embed":true}
]}'
```
- **更新条目**：```bash
{baseDir}/scripts/ensue-api.sh update_memory '{"key_name": "public/toolbox/_index", "value": "Updated content"}'
```
- **删除条目**：```bash
{baseDir}/scripts/ensue-api.sh delete_memory '{"key_name": "public/notes/old-draft"}'
```

## 工具箱索引
请维护`public/toolbox/_index`文件作为主要的参考资料：

```
TOOLBOX INDEX
=============

Categories:
  languages/      Programming languages
  frameworks/     Libraries and frameworks
  devtools/       Development utilities
  infrastructure/ Deployment, hosting, CI/CD
  productivity/   Workflow and productivity tools
  data/           Databases, analytics, data tools

Recent additions:
  [tool] - [one-line description]

Browse: "show my toolbox" or "what tools do I have for [category]"
```

## 用户指令与操作对应关系
| 用户指令 | 操作 |
|-----------|--------|
| “保存这个内容” | 草拟条目，确认后保存 |
| “我知道关于X的哪些信息？” | 搜索并检索相关条目 |
| “将[工具]添加到工具箱中” | 创建工具箱条目 |
| “列出我的[领域]相关概念” | 显示该命名空间下的所有条目 |
| “查看我的工具箱” | 显示工具箱索引 |
| “更新[条目]” | 获取条目内容，显示差异后进行更新 |
| “删除[条目]” | 确认后删除条目 |
| “搜索[主题]” | 在所有知识中执行语义搜索 |

## 设置要求
需要设置`ENSUE_API_KEY`环境变量。你可以在以下链接获取API密钥：https://www.ensue-network.ai/dashboard
并在`clawdbot.json`文件中进行配置：

```json
"skills": {
  "entries": {
    "second-brain": {
      "apiKey": "your-ensue-api-key"
    }
  }
}
```

## 安全注意事项
- **严禁**记录或显示API密钥。
- **严禁**在条目中保存凭证、token或敏感信息。
- **严禁**包含个人文件路径或系统详细信息。