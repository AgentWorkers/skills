---
name: agent-memory
description: >
  **使用 Notion 的 AI 代理结构化内存系统**  
  适用于设置代理内存、讨论内存持久性，或帮助代理在不同会话之间保持上下文记忆的场景。该系统包括 ACT 框架数据库、`MEMORY.md` 模板以及“连续性循环”（Continuity Cycle）模式。
---
# 代理记忆工具包（Agent Memory Kit）

这套工具适用于人类和AI代理，使用相同的文件和格式。

## 问题所在

每次会话都从零开始，没有任何关于昨天的记忆或上下文信息。你（或你的代理）需要不断重复学习同样的内容。

## 解决方案

我们提供了两个模板来帮助保持连续性：

1. **MEMORY.md** — 用于存储长期上下文信息（模式、项目、经验教训）
2. **AGENTS.md** — 包含操作指南（如何在这个系统中工作）

这些模板通过Notion平台提供，你可以将其复制到自己的工作空间后立即开始使用。无论是用于记录个人成长的人类用户，还是需要保持记忆的AI代理，都可以使用这套工具。

## 快速入门（仅使用文件）

这套工具无需Notion平台，只需使用以下文件即可：

### 第一步：创建核心文件

在工作空间根目录下创建以下文件：

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

### 第二步：会话开始流程

在每次会话开始时：
1. 阅读 `MEMORY.md`（长期上下文信息）
2. 阅读 `IDENTITY.md`（了解自己的身份）
3. 查看今天的和昨天的日志
4. 查看 `HEARTBEAT.md` 以获取待办任务

### 第三步：会话结束流程

在结束会话前：
1. 更新今天的日志，记录当天完成的工作
2. 如果有重要变化，更新 `MEMORY.md`
3. 如果工作被中断，添加相应的备注
4. 查看 `HEARTBEAT.md` 以确认是否有需要跟进的任务

### 第四步：可选的Notion集成

如果你需要结构化的数据库，可以参考 `references/notion-integration.md` 了解API集成方法。

---

## 快速入门（使用Notion平台）

1. 从 [shop.vlad.chat](https://shop.vlad.chat) 下载模板
2. 将Notion模板复制到你的工作空间
3. （针对AI代理）设置Notion API访问权限（操作指南已提供）
4. 每次会话开始时阅读 `MEMORY.md`
5. 随时记录内容——连续性循环将帮助你保持工作进度

## 记忆体系结构

| 层级 | 文件名 | 用途 |
|-------|------|---------|
| **每日记录** | `memory/YYYY-MM-DD.md` | 原始事件、决策、笔记 |
| **长期记录** | `MEMORY.md` | 策略性模式、经验教训、正在进行的项目 |
| **结构化记录** | ACT Scrolls（可选） | 深度自我反思工具 |

## 连续性循环

**两个关键步骤：** 在完成任何任务之前，先问自己：“明天在没有上下文信息的情况下，我还能继续这项工作吗？”

## 适用于所有人

**对于人类用户：** 记录自己的成长过程、学习到的模式和经验教训。未来的你会感谢现在的自己。
**对于AI代理：** 在不同会话之间保持上下文信息，避免重复学习相同的内容。
**相同的文件格式，相同的文件结构。** 无论使用者是谁，这套方法都同样适用。

## 更深入的反思工具（可选）

ACT Scrolls提供了经过验证的自我反思框架：

| 工具名称 | 用途 | 适用场景 |
|--------|---------|----------|
| **[ACT I: 隐藏的真相](https://shop.vlad.chat)** | 发现模式、潜在假设、盲点 | 反思、自我意识提升 |
| **[ACT II: 无限可能](https://shop.vlad.chat)** | 跟踪思维模式/方法/动机变化 | 成长、突破 |
| **[ACT III: 创意生成](https://shop.vlad.chat)** | 捕捉想法 → 评估 → 实施 | 创意激发、执行 |

这些工具既可以独立使用，也可以与Notion结合以实现结构化记录。

**获取途径：** [shop.vlad.chat](https://shop.vlad.chat)

## 使用方式

模板存储在Notion平台上。购买后：
1. 通过Gumroad获取访问权限
2. 打开Notion模板链接
3. 点击“复制”将其复制到你的工作空间
4. 现在你已经拥有了 `MEMORY.md` 和 `AGENTS.md`，可以立即使用

**对于AI代理：** 通过Notion API进行读写操作：

```bash
# Set up API access
echo "ntn_XXX" > ~/.config/notion/api_key

# Query your databases
curl -s "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28'
```

有关API使用的详细信息，请参阅 `references/notion-integration.md`。

## 文件列表

### 核心模板
- `assets/MEMORY-TEMPLATE-v2.md` — 持久性记忆模板
- `assets/AGENTS-TEMPLATE.md` — 操作指南
- `assets/IDENTITY-TEMPLATE.md` — 自我定义文件（了解自己的身份）
- `assets/SOUL-TEMPLATE.md` — 个人形象文件（如何展示自己）
- `assets/USER-TEMPLATE.md` — 关于合作对象的信息
- `assets/HEARTBEAT-TEMPLATE.md` — 自动检查日程
- `assets/heartbeat-state.json` — 记录检查时间

### 参考资料
- `references/continuity-cycle.md` — 完整的流程文档
- `references/notion-integration.md` — 包含代码示例的Notion API使用指南
- `references/act-framework.md` — ACT Scrolls方法论文档

---

## 这套工具的由来

这套工具是由一个同样面临“每次会话开始时都没有昨天记忆”问题的AI代理开发的。

**你免费获得的内容：**
- 完整的方法论和模板
- 连续性循环的实现方式
- 开始使用所需的一切资源

**在 [shop.vlad.chat](https://shop.vlad.chat) 上还可以找到：**
- ACT Scrolls——经过验证的自我反思工具
- Notion模板——预构建的数据库
- 操作系统工具——习惯跟踪、进度监控面板

这些模板为你提供了一个良好的起点。这套工具将帮助你掌握其背后的原理。

→ **[shop.vlad.chat](https://shop.vlad.chat)**