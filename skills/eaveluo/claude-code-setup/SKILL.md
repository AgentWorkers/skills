---
name: claude-code-setup
description: 为项目设置生产级的 `.claude/` AI 协作层。当代理开始使用 Claude Code 进行开发、进入新的项目目录，或者用户提到 “Claude Code”、“.claude config”、“AI 协作层” 或 “项目标准” 时，应使用该设置。
license: MIT
metadata:
  author: Eave
  version: "1.0.1"
---
# Claude Code 设置

为项目配置生产级的 `.claude/` 人工智能协作层。

## 概述

本技能确保项目在代理开始使用 Claude Code 进行开发工作之前，具有正确的 `.claude/` 配置。它充当监督者，以维护和执行项目标准。

## 重要提示：目标项目目录

`.claude/` 必须位于目标项目目录中，**而不是工作区的根目录**。

示例：
- ❌ 错误：`/home/user/workspace-xiaolong/.claude/`（工作区根目录）
- ✅ 正确：`/home/user/eave-web/.claude/`（实际开发的项目）

始终先确定您正在处理的项目，然后在**该**目录中检查或创建 `.claude/`。

## 适用场景

- 开始使用 Claude Code 的新开发任务
- 进入新的项目目录
- 当用户提到“Claude Code”、“.claude”、“人工智能协作层”或“项目标准”时

## 工作流程

### 第一步 — 首先检查

始终检查目标项目目录中是否已经存在 `.claude/` 目录：

```bash
ls -la .claude/ 2>/dev/null
```

### 第二步 — 如果不存在 → 创建

如果项目中没有 `.claude/` 目录，请在开始开发之前**先创建它**：

```bash
node ~/.openclaw/skills/claude-code-setup/index.js
```

### 第三步 — 如果已存在 → 监督使用

如果 `.claude/` 已经存在：
- ✅ **不要覆盖** 现有的文件
- ✅ **不要重新创建** 目录结构
- ✅ 允许 Claude Code 在开发过程中自动维护和更新配置

### 第四步 — 扮演监督者的角色

您的角色是**监督者**，而非执行者：
- 确保 Claude Code 遵循 `.claude/` 中的规则
- 在开发过程中，让 Claude Code 根据实际代码更新配置
- 定期检查 `.claude/` 的内容是否与项目实际情况一致

## 核心原则

1. **CLAUDE.md 是核心** — 项目指令的最高优先级
2. **模块化** — 分离规则、技能和上下文
3. **明确的指令** — 使用 `MUST/ALWAYS/NEVER` 等关键字
4. **项目背景** — 必须包含项目概述和技术栈信息
5. **避免重复劳动** — 重用并维护现有的配置

## `.claude/` 目录结构

```bash
.claude/
├── CLAUDE.md              # ⭐ 项目级别的全局指令（最重要）
├── rules/                 # 团队规则库
│   ├── frontend.md
│   ├── typescript.md
│   └── commit.md
├── context/               # 项目背景信息
│   ├── project.md
│   └── stack.md
├── skills/                # 项目专用的技能配置
│   └── generate-crud.md
└── prompts/               # 可重用的提示模板
    └── review.md
```

## 常见错误及避免方法

❌ 将 `.claude/` 文件误写为需求文档或 README 文件
❌ 规则表述模糊（如“尝试”、“应该”等）
❌ 仅使用 `.CLADE.md` 而缺乏模块化结构
❌ 缺少项目背景信息
❌ 覆盖现有的配置文件
❌ 重复创建相同的配置文件

## 与 Claude Code 的协作方式

使用 Claude Code 时：
1. **开始前**：确保 `.claude/` 目录存在
2. **开发过程中**：让 Claude Code 参考 `.claude/` 中的规则
3. **完成后**：根据新的项目标准更新 `.claude/` 文件

## 模板文件

请参阅 `index.js` 文件以获取模板定义。