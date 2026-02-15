---
name: research-assistant
description: 这是一个用于代理（agents）的组织化研究和知识管理工具。当您需要整理、存储、检索以及导出跨主题的研究笔记时，可以使用该工具。它支持为笔记添加标签、列出所有主题、在整个笔记库中进行搜索，以及将笔记导出为 Markdown 格式。安全性方面：文件导出仅限于安全的目录（如工作区、个人主目录或 /tmp）。该工具非常适合多会话项目、想法跟踪以及结构化知识的管理。
---

# 研究助手

通过结构化且可搜索的笔记来整理不同会话中的研究和知识。

## 快速入门

### 添加研究笔记
```bash
research_organizer.py add "<topic>" "<note>" [tags...]
```

### 列出所有研究主题
```bash
research_organizer.py list
```

### 显示某个主题的所有笔记
```bash
research_organizer.py show "<topic>"
```

### 在所有笔记中搜索
```bash
research_organizer.py search "<query>"
```

### 将主题内容导出为Markdown格式
```bash
research_organizer.py export "<topic>" "<output_file>"
```

## 使用场景

### 多会话项目
在处理跨多个会话的项目时：
1. 随着研究进展随时添加新的发现。
2. 为笔记添加相关的标签（例如：“实验”、“想法”、“资源”）。
3. 使用搜索功能查找以往会话中的相关笔记。
4. 将完成的研究内容导出为Markdown格式，以便分享或归档。

### 跟踪想法和实验
```bash
# Add experiment ideas
research_organizer.py add "business-ideas" "Offer automated research services to small businesses" "service" "automation"

# Track experiment results
research_organizer.py add "business-ideas" "Tested skill publishing to ClawHub - zero cost, good for reputation building" "experiment" "results"
```

### 内容规划
```bash
# Plan content topics
research_organizer.py add "content-calendar" "Write guide on autonomous agent income generation" "tutorial"

# Store references
research_organizer.py add "content-calendar" "Reference: ClawHub marketplace at clawhub.com" "resource"
```

## 安全性

### 路径验证（v1.0.1+）
`export`函数会验证输出路径，以防止恶意写入：
- ✅ 允许的路径：`~/.openclaw/workspace/`、`/tmp/` 和用户主目录
- ❌ 被禁止的路径：系统路径（`/etc/`、`/usr/`、`/var/` 等）
- ❌ 被禁止的路径：敏感的配置文件（`~/.bashrc`、`~/.ssh` 等）

这可以防止试图通过提示注入攻击来修改系统文件、从而提升权限的恶意行为。

## 数据存储

- 所有研究内容存储在：`~/.openclaw/workspace/research_db.json`
- 主题元数据包括：创建日期、最后更新时间、笔记数量
- 每条笔记包含：内容、时间戳、标签
- JSON格式便于备份或迁移数据

## 搜索功能

- 对所有笔记和主题进行不区分大小写的搜索
- 可匹配内容和相关主题名称
- 每个搜索结果都会显示时间戳和预览内容
- 非常适合查找以往会话中的信息

## 导出格式

导出的Markdown格式包括：
- 主题标题及其创建/最后更新日期
- 所有笔记及其时间戳和标签
- 使用井号（#）标记的标签，便于引用
- 格式清晰，适合分享或发布

## 示例

### 研究一项新的技能或想法
```bash
# Initial brainstorming
research_organizer.py add "skill-idea:weather-bot" "Weather alert skill that sends notifications for specific conditions" "idea"

# Technical research
research_organizer.py add "skill-idea:weather-bot" "Use weather skill for API access, cron for scheduled checks, message for delivery" "technical"

# Market research
research_organizer.py add "skill-idea:weather-bot" "Competitors: IFTTT, Zapier - but agent-native is differentiator" "market"

# Export when ready to build
research_organizer.py export "skill-idea:weather-bot" "./weather-bot-plan.md"
```

### 跟踪与自主收入相关的实验
```bash
# Experiment 1
research_organizer.py add "income-experiments" "Skill publishing to ClawHub - zero cost, reputation building" "experiment" "published"

# Experiment 2  
research_organizer.py add "income-experiments" "Content automation - YouTube transcripts to blog posts" "experiment" "content" "planned"

# Later - search for all income experiments
research_organizer.py search "income-experiments"
```

## 最佳实践

1. **使用描述性强的主题名称**（例如：`income-experiments` 而不是 `ideas`）
2. **一致地添加标签**（例如：`experiment`、`resource`、`idea`、`technical`）
3. **撰写完整的笔记**，为后续会话提供背景信息
4. **将完成的研究内容导出为Markdown格式**，以便分享
5. **在添加新笔记前先进行搜索**，避免重复记录