---
name: infographic-generation
description: 使用 each::sense AI 生成专业的信息图。这些信息图可以是统计类、流程类、对比类、时间线类、列表类、地理类、层次结构类、简历类、报告类以及社交媒体类信息图，均经过优化，以便于视觉传达。
metadata:
  author: eachlabs
  version: "1.0"
---
# 信息图生成

使用 `each-sense` 功能生成专业且视觉效果出色的信息图。该技能能够创建基于数据的信息可视化内容，适用于演示文稿、报告、社交媒体和营销材料。

## 主要功能

- **统计信息图**：包含图表、图形和关键指标的数据可视化展示
- **流程/操作指南信息图**：分步骤的可视化教程
- **对比信息图**：产品、服务或概念的并排对比
- **时间线信息图**：历史事件、项目里程碑或公司发展历程
- **列表信息图**：前十名榜单、实用技巧、功能介绍等
- **地理/地图信息图**：基于位置的数据和区域统计信息
- **层次结构信息图**：组织结构图、分类体系图、流程图
- **简历信息图**：可视化的简历和职业简介
- **报告信息图**：年度报告、季度总结、研究成果
- **社交媒体信息图**：针对不同平台优化的视觉内容

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a statistical infographic showing global renewable energy adoption rates with bar charts and key statistics",
    "mode": "max"
  }'
```

## 信息图类型及最佳实践

| 类型 | 适用场景 | 关键元素 |
|------|----------|--------------|
| 统计信息图 | 数据展示、研究成果 | 图表、图形、百分比、图标 |
| 流程信息图 | 操作指南、工作流程 | 编号步骤、箭头、图标 |
| 对比信息图 | 产品对比、决策辅助 | 并排布局、勾选框、评分 |
| 时间线信息图 | 历史事件、项目计划 | 线性时间轴、日期、里程碑 |
| 列表信息图 | 实用技巧、功能介绍 | 数字、项目符号、图标 |
| 地理信息图 | 区域数据、市场分析 | 地图、位置标记、区域统计 |
| 层次结构信息图 | 组织结构图、分类体系图 | 树状图、方框、连接线 |
| 简历信息图 | 个人简历 | 技能展示、时间线、图标 |
| 报告信息图 | 业务总结、数据分析 | 多个章节、关键绩效指标（KPI）、图表 |
| 社交媒体信息图 | 互动性强的视觉内容 | 适合平台的特点、醒目的文字、简洁的图形 |

## 使用案例示例

### 1. 统计信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a statistical infographic about global coffee consumption. Include: bar chart showing top 5 consuming countries, pie chart of coffee types (espresso, latte, cappuccino, etc.), key stats like 2.25 billion cups consumed daily, and icons representing coffee culture. Modern minimal design with warm brown and cream color palette. Portrait orientation.",
    "mode": "max"
  }'
```

### 2. 流程/操作指南信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a how-to infographic for making sourdough bread. Show 8 steps: 1) Create starter, 2) Feed starter, 3) Mix dough, 4) Autolyse, 5) Stretch and fold, 6) Bulk ferment, 7) Shape and proof, 8) Bake. Use illustrated icons for each step, numbered circles, arrows showing flow. Rustic warm color scheme. Vertical layout.",
    "mode": "max"
  }'
```

### 3. 对比信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comparison infographic: Electric Cars vs Gas Cars. Compare: Initial cost, Fuel/charging costs, Maintenance costs, Environmental impact, Range, Charging/refueling time. Use side-by-side layout with green for electric and gray for gas. Include icons for each category, checkmarks for advantages. Clean modern design.",
    "mode": "max"
  }'
```

### 4. 时间线信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a timeline infographic showing the history of artificial intelligence. Key milestones: 1950 Turing Test proposed, 1956 Dartmouth Conference (AI term coined), 1966 ELIZA chatbot, 1997 Deep Blue beats Kasparov, 2011 IBM Watson wins Jeopardy, 2012 Deep Learning breakthrough, 2016 AlphaGo beats Lee Sedol, 2022 ChatGPT released. Horizontal timeline with alternating above/below entries, tech-inspired blue color scheme, circuit board design elements.",
    "mode": "max"
  }'
```

### 5. 列表信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a list infographic: Top 10 Productivity Tips for Remote Workers. Include: 1) Create dedicated workspace, 2) Set regular hours, 3) Take scheduled breaks, 4) Use time-blocking, 5) Minimize distractions, 6) Dress for work, 7) Stay connected with team, 8) Set boundaries, 9) Exercise daily, 10) End work ritual. Use numbered list format with icons for each tip, modern gradient purple and blue color scheme, clean typography.",
    "mode": "max"
  }'
```

### 6. 地理/地图信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a geographic infographic showing internet penetration rates across continents. Include a world map with color-coded regions: North America 93%, Europe 89%, South America 75%, Asia 64%, Africa 43%. Add data callouts for top 5 countries by users. Use a tech-inspired blue gradient for high penetration to gray for low. Include legend and source citation area.",
    "mode": "max"
  }'
```

### 7. 层次结构信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a hierarchical infographic showing a typical tech startup organizational structure. CEO at top, branching to: CTO (with Engineering Manager, then Frontend/Backend/DevOps teams), CPO (with Product Managers, UX Designers), CFO (with Finance, HR), CMO (with Marketing, Sales). Use tree diagram format with connecting lines, professional corporate blue and gray colors, rounded rectangles for each role, icons representing each department.",
    "mode": "max"
  }'
```

### 8. 简历信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a visual resume infographic for a UX Designer. Include sections: Profile summary with placeholder for photo, Skills with horizontal progress bars (Figma 95%, User Research 90%, Prototyping 85%, HTML/CSS 70%), Work experience as vertical timeline (2020-2023 Senior UX at TechCorp, 2017-2020 UX Designer at StartupXYZ), Education icons, Contact info with icons. Modern minimalist design, teal and dark gray color scheme, A4 portrait.",
    "mode": "max"
  }'
```

### 9. 报告信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an annual report infographic for a SaaS company. Include: Header with company logo placeholder and year 2024, Key metrics section (Revenue $12M up 45%, Customers 5,000+ up 60%, Team size 85 up 30%, NPS score 72), Revenue growth line chart, Customer acquisition funnel, Geographic expansion map showing presence in 25 countries, Product milestones timeline. Professional corporate design, navy blue and gold accent colors.",
    "mode": "max"
  }'
```

### 10. 社交媒体信息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a square 1:1 social media infographic about benefits of meditation. Title: 5 Science-Backed Benefits of Daily Meditation. Points: 1) Reduces stress hormones by 23%, 2) Improves focus and concentration, 3) Better sleep quality, 4) Lower blood pressure, 5) Increased emotional well-being. Bold readable text, calming purple and teal gradient background, simple icons for each benefit, Instagram-optimized with high contrast for mobile viewing.",
    "mode": "max"
  }'
```

## 多轮创意迭代

使用 `session_id` 进行信息图设计的多次迭代：

```bash
# Initial infographic
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an infographic about climate change impacts with key statistics and a world map",
    "session_id": "climate-infographic-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more emphasis on ocean temperature data and include a temperature anomaly chart",
    "session_id": "climate-infographic-001"
  }'

# Request color variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an alternate version with a warmer color palette using oranges and reds to emphasize urgency",
    "session_id": "climate-infographic-001"
  }'
```

## 批量生成以进行 A/B 测试

生成多个信息图版本以进行测试：

```bash
# Variation A - Minimalist style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist infographic about healthy eating habits, white background, simple line icons, lots of whitespace",
    "mode": "eco"
  }'

# Variation B - Bold colorful style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bold colorful infographic about healthy eating habits, vibrant gradients, filled icons, energetic design",
    "mode": "eco"
  }'

# Variation C - Corporate professional style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate professional infographic about healthy eating habits, navy and gray colors, formal typography, business report style",
    "mode": "eco"
  }'
```

## 最佳实践

### 设计原则
- **视觉层次**：利用大小、颜色和布局引导观众的视线
- **一致性**：在整个设计中保持图标、颜色和字体的统一性
- **留白**：避免元素过于拥挤，确保视觉清晰
- **数据准确性**：按比例准确地呈现数据
- **可读性**：使用足够的对比度和易读的字体大小

### 内容指南
- **核心信息**：突出一个主要信息点
- **便于扫描**：设计时要便于快速浏览，标题要清晰
- **来源标注**：注明数据来源以提高可信度
- **行动号召**：在适当的地方提供下一步操作建议

### 平台优化建议
| 平台 | 推荐尺寸 | 注意事项 |
|----------|-----------------|-------|
| Pinterest | 1000x1500 (2:3) | 高宽比为 2:3 的格式效果最佳 |
| Instagram 主页 | 1080x1080 (1:1) | 正方形格式 |
| Instagram Stories | 1080x1920 (9:16) | 全屏垂直格式 |
| LinkedIn | 1200x627 (1.91:1) | 横屏格式 |
| Twitter/X | 1200x675 (16:9) | 横屏格式 |
| 博客/网页 | 800x2000+ | 长格式垂直布局 |
| 演示文稿 | 1920x1080 (16:9) | 幻灯片格式 |

## 信息图制作提示

在制作信息图时，请包含以下细节：

1. **类型**：指定信息图的类型（统计、流程、时间线等）
2. **主题**：明确说明内容主题
3. **数据点**：提供具体的数字、统计数据或内容项
4. **布局**：说明信息图的方向（竖屏/横屏）和结构
5. **风格**：描述所需的设计风格（简约、醒目、企业风格或趣味性）
6. **颜色**：指定颜色方案或品牌颜色
7. **用途**：说明信息图的使用场景（社交媒体、演示文稿、打印材料）

### 示例提示结构

```
"Create a [type] infographic about [topic].
Include: [specific data points, sections, or elements].
Layout: [orientation and structure].
Style: [aesthetic description].
Colors: [color palette].
For: [intended platform/use]."
```

## 制作模式选择

在生成信息图之前，请询问用户：

**“您需要快速且低成本的信息图，还是高质量的信息图？”**

| 制作模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终设计、客户演示文稿、打印材料 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、A/B 测试 | 较快 | 适合初步设计 |

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 平台上补充数据 |
| 内容违规 | 内容不符合规定 | 调整提示内容 |
| 超时 | 生成过程复杂 | 将客户端的超时时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `data-visualization`：图表和图形制作工具
- `presentation-design`：幻灯片设计和演示材料制作
- `social-media-graphics`：针对不同平台的视觉内容优化工具