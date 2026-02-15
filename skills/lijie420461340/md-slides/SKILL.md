---
name: md-slides
description: 使用 Marp 从 Markdown 创建演示文稿——简单的语法，专业的输出
author: claude-office-skills
version: "1.0"
tags: [presentation, marp, markdown, pdf, pptx]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: marp
  url: https://github.com/marp-team/marp
  stars: 3.1k
---

# Markdown Slides Skill

## 概述

该技能允许您使用 **Marp** 从纯 Markdown 格式创建演示文稿。您可以使用熟悉的 Markdown 语法编写幻灯片内容，并将其导出为 PDF、PPTX 或带有专业主题的 HTML 格式。

## 使用方法

1. 编写或提供 Markdown 内容。
2. 我会使用相应的指令将内容格式化为适合 Marp 使用的格式。
3. 将格式化后的内容导出为您所需的格式（PDF/PPTX/HTML）。

**示例提示：**
- “将我的笔记转换为演示文稿。”
- “根据这段 Markdown 代码生成幻灯片。”
- “使用 Markdown 创建一个提案演示文稿。”
- “根据这个大纲生成 PDF 幻灯片。”

## 相关知识

### 基本语法

```markdown
---
marp: true
---

# First Slide

Content here

---

# Second Slide

- Bullet 1
- Bullet 2
```

### 主题（Themes）

```markdown
---
marp: true
theme: default  # default, gaia, uncover
---
```

### 指令（Directives）

```markdown
---
marp: true
theme: gaia
class: lead        # Centered title
paginate: true     # Page numbers
header: 'Header'   # Header text
footer: 'Footer'   # Footer text
backgroundColor: #fff
---
```

### 图片（Images）

```markdown
![width:500px](image.png)
![bg](background.jpg)
![bg left:40%](sidebar.jpg)
```

### 列（Columns）

```markdown
<div class="columns">
<div>

## Left

Content

</div>
<div>

## Right

Content

</div>
</div>
```

## 示例

```markdown
---
marp: true
theme: gaia
paginate: true
---

<!-- _class: lead -->

# Project Update

Q4 2024 Review

---

# Highlights

- Revenue: +25%
- Users: +50%
- NPS: 72

---

# Roadmap

| Q1 | Q2 | Q3 | Q4 |
|----|----|----|-----|
| MVP | Beta | Launch | Scale |

---

<!-- _class: lead -->

# Thank You!

questions@company.com
```

## 命令行工具（CLI）使用方法

```bash
# Install
npm install -g @marp-team/marp-cli

# Convert
marp slides.md -o presentation.pdf
marp slides.md -o presentation.pptx
marp slides.md -o presentation.html
```

## 资源

- [Marp 文档](https://marp.app/)
- [GitHub](https://github.com/marp-team/marp)