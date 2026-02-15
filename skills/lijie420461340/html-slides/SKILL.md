---
name: html-slides
description: 使用reveal.js创建交互式HTML演示文稿——reveal.js是网络上最受欢迎的演示文稿框架。
author: claude-office-skills
version: "1.0"
tags: [presentation, reveal.js, html, slides, interactive]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: reveal.js
  url: https://github.com/hakimel/reveal.js
  stars: 70.5k
---

# HTML幻灯片制作技能

## 概述

该技能允许您使用**reveal.js**（目前最流行的Web演示框架）来创建精美的HTML演示文稿。您可以制作包含动画、代码高亮显示、演讲者备注等功能的交互式、响应式幻灯片。

## 使用方法

1. 描述您想要制作的演示文稿内容。
2. 指定所需的主题、过渡效果及其他功能。
3. 我将为您生成相应的reveal.js演示文稿。

**示例提示：**
- “制作一个关于我们产品的交互式演示文稿。”
- “创建一个带有代码高亮显示功能的演示文稿。”
- “制作一个包含演讲者备注和计时器的演示文稿。”
- “制作包含动画和过渡效果的幻灯片。”

## 相关知识

### reveal.js基础

```html
<!doctype html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/black.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section>Slide 1</section>
            <section>Slide 2</section>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
    <script>Reveal.initialize();</script>
</body>
</html>
```

### 幻灯片结构

```html
<!-- Horizontal slides -->
<section>Slide 1</section>
<section>Slide 2</section>

<!-- Vertical slides (nested) -->
<section>
    <section>Vertical 1</section>
    <section>Vertical 2</section>
</section>

<!-- Markdown slides -->
<section data-markdown>
    <textarea data-template>
        ## Slide Title
        - Point 1
        - Point 2
    </textarea>
</section>
```

### 主题

内置主题：`black`、`white`、`league`、`beige`、`sky`、`night`、`serif`、`simple`、`solarized`、`blood`、`moon`

```html
<link rel="stylesheet" href="reveal.js/dist/theme/moon.css">
```

### 过渡效果

```javascript
Reveal.initialize({
    transition: 'slide',  // none, fade, slide, convex, concave, zoom
    transitionSpeed: 'default',  // default, fast, slow
    backgroundTransition: 'fade'
});
```

### 动画效果

```html
<section>
    <p class="fragment">Appears first</p>
    <p class="fragment fade-in">Then this</p>
    <p class="fragment fade-up">Then this</p>
    <p class="fragment highlight-red">Highlight</p>
</section>
```

动画效果类型：`fade-in`（淡入）、`fade-out`（淡出）、`fade-up`（淡入）、`fade-down`（淡出）、`fade-left`（向左淡入）、`fade-right`（向右淡入）、`highlight-red`（高亮显示为红色）、`highlight-blue`（高亮显示为蓝色）、`highlight-green`（高亮显示为绿色）、`strike`（划线效果）

### 代码高亮显示

```html
<section>
    <pre><code data-trim data-line-numbers="1|3-4">
def hello():
    print("Hello")
    print("World")
    return True
    </code></pre>
</section>
```

### 演讲者备注

```html
<section>
    <h2>Slide Title</h2>
    <p>Content</p>
    <aside class="notes">
        Speaker notes go here. Press 'S' to view.
    </aside>
</section>
```

### 背景图片

```html
<!-- Color background -->
<section data-background-color="#4d7e65">

<!-- Image background -->
<section data-background-image="image.jpg" data-background-size="cover">

<!-- Video background -->
<section data-background-video="video.mp4">

<!-- Gradient background -->
<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
```

### 配置选项

```javascript
Reveal.initialize({
    // Display controls
    controls: true,
    controlsTutorial: true,
    progress: true,
    slideNumber: true,
    
    // Behavior
    hash: true,
    respondToHashChanges: true,
    history: true,
    keyboard: true,
    overview: true,
    center: true,
    touch: true,
    loop: false,
    rtl: false,
    shuffle: false,
    
    // Timing
    autoSlide: 0,  // 0 = disabled
    autoSlideStoppable: true,
    
    // Appearance
    width: 960,
    height: 700,
    margin: 0.04,
    minScale: 0.2,
    maxScale: 2.0,
    
    // Plugins
    plugins: [RevealMarkdown, RevealHighlight, RevealNotes]
});
```

## 示例

### 示例1：技术讲座
```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>API Design Best Practices</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/night.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/monokai.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section data-background-gradient="linear-gradient(to bottom right, #1a1a2e, #16213e)">
                <h1>API Design</h1>
                <h3>Best Practices for 2024</h3>
                <p><small>Engineering Team</small></p>
            </section>
            
            <section>
                <h2>Agenda</h2>
                <ol>
                    <li class="fragment">RESTful Principles</li>
                    <li class="fragment">Authentication</li>
                    <li class="fragment">Error Handling</li>
                    <li class="fragment">Documentation</li>
                </ol>
            </section>
            
            <section>
                <section>
                    <h2>RESTful Principles</h2>
                </section>
                <section>
                    <h3>Resource Naming</h3>
                    <pre><code data-trim class="language-http">
GET /users           # Collection
GET /users/123       # Single resource
POST /users          # Create
PUT /users/123       # Update
DELETE /users/123    # Delete
                    </code></pre>
                </section>
            </section>
            
            <section>
                <h2>Questions?</h2>
                <p>api-team@company.com</p>
            </section>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/plugin/highlight/highlight.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            plugins: [RevealHighlight]
        });
    </script>
</body>
</html>
```

### 示例2：产品发布会
```html
<!doctype html>
<html>
<head>
    <title>Product Launch</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/theme/white.css">
    <style>
        .reveal h1 { color: #2d3748; }
        .metric { font-size: 3em; color: #3182ce; }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <section data-background-color="#f7fafc">
                <h1>Introducing</h1>
                <h2 style="color: #3182ce;">ProductX 2.0</h2>
            </section>
            
            <section>
                <h2>The Problem</h2>
                <p class="fragment">Teams waste <span class="metric">20%</span> of time on manual tasks</p>
            </section>
            
            <section data-auto-animate>
                <h2>Our Solution</h2>
                <div data-id="box" style="background: #3182ce; padding: 20px;">
                    AI-Powered Automation
                </div>
            </section>
            
            <section data-auto-animate>
                <h2>Our Solution</h2>
                <div data-id="box" style="background: #38a169; padding: 40px; width: 400px;">
                    <p>AI-Powered Automation</p>
                    <p>90% faster</p>
                </div>
            </section>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
    <script>Reveal.initialize();</script>
</body>
</html>
```

## 资源

- [reveal.js官方文档](https://revealjs.com/)
- [GitHub仓库](https://github.com/hakimel/reveal.js)
- [演示文稿示例](https://revealjs.com/demo/)