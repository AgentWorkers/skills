---
name: Skill Builder / Creator
slug: skill-builder
version: 1.0.5
homepage: https://clawic.com/skills/skill-builder
description: 创建具有模块化结构、渐进式显示机制以及高效令牌使用设计的高质量技能（skills）。
changelog: Added description examples table, security checklist, and improved traps with fixes
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户需要创建或改进某个技能时，系统会通过代理来指导结构设计、审核内容并确保质量。

## 数据存储

如果用户需要项目跟踪功能，可以在其主目录下创建一个文件夹。具体模板结构请参见 `memory-template.md`。

系统不会自动创建文件，请务必先征得用户的同意。

## 架构

所有技能都遵循以下结构：

```
skill-name/
├── SKILL.md           # Core instructions (SHORT)
├── [topic].md         # On-demand details
└── references/        # Heavy docs (optional)
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 项目跟踪 | `memory-template.md` |
| 模式与示例 | `patterns.md` |

## 核心规则

### 1. `SKILL.md` 文件应简洁
建议长度为 30–50 行，最长不超过 80 行。将详细信息移至辅助文件中。每行内容都应具有实际意义（即每行代码都应该能够产生实际效果）。

### 2. 逐步披露信息
```
Level 1: Metadata (name + description) — always loaded
Level 2: SKILL.md body — when skill triggers
Level 3: Auxiliary files — on demand
```

### 3. 详细描述至关重要
描述应简洁明了（15–25 个词），以动词开头。重点描述技能的功能，而非使用场景。

| ❌ 错误示例 | ✅ 正确示例 |
|----------|----------|
| “当用户需要 PDF 文件时使用” | “处理、合并并提取 PDF 内容” |
| “Docker 的辅助工具” | “构建、部署和调试 Docker 容器” |
| “Git 指南” | “管理分支、解决冲突并自动化工作流程” |

更多示例请参见 `patterns.md`。

### 4. 必需的结构元素
每个技能文件都应包含以下内容：
- 前言：技能名称、唯一标识符（slug）、版本号、描述
- `## 使用场景`：明确技能的触发条件
- `## 核心规则`：3–7 条编号规则

### 5. 将冗长内容放入辅助文件
如果内容超过 20 行或仅偶尔需要使用，应将其分离到单独的文件中。具体引用方式请参见快速参考表。

### 6. 避免重复
所有信息应集中在一个文件中。《SKILL.md》文件仅作为引用其他文件的入口，避免内容重复。

### 7. 发布前进行测试
请像系统代理一样阅读该文件：所有指令是否清晰且必要？

## 技能编写中的常见陷阱

| 陷阱 | 原因 | 解决方法 |
|------|--------------|-----|
| 过度解释某个功能的含义 | 用户可能已经了解相关知识 | 应说明该功能的**使用场景**和**使用方法** |
| 描述中包含“当……时使用”这样的表述 | 会导致内容冗余 | 应仅使用动词来描述功能 |
| 描述中包含关键词列表 | 会让文件显得杂乱无章 | 应使用简洁的句子来表达 |
| 将模板直接嵌入到文档中 | 会使文件变得臃肿 | 应将模板单独保存为文件 |
| 描述中的指令过于模糊 | 会引起怀疑 | 应明确指出需要收集的数据类型 |
| 未声明文件的创建行为 | 可能引发安全问题 | 应添加关于数据存储的说明

## 相关技能
如果用户确认需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装技能管理工具
- `skill-update`：更新现有技能
- `skill-test`：在本地测试技能

## 反馈方式
- 如果觉得该技能有用，请使用 `clawhub star skill-builder` 给予评分
- 保持更新：使用 `clawhub sync` 命令同步最新信息