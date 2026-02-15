---
name: swipe-file-generator
description: 该工具用于分析来自URL的高性能内容，并生成相应的“swipe文件”。适用于希望研究并剖析成功案例（如文章、推文、视频）的用户，以便从中提取模式、心理学技巧以及可复用的框架结构。
---

# 刷屏文件生成器

这是一个用于分析高效果内容（如文章、博客帖子、推文等）的工具，旨在研究其结构、心理模式和核心理念。该工具的主要职责包括协调内容的获取与分析过程、跟踪处理状态，并持续更新和维护刷屏文件。

## 文件位置

- **源URL列表文件：** `swipe-file/swipe-file-sources.md`
- **已处理URL注册表：** `swipe-file/.digested-urls.json`
- **主刷屏文件：** `swipe-file/swipe-file.md`

## 工作流程

### 第1步：检查源URL列表

1. 读取 `swipe-file/swipe-file-sources.md` 以获取待处理的URL列表。
2. 如果该文件不存在或未包含任何URL，请让用户直接提供URL。
3. 从源文件中提取所有有效的URL（每行一个URL，忽略以#开头的注释）。

### 第2步：识别新URL

1. 读取 `swipe-file/.digested-urls.json` 以获取之前已处理的URL。
2. 如果注册表不存在，则创建一个空的 `digested` 数组。
3. 将源URL与已处理的URL列表进行比对，找出尚未处理的URL。

### 第3步：批量获取新URL

1. **检测URL类型并选择获取策略：**
   - **Twitter/X URL：** 使用 FxTwitter API（详见下文）。
   - **其他所有URL：** 使用 web_fetch 工具。
2. **并行获取所有内容**，针对每种URL使用相应的获取方法。
3. **跟踪获取结果：**
   - 成功获取的URL及其内容将被存储以供进一步处理。
   - 获取失败的URL将被记录下来，以便后续报告问题。
4. 仅处理成功获取的内容。

#### Twitter/X URL的处理方式

Twitter/X URL需要特殊处理，因为它们需要JavaScript才能正确显示。请使用 **FxTwitter API**：

**检测方法：** URL中包含 `twitter.com` 或 `x.com`。

**API端点：** `https://api.fxtwitter.com/{username}/status/{tweet_id}`

**URL转换示例：**
- 输入：`https://x.com/gregisenberg/status/2012171244666253777`
- API URL：`https://api.fxtwitter.com/gregisenberg/status/2012171244666253777`

### 第4步：分析所有内容

对于获取到的每一部分内容，请按照以下 **内容分析指南** 进行分析：
1. 对每部分内容应用完整的分析框架。
2. 为每部分内容生成详细的分析报告。
3. 确保所有分析报告的格式保持一致。

### 第5步：更新刷屏文件

1. 读取现有的 `swipe-file/swipe-file.md`（如果文件不存在，则根据模板创建）。
2. **生成/更新目录**（详见下文）。
3. 将所有新的分析结果按时间顺序（最新内容优先）添加到目录之后。
4. 保存更新后的刷屏文件。
5. 更新已处理的URL列表（`swipe-file/.digested-urls.json`）。

#### 目录自动生成

刷屏文件必须包含一个自动生成的目录，列出所有已分析的内容。

**目录结构：**
```markdown
## Table of Contents

| # | Title | Type | Date |
|---|-------|------|------|
| 1 | [Content Title 1](#content-title-1) | article | 2026-01-19 |
| 2 | [Content Title 2](#content-title-2) | tweet | 2026-01-19 |
```

### 第6步：生成报告摘要

向用户报告以下信息：
- 处理了多少个新URL。
- 哪些URL已被处理（附带标题）。
- 哪些URL获取失败（附带失败原因）。
- 更新后的刷屏文件的位置。

## 处理特殊情况

### 没有新URL

如果源文件中的所有URL都已被处理：
1. 通知用户所有URL均已处理完毕。
2. 询问用户是否需要手动添加新的URL。

### URL获取失败

- 记录在获取过程中失败的URL。
- **不要** 将这些失败的URL添加到已处理URL列表中。
- 在报告中列出所有失败的情况及其原因。

### 首次运行（文件不存在）

1. 创建一个空的 `swipe-file/.digested-urls.json` 文件。
2. 根据模板结构创建 `swipe-file/swipe-file.md` 文件。
3. 处理来自源文件（或用户提供的）所有URL。

## 分析内容的输出格式

每部分分析结果应遵循以下格式（并添加到刷屏文件中）：
```markdown
## [Content Title]
**Source:** [URL]
**Type:** [article/tweet/video/etc.]
**Analyzed:** [date]

### Why It Works
[Summary of effectiveness]

### Structure Breakdown
[Detailed structural analysis]

### Psychological Patterns
[Identified patterns and techniques]

### Recreatable Framework
[Template/checklist for recreation]

### Key Takeaways
[Bullet points of main lessons]
```

## 注册表格式

`.digested-urls.json` 文件的结构如下：
```json
{
  "digested": [
    {
      "url": "https://example.com/article",
      "digestedAt": "2024-01-15T10:30:00Z",
      "contentType": "article",
      "title": "Example Article Title"
    }
  ]
}
```

---

# 内容分析指南

您是一位专门研究如何分析高效果内容（如文章、博客帖子、推文等）的专家。您的任务是深入剖析这些内容，提取可复制的模式和有价值的见解。

## 您的使命

彻底分解内容，以便他人能够从头开始重新创作出同样有效的作品。重点关注以下方面：
- 内容为何有效（而不仅仅是其表达的内容）。
- 驱动读者参与的心理模式。
- 可复制的结构元素。
- 可用于重新创作的内容框架。

## 分析框架

### 1. 结构分析

- **开头吸引注意力的技巧：** 内容是如何吸引读者的注意力的？使用了哪些模式（问题、加粗的声明、故事、统计数据）？
- **内容流程与过渡：** 内容是如何逐步展开的？哪些元素让读者保持兴趣？
- **章节组织：** 内容是如何分块的？逻辑顺序是什么？
- **结尾与行动号召：** 内容是如何结束的？它引导读者采取什么行动？
- **长度与节奏：** 短小精悍的章节还是长篇大论？节奏如何？

### 2. 心理模式

- **说服技巧：** 稀缺性、社会认同、权威性、互惠原则、喜好、承诺/一致性。
- **情感触发因素：** 恐惧、渴望、好奇心、愤怒、喜悦、惊讶。
- **认知偏见：** 锚定效应、损失厌恶、从众心理、框架效应。
- **建立信任的元素：** 专业背景、具体性、展现脆弱性、证据。
- **吸引读者的元素：** 开放式结尾、情节转折、好奇心缺口、悬念。

### 3. 写作技巧

- **标题/副标题的编写：** 采用了什么模式？为什么具有吸引力？
- **句子结构：** 短句还是长句？使用分段还是疑问句？
- **词汇与语气：** 语言风格是随意的还是正式的？使用了专业术语还是通俗易懂的语言？
- **格式技巧：** 列表、加粗文字、空白间距、子标题。
- **叙事元素：** 人物设定、冲突、解决方案、故事发展。

### 4. 内容策略

- **目标受众：** 这些内容是为谁准备的？解决了哪些问题？
- **价值主张：** 提供了什么价值？何时揭示这些价值？
- **应对反对意见：** 预先解决了哪些潜在的质疑？
- **独特视角/定位：** 这些内容的独特之处在哪里？

### 5. 可复制的模板

- **步骤式结构大纲：** 可供复制的写作框架。
- **填空式模板：** 为关键部分提供的模板。
- **必备元素清单：** 必须包含的关键组成部分。

## 输出格式

```markdown
## [Content Title]
**Source:** [URL]
**Type:** [article/tweet/video/etc.]

### Why It Works
[2-3 sentence summary of what makes this effective]

### Structure Breakdown
**Opening Hook:** [Describe technique and why it works]

**Content Flow:**
- [Point 1]
- [Point 2]
- [Point 3]

**Closing/CTA:** [How it ends and what action it drives]

**Pacing:** [Notes on length, rhythm, formatting]

### Psychological Patterns
**Primary Techniques Used:**
- [Technique 1]: [How implemented]
- [Technique 2]: [How implemented]
- [Technique 3]: [How implemented]

**Emotional Triggers:** [List emotions targeted and how]

**Trust Elements:** [What builds credibility]

### Recreatable Framework
**Structure Template:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Fill-in-the-Blank:**
> [Opening]: Start with [type of hook] about [topic]...
> [Body]: Present [number] points that [do what]...
> [Close]: End with [type of CTA]...

**Must-Have Checklist:**
- [ ] [Element 1]
- [ ] [Element 2]
- [ ] [Element 3]

### Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]
```

## 编写指南

1. **具体说明：** 不要只是简单地说“使用了社会认同”——要详细解释具体是如何使用的以及使用在何处。
2. **提供可操作的指导：** 每一条分析结果都应提供具体的操作建议，帮助他人重现相同的效果。
3. **全面分析：** 覆盖所有五个分析领域。
4. **引用示例：** 在适当的情况下，引用具体示例来说明分析技巧。