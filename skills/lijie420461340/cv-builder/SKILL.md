---
name: cv-builder
description: 使用 `rendercv` 从 YAML 文件生成专业的简历（CV），支持多种模板格式，并输出为 PDF 文件。
author: claude-office-skills
version: "1.0"
tags: [resume, cv, rendercv, yaml, pdf]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: rendercv
  url: https://github.com/sinaatalay/rendercv
  stars: 15.4k
---

# CV Builder 技能

## 概述

该技能允许您使用 **rendercv** 从结构化的 YAML 文件生成专业的简历（CV）。只需定义一次您的工作经验、教育背景和技能信息，即可生成多种主题的精美 PDF 简历。

## 使用方法

1. 提供您的简历信息（工作经验、教育背景、技能）
2. 选择一个模板/主题
3. 我会将您提供的信息转换为 YAML 格式，并生成对应的 PDF 文件

**示例提示：**
- “根据我的工作经验生成一份简历”
- “以经典主题生成一份简历”
- “用新的工作经历更新我的简历”
- “制作一份突出项目经验的技术简历”

## 相关知识

### YAML 结构

```yaml
cv:
  name: John Doe
  location: San Francisco, CA
  email: john@email.com
  phone: "+1-555-555-5555"
  website: https://johndoe.com
  social_networks:
    - network: LinkedIn
      username: johndoe
    - network: GitHub
      username: johndoe
  
  sections:
    summary:
      - "Senior software engineer with 10+ years experience..."
    
    experience:
      - company: Tech Corp
        position: Senior Engineer
        location: San Francisco, CA
        start_date: 2020-01
        end_date: present
        highlights:
          - "Led team of 5 engineers"
          - "Increased performance by 40%"
    
    education:
      - institution: MIT
        area: Computer Science
        degree: BS
        start_date: 2008
        end_date: 2012
    
    skills:
      - label: Languages
        details: Python, JavaScript, Go
      - label: Frameworks
        details: React, Django, FastAPI
```

### 可用主题

可用主题：`classic`、`sb2nov`、`moderncv`、`engineeringresumes`

```yaml
design:
  theme: classic
  font: Source Sans 3
  font_size: 10pt
  page_size: letterpaper
  color: '#004f90'
```

### 命令行工具（CLI）使用方法

```bash
# Install
pip install rendercv

# Create new CV
rendercv new "John Doe"

# Render to PDF
rendercv render cv.yaml

# Output: rendercv_output/John_Doe_CV.pdf
```

## 示例

```yaml
cv:
  name: Sarah Chen
  location: New York, NY
  email: sarah@email.com
  phone: "+1-555-123-4567"
  website: https://sarahchen.dev
  social_networks:
    - network: LinkedIn
      username: sarahchen
    - network: GitHub
      username: sarahchen

  sections:
    summary:
      - "Full-stack developer with 8 years of experience building scalable web applications. Passionate about clean code and user experience."

    experience:
      - company: Startup Inc
        position: Lead Developer
        location: New York, NY
        start_date: 2021-03
        end_date: present
        highlights:
          - "Architected microservices handling 1M+ requests/day"
          - "Mentored 4 junior developers"
          - "Reduced deployment time by 60% with CI/CD"

      - company: Big Tech Co
        position: Software Engineer
        location: San Francisco, CA
        start_date: 2018-06
        end_date: 2021-02
        highlights:
          - "Built real-time analytics dashboard"
          - "Optimized database queries, 3x faster"

    education:
      - institution: Stanford University
        area: Computer Science
        degree: MS
        start_date: 2016
        end_date: 2018

    skills:
      - label: Languages
        details: Python, TypeScript, Go, SQL
      - label: Technologies
        details: React, Node.js, PostgreSQL, AWS, Docker
      - label: Practices
        details: Agile, TDD, Code Review, CI/CD

design:
  theme: sb2nov
  font_size: 10pt
```

## 资源

- [rendercv 文档](https://docs.rendercv.com/)
- [GitHub 仓库](https://github.com/sinaatalay/rendercv)
- [主题库](https://docs.rendercv.com/user_guide/themes/)