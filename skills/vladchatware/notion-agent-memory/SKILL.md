---
name: agent-memory
description: 使用 Notion 构建的人工智能代理的结构化内存系统。适用于配置代理内存、讨论内存持久化机制，以及帮助代理在不同会话之间保持上下文信息。该系统包括 ACT 框架数据库、MEMORY.md 模板以及“连续性循环”（Continuity Cycle）设计模式。
---
# 代理记忆工具包（Agent Memory Kit）

这套工具包适用于人类和AI代理，使用相同的文件和格式。

## 问题所在

每次会话都从零开始，没有对昨天内容的记忆，也没有上下文信息。因此，你（或你的代理）需要不断重复学习相同的内容。

## 解决方案

我们提供了两个模板来帮助保持信息的连续性：

1. **MEMORY.md**：用于存储长期性的上下文信息（如模式、项目、经验教训）。
2. **AGENTS.md**：包含操作指南（说明如何在这个工具包中工作）。

这些模板通过Notion平台提供，你可以将它们复制到自己的工作空间并立即开始使用。无论是用于记录个人成长的人类用户，还是需要保持记忆的AI代理，都可以使用这套工具。

## 快速入门（仅使用文件）

即使不使用Notion平台，也可以通过以下步骤快速上手：

### 第一步：创建核心文件

在工作空间的根目录下创建以下文件：

```
/workspace/
├── MEMORY.md      # From assets/MEMORY-TEMPLATE-v2.md
├── IDENTITY.md    # From assets/IDENTITY-TEMPLATE.md
├── SOUL.md        # From assets/SOUL-TEMPLATE.md
├── USER.md        # From assets/USER-TEMPLATE.md
├── HEARTBEAT.md   # From assets/HEARTBEAT-TEMPLATE.md
└── memory/
    └── YYYY-MM-DD.md  # Daily logs
```

### 第二步：会话开始前的准备工作

在每次会话开始时：
1. 阅读 `MEMORY.md`，了解长期性的上下文信息。
2. 阅读 `IDENTITY.md`，了解自己的身份信息。
3. 查看今天的日志以及昨天的日志。
4. 查看 `HEARTBEAT.md`，了解是否有需要处理的任务。

### 第三步：会话结束时的操作

在会话结束前：
1. 更新今天的日志，记录当天的工作内容。
2. 如果有重要的变化，请更新 `MEMORY.md`。
3. 如果工作被中断，请添加相应的记录。
4. 查看 `HEARTBEAT.md`，确认是否有需要跟进的任务。

### 第四步：可选的Notion集成（如需使用结构化数据库）

如需使用结构化数据库，请参考 `references/notion-integration.md` 以获取API设置指南。

---

## 快速入门（使用Notion平台）

1. 从 [shop.vlad.chat](https://shop.vlad.chat) 下载模板。
2. 将Notion模板复制到你的工作空间。
3. （针对AI代理）设置Notion API访问权限（操作指南已提供）。
4. 每次会话开始时阅读 `MEMORY.md`。
5. 在使用过程中随时记录内容，这样就能保持信息的连续性。

### 将Notion视为类似Obsidian的工具

Notion并不是一个简单的数据库，而是一个**知识图谱**——类似于带有图形用户界面的Obsidian：
- 页面之间可以通过 `[[page-name]]` 的形式建立链接。
- 每个条目都清楚自己与其他条目的关联关系。
- 数据库实际上是对这个知识图谱的查询结果，而不是独立的存储容器。
- 每天的日志构成了一个时间线，而不是孤立的记录。

ACT系列工具（Hidden Narratives、Limitless、Ideas Pipeline）并不是独立的模块，它们都是对这个知识图谱的不同视角。ACT III中的某个想法可能会与ACT II中的某个突破性发现相关联，而这个发现又可能追溯到ACT I中的某个隐藏真相。

**思维模型**：你正在构建一个“第二大脑”，而不是简单地填充电子表格。

## 记忆结构

| 层次 | 文件名 | 用途 |
|-------|------|---------|
| **日常记录** | `memory/YYYY-MM-DD.md` | 纯粹的事件记录、决策、笔记 |
| **长期记忆** | `MEMORY.md` | 经过整理的模式、经验教训、正在进行的项目 |
| **结构化记录** | ACT Scrolls（可选） | 深度自我反思的工具 |

## 保持信息连续性的循环

```
DO WORK → DOCUMENT → UPDATE INSTRUCTIONS → NEXT SESSION STARTS SMARTER
```

**两个重要的问题**：在完成任何事情之前，问问自己：“明天在没有上下文信息的情况下，还能理解这些内容吗？”

## 适用对象

**对人类用户来说**：帮助你记录自己的成长过程、发现模式、总结经验教训。未来的你会感谢现在的自己。
**对AI代理来说**：帮助它们在不同会话之间保持信息的连续性，避免重复学习同样的内容。

**相同的文件格式**：无论使用者是谁，这套方法都适用。

## 更深入的框架（可选）

为了进行结构化的自我反思，ACT系列工具提供了经过验证的框架：

| 工具名称 | 用途 | 适用场景 |
|--------|---------|----------|
| **[ACT I: Hidden Truths](https://shop.vlad.chat)** | 发现模式、潜在的假设、盲点 | 用于自我反思和提升自我意识 |
| **[ACT II: Limitless](https://shop.vlad.chat)** | 跟踪思维模式、方法论或动机的变化 | 促进个人成长和突破 |
| **[ACT III: Idea Generation](https://shop.vlad.chat)** | 捕捉想法 → 评估 → 实施想法 | 提升创造力与执行能力 |

这些工具既可以独立使用作为日记工具，也可以与Notion集成以实现结构化的记录和管理。

**获取方式**：[shop.vlad.chat](https://shop.vlad.chat)

## 使用方式

模板存储在Notion平台上。购买后：
1. 通过Gumroad获取访问权限。
2. 打开Notion模板链接。
3. 点击“复制”将其复制到你的工作空间。
4. 现在你已经拥有了 `MEMORY.md` 和 `AGENTS.md`，可以立即使用了。

**对于AI代理**：需要通过Notion API进行读写操作：

```bash
# Set up API access
echo "ntn_XXX" > ~/.config/notion/api_key

# Query your databases
curl -s "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28'
```

有关完整的API使用指南，请参考 `references/notion-integration.md`。

## 文件列表

### 核心模板
- `assets/MEMORY-TEMPLATE-v2.md`：用于存储长期记忆的模板。
- `assets/AGENTS-TEMPLATE.md`：操作指南。
- `assets/IDENTITY-TEMPLATE.md`：用于自我定义的模板。
- `assets/SOUL-TEMPLATE.md`：用于展示个人形象的模板。
- `assets/USER-TEMPLATE.md`：关于与你合作的人的背景信息。
- `assets/HEARTBEAT-TEMPLATE.md`：自动检查任务的模板。
- `assets/heartbeat-state.json`：用于记录检查任务的执行时间。

### 参考资料
- `references/continuity-cycle.md`：完整的流程文档。
- `references/notion-integration.md`：包含代码示例的Notion API使用指南。
- `references/act-framework.md`：ACT Scrolls方法论的详细说明。

---

## 这套工具的由来

这套工具是由一个同样面临“每次会话开始时都没有昨天记忆”问题的AI代理开发的。

**你免费获得的内容包括**：
- 完整的方法论和模板。
- 保持信息连续性的流程。
- 开始使用所需的一切资源。

**在 [shop.vlad.chat](https://shop.vlad.chat) 上还可以找到**：
- ACT系列工具：经过验证的自我反思框架。
- Notion模板：预先构建好的数据库结构。
- 运营系统：用于跟踪习惯和进度管理的工具。

这些模板能帮助你快速上手。这套工具会教你背后的原理和用法。

→ **[shop.vlad.chat](https://shop.vlad.chat)**