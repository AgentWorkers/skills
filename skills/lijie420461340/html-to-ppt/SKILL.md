---
name: html-to-ppt
description: 使用 Marp 将 HTML/Markdown 文件转换为 PowerPoint 演示文稿
author: claude-office-skills
version: "1.0"
tags: [presentation, marp, markdown, html, slides]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: marp-cli
  url: https://github.com/marp-team/marp-cli
  stars: 3.1k
---

# 将Markdown或HTML转换为PowerPoint的技能

## 概述

该技能利用**Marp**（Markdown Presentation Ecosystem）工具，能够将Markdown或HTML内容转换为专业的PowerPoint演示文稿。通过简单的Markdown语法以及基于CSS的主题，您可以轻松创建美观且结构统一的幻灯片。

## 使用方法

1. 提供用于制作幻灯片的Markdown内容。
2. （可选）指定主题或自定义样式。
3. Marp会将内容转换为PowerPoint、PDF或HTML格式的幻灯片。

**示例指令：**
- “将这段Markdown内容转换为PowerPoint演示文稿。”
- “使用Marp根据这个大纲生成幻灯片。”
- “用‘gaia’主题将我的笔记制作成演示文稿。”
- “从这段Markdown内容生成PDF格式的幻灯片。”

## 相关知识

### Marp基础

Marp使用简单的语法来组织幻灯片，其中`---`用于分隔不同的幻灯片内容：

```markdown
---
marp: true
theme: default
---

# Slide 1 Title

Content for first slide

---

# Slide 2 Title

Content for second slide
```

### 命令行使用方法

```bash
# Convert to PowerPoint
marp slides.md -o presentation.pptx

# Convert to PDF
marp slides.md -o presentation.pdf

# Convert to HTML
marp slides.md -o presentation.html

# With specific theme
marp slides.md --theme gaia -o presentation.pptx
```

### 幻灯片结构

#### 基础幻灯片
```markdown
---
marp: true
---

# Title

- Bullet point 1
- Bullet point 2
- Bullet point 3
```

#### 标题幻灯片
```markdown
---
marp: true
theme: gaia
class: lead
---

# Presentation Title

## Subtitle

Author Name
Date
```

### 前言部分（Frontmatter）的设置选项
```yaml
---
marp: true
theme: default          # default, gaia, uncover
size: 16:9              # 4:3, 16:9, or custom
paginate: true          # Show page numbers
header: 'Company Name'  # Header text
footer: 'Confidential'  # Footer text
backgroundColor: #fff
backgroundImage: url('bg.png')
---
```

### 主题

#### 内置主题
```markdown
---
marp: true
theme: default   # Clean, minimal
---

---
marp: true
theme: gaia      # Colorful, modern
---

---
marp: true
theme: uncover   # Bold, presentation-focused
---
```

#### 主题样式（Theme Classes）
```markdown
---
marp: true
theme: gaia
class: lead     # Centered title slide
---

---
marp: true
theme: gaia
class: invert   # Inverted colors
---
```

### 格式化

#### 文本样式
```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

`inline code`

> Blockquote for emphasis
```

#### 列表
```markdown
- Unordered item
- Another item
  - Nested item

1. Ordered item
2. Second item
   1. Nested numbered
```

#### 代码块
```markdown
# Code Example

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`
```

#### 表格
```markdown
| Feature | Status |
|---------|--------|
| Tables  | ✅     |
| Charts  | ✅     |
| Images  | ✅     |
```

#### 图片

#### 基本图片
```markdown
![](image.png)
```

#### 定制大小的图片
```markdown
![width:500px](image.png)
![height:300px](image.png)
![width:80%](image.png)
```

#### 背景图片
```markdown
---
marp: true
backgroundImage: url('background.jpg')
---

# Slide with Background
```

### 高级布局

#### 双列布局
```markdown
---
marp: true
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
---

# Two Column Layout

<div class="columns">
<div>

## Left Column
- Point 1
- Point 2

</div>
<div>

## Right Column
- Point A
- Point B

</div>
</div>
```

#### 分割背景
```markdown
---
marp: true
theme: gaia
class: gaia
---

<!-- 
_backgroundImage: linear-gradient(to right, #4a90a4, #4a90a4 50%, white 50%)
-->

<div class="columns">
<div style="color: white;">

# Dark Side

</div>
<div>

# Light Side

</div>
</div>
```

### 语法指令

#### 本地指令（针对单个幻灯片）
```markdown
---
marp: true
---

<!-- 
_backgroundColor: #123
_color: white
_paginate: false
-->

# Special Slide
```

#### 局部样式设置
```markdown
---
marp: true
---

<style scoped>
h1 {
  color: red;
}
</style>

# This Title is Red
```

### 与Python的集成
```python
import subprocess
import tempfile
import os

def markdown_to_pptx(md_content, output_path, theme='default'):
    """Convert Markdown to PowerPoint using Marp."""
    
    # Add marp directive if not present
    if '---\nmarp: true' not in md_content:
        md_content = f"---\nmarp: true\ntheme: {theme}\n---\n\n" + md_content
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(md_content)
        temp_path = f.name
    
    try:
        # Convert using marp
        subprocess.run([
            'marp', temp_path, '-o', output_path
        ], check=True)
        
        return output_path
    finally:
        os.unlink(temp_path)

# Usage
md = """
# Welcome

Introduction slide

---

# Agenda

- Topic 1
- Topic 2
- Topic 3
"""

markdown_to_pptx(md, 'presentation.pptx')
```

### Node.js/marp-cli API
```javascript
const { marpCli } = require('@marp-team/marp-cli');

// Convert file
marpCli(['slides.md', '-o', 'output.pptx']).then(exitCode => {
    console.log('Done:', exitCode);
});
```

## 最佳实践

1. **每个幻灯片只包含一个主要信息**：保持幻灯片的简洁性。
2. **使用清晰的层次结构**：确保标题层级的一致性。
3. **限制文本量**：每个幻灯片最多使用6个项目符号。
4. **添加图片**：视觉内容有助于提高记忆效果。
5. **预览输出**：在最终导出前先查看预览效果。

## 常见用法

### 演示文稿生成工具
```python
def create_presentation(title, sections, output_path, theme='gaia'):
    """Generate presentation from structured data."""
    
    md_content = f"""---
marp: true
theme: {theme}
paginate: true
---

<!-- _class: lead -->

# {title}

{sections.get('subtitle', '')}

{sections.get('author', '')}

"""
    
    for section in sections.get('slides', []):
        md_content += f"""---

# {section['title']}

"""
        for point in section.get('points', []):
            md_content += f"- {point}\n"
        
        if section.get('notes'):
            md_content += f"\n<!-- Notes: {section['notes']} -->\n"
    
    md_content += """---

<!-- _class: lead -->

# Thank You!

Questions?
"""
    
    return markdown_to_pptx(md_content, output_path, theme)
```

### 批量生成幻灯片
```python
def generate_report_slides(data_list, template, output_dir):
    """Generate multiple presentations from data."""
    import os
    
    for data in data_list:
        content = template.format(**data)
        output_path = os.path.join(output_dir, f"{data['name']}_report.pptx")
        markdown_to_pptx(content, output_path)
```

## 示例

### 示例1：技术演示文稿
```markdown
---
marp: true
theme: gaia
class: lead
paginate: true
---

# API Documentation

## REST API Best Practices

Engineering Team
January 2024

---

# Agenda

1. Authentication
2. Endpoints Overview
3. Error Handling
4. Rate Limiting
5. Examples

---

# Authentication

All requests require an API key:

```
Authorization: Bearer YOUR_API_KEY
```

- Keys expire after 90 days
- Store securely, never commit to git
- Rotate regularly

---

# Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List all users |
| POST | /users | Create user |
| GET | /users/:id | Get user details |
| PUT | /users/:id | Update user |
| DELETE | /users/:id | Delete user |

---

# Error Handling

```
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "无效的电子邮件格式",
    "details": ["电子邮件必须有效"]
  }
}
```

---

<!-- _class: lead -->

# Questions?

api-support@company.com
```

### 示例2：商业提案
```python
def create_pitch_deck(company_data):
    """Generate investor pitch deck."""
    
    md = f"""---
marp: true
theme: uncover
paginate: true
---

<!-- _class: lead -->
<!-- _backgroundColor: #2d3748 -->
<!-- _color: white -->

# {company_data['name']}

{company_data['tagline']}

---

# The Problem

{company_data['problem_statement']}

**Market Pain Points:**
"""
    
    for pain in company_data['pain_points']:
        md += f"- {pain}\n"
    
    md += f"""
---

# Our Solution

{company_data['solution']}

![width:600px]({company_data.get('product_image', 'product.png')})

---

# Market Opportunity

- **TAM:** {company_data['tam']}
- **SAM:** {company_data['sam']}
- **SOM:** {company_data['som']}

---

# Traction

| Metric | Value |
|--------|-------|
| Monthly Revenue | {company_data['mrr']} |
| Customers | {company_data['customers']} |
| Growth Rate | {company_data['growth']} |

---

# The Ask

**Seeking:** {company_data['funding_ask']}

**Use of Funds:**
- Product Development: 40%
- Sales & Marketing: 35%
- Operations: 25%

---

<!-- _class: lead -->

# Let's Build the Future Together

{company_data['contact']}
"""
    
    return md

# Generate deck
pitch_data = {
    'name': 'TechStartup Inc',
    'tagline': 'AI-Powered Document Processing',
    'problem_statement': 'Businesses waste 20% of time on manual document work',
    'pain_points': ['Manual data entry', 'Error-prone processes', 'Slow turnaround'],
    'solution': 'Automated document processing with 99.5% accuracy',
    'tam': '$50B',
    'sam': '$10B',
    'som': '$500M',
    'mrr': '$100K',
    'customers': '50',
    'growth': '20% MoM',
    'funding_ask': '$5M Series A',
    'contact': 'founders@techstartup.com'
}

md_content = create_pitch_deck(pitch_data)
markdown_to_pptx(md_content, 'pitch_deck.pptx', theme='uncover')
```

## 限制事项

- 不支持复杂的动画效果。
- 部分PowerPoint特有的功能无法使用。
- 自定义字体需要通过CSS进行配置。
- 视频嵌入功能有限。
- 演讲者备注的支持较为基础。

## 安装方法

```bash
# Using npm
npm install -g @marp-team/marp-cli

# Using Homebrew
brew install marp-cli

# Verify installation
marp --version
```

## 资源链接

- [Marp官方文档](https://marp.app/)
- [Marp CLI的GitHub仓库](https://github.com/marp-team/marp-cli)
- [Marpit框架](https://marpit.marp.app/)
- [主题CSS样式指南](https://marpit.marp.app/theme-css)