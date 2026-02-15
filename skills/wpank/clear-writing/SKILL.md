---
name: clear-writing
model: standard
version: 1.0.0
description: >
  Write clear, concise prose for humans — documentation, READMEs, API docs, commit messages,
  error messages, UI text, reports, and explanations. Combines Strunk's rules for clearer prose
  with technical documentation patterns, structure templates, and review checklists.
tags: [writing, documentation, style, technical-writing, prose]
---

# 清晰的写作

写作应当简洁明了、富有说服力。本技能涵盖了写作时应遵循的原则（如威廉·斯特伦克（William Strunk）提出的规则）、技术文档的结构规范（如Divio框架提供的模板），以及应避免的写作误区（如人工智能写作中常见的错误模式）。

## 适用场景

每当你需要为人类读者撰写文字时，都可以运用这一技能：
- 文档说明、README文件、技术解释
- API文档、端点参考、集成指南
- 教程、操作指南、架构文档
- 提交信息、拉取请求描述
- 错误信息、用户界面文本、帮助文档、注释
- 报告、总结或任何需要解释的内容
- 修订现有文本以提高其清晰度

**如果你在为人类读者撰写内容，那么请运用这一技能。**

## 有限上下文策略

当上下文信息较为有限时：
1. 根据自己的判断完成初稿的撰写。
2. 将初稿及相关参考文件交给辅助工具进行修订。
3. 由辅助工具完成校对并返回修改后的版本。

仅加载单个参考文件（约1,000至4,500个单词），而非整个文档，可以显著减少所需的信息量。

## 文体要素

威廉·斯特伦克在其著作《风格的要素》（The Elements of Style, 1918年）中提出了许多关于清晰写作的建议：

### 基本使用规则（语法/标点）

1. 表示单数所有格时添加“s”。
2. 一系列词语中，除了最后一个词外，每个词后都加逗号。
3. 用逗号将括号内的内容括起来。
4. 引入并列从句的连词前需加逗号。
5. 不要用逗号连接独立从句。
6. 不要将句子拆分成两部分。
7. 开头的分词短语应与句子的主语保持一致。

### 基本写作原则

8. 每个段落只讨论一个主题。
9. 每段以主题句开头。
10. 使用主动语态。
11. 用积极、具体的语言表达。
12. 省略不必要的词语。
13. 避免连续使用松散的句子。
14. 以相似的形式表达并列的概念。
15. 将相关的词语放在一起。
16. 摘要部分应保持时态一致。
17. 重要的词语应放在句子的末尾。

### 参考文件

如需详细解释及示例，请参阅以下文件：
| 部分 | 文件名 | 字数 |
|---------|------|---------|
| 语法、标点、逗号规则 | `references/elements-of-style/02-elementary-rules-of-usage.md` | 2,500 |
| 段落结构、主动语态、简洁性 | `references/elements-of-style/03-elementary-principles-of-composition.md` | 4,500 |
| 标题、引文、格式 | `references/elements-of-style/04-a-few-matters-of-form.md` | 1,000 |
| 词汇选择、常见错误 | `references/elements-of-style/05-words-and-expressions-commonly-misused.md` | 4,000 |

**大多数任务只需参考`03-elementary-principles-of-composition.md`即可**，因为它涵盖了主动语态、具体语言和省略不必要的词语等内容。

## 应避免的人工智能写作模式

大型语言模型（LLMs）往往会生成过于笼统、冗长的文本。请避免使用以下表达：
- **浮夸的词汇**：如“pivotal”（关键的）、“crucial”（至关重要的）、“vital”（至关重要的）、“testament”（见证）、“enduring legacy”（永恒的遗产）等。
- **空洞的短语**：如“ensuring reliability”（确保可靠性）、“showcasing features”（展示功能）、“highlighting capabilities”（突出能力）等。
- **过度使用的AI术语**：如“delve”（深入研究）、“leverage”（利用）、“multifaceted”（多方面的）、“foster”（培养）、“realm”（领域）、“tapestry”（织锦）等。
- **格式滥用**：如过多的项目符号、过多的表情符号、每隔一个词就使用粗体等。

请使用具体、准确的语言，而不是华丽的辞藻。只需说明事物本身的功能即可。

有关这些写作误区产生原因的详细研究，请参阅`references/signs-of-ai-writing.md`。维基百科编辑们制定了这份指南，用于识别人工智能生成的文档——这些模式已被广泛记录并经过实际测试。

## 文档类型（Divio框架）

| 文档类型 | 目的 | 结构 |
|------|---------|-----------|
| README | 给读者留下第一印象、项目概述 | 标题、描述、快速入门、安装指南、使用说明 |
| 教程 | 以学习为导向、提供指导 | 带有预期结果的步骤说明 |
| 操作指南 | 以解决问题为导向 | 问题描述 → 解决步骤 → 结果 |
| 参考文档 | 以信息提供为导向、内容完整准确 | 按字母顺序或分类排列、格式统一 |
| 解释性文档 | 以帮助理解为导向、包含背景和理由 | 叙事性文字、图表、历史背景 |
| 架构文档 | 介绍系统设计、组件关系 | 背景 → 组件 → 数据流 → 决策过程 |

## 结构规范

### 倒金字塔结构

首先介绍最重要的信息，后续部分逐步提供详细内容。

```
1. What it does (one sentence)
2. How to use it (quick start)
3. Configuration options
4. Advanced usage
5. Internals / implementation details
```

### 问题-解决方案

```
1. Problem — what goes wrong, symptoms, error messages
2. Cause — why it happens (brief)
3. Solution — step-by-step fix
4. Prevention — how to avoid it in the future
```

### 顺序步骤

每个步骤都应是一个可验证的结果。

```
1. Step — one action, one verb
   Expected result: what the reader should see
2. Step — next action
   Expected result: confirmation of success
```

## 写作规则

| 规则 | 指导原则 | 示例 |
|------|-----------|---------|
| 短句 | 每句话不超过25个单词 | “配置更改后，服务器会自动重启。” |
| 主动语态 | 用主语表示动作 | “该函数返回一个结果”而非“返回一个结果” |
| 现在时态 | 描述当前的行为 | “此端点接受JSON格式的数据”而非“将接受JSON格式的数据” |
| 每段一个主题 | 每段只讨论一个观点 | 当主题发生变化时，拆分复合段落 |
| 首次使用术语时进行定义 | 不要假设读者已了解专业术语 | “ORM（对象关系映射器）用于将……转换……” |
| 用第二人称写作 | 直接与读者交流 | “你可以配置……”而非“有人可以配置……” |
| 保持术语一致性 | 选择一种术语并始终使用 | 不要在“repo”和“repository”之间来回切换 |
| 具体而非抽象 | 使用具体细节而非泛泛而谈 | “返回404状态码”而非“返回错误信息” |

## 文档中的代码示例

所有代码示例都必须遵循以下规则：
1. **完整且可执行**——可以直接复制并运行，无需修改。
2. **附带注释**——仅对不易理解的部分进行注释，而非显而易见的部分。
3. **逐步增加复杂性**——先从最简单的情况开始，再介绍高级用法。
4. **标注语言**——在代码块中明确指定使用的语言。
5. **保持时效性**——示例必须与文档中描述的版本兼容。
6. **精简内容**——仅展示相关内容，去除无关的冗余代码。

```python
# Good: complete, annotated, minimal
import httpx

# Create a client with a base URL to avoid repeating it
client = httpx.Client(base_url="https://api.example.com")

# Fetch a user by ID — returns a User dict or raises for 4xx/5xx
response = client.get("/users/42")
response.raise_for_status()
user = response.json()
print(user["name"])  # "Ada Lovelace"
```

## README模板

```markdown
# Project Name

One-line description of what this project does and who it is for.

## Quick Start

The fastest path from zero to working. Three commands or fewer.

## Installation

Prerequisites, system requirements, and step-by-step install.

## Usage

Common use cases with code examples. Cover the 80% case.

## API

Public API surface — functions, classes, CLI flags, endpoints.

## Configuration

Environment variables, config files, and their defaults.

## Contributing

How to set up the dev environment, run tests, and submit changes.

## License

License name and link to the full LICENSE file.
```

**README文档的编写规则：**
- 快速入门部分的阅读时间应控制在60秒以内。
- 仅在徽章信息更新时才添加徽章列表。
- 避免在README中包含过多的内容，而是链接到更详细的文档。
- 每当公共接口发生变化时，及时更新README。

## API文档的编写规范

使用以下结构来记录每个端点：

```markdown
### GET /users/:id

Retrieve a single user by their unique identifier.

**Authentication:** Bearer token required

**Path Parameters:**

| Parameter | Type   | Required | Description          |
|-----------|--------|----------|----------------------|
| id        | string | Yes      | The user's unique ID |

**Response: 200 OK**

{json response example}

**Error Responses:**

| Status | Code         | Description              |
|--------|--------------|--------------------------|
| 401    | UNAUTHORIZED | Missing or invalid token |
| 404    | NOT_FOUND    | User does not exist      |
```

在文档中，务必记录错误信息，包括HTTP状态码、机器可读的错误代码、人类可读的错误信息以及解决方法。

## 根据受众调整文档内容

| 受众群体 | 文档的复杂度 | 重点 | 语气 |
|----------|--------------|-------|------|
| 初学者 | 高度复杂 | 定义术语、解释先决条件 | 从基础开始，逐步讲解 | 采用鼓励性、耐心的语气 |
| 中级读者 | 中等复杂度 | 假设读者具备基本知识 | 介绍具体操作和最佳实践 | 采用直接、实用的语气 |
| 专家读者 | 低度复杂 | 跳过基础内容，讨论高级主题和权衡因素 | 采用简洁、精确的语气 |

**编写规则：**
- 在文档开头明确说明目标受众。
- 链接到相关的先决知识，避免重复解释。
- 在专家级文档中使用可扩展的部分（如`<details>`）来提供初学者的补充信息。
- 不要在同一部分中混合不同复杂度的内容。

## 审核 checklist

在发布任何文档之前，请确保：
- [ ] **所有代码示例都能正常运行**。
- [ ] **所有命令都能正确执行**。
- [ ] **所有链接都有效**。
- [ ] **术语、格式和语气与文档整体保持一致**。
- [ ] **文档易于阅读**——即使是对项目不熟悉的人也能轻松理解。
- [ ] **文档易于浏览**——标题、表格和列表有助于快速查找所需信息。
- [ ] **示例能够正常工作**——每个代码块都经过当前版本的测试。
- [ ] **所有链接都是有效的**。
- [ ] **文档内容适合目标受众**。
- [ ] **文档内容是最新的**——不包含过时的功能或旧版本的信息。
- [ ] **无拼写错误**。

## 应避免的文档写作误区

| 错误模式 | 问题 | 解决方法 |
|--------------|---------|-----|
| 过长的文本 | 读者难以阅读 | 将内容分成多个部分，并使用标题和列表来组织。
| 过时的文档 | 降低可信度 | 将文档更新与拉取请求（PR）的审核流程关联起来，并在页面上标注更新日期。
| 没有示例 | 读者无法根据抽象描述进行操作 | 为每个公开提供的功能添加代码示例。
| 假设读者已掌握所有知识 | 会排除初学者的理解 | 在首次使用术语时进行定义，并提供相关先决条件的链接。
| 代码格式混乱 | 代码中包含不必要的提示或行号 | 提供清晰、可直接运行的代码块。
| 仅使用截图的说明 | 无法搜索，容易过时且不易理解 | 将截图与文字和操作步骤结合使用。

## 绝对不能做的事情：
1. **绝对不要在未测试所有代码示例的情况下发布文档**——有问题的代码示例会迅速破坏文档的可信度。
2. **绝对不要事后才编写文档**——应在编写代码的同时编写文档；如果无法解释代码的功能，说明设计存在问题。
3. **绝对不要使用“simply”（简单地）、“just”（仅仅）或“obviously”（显然）这样的词语**——这些词语对阅读者毫无帮助，反而会让他们感到困惑。
4. **绝对不要在一个文档中同时面向多个受众群体**——应为初学者和高级读者分别编写文档，或使用明确的章节划分。
5. **绝对不要在已发布的文档中留下占位符内容**——如“TODO”、“TBD”或“lorem ipsum”等词语会让人觉得文档未完成。
6. **绝对不要在多个文档中重复内容**——应链接到统一的信息来源，避免内容重复。
7. **绝对不要省略文档的日期或版本信息**——读者需要知道他们看到的是最新版本的信息。
8. **绝对不要使用浮夸的词汇**——如“pivotal”（关键的）、“crucial”（至关重要的）等词语，这些词语毫无实际意义，只会显得作者工作草率。