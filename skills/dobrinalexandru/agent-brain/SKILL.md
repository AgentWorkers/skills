---
name: agent-brain
description: "具有6个认知模块的AI代理持续学习系统"
homepage: https://github.com/alexdobri/clawd/tree/main/skills/agent-brain
metadata:
  clawdbot:
    emoji: 🧠
    modules: [archive, ingest, vibe, gauge, signal, ritual]
---
# Agent Brain 🧠

这是一个用于AI代理的持续学习系统，其运作方式类似于人类大脑：通过学习、记忆并从经验中不断改进。

## 外部端点

| 端点 | 发送的数据 | 接收的数据 |
|----------|-----------|---------------|
| 无 | 该技能仅用于接收指令 | 不适用 |

## 安全性与隐私

该技能在本地运行，不会将任何数据传输到外部。所有数据仅存储在`memory/`文件夹中。

## 模型调用

该技能会在每个任务中自动执行；您也可以通过卸载该技能来禁用它的功能。

## 信任机制

使用该技能即表示您同意其指令在您的会话中执行。请仅在信任技能作者的情况下安装该技能。

## 概述

该技能包含6个认知模块：

| 模块 | 文件路径 | 功能 |
|--------|------|----------|
| **Archive** | `modules/archive/SKILL.md` | 数据存储与检索 |
| **Ingest** | `modules/ingest/SKILL.md` | 外部知识导入 |
| **Vibe** | `modules/vibe/SKILL.md` | 情感氛围检测 |
| **Gauge** | `modules/gauge/SKILL.md` | 自信度评估与资源管理 |
| **Signal** | `modules/signal/SKILL.md` | 冲突检测 |
| **Ritual** | `modules/ritual/SKILL.md` | 习惯养成 |

## 工作原理

该技能会自动运行。调度器会根据任务类型选择所需的模块，不会每次都运行所有模块。

## 核心流程

```
Task received
    ↓
[DISPATCHER] → Determine which modules needed
    ↓
[RELEVANT MODULES] → Only run these
    ↓
[EXECUTE]
    ↓
[ARCHIVE] → Store outcome (always)
```

### 根据任务类型选择模块

| 任务类型 | 运行的模块 |
|-----------|-------------|
| 简单问题 | Gauge + Archive |
| 提供URL的任务 | Gauge + Ingest + Archive + Vibe |
| 循环任务 | Gauge + Ritual + Vibe |
| 错误检查 | Gauge + Signal + Vibe |
| 新主题 | Gauge + Archive + Ingest + Signal + Vibe |

## 使用方法

```
/skill agent-brain
```

该技能已包含所有6个模块，无需额外安装。