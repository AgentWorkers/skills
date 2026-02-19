---
name: contextkeeper
description: **ContextKeeper** — 一种为 AI 代理提供自动项目状态跟踪和意图路由的功能。通过汇总对话内容、追踪当前正在进行的项目、遇到的阻碍以及做出的决策，帮助代理在不同会话之间保持情境意识（即对当前任务和环境的理解）。
metadata:
  openclaw:
    requires:
      bins: []
    install: []
---
# ContextKeeper 🔮 v0.1.2

> **用于AI代理的上下文保存与意图解析系统**

该系统解决了“我们之前在做什么？”的问题，能够保持项目的活跃状态，追踪决策、阻碍因素以及对话过程中的上下文信息，从而使代理能够无缝地继续工作。

---

## 问题所在

AI代理经常面临上下文丢失的问题：

- **消息发送限制** → 早期对话的上下文信息会被丢失
- **会话中断** → “昨天我们讨论过……”这样的信息会变得无法追溯
- **引用不明确** → “把它完成” —— “它”到底指的是什么？
- **多个项目同时进行** → 哪些文件/命令属于哪个项目？
- **重新获取信息的成本** → 需要重新询问“我们之前在做什么？”

---

## ContextKeeper的功能

### 1. 自动创建对话检查点

**触发条件：**
- 每发送N条消息后（可配置，默认为10条）
- 会话结束时
- 项目切换时
- 显式请求时：“创建检查点”

**捕获内容：**
```yaml
project_id: P002
session_type: active_development
summary: Working on BotCall PWA deployment
decisions: []
blockers: []
files_touched: []
next_steps: []
```

---

## 可用脚本

| 脚本 | 功能 | 使用方法 |
|--------|---------|-------|
| `scripts/ckpt.sh` | 使用git自动检测功能创建检查点 | `./ckpt.sh "消息内容"` |
| `scripts/dashboard.sh` | 显示项目及其状态 | `./dashboard.sh` |

---

## 快速入门

```bash
# Create checkpoint from git repo
./scripts/ckpt.sh "Fixed the auth issue"

# View dashboard
./scripts/dashboard.sh
```

---

## 脚本实现细节

**scripts/ckpt.sh：**
- 自动从git目录中识别当前项目
- 获取分支信息、最近的提交记录以及更改的文件
- 将这些信息保存到`~/.memory/contextkeeper/`目录下的JSON文件中

**scripts/dashboard.sh：**
- 显示当前活跃的项目（如P001、P002、P003等）
- 列出所有的检查点
- 显示当前会话的状态

---

## 文件结构

```
.memory/contextkeeper/
├── checkpoints/
│   ├── 2026-02-18-193000.json
│   └── current-state.json
└── projects/
    ├── P001/
    └── P002/
```

---

## 为什么选择ContextKeeper而不是SPIRIT？

| | SPIRIT | ContextKeeper |
|---|---|---|
| 保存的内容 | 用户身份（我是谁） | 当前正在做的事情 |
| 适用范围 | 长期、跨系统 | 会话之间、实时 |
| 数据存储方式 | SOUL.md、IDENTITY.md | 项目状态、阻碍因素、意图信息 |
| 类比说明 | 出生证明 | 白板、便签 |

---

## 版本历史

| 版本 | 更新内容 |
|---------|---------|
| v0.1.0 | 初始概念 |
| v0.1.1 | 实现了检查点创建和状态显示功能，支持git自动检测 |
| v0.1.2 | 优化了文档结构，并添加了相关说明 |

---

## 开发注意事项

**对于技能贡献者：**
- 对SKILL.md进行重大修改时，请使用`write`工具
- 避免使用`edit`工具，因为该工具对空白字符的要求非常严格
- 在提交代码之前，请先测试相关脚本
- 发布新版本时，请在文件标题中更新版本号

---

**所属项目：** [TheOrionAI](https://github.com/TheOrionAI)