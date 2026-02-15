---
name: content-creator
description: 创建具有统一品牌风格的SEO优化营销内容。该工具包包含品牌风格分析器、SEO优化工具、内容框架以及社交媒体模板，适用于撰写博客文章、制作社交媒体内容、分析品牌风格、优化SEO、规划内容发布计划，或在进行与内容创作、品牌风格管理、SEO优化、社交媒体营销或内容策略相关的工作时使用。
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# 内容创作者

提供专业级别的品牌声音分析、SEO优化以及针对不同平台的定制化内容框架服务。

---

## 目录

- [关键词](#keywords)
- [快速入门](#quick-start)
- [核心工作流程](#core-workflows)
- [工具](#tools)
- [参考指南](#reference-guides)
- [最佳实践](#best-practices)
- [集成点](#integration-points)

---

## 关键词

内容创作、博客文章、SEO、品牌声音、社交媒体、内容日历、营销内容、内容策略、内容营销、品牌一致性、内容优化、社交媒体营销、内容规划、博客写作、内容框架、品牌指南、社交媒体策略

---

## 快速入门

### 品牌声音开发

1. 在现有内容上运行 `scripts/brand_voice_analyzer.py` 以建立基准。
2. 查阅 `references/brand_guidelines.md` 以选择品牌声音特征。
3. 在所有内容中一致地应用所选的品牌声音特征。

### 博客内容创作

1. 从 `references/content_frameworks.md` 中选择一个模板。
2. 研究相关主题的关键词。
3. 按照模板结构撰写内容。
4. 运行 `scripts/seo_optimizer.py [文件] [主要关键词]` 进行优化。
5. 发布前应用优化建议。

### 社交媒体内容

1. 查阅 `references/social_media_optimization.md` 中的平台最佳实践。
2. 使用 `references/content_frameworks.md` 中的相应模板。
3. 根据平台特定指南进行优化。
4. 使用 `assets/content_calendar_template.md` 进行内容调度。

---

## 核心工作流程

### 工作流程 1：建立品牌声音（首次设置）

对于新品牌或新客户：

**步骤 1：分析现有内容（如果有的话）**

```bash
python scripts/brand_voice_analyzer.py existing_content.txt
```

**步骤 2：定义品牌声音特征**

- 查阅 `references/brand_guidelines.md` 中的品牌人格原型。
- 选择主要和次要的人格原型。
- 选择 3-5 个语气特征。
- 将这些特征记录在品牌指南中。

**步骤 3：创建声音样本**

- 用选定的品牌声音风格撰写 3 篇样本内容。
- 使用分析工具测试内容的一致性。
- 根据测试结果进行调整。

### 工作流程 2：创建 SEO 优化的博客文章

**步骤 1：关键词研究**

- 确定主要关键词（每月搜索量在 500-5000 次之间）。
- 找到 3-5 个次要关键词。
- 列出 10-15 个长尾关键词（LSI 关键词）。

**步骤 2：内容结构**

- 使用 `references/content_frameworks.md` 中的博客模板。
- 在标题、首段以及 2-3 个 H2 标题中包含关键词。
- 内容长度控制在 1,500-2,500 字左右，以确保全面覆盖。

**步骤 3：优化检查**

```bash
python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
```

**步骤 4：应用 SEO 建议**

- 调整关键词密度，使其保持在 1-3% 之间。
- 确保标题结构正确。
- 添加内部和外部链接。
- 优化元描述。

### 工作流程 3：创建社交媒体内容

**步骤 1：平台选择**

- 根据目标受众选择合适的社交媒体平台。
- 查阅 `references/social_media_optimization.md` 中的平台特定指南。

**步骤 2：内容调整**

- 以博客文章或核心信息为基础进行创作。
- 使用 `references/content_frameworks.md` 中的内容复用矩阵。
- 根据每个平台的要求进行调整。

**步骤 3：优化检查**

- 确保内容长度符合平台要求。
- 选择合适的发布时间。
- 图片尺寸要符合平台规范。
- 使用平台特定的标签（hashtags）。
- 添加互动元素（如投票、问题等）。

### 工作流程 4：规划内容日历

**步骤 1：月度规划**

- 复制 `assets/content_calendar_template.md`。
- 设定月度目标和关键绩效指标（KPIs）。
- 确定关键的活动或主题。

**步骤 2：每周内容分配**

- 遵循 40/25/25/10 的内容分配比例。
- 在一周内均衡发布内容到各个平台。
- 确保发布时间符合平台的最佳时机。

**步骤 3：批量创作**

- 一次性完成所有每周的内容创作。
- 保持各篇文章风格的一致性。
- 同时准备所有视觉素材。

---

## 工具

### 品牌声音分析器

分析文本内容，评估其声音特征、可读性和一致性。

**使用方法：**

```bash
# Human-readable output
python scripts/brand_voice_analyzer.py content.txt

# JSON output for integrations
python scripts/brand_voice_analyzer.py content.txt json
```

**参数：**

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `file` | 是 | 内容文件的路径 |
| `format` | 否 | 输出格式：`text`（默认）或 `json` |

**输出：**

- 品牌声音特征（正式程度、语气、视角）
- 可读性评分（Flesch Reading Ease）
- 句子结构分析
- 优化建议

### SEO 优化器

分析内容以进行 SEO 优化，并提供可操作的改进建议。

**使用方法：**

```bash
# Basic analysis
python scripts/seo_optimizer.py article.md "main keyword"

# With secondary keywords
python scripts/seo_optimizer.py article.md "main keyword" "secondary,keywords,list"

# JSON output
python scripts/seo_optimizer.py article.md "keyword" --json
```

**参数：**

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `file` | 是 | 内容文件的路径（md 或 html 格式） |
| `primary_keyword` | 是 | 主要目标关键词 |
| `secondary_keywords` | 否 | 用逗号分隔的次要关键词 |
| `--json` | 否 | 输出格式为 JSON |

**输出：**

- SEO 评分（0-100 分）
- 关键词密度分析
- 结构评估
- 元标签建议
- 具体的优化建议

---

## 参考指南

### 各参考指南的适用场景

**references/brand_guidelines.md**

- 设置新的品牌声音
- 确保内容的一致性
- 培训新团队成员
- 解决关于品牌声音/语气的问题

**references/content_frameworks.md**

- 在开始新内容创作时使用
- 规范不同类型的内容结构
- 创建内容模板
- 规划内容的复用

**references/social_media_optimization.md**

- 平台特定的优化策略
- 标签策略制定
- 了解算法相关因素
- 设置分析跟踪

**references/analytics_guide.md**

- 跟踪内容表现
- 设置测量框架
- 创建绩效报告
- 建立内容归因模型

---

## 最佳实践

### 内容创作流程

1. 从受众的需求和痛点出发。
2. 在写作前进行充分研究。
3. 使用模板制定大纲。
4. 先撰写初稿，不进行编辑。
5. 进行 SEO 优化。
6. 根据品牌声音调整内容。
7. 校对并核实事实。
8. 根据平台要求进行优化。
9. 战略性地安排发布时间。

### 质量指标

- SEO 评分高于 75/100。
- 内容的可读性适合目标受众。
- 全文保持一致的品牌声音。
- 清晰的价值主张。
- 提供可操作的行动建议。
- 视觉格式符合要求。
- 内容针对特定平台进行了优化。

### 常见误区

- 在研究关键词之前就开始写作。
- 忽视平台的具体要求。
- 品牌声音不一致。
- 过度优化 SEO（关键词堆砌）。
- 发布前不进行校对。
- 忽略分析反馈。

---

## 集成点

本技能最适合与以下工具和平台集成：

- **分析平台**：Google Analytics、社交媒体分析工具（参见 `references/analytics_guide.md`）。
- **SEO 工具**：用于关键词研究和竞争分析。
- **设计工具**：Canva、Figma（用于制作视觉内容）。
- **内容调度平台**：Buffer、Hootsuite（用于内容分发）。
- **电子邮件营销系统**：用于发送新闻通讯。