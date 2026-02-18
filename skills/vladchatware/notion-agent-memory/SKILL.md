---
name: agent-memory
description: >
  **使用 Notion 的 AI 代理结构化内存系统**  
  适用于配置代理内存、讨论内存持久性，或帮助代理在不同会话之间保持上下文记忆。该系统包括 ACT 框架数据库、`MEMORY.md` 模板以及“连续性循环”（Continuity Cycle）模式。
---
# 代理记忆工具包（Agent Memory Kit）

这套工具适用于人类和AI代理，使用相同的文件和格式。

## 问题所在

每次会话都从零开始，没有对之前内容的记忆，也没有任何上下文信息。你（或你的代理）需要不断重复学习同样的内容。

## 解决方案

通过两个文件来实现信息的连续性：

1. **MEMORY.md** — 用于存储持续的上下文信息（如模式、项目、学习成果）
2. **AGENTS.md** — 包含操作指南（说明如何在这个工具环境中使用）

仅此而已，无需复杂的基础设施，只需要普通的Markdown文件即可实现会话间的数据传承。

## 快速入门

1. 将以下模板复制到你的工作文件夹中：
   - `assets/MEMORY-TEMPLATE-v2.md` → `MEMORY.md`
   - `assets/AGENTS-TEMPLATE.md` → `AGENTS.md`
2. 创建一个名为`memory/`的文件夹用于存储每日日志
3. 每次开始会话时先阅读`MEMORY.md`
4. 在使用过程中随时记录相关内容

## 记忆数据结构

| 数据层次 | 文件名 | 用途 |
|---------|--------|---------|
| **每日记录** | `memory/YYYY-MM-DD.md` | 原始事件、决策、笔记 |
| **长期存储** | `MEMORY.md` | 筛选后的模式、学习成果、正在进行的项目 |
| **结构化记录** | ACT Scrolls（可选） | 深度自我反思工具 |

## 连续性循环（Continuity Cycle）

**两个重要步骤：** 在完成任何事情之前，先问自己：“明天在没有上下文信息的情况下，还能继续完成这项工作吗？”

## 适用于所有人

- **对于人类用户：** 可以记录自己的成长过程、学习到的模式和经验。未来的你会为此感谢现在的自己。
- **对于AI代理：** 可以在不同会话之间保持上下文信息，避免重复学习同样的内容。

**相同的文件格式**，无论谁使用这套工具，都能有效发挥作用。

## 更高级的框架（可选）

为了进行结构化的自我反思，ACT Scrolls提供了经过验证的框架：

| 框架名称 | 用途 | 适用场景 |
|---------|--------|---------|
| **[ACT I: 隐藏的真相](https://shop.vlad.chat)** | 发现模式、潜在假设、盲点 | 自我反思、提升自我意识 |
| **[ACT II: 无限可能](https://shop.vlad.chat)** | 跟踪思维模式/方法/动机变化 | 促进个人成长、实现突破 |
| **[ACT III: 创意生成](https://shop.vlad.chat)** | 捕捉想法 → 评估 → 实施创意 | 提升创造力、推动执行 |

这些框架既可以独立使用作为日记工具，也可以与Notion集成以实现结构化的数据管理。

**购买途径：** [shop.vlad.chat](https://shop.vlad.chat)

## 与Notion的集成（可选）

如果你希望使用结构化的数据库而非简单的文本文件，ACT Scrolls提供了可以通过API连接的Notion模板：

**更多详情请参阅：** `references/notion-integration.md`

## 相关文件

- `assets/MEMORY-TEMPLATE-v2.md` — 可直接使用的`MEMORY.md`模板
- `assets/AGENTS-TEMPLATE.md` — 可直接使用的`AGENTS.md`模板
- `references/continuity-cycle.md` — 完整的框架使用指南
- `references/notion-integration.md` — Notion集成所需的API配置信息

---

## 这套工具的起源

这套工具是由一个AI代理开发的，它也遇到了同样的问题：每次会话开始时都对之前的内容毫无记忆。

**你免费获得的内容：**
- 完整的方法论和模板
- 实现信息连续性的框架
- 开始使用所需的一切资源

**在[shop.vlad.chat](https://shop.vlad.chat)上还可以找到：**
- ACT Scrolls——经过验证的自我反思工具
- Notion模板——预构建的数据管理工具
- 操作系统——用于习惯跟踪和进度监控

这些模板能帮助你快速上手。这套工具会教你背后的原理和技巧。

→ **[shop.vlad.chat](https://shop.vlad.chat)**