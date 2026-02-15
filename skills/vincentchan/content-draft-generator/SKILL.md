---
name: content-draft-generator
description: 根据参考内容的分析生成新的内容草稿。适用于需要根据表现优异的示例来创建内容（如文章、推文或帖子）的情况。该工具会分析参考链接，提取其中的模式，生成相关的问题，构建元提示（meta-prompts），并生成多种内容草稿版本。
---

# 内容草稿生成器

作为一个内容草稿生成器，我的核心功能是构建一个端到端的流程，根据参考示例来创建新的内容。我的工作包括分析参考内容、提取关键信息、收集相关背景信息、生成元提示（meta prompt），并最终生成多种内容变体。

## 文件目录结构

- **内容结构分解：** `content-breakdown/`
- **内容架构指南：** `content-anatomy/`
- **背景信息需求：** `content-context/`
- **元提示生成：** `content-meta-prompt/`
- **内容草稿：** `content-draft/`

## 参考文档

有关每个子模块的详细说明，请参阅以下文档：
- `references/content-deconstructor.md` - 如何分析参考内容
- `references/content-anatomy-generator.md` - 如何将分析结果整合成指南
- `references/content-context-generator.md` - 如何生成背景信息相关的问题
- `references/meta-prompt-generator.md` - 如何创建最终的提示模板

## 工作流程概述

```
Step 1: Collect Reference URLs (up to 5)

Step 2: Content Deconstruction
     → Fetch and analyze each URL
     → Save to content-breakdown/breakdown-{timestamp}.md

Step 3: Content Anatomy Generation
     → Synthesize patterns into comprehensive guide
     → Save to content-anatomy/anatomy-{timestamp}.md

Step 4: Content Context Generation
     → Generate context questions needed from user
     → Save to content-context/context-{timestamp}.md

Step 5: Meta Prompt Generation
     → Create the content generation prompt
     → Save to content-meta-prompt/meta-prompt-{timestamp}.md

Step 6: Execute Meta Prompt
     → Phase 1: Context gathering interview (up to 10 questions)
     → Phase 2: Generate 3 variations of each content type

Step 7: Save Content Drafts
     → Save to content-draft/draft-{timestamp}.md
```

## 详细操作步骤

### 第1步：收集参考链接

1. 向用户请求：“请提供最多5个能够代表您想要创建的内容类型的参考链接。”
2. 可以逐个接收链接，也可以接收链接列表。
3. 在继续之前验证链接的有效性。
4. 如果用户没有提供链接，请要求他们至少提供1个链接。

### 第2步：内容解析

1. 从所有提供的链接中获取内容（使用 `web_fetch` 工具）。
2. 对于 Twitter 或 X 的链接，将其转换为 FxTwitter API 格式：`https://api.fxtwitter.com/username/status/123456`。
3. 按照 `references/content-deconstructor.md` 中的指导分析每段内容。
4. 将解析后的结果保存到 `content-breakdown/breakdown-{timestamp}.md` 文件中。
5. 报告：“✓ 内容结构分解已完成。”

### 第3步：内容架构生成

1. 根据第2步的分析结果，按照 `references/content-anatomy-generator.md` 的指导提取内容模式。
2. 创建一份全面的指南，包括：
   - 内容的核心结构框架
   - 写作时的心理策略
   - 可填充的模板
3. 将生成的指南保存到 `content-anatomy/anatomy-{timestamp}.md` 文件中。
4. 报告：“✓ 内容架构指南已保存。”

### 第4步：背景信息生成

1. 按照 `references/content-context-generator.md` 的指导分析内容架构指南。
2. 生成关于以下方面的背景信息问题：
   - 主题与内容范围
   - 目标受众
   - 写作目标与预期效果
   - 文风与定位
3. 将生成的背景信息问题保存到 `content-context/context-{timestamp}.md` 文件中。
4. 报告：“✓ 背景信息需求已收集。”

### 第5步：元提示生成

1. 根据 `references/meta-prompt-generator.md` 的指导，创建一个两阶段的提示模板：

**第1阶段 - 背景信息收集：**
   - 与用户交流他们想要撰写的内容主题。
   - 使用第4步中生成的背景信息问题。
   - 如有需要，可再提出最多10个问题。

**第2阶段 - 内容撰写：**
   - 为每种内容类型生成3个不同的版本。
   - 确保遵循内容架构指南中的结构要求。
5. 将生成的元提示保存到 `content-meta-prompt/meta-prompt-{timestamp}.md` 文件中。
6. 报告：“✓ 元提示已生成。”

### 第6步：执行元提示

1. 开始**第1阶段：背景信息收集**：
   - 通过背景信息问题与用户交流他们的写作需求。
   - 提出最多10个问题，并等待用户的回答。
2. 进入**第2阶段：内容撰写**：
   - 为每种内容类型生成3个不同的版本。
   - 确保遵循内容架构指南中的结构要求，并运用之前确定的写作策略。

### 第7步：保存内容草稿

1. 将所有生成的草稿保存到 `content-draft/draft-{timestamp}.md` 文件中。
2. 文件中应包含：
   - 第1阶段收集的背景信息总结
   - 每种内容类型的3个版本及其写作策略
   - 每个版本的预写作检查清单
3. 报告：“✓ 内容草稿已保存。”

## 文件命名规则

所有生成的文件都会使用时间戳格式：`{类型}-{YYYY-MM-DD-HHmmss}.md`

示例文件名：
- `breakdown-2026-01-20-143052.md`
- `anatomy-2026-01-20-143125.md`
- `context-2026-01-20-143200.md`
- `meta-prompt-2026-01-20-143245.md`
- `draft-2026-01-20-143330.md`

## Twitter/X 链接处理

Twitter 或 X 的链接需要特殊处理：

- **检测方式：** 链接中包含 `twitter.com` 或 `x.com`。
- **转换规则：**
  - 输入格式：`https://x.com/username/status/123456`
  - 转换后的 API 格式：`https://api.fxtwitter.com/username/status/123456`

## 错误处理

- **链接获取失败：**
  - 记录失败的链接。
  - 继续处理成功获取的内容。
  - 向用户报告失败情况。

- **没有有效内容：**
  - 如果所有链接都无法获取内容，请要求用户提供其他链接或直接提供内容文本。

## 重要注意事项

- 在同一运行过程中，所有文件应使用相同的时间戳以确保可追溯性。
- 请保留所有生成的文件，切勿覆盖之前的结果。
- 在第1阶段收集背景信息时，请等待用户的输入。
- 在第2阶段必须生成恰好3个内容变体。