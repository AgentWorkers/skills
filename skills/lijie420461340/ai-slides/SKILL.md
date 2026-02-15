---
name: ai-slides
description: 使用 AI 生成完整的演示文稿——从大纲到精美的幻灯片
author: claude-office-skills
version: "1.0"
tags: [presentation, ai, automation, slides, content]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
---

# AI Slides Skill

## 概述

该技能支持使用人工智能生成演示文稿。只需提供一个主题或大纲，即可获得结构完整、内容丰富且格式规范的演示文稿。

## 使用方法

1. 提供主题、大纲或简要的笔记；
2. 指定目标受众和演示文稿的时长；
3. 我将为您生成完整的演示文稿。

**示例提示：**
- “生成一份关于机器学习的10页演示文稿”；
- “为一家SaaS初创公司制作一份 pitching deck（推介材料）”；
- “根据这些数据制作一份季度回顾演示文稿”；

## 相关领域知识

### 演示文稿结构

```yaml
# Effective presentation structure
structure:
  - title_slide:
      title: "Clear, compelling title"
      subtitle: "Context or tagline"
      author: "Presenter name"
  
  - agenda:
      items: 3-5 main topics
  
  - introduction:
      hook: "Attention-grabbing opening"
      context: "Why this matters"
  
  - main_content:
      sections: 3-5 key points
      each_section:
        - heading
        - 3-5 bullets or visual
        - supporting data
  
  - conclusion:
      summary: "Key takeaways"
      call_to_action: "What to do next"
  
  - closing:
      thank_you: true
      contact_info: true
      qa_prompt: true
```

### 内容生成机制

```python
def generate_presentation(topic, audience, slide_count=10):
    """AI-powered presentation generation."""
    
    # 1. Generate outline
    outline = generate_outline(topic, slide_count)
    
    # 2. Expand each section
    slides = []
    for section in outline:
        slide_content = expand_section(section, audience)
        slides.append(slide_content)
    
    # 3. Add visuals suggestions
    for slide in slides:
        slide['visuals'] = suggest_visuals(slide['content'])
    
    # 4. Format as Marp markdown
    presentation = format_as_marp(slides)
    
    return presentation

def generate_outline(topic, count):
    """Generate presentation outline."""
    # Typical structure
    outline = [
        {'type': 'title', 'title': topic},
        {'type': 'agenda'},
        # Main content (60% of slides)
        # ... content slides
        {'type': 'summary'},
        {'type': 'closing'}
    ]
    return outline
```

### Marp 的输出结果

```python
def format_as_marp(slides):
    """Convert slides to Marp markdown."""
    
    marp = """---
marp: true
theme: gaia
paginate: true
---

"""
    
    for slide in slides:
        if slide['type'] == 'title':
            marp += f"""<!-- _class: lead -->

# {slide['title']}

{slide.get('subtitle', '')}

---

"""
        elif slide['type'] == 'content':
            marp += f"""# {slide['heading']}

"""
            for point in slide['points']:
                marp += f"- {point}\n"
            marp += "\n---\n\n"
    
    return marp
```

## 示例：生成技术相关演示文稿

```python
topic = "Introduction to Docker"
audience = "Developers new to containers"
slides = 10

# Generated presentation
presentation = """---
marp: true
theme: gaia
paginate: true
---

<!-- _class: lead -->

# Introduction to Docker

Containerization Made Simple

---

# Agenda

1. What is Docker?
2. Core Concepts
3. Getting Started
4. Best Practices
5. Demo

---

# What is Docker?

- Container platform for packaging applications
- Lightweight alternative to VMs
- "Build once, run anywhere"
- 15M+ developers, 7M+ applications

---

# Why Containers?

| VMs | Containers |
|-----|------------|
| GB size | MB size |
| Minutes to start | Seconds to start |
| Full OS | Shared kernel |

---

# Core Concepts

- **Image**: Blueprint/template
- **Container**: Running instance
- **Dockerfile**: Build instructions
- **Registry**: Image storage (Docker Hub)

---

# Getting Started

```bash
# 下载一张图片
docker pull nginx

# 运行容器
docker run -p 8080:80 nginx

# 列出所有容器
docker ps

```

---

# Your First Dockerfile

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

---

# Best Practices

- Use official base images
- Minimize layers
- Don't run as root
- Use .dockerignore
- Multi-stage builds

---

# Summary

✅ Docker simplifies deployment
✅ Containers are lightweight & fast
✅ Easy to get started
✅ Industry standard

---

<!-- _class: lead -->

# Questions?

Resources: docs.docker.com
"""
```

## 最佳实践

1. **了解目标受众**：根据受众调整内容的复杂度和示例的适用性；
2. **每张幻灯片只展示一个核心观点**：保持内容的简洁性；
3. **遵循“6x6规则”**：每个项目符号最多6个单词；
4. **优先使用视觉元素**：适当添加图片或图表；
5. **设计引人注目的开头和结尾**：激发观众的兴趣并引导他们的行动。

## 可用资源

- [Marp](https://marp.app/) – 基于Markdown的演示文稿工具；
- [Slidev](https://sli.dev/) – 基于Vue技术的幻灯片生成工具；
- [reveal.js](https://revealjs.com/) – 基于HTML的演示文稿生成工具。