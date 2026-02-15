---
name: Article Illustrator
model: reasoning
description: >
  When the user wants to add illustrations to an article or blog post. Triggers
  on: "illustrate article", "add images to article", "generate illustrations",
  "article images", or requests to visually enhance written content. Analyzes
  article structure, identifies positions for visual aids, and generates
  illustrations using a Type x Style two-dimension approach.
version: 1.0.0
tags: [writing, illustration, images, articles, content]
---

# Article Illustrator

该工具用于分析文章内容，确定插图的最佳位置，并根据Type x Style一致性系统生成相应的插图。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install article-illustrator
```

## 注意事项：

- **切勿**：
  - 直接将比喻性语言（例如“链锯切割西瓜”）照字面意思绘制出来；应尝试理解其背后的概念。
  - 生成与文章内容无关的通用装饰性插图。
  - 跳过设置确认步骤（步骤3）。
  - 在未与用户确认插图类型、密度和风格之前就开始生成插图。
  - 生成插图时，必须确保每个插图的位置都符合文章内容的需求。

## 两种维度

| 维度 | 控制选项 | 示例 |
|---------|-----------|---------|
| **类型** | 信息结构、布局 | 信息图、场景图、流程图、对比图、框架图、时间线图 |
| **风格** | 视觉美感、整体风格 | 简约风格、温暖风格、蓝图风格、水彩风格、优雅风格、新闻风格、科学风格 |

类型和风格可以自由组合：`--type infographic --style blueprint`

### 类型选择指南

| 类型 | 适用场景 |
|------|---------|
| `infographic` | 数据展示、技术文章 |
| `scene` | 叙事内容、个人故事、情感类文章 |
| `flowchart` | 教程、工作流程 |
| `comparison` | 并列对比、前后对比 |
| `framework` | 方法论、模型、架构 |
| `timeline` | 历史事件、发展过程 |

### 风格选择指南

| 风格 | 适用场景 |
|-------|---------|
| `notion`（默认） | 知识分享、SaaS产品介绍、提升效率 |
| `elegant` | 商业类内容、思想领导力相关 |
| `warm` | 个人成长、生活方式相关内容 |
| `minimal` | 哲学类内容、核心概念讲解 |
| `blueprint` | 系统架构图 |
| `watercolor` | 与生活方式、旅行相关的内容 |
| `editorial` | 技术说明文档、新闻报道 |
| `scientific` | 学术文章、技术研究 |

完整的风格规格和兼容性矩阵：[references/styles.md](references/styles.md)

### 根据内容自动选择插图类型和风格

| 内容特征 | 推荐类型 | 推荐风格 |
|---------|---------|---------|
| API、数据、数字 | 信息图 | 蓝图风格、简约风格 |
| 故事、情感表达 | 场景图 | 温暖风格、水彩风格 |
| 操作步骤、工作流程 | 流程图 | 简约风格 |
| 对比分析 | 对比图 | 简约风格、优雅风格 |
| 方法论、模型、架构 | 框架图 | 蓝图风格、简约风格 |
| 历史事件、发展过程 | 时间线图 | 优雅风格、温暖风格 |

## 工作流程

### 第1步：预检查

1. **确定输入类型**：文件路径或粘贴的文章内容。
2. **确定输出目录**：根据用户偏好选择：
   - `{article-dir}/`：与文章在同一目录下。
   - `{article-dir}/illustrations/`：插图子目录（推荐）。
   - `illustrations/{topic-slug}/`：独立插图目录。
3. **检查现有插图**：如果已有插图，需决定是补充、覆盖还是重新生成。
4. **确认文章更新方式**：仅更新原始文件，或创建 `{name}-illustrated.md` 的副本。

### 第2步：分析文章内容

- **分析内容类型**：技术类、教程类、方法论类或叙事类文章。
- **确定需要可视化的核心观点**（2-5个）。
- **分析适合插入插图的位置**。
- **根据内容特征选择合适的插图类型和风格**。

**需要绘制的插图类型**：核心观点、抽象概念、数据对比图、工作流程图。
**无需绘制的插图类型**：字面意义上的比喻性内容、装饰性场景图、通用插图。

### 第3步：确认设置（必选）

使用以下结构化问题进行设置确认：
- **Q1：类型**：推荐类型及可选方案。
- **Q2：密度**：简约（1-2个插图）、平衡（3-5个插图）、丰富（6个以上插图）。
- **Q3：风格**：根据类型和内容选择合适的风格。
- **Q4：语言**（仅当源语言与用户语言不同时需要考虑）。

### 第4步：生成插图大纲

将结果保存为 `outline.md` 文件，文件包含 YAML 标头（类型、插图数量、风格等信息），以及每个插图的详细信息（位置、用途、视觉内容、文件名）。

### 第5步：生成插图

- 根据 [references/prompt-construction.md](references/prompt-construction.md) 中的提示生成插图。
- 将生成的插图提示保存到 `prompts/illustration-{slug}.md` 文件中。
- 按顺序生成插图，并在生成过程中记录进度。
- 如果生成失败，重试一次；如果仍然失败，请记录错误信息并继续尝试。

### 第6步：最终整理

在相关段落后插入插图引用。

## 输出结果

输出包含文章路径、设置信息、插图数量和插图位置的总结。

## 输出文件结构

```
illustrations/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/
│   └── illustration-{slug}.md
└── NN-{type}-{slug}.png
```

## 插图提示编写原则

优秀的插图提示应包含以下要素：
- **布局结构**：描述插图的组成元素和布局方向。
- **具体数据/标签**：使用文章中的实际数据和术语。
- **元素之间的视觉关系**：说明各个元素之间的连接方式。
- **颜色选择**：根据语义选择颜色（例如红色表示警告、绿色表示高效）。
- **风格特征**：包括线条处理方式、纹理和整体视觉效果。
- **宽高比**：明确指出插图的宽高比和复杂程度。

完整的插图提示模板：[references/prompt-construction.md](references/prompt-construction.md)

## 类型与风格的兼容性

| 类型 | 简约风格 | 温暖风格 | 简约风格 | 蓝图风格 | 水彩风格 | 优雅风格 | 新闻风格 | 科学风格 |
|---|---|---|---|---|---|---|---|
| 信息图 | ++ | + | ++ | ++ | + | ++ | ++ | ++ |
| 场景图 | + | ++ | + | - | ++ | + | + | - |
| 流程图 | ++ | + | + | ++ | - | + | ++ | + |
| 对比图 | ++ | + | ++ | + | + | ++ | ++ | + |
| 框架图 | ++ | + | ++ | ++ | - | ++ | + | ++ |
| 时间线图 | ++ | + | + | + | ++ | ++ | ++ | + |

`++`：强烈推荐；`+`：兼容；`-`：不推荐

## 使用示例

```bash
# Auto-select type and style
illustrate path/to/article.md

# Specify type
illustrate path/to/article.md --type infographic

# Specify type and style
illustrate path/to/article.md --type flowchart --style notion

# Specify density
illustrate path/to/article.md --density rich
```

## 扩展功能支持

通过 `EXTEND.md` 文件自定义配置：
- **项目级别**：`.article-illustrator/EXTEND.md`
- **用户级别**：`$HOME/.config/article-illustrator/EXTEND.md`

支持的功能包括：添加水印、指定插图类型/风格、自定义样式、设置输出目录等。

## 修改操作

- **编辑**：修改插图提示、重新生成插图、更新相关文件。
- **添加新插图**：确定插图位置、编写提示、生成插图、更新大纲并插入文章。
- **删除插图**：删除相关文件、移除插图引用、更新大纲。

## 参考资料

- [references/usage.md](references/usage.md)：命令语法、使用选项、输入方式。
- [references/styles.md](references/styles.md)：插图风格库、兼容性矩阵、自动选择规则。
- [references/prompt-construction.md](references/prompt-construction.md)：各类插图的提示模板。
- `references/styles/<style>.md`：每种插图风格的详细规格。
- [references/config/preferences-schema.md]：`EXTEND.md` 文件的配置格式。
- [references/config/first-time-setup.md]：首次使用时的配置指南。
- [prompts/system.md]：系统提示生成规则。