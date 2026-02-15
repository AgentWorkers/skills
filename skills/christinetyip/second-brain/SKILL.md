---
name: second-brain
description: 由 Ensue 提供支持的个性化知识库，用于捕获和检索用户的学习内容。当用户希望保存知识、回忆已学内容、管理自己的工具箱或基于以往的学习成果进行进一步学习时，可以使用该知识库。触发相关操作的关键词包括：“保存此内容”、“记住”、“我知道什么”、“添加到工具箱”、“关于……的笔记”以及“存储这个概念”。
metadata: {"clawdbot":{"emoji":"🧠","requires":{"env":["ENSUE_API_KEY"]},"primaryEnv":"ENSUE_API_KEY","homepage":"https://ensue-network.ai?utm_source=clawdbot&utm_medium=workflow"}}
---
*需要 API 密钥：请访问 https://ensue-network.ai?utm_source=clawdbot 获取*

# 第二大脑（Second Brain）

这是一个用于**逐步积累知识**的个人知识库。它不是一个简单的笔记堆砌，而是一个结构化的系统，可以帮助你轻松检索和运用所学知识。

## 哲学理念

你的“第二大脑”应该：
- **记录理解，而不仅仅是事实**——为你未来的自己编写内容，因为未来的你可能会忘记具体的背景信息。
- **便于检索**——内容需要结构化，以便你在需要时能够快速找到所需的信息。
- **保持知识的时效性**——不存储私人信息、凭证或时效性强的数据。
- **反映真实的经验**——只保存你真正学过或用过的内容。

在保存内容之前，请问自己：**未来的我会感谢我这样做吗？**

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

**示例命名空间：** `programming`、`devops`、`design`、`business`、`data`、`security`、`productivity`

## 内容格式

### 概念（Concepts）

用于理解某事物的工作原理：

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

用于快速查找相关资料：

```
REFERENCE: [TOPIC]

[Organized, scannable content]
[Tables, lists, code snippets]
[Minimal prose, maximum signal]
```

## 使用规则

### 保存知识

保存前请务必确认：
1. “是否要将这些内容保存到我的‘第二大脑’中？”
2. 显示即将保存的内容草稿。
3. 确认后进行保存。
4. 确认保存了哪些内容以及保存的位置。

### 检索知识

当相关主题出现时：
- 搜索已有的知识。
- 提取相关的概念。
- 将新学到的知识与已有的理解联系起来。

### 保持质量

保存前请验证：
- 内容是为未来的自己编写的（未来的你可能会忘记背景信息）。
- 包含“为什么”（原因），而不仅仅是“是什么”。
- 包含具体的示例。
- 不包含凭证、API 密钥或私人文件路径。
- 内容需要结构化，以便于检索。

## 避免的错误做法：
1. **不要自动保存**——每次保存前都要先询问。
2. **不要保存未使用的工具**——只保存实际使用过的工具。
3. **不要保存理解不清晰的概念**——先学习清楚，再保存。
4. **不要包含敏感信息**——不要保存 API 密钥、密码或令牌。
5. **不要创建浅层次的内容**——如果无法清晰解释某个内容，就不要保存。
6. **不要重复保存**——先检查是否已有相同的内容，如有需要再更新。

## API 使用方法

使用相应的包装脚本：

```bash
{baseDir}/scripts/ensue-api.sh <method> '<json_args>'
```

### 操作说明

**搜索知识：**
```bash
{baseDir}/scripts/ensue-api.sh discover_memories '{"query": "how does X work", "limit": 5}'
```

**按命名空间列出内容：**
```bash
{baseDir}/scripts/ensue-api.sh list_keys '{"prefix": "public/concepts/", "limit": 20}'
```

**获取特定条目：**
```bash
{baseDir}/scripts/ensue-api.sh get_memory '{"key_names": ["public/concepts/programming/recursion"]}'
```

**创建条目：**
```bash
{baseDir}/scripts/ensue-api.sh create_memory '{"items":[
  {"key_name":"public/concepts/domain/name","description":"Short description","value":"Full content","embed":true}
]}'
```

**更新条目：**
```bash
{baseDir}/scripts/ensue-api.sh update_memory '{"key_name": "public/toolbox/_index", "value": "Updated content"}'
```

**删除条目：**
```bash
{baseDir}/scripts/ensue-api.sh delete_memory '{"key_name": "public/notes/old-draft"}'
```

## 工具箱索引（Toolbox Index）

请维护 `public/toolbox/_index` 文件作为主要参考：

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
| “关于 X，我知道些什么？” | 搜索并检索相关条目 |
| “将 [工具] 添加到工具箱中” | 创建工具箱条目 |
| “列出我的 [领域] 相关概念” | 显示该命名空间下的所有条目 |
| “查看我的工具箱” | 显示工具箱索引 |
| “更新 [条目]” | 获取条目内容，显示差异后进行更新 |
| “删除 [条目]” | 确认后删除条目 |
| “搜索 [主题]” | 在所有知识中执行语义搜索 |

## 设置要求

需要设置 `ENSUE_API_KEY` 环境变量。请访问 https://www.ensue-network.ai?utm_source=clawdbot&utm_medium=workflow 获取 API 密钥，并在 `clawdbot.json` 文件中进行配置：

```json
"skills": {
  "entries": {
    "second-brain": {
      "apiKey": "your-ensue-api-key"
    }
  }
}
```

## 安全注意事项：

- **绝对不要** 记录或显示 API 密钥。
- **绝对不要** 在条目中存储凭证、令牌或敏感信息。
- **绝对不要** 包含个人文件路径或系统细节。