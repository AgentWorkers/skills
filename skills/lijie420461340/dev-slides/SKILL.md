---
name: dev-slides
description: 使用 Slidev 创建对开发者友好的演示文稿：基于 Vue 的幻灯片工具，支持代码执行功能
author: claude-office-skills
version: "1.0"
tags: [presentation, slidev, vue, developer, code]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: slidev
  url: https://github.com/slidevjs/slidev
  stars: 44k
---

# 开发者幻灯片技能

## 概述

该技能支持使用 **Slidev**（一个基于 Vue 的幻灯片制作框架）来创建以开发者为中心的演示文稿。您可以使用 Markdown 格式编写幻灯片，并在其中添加实时代码演示、图表和自定义组件。

## 使用方法

1. 描述您的技术演示需求；
2. 我将为您生成符合 Slidev 标准语法的 Markdown 代码；
3. 生成的代码中会包含代码块、图表和 Vue 组件。

**示例提示：**
- “创建一个 Vue.js 工作坊演示文稿”；
- “制作包含实时代码执行的幻灯片”；
- “制作包含图表的技术演讲幻灯片”；
- “制作开发者入职培训用的幻灯片”。

## 相关领域知识

### Slidev 基础知识
```markdown
---
theme: default
title: My Presentation
---

# Welcome

This is the first slide

---

# Second Slide

Content here
```

### 幻灯片分隔符
```markdown
---   # New horizontal slide

---   # Another slide
layout: center
---

# Centered Content
```

### 布局方式
```markdown
---
layout: cover
---
# Title Slide

---
layout: intro
---
# Introduction

---
layout: center
---
# Centered

---
layout: two-cols
---
# Left
::right::
# Right

---
layout: image-right
image: ./image.png
---
# Content with Image
```

### 代码块
```markdown
# Code Example

\`\`\`ts {all|1|2-3|4}
const name = 'Slidev'
const greeting = \`Hello, \${name}!\`
console.log(greeting)
// Outputs: Hello, Slidev!
\`\`\`

<!-- Lines highlighted step by step -->
```

### Monaco 编辑器（实时代码编辑）
```markdown
\`\`\`ts {monaco}
// Editable code block
function add(a: number, b: number) {
  return a + b
}
\`\`\`

\`\`\`ts {monaco-run}
// Runnable code
console.log('Hello from Slidev!')
\`\`\`
```

### 图表（Mermaid）
```markdown
\`\`\`mermaid
graph LR
  A[Start] --> B{Decision}
  B -->|Yes| C[Action 1]
  B -->|No| D[Action 2]
\`\`\`

\`\`\`mermaid
sequenceDiagram
  Client->>Server: Request
  Server-->>Client: Response
\`\`\`
```

### Vue 组件
```markdown
<Counter :count="10" />

<Tweet id="1390115482657726468" />

<!-- Custom component -->
<MyComponent v-click />
```

### 动画效果
```markdown
<v-click>

This appears on click

</v-click>

<v-clicks>

- Item 1
- Item 2
- Item 3

</v-clicks>

<!-- Or with v-click directive -->
<div v-click>Animated content</div>
```

### 文档头部（Frontmatter）
```yaml
---
theme: seriph
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: true
drawings:
  persist: false
css: unocss
---
```

## 示例

### 示例：API 工作坊演示文稿
```markdown
---
theme: seriph
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
---

# REST API Workshop

Building Modern APIs with Node.js

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer">
    Press Space for next page <carbon:arrow-right />
  </span>
</div>

---
layout: two-cols
---

# What We'll Cover

<v-clicks>

- RESTful principles
- Express.js basics
- Authentication
- Error handling
- Testing

</v-clicks>

::right::

\`\`\`ts
// Preview
const app = express()
app.get('/api/users', getUsers)
app.listen(3000)
\`\`\`

---

# Live Demo

\`\`\`ts {monaco-run}
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
]

console.log(JSON.stringify(users, null, 2))
\`\`\`

---
layout: center
---

# Questions?

[GitHub](https://github.com) · [Documentation](https://docs.example.com)
```

## 安装方法
```bash
npm init slidev@latest
```

## 资源

- [Slidev 官方文档](https://sli.dev/)
- [GitHub 仓库](https://github.com/slidevjs/slidev)
- [主题模板](https://sli.dev/themes/gallery.html)