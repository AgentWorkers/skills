---
name: slide-maker
description: "Presentation and slide deck generator. Create outlines, full slide decks, speaker notes, pitch decks, training slides, report presentations, and design recommendations. Outputs Markdown with 
---

# 🎬 幻灯片制作工具 — 演示文稿生成器

> 仅需一个命令，即可将大纲转换为完整的幻灯片集。再也不用面对空白的幻灯片发愁了。

## 📌 使用场景

### 🏢 工作报告 → `report`
用于制作包含数据驱动内容的周/月/季度评审幻灯片。

### 💰 筹款 → `pitch`
标准的10-15页提案幻灯片，涵盖问题、解决方案、市场分析、商业模式、团队介绍以及资金需求。

### 📚 培训与研讨会 → `training`
包含目标、内容、练习和总结的课程幻灯片，非常适合内部培训或研讨会使用。

### 🎤 演讲准备 → `speaker`
自动生成包含时间安排和过渡语的演讲稿，让您在舞台上充满自信。

### 📝 快速大纲 → `outline`
还不确定内容结构？先创建大纲，再逐步填充内容。

### 📊 完整内容 → `slides`
可以直接使用Markdown格式（使用`---`作为页面分隔符）将大纲转换为完整的幻灯片集。

### 🎨 设计指南 → `design`
提供配色方案、字体选择和布局建议，让您的幻灯片看起来更加专业。

## 💡 输出格式

每张幻灯片之间使用`---`分隔，采用Markdown格式。可以直接导入到Marp、Slidev或Reveal.js等工具中。

```
# Title Page
---
## Slide Two
- Point 1
- Point 2
---
## Slide Three
```

## 📂 脚本
- `scripts/slides.sh` — 主脚本