---
name: pptx-creator
description: 根据提供的文档内容，以下是翻译后的中文版本：

**创建专业的 PowerPoint 演示文稿：**

您可以使用该工具根据大纲、数据源或 AI 生成的内容来创建专业的 PowerPoint 演示文稿。该工具支持自定义模板、样式预设，以及从数据中生成图表/表格和图片的功能。适用于需要制作幻灯片、提案文档、报告或演示文稿的各种场景。

**主要特点：**
- **基于大纲/数据源/AI 生成内容**：支持根据用户提供的大纲、数据源或 AI 生成的内容来构建演示文稿。
- **自定义模板与样式**：提供丰富的自定义模板和样式选项，以满足不同场景的需求。
- **数据驱动的可视化**：能够从数据中自动生成图表和表格，提升演示文稿的直观性。
- **AI 生成的图片**：利用 AI 技术生成高质量的图片，增强演示文稿的视觉效果。
- **多用途应用**：适用于制作各种类型的演示文稿，如商业提案、报告或教学材料。

**使用场景：**
- **商业演示**：用于向客户或团队展示项目方案、产品功能或市场分析。
- **报告制作**：用于生成结构清晰、数据支持的报告。
- **教学用途**：帮助教师或学生制作包含图表和动画的讲解材料。

**总结：**  
该工具结合了手动设计和自动化生成的优点，能够帮助用户高效地创建专业、美观的 PowerPoint 演示文稿，适用于多种专业场景。
homepage: https://python-pptx.readthedocs.io
metadata: {"clawdbot":{"emoji":"📽️","requires":{"bins":["uv"]}}}
---

# PowerPoint Creator

该工具能够根据大纲、主题或数据源生成专业的演示文稿。

## 快速入门

### 从大纲/Markdown格式开始
```bash
uv run {baseDir}/scripts/create_pptx.py --outline outline.md --output deck.pptx
```

### 从主题开始创建演示文稿
```bash
uv run {baseDir}/scripts/create_pptx.py --topic "Q4 Sales Review" --slides 8 --output review.pptx
```

### 使用样式模板
```bash
uv run {baseDir}/scripts/create_pptx.py --outline outline.md --template corporate --output deck.pptx
```

### 从JSON格式开始创建演示文稿
```bash
uv run {baseDir}/scripts/create_pptx.py --json slides.json --output deck.pptx
```

## 大纲格式（Markdown）
```markdown
# Presentation Title
subtitle: Annual Review 2026
author: Your Name

## Introduction
- Welcome and agenda
- Key objectives for today
- ![image](generate: modern office building, minimalist style)

## Market Analysis
- chart: bar
- data: sales_by_region.csv
- Market grew 15% YoY
- Strong competitive position

## Financial Summary
- table: quarterly_results
- Strong Q4 performance
- Revenue targets exceeded
```

## JSON格式
```json
{
  "title": "Quarterly Review",
  "subtitle": "Q4 Performance",
  "author": "Your Name",
  "template": "corporate",
  "slides": [
    {
      "title": "Introduction",
      "layout": "title_and_content",
      "bullets": ["Welcome", "Agenda", "Goals"],
      "notes": "Speaker notes here"
    },
    {
      "title": "Revenue Chart",
      "layout": "chart",
      "chart_type": "bar"
    },
    {
      "title": "Team",
      "layout": "image_and_text",
      "image": "generate: professional team collaboration, corporate style",
      "bullets": ["Leadership", "Sales", "Operations"]
    }
  ]
}
```

## 内置的样式模板

- `minimal`：简洁的白色背景，使用Helvetica Neue字体，蓝色点缀（默认样式）
- `corporate`：专业的蓝色背景，使用Arial字体，适合商务场合
- `creative`：使用粗体橙色文字，Avenir字体，风格现代
- `dark`：深色背景，使用SF Pro字体，带有青色点缀
- `executive`：金色点缀，使用Georgia/Calibri字体，风格优雅
- `startup`：紫色点缀，使用Poppins/Inter字体，适合创业演示文稿

### 生成所有可用模板
```bash
uv run {baseDir}/scripts/create_template.py --all
```

### 列表模板
```bash
uv run {baseDir}/scripts/create_pptx.py --list-templates
```

## 自定义模板

### 将现有的PPTX文件保存为模板
```bash
uv run {baseDir}/scripts/create_pptx.py --save-template "my-brand" --from existing.pptx
```

### 分析模板结构
```bash
uv run {baseDir}/scripts/analyze_template.py existing.pptx
uv run {baseDir}/scripts/analyze_template.py existing.pptx --json
```

### 基于自定义模板创建新的演示文稿
```bash
uv run {baseDir}/scripts/use_template.py \
  --template my-brand \
  --slides content.json \
  --keep-slides 2 \
  --output presentation.pptx
```

## 数据源

- **CSV/Excel文件**：可以导入CSV或Excel格式的数据用于演示文稿
```markdown
## Regional Sales
- chart: pie
- data: sales.csv
- columns: region, revenue
```

- **内联数据**：可以直接在演示文稿中插入数据
```markdown
## Quarterly Comparison
- chart: bar
- data:
  - Q1: 120
  - Q2: 145  
  - Q3: 132
  - Q4: 178
```

## 图片生成

- 可以使用兼容的图片生成技术来在演示文稿中插入图片：
```markdown
## Our Vision
- ![hero](generate: futuristic cityscape, clean energy, optimistic)
- Building tomorrow's solutions
```

- 也可以通过JSON格式导入图片数据：
```json
{
  "title": "Innovation",
  "image": {
    "generate": "abstract technology visualization, blue tones",
    "position": "right",
    "size": "half"
  }
}
```

## 演示文稿布局选项

- `title`：仅包含标题的幻灯片
- `title_and_content`：包含标题和列表项的幻灯片（默认布局）
- `two_column`：并排显示内容的幻灯片
- `image_and_text`：包含图片和文本的幻灯片
- `chart`：仅包含图表的幻灯片
- `table`：包含数据表格的幻灯片
- `section`：用于分隔不同内容的幻灯片
- `blank`：空白幻灯片，可用于自定义内容

## 图表类型

- `bar`：条形图
- `column`：柱状图
- `line`：折线图
- `pie`：饼图
- `doughnut`：甜甜圈图
- `area`：面积图
- `scatter`：散点图

## 示例

- **创业演示文稿（Pitch Deck）**
```bash
uv run {baseDir}/scripts/create_pptx.py \
  --topic "Series A pitch for tech startup" \
  --slides 10 \
  --template startup \
  --output pitch-deck.pptx
```

- **高管报告**
```bash
uv run {baseDir}/scripts/create_pptx.py \
  --outline report.md \
  --template executive \
  --output board-report.pptx
```

- **营销演示文稿**
```bash
uv run {baseDir}/scripts/create_pptx.py \
  --outline campaign.md \
  --template creative \
  --output marketing-deck.pptx
```