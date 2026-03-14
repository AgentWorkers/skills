---
name: context-engine
description: Smart Context Engine - Maintains conversation state and project continuity across OpenClaw sessions. Tracks active projects, saves/restores context, and provides project management. Use when: (1) starting a new session and wanting to restore previous context, (2) working on a specific project and wanting to track progress, (3) switching between projects, (4) asking "what are we working on" or "where did we leave off", (5) wanting to save current context manually.

metadata:
  claname: context-engine
  category: memory
  tags:
    - memory
    - context
    - projects
    - workflow
  version: 1.0.0
  author: Community
  license: MIT

requires:
  env: []
  bins: []
  config: []

files:
  - scripts/*
  - "*.md"
---

# 上下文引擎（Context Engine）

Smart Context Engine 负责在多个 OpenClaw 会话之间维护对话状态和项目连续性。

## 快速入门

上下文引擎会自动执行以下操作：
- 在会话开始时恢复您上次使用的项目
- 定期（通过心跳机制）以及会话结束时保存上下文信息
- 记录每个项目的待办任务和备注

### 命令

- **"remember" / "save context"** - 手动保存当前上下文
- **"switch to [project]"** - 切换到指定项目（如果项目不存在，则创建该项目）
- **"show projects" / "what are we working on"** - 列出所有项目
- **"summarize" / "where did we leave off"** - 获取项目概要

## 存储

项目数据存储在：`/home/deus/.openclaw/workspace/memory/projects/` 目录下：
- `projects.json` - 所有项目数据
- `session.json` - 当前会话状态

## 动作

### save_context

保存当前上下文信息，包括：
- 最后讨论的主题
- 最后处理的文件
- 最后执行的命令
- 待办任务
- 备注

**触发条件**：用户明确执行命令（如 "remember", "save context"），或会话结束，或心跳机制触发

### restore_context

恢复上一个会话的上下文：
- 加载上次使用的项目
- 显示“欢迎回到 [project]”提示
- 如果有待办任务，则显示这些任务

**触发条件**：会话开始，或用户明确请求

### switch_project

在项目之间切换：
- 保存当前项目的上下文
- 加载或创建新项目
- 将新项目设置为当前活动项目

**触发条件**：用户明确执行命令（如 "switch to X"）

### list_projects

列出所有项目，并显示项目状态：
- 突出显示当前活动项目
- 显示项目状态（活动/暂停/已完成/已归档）
- 显示上次会话的日期

**触发条件**：用户明确执行命令（如 "show projects", "what are we working on"）

### summarize

生成当前项目的概要：
- 项目当前状态
- 待办任务
- 最后讨论的主题
- 会话历史记录

**触发条件**：用户明确执行命令（如 "summarize", "where did we leave off"）

## 触发机制

| 触发条件 | 优先级 |
|---------|-----------|
| 会话开始 | 新会话开始 | 1 |
| 用户明确命令 | 用户执行 "remember", "save context", "project", "switch to", "show projects", "summarize" | 2 |
| 心跳机制 | 每 30 分钟触发一次（如果启用） | 3 |

## 集成

该上下文引擎与 MEMORY.md 系统协同工作，将项目概要更新到长期存储中。