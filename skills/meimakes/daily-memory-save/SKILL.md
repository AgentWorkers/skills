---
name: daily-memory-save
description: 定期审查对话记录，并将相关数据写入内存文件，以确保代理在会话之间的连续性。该系统采用双层架构：一层用于存储每日生成的原始笔记，另一层用于保存经过整理的长期记忆数据。
metadata: {"openclaw":{"writablePaths":["memory/","MEMORY.md"],"retention":"persistent, user-managed, review regularly","security":"writes only to declared workspace paths, no external network access, no credential handling","homepage":"https://github.com/meimakes/daily-memory-save","author":"Mei Park (@meimakes)"}}
---
# 每日记忆保存功能

该功能会定期审查对话记录，并将相关内容写入内存文件，以确保代理在会话之间保持连续性。

## ⚠️ 隐私与透明度声明

**在安装之前，请了解该功能的用途：**

- **仅访问主会话数据**：该功能仅在您的主会话中运行，并读取对话记录以提取记忆内容。请仅在您信任您的工作环境时才进行安装。
- **默认为静默模式**：默认情况下，该功能不会发出任何提示。如果您希望在记忆被保存时收到通知，请修改相应的 cron 配置（详见下文“通知模式”部分）。
- **文件存储位置**：将数据写入 `memory/YYYY-MM-DD.md` 和 `MEMORY.md` 文件中。请确保您的工作空间是私有的，并已备份这些文件。
- **无网络请求**：该功能不会进行任何网络请求，仅读取对话记录并写入本地文件。您的运行环境应确保这一点——仅依赖该功能的声明并不能保证安全性。
- **不使用任何凭证**：该功能不会使用或存储任何 API 密钥、令牌或敏感信息。

**建议**：定期查看保存的记忆文件，并删除您不希望长期保留的内容。

## 功能概述

该功能作为主会话中的定期系统事件运行，会审查最近的对话内容，筛选出值得记录的信息，并生成每日记忆笔记。

## Cron 配置方法

将此功能设置为每 2 小时执行一次的主会话系统事件：

```
Schedule: 0 9,11,13,15,17,19,21,23 * * *
Target: main (system event)
```

### 静默模式（默认设置）
```
AUTOMATION: Daily memory save. Review today's conversation for anything worth remembering.
Look for: decisions made, preferences expressed, new info about people/projects,
lessons learned, things the user asked you to remember, emotional context worth noting.

Create or update workspace/memory/YYYY-MM-DD.md (today's date) with a daily note
capturing what matters. If anything is significant enough for long-term memory,
also update workspace/MEMORY.md.

If it's been a quiet day with nothing notable, skip silently.
Be selective — capture signal, not noise. Write like future-you will need this context.
Do NOT message the user about this — just do it quietly.
```

### 通知模式（可选）
如果您希望在记忆被保存时收到通知，请将以下内容替换为：
```
After saving, send a brief summary of what was captured (1-2 lines max).
```

## 内存文件格式

### 每日笔记（`memory/YYYY-MM-DD.md`）
按主题和时间组织的原始日志，包含以下内容：
- 作出的决策
- 项目更新
- 表达的偏好
- 学到的经验
- 重要的互动记录

### 长期记忆（`MEMORY.md`）
经过筛选的、具有长期价值的精华内容，会在发生重要事件时更新。

## 关键设计决策

- **目标会话**：作为主会话中的系统事件运行，因此可以访问对话记录。
- **默认静默模式**：可通过“通知模式”进行配置。
- **选择性记录**：仅记录重要内容，忽略安静时段的对话。
- **双层记忆结构**：`memory/YYYY-MM-DD.md` 存储原始对话记录，`MEMORY.md` 存储经过整理的精华内容。

## 系统要求

- 需要支持 cron 的 OpenClaw。
- 主会话应具备系统事件执行能力。
- 工作空间中必须有可写的 `memory/` 目录。