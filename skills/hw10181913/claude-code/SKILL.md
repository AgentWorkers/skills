---
name: claude-code
description: |
  Claude Code integration for OpenClaw. This skill provides interfaces to:
  - Query Claude Code documentation from https://code.claude.com/docs
  - Manage subagents and coding tasks
  - Execute AI-assisted coding workflows
  - Access best practices and common workflows
  Use this skill when users want to:
  - Get help with coding tasks
  - Query Claude Code documentation
  - Manage AI-assisted development workflows
  - Execute complex programming tasks
homepage: https://code.claude.com/docs
---

# Claude Code 集成

本技能将 Claude Code 的功能集成到 OpenClaw 中，使用户能够使用 AI 辅助的编码工作流程、文档以及最佳实践。

## 功能概述

### 📚 文档查询
- 查询 Claude Code 的文档
- 获取最佳实践和工作流程
- 了解设置和自定义选项
- 解决常见问题

### 🤖 子代理管理
- 创建编码子代理
- 管理代理团队
- 执行复杂的开发任务
- 自动化代码审查和 Pull Request（PR）流程

### 🛠️ 开发工作流程
- AI 辅助编码的最佳实践
- 常见的工作流程和模式
- 设置和配置选项
- 故障排除指南

## 使用示例

### 查询文档
```bash
# Get documentation about a specific topic
claude-code query "subagents"
claude-code query "best practices"
claude-code query "settings"
```

### 执行编码任务
```bash
# Create a coding subagent for a complex task
claude-code task --description "Fix the login bug" --priority high
claude-code task --description "Refactor the database layer" --model claude-3-5-sonnet
```

### 列出可用命令
```bash
# Show all available commands
claude-code --help
```

## 可用命令

### `query`
查询 Claude Code 中关于特定主题的文档。

**用法:**
```bash
claude-code query <topic>
```

**示例:**
```bash
claude-code query "subagents"
claude-code query "agent-teams"
claude-code query "best practices"
claude-code query "common workflows"
claude-code query "settings"
claude-code query "troubleshooting"
```

**可查询的主题包括:**
- 子代理和代理团队
- 最佳实践和工作流程
- 设置和自定义选项
- 故障排除指南
- 插件和扩展
- MCP（模型上下文协议）
- 无界面/编程式使用方式

### `task`
创建并执行一个编码子代理任务。

**用法:**
```bash
claude-code task --description "<task description>" [--priority <level>] [--model <model-name>]
```

**选项:**
- `--description, -d`: 任务描述（必填）
- `--priority, -p`: 任务优先级（低/中/高，默认：中等）
- `--model, -m`: 要使用的模型（可选，未指定时使用默认模型）

**示例:**
```bash
claude-code task --description "Implement user authentication module"
claude-code task --description "Refactor database queries" --priority high
claude-code task --description "Write unit tests for the API" --model claude-3-5-sonnet
```

### `docs`
获取 Claude Code 文档的概览。

**用法:**
```bash
claude-code docs [section]
```

**文档章节包括:**
- `quickstart` - 入门指南
- `best-practices` - AI 编码最佳实践
- `common-workflows` - 常见开发工作流程
- `settings` - 自定义选项
- `troubleshooting` - 常见问题及解决方法
- `all` - 全部文档概览（默认）

**示例:**
```bash
claude-code docs
claude-code docs quickstart
claude-code docs best-practices
claude-code docs troubleshooting
```

### `info`
显示 Claude Code 的配置和状态。

**用法:**
```bash
claude-code info
```

**输出内容包括:**
- 版本信息
- 可用的子代理
- 配置的模型
- MCP 服务器状态

## 与 OpenClaw 的集成

本技能可与 OpenClaw 的原生功能无缝协作：

- **子代理**: Claude Code 的子代理可补充 OpenClaw 的子代理系统
- **代码执行**: 通过 OpenClaw 的执行工具完成整个开发流程
- **文件管理**: 结合 OpenClaw 的读写工具进行完整的代码库管理
- **会话管理**: Claude Code 的任务与 OpenClaw 的会话管理集成

## 示例工作流程

### 复杂错误修复
```bash
# 1. Query best practices for debugging
claude-code query "debugging best practices"

# 2. Create a subagent to investigate and fix
claude-code task --description "Find and fix the null pointer exception in userService.js" --priority high

# 3. Review the changes
claude-code query "code review best practices"
```

### 新功能开发
```bash
# 1. Get best practices for the feature type
claude-code query "API design best practices"

# 2. Create development task
claude-code task --description "Implement REST API for user management" --priority medium

# 3. Check settings for code style
claude-code query "code style settings"
```

### 代码审查自动化
```bash
# 1. Query PR review best practices
claude-code query "PR review workflows"

# 2. Set up automated review task
claude-code task --description "Review all PRs in the last week" --priority low
```

## 配置

### 环境变量
基本使用无需环境变量。Claude Code 的集成依赖于 OpenClaw 的原生功能。

### 模型
使用 OpenClaw 配置的默认模型。可通过 `--model` 选项根据任务进行自定义。

### 子代理限制
由 OpenClaw 的子代理配置管理（默认：同时运行 8 个子代理）。

## 注意事项

- 本技能提供了对 Claude Code 文档和工作流程的封装
- 复杂的编码任务通过 OpenClaw 的原生子代理系统执行
- 如需直接使用 Claude Code 的命令行界面（CLI），请从 https://claude.com/code 单独安装 Claude Code
- 所有任务执行均通过 OpenClaw 的安全代理基础设施完成

## 相关资源

- Claude Code 官方文档: https://code.claude.com/docs
- OpenClaw 子代理: 使用 OpenClaw 的原生子代理功能
- 最佳实践: 从 Claude Code 的指南中整合而来