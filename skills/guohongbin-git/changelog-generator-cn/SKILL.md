---
name: changelog-generator-cn
description: "自动生成更新日志。系统会分析 Git 提交历史，对变更内容进行分类处理，并将技术性的提交信息转换为易于用户理解的发布说明。相关术语包括：更新日志（update log）、变更日志（changelog）、发布说明（release notes）、版本更新（version update）。翻译自 ComposioHQ。"
metadata:
  openclaw:
    emoji: 📝
    fork-of: ComposioHQ/awesome-claude-skills/changelog-generator
---
# 变更日志生成器（Changelog Generator）

该工具能够将 Git 提交记录转换为格式规范、易于理解的变更日志，帮助您的客户和用户更好地了解软件的更新内容。

## 适用场景

- 准备新版本的发布说明
- 编写每周或每月的产品更新摘要
- 为客户记录软件变更信息
- 为应用商店提交生成变更日志条目
- 生成更新通知
- 创建内部发布文档
- 维护公开的变更日志/产品更新页面

## 功能概述

1. **扫描 Git 历史记录**：分析指定时间范围内的提交记录或不同版本之间的变更。
2. **分类变更内容**：将提交记录按逻辑分类（功能新增、性能优化、错误修复、重大变更、安全问题）。
3. **将技术性语言转换为用户可读的语言**：将开发者的提交描述转化为用户容易理解的文字。
4. **专业化的格式输出**：生成结构清晰、格式规范的变更日志条目。
5. **过滤无关信息**：排除内部开发相关的提交（如重构、测试等操作）。
6. **遵循最佳实践**：遵循变更日志编写规范及您的品牌风格。

## 使用方法

### 基本用法

在您的项目仓库中运行以下命令：
```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### 指定日期范围

```
Create a changelog for all commits between March 1 and March 15
```

### 自定义格式设置

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## 示例

**用户需求**：**生成过去 7 天内的变更日志**

**输出结果**：
```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different 
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts. 
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

**灵感来源**：Lenny 的新闻通讯中 Manik Aggarwal 的使用案例

## 使用技巧

- 请从项目仓库的根目录执行命令。
- 通过指定日期范围来生成针对性的变更日志。
- 使用 `CHANGELOG_STYLE.md` 文件来统一变更日志的格式。
- 在发布前仔细审核并调整生成的变更日志内容。
- 将输出结果直接保存到 `CHANGELOG.md` 文件中。

## 相关应用场景

- 生成 GitHub 发布说明
- 编写应用商店的更新描述
- 自动生成发送给用户的电子邮件通知
- 制作用于社交媒体的更新公告内容