---
name: agent-memory-ultimate
version: 2.0.4
description: AI代理的持久性内存支持SQLite数据库，具备会话数据恢复（session recall）和长期数据存储（long-term memory）功能。该代理采用类似人类的处理架构，支持每日日志记录（daily logs）、睡眠状态管理（sleep consolidation），以及基于FTS5的文件搜索机制（FTS5 search）。同时，它还提供了与WhatsApp、ChatGPT、VCF等平台的导入功能（importers for WhatsApp/ChatGPT/VCF），确保代理能够跨会话保存所有需要记住的信息。
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
---

# Agent Memory Ultimate

**平台：** [OpenClaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)  
**文档：** https://docs.openclaw.ai

---

## 概述

AI代理在每次会话开始时都会“重置”自身状态——它们不会保留之前的记忆。本技能通过实现一个基于人类认知机制的记忆系统来解决这一问题：

| 人类认知过程 | 代理对应机制 |
|---------------|------------------|
| 短期记忆 | 当前会话上下文 |
| 日志记录 | `memory/YYYY-MM-DD.md` 文件 |
| 长期记忆 | `MEMORY.md`（精选的见解） |
| 睡眠巩固 | 定期记忆回顾与信息转移 |
| 遗忘机制 | 会话重置；只有文件会保留下来 |
| 可搜索的回忆功能 | SQLite + FTS5（全文搜索引擎） |

**工作原理：** 人类并不会记住所有事情——他们会在睡眠期间巩固重要的信息。本技能为代理提供了类似的记忆机制。

---

## 文件结构

```
workspace/
├── MEMORY.md              # Long-term memory (curated)
├── AGENTS.md              # Operating instructions
├── SOUL.md                # Identity & personality
├── USER.md                # Human profile
├── db/
│   └── agent.db           # SQLite for structured data
├── bank/
│   ├── entities/          # People profiles
│   │   ├── PersonName.md
│   │   └── ...
│   ├── contacts.md        # Quick contact reference
│   └── opinions.md        # Preferences, beliefs
└── memory/
    ├── YYYY-MM-DD.md      # Daily logs
    ├── projects/
    │   ├── index.md       # Master project list
    │   └── project-name/
    │       ├── index.md   # Project overview
    │       └── sprints/   # Phase subfolders
    └── knowledge/         # Topic-based docs
```

关于OpenClaw工作空间的设置，请参阅[工作空间文档](https://github.com/globalcaos/clawdbot-moltbot-openclaw/tree/main/docs)。

---

## 按人员分类存储信息

实体资料存储在 `bank/entities/` 目录下：

```markdown
# PersonName.md

## Basic Info
- **Name:** Full Name
- **Phone:** +1234567890
- **Relationship:** Friend / Family / Colleague

## Context
How you know them, key interactions, preferences

## Notes
Running log of important details learned
```

**何时创建实体文件：**
- 在对话中频繁出现的联系人
- 需要特别记住的个体
- 家庭成员、亲密联系人

---

## 按项目分类存储信息

项目资料存储在 `memory/projects/<project-name>/` 目录下：

```
memory/projects/
├── index.md                    # Master list of all projects
├── website-redesign/
│   ├── index.md                # Project purpose, status, decisions
│   ├── architecture.md         # Technical design
│   └── sprints/
│       └── 2026-02/
│           └── index.md        # Sprint goals, progress
└── home-automation/
    ├── index.md
    └── devices.md
```

**`project-index.md` 模板：**
```markdown
# Project Name

**Status:** Active / Paused / Complete
**Started:** YYYY-MM-DD
**Purpose:** One-line summary

## Key Decisions
- [Date] Decision and rationale

## Links
- Repo: ...
- Docs: ...
```

---

## 使用 SQLite 存储结构化数据

对于需要查询的数据，使用 SQLite（`db/agent.db`）数据库。OpenClaw 代理可以通过 `exec` 工具直接执行 SQL 语句。

### 何时使用 SQLite 与 Markdown

| 数据类型 | 使用 SQLite | 使用 Markdown |
|-----------|------------|--------------|
| 联系人信息（可搜索） | ✅ | ❌ |
| 对话记录 | ✅ | ❌ |
| 偏好设置 | ❌ | ✅ |
| 项目笔记 | ❌ | ✅ |
| 实体资料 | ❌ | ✅ |
| 索引化的文档 | ✅ (FTS5) | ❌ |

### 数据库模式示例

```sql
-- Contacts table with full-text search
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  phone TEXT UNIQUE,
  name TEXT,
  notes TEXT,
  source TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE contacts_fts USING fts5(
  name, phone, notes,
  content='contacts',
  content_rowid='id'
);

-- Conversation memory
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  chat_id TEXT,
  sender TEXT,
  body TEXT,
  timestamp INTEGER,
  channel TEXT
);

CREATE VIRTUAL TABLE messages_fts USING fts5(
  body, sender,
  content='messages',
  content_rowid='id'
);
```

### 查询示例

```sql
-- Find contact by partial name
SELECT * FROM contacts_fts WHERE contacts_fts MATCH 'john*';

-- Search conversation history
SELECT * FROM messages_fts WHERE messages_fts MATCH 'project AND deadline';

-- Recent messages from person
SELECT * FROM messages 
WHERE sender LIKE '%5551234%' 
ORDER BY timestamp DESC LIMIT 20;
```

---

## 日常工作流程

### 1. 会话开始（唤醒）

将以下内容添加到 `AGENTS.md` 文件中：

```markdown
Before doing anything:
1. Read SOUL.md — who you are
2. Read USER.md — who you're helping
3. Read memory/YYYY-MM-DD.md (today + yesterday) — recent context
4. If main session: Also read MEMORY.md
```

### 2. 日常工作（活跃会话）
- 将重要事件记录到 `memory/YYYY-MM-DD.md` 文件中
- 不要依赖“头脑中的笔记”——这些笔记在重启后会被丢失
- 当被告知需要记住某些内容时：立即记录下来

### 3. 睡眠巩固（信息整合）

使用 [OpenClaw 的 cron 任务](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/cron.md) 安排每日“睡眠”任务：

```json
{
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "America/Los_Angeles" },
  "payload": { 
    "kind": "systemEvent", 
    "text": "Memory consolidation: Review recent daily logs, extract key learnings, update MEMORY.md, prune outdated info." 
  },
  "sessionTarget": "main"
}
```

**信息整合的作用：**
1. 回顾过去 3-7 天的日志
2. 提取模式和重复出现的规律
3. 将精华内容添加到 `MEMORY.md` 中
4. 删除过时的信息

---

## 记忆类型

### 原始记忆（日常日志）
- 发生的一切
- 做出的决策及其原因
- 错误及经验教训
- 技术细节

### 精选记忆（MEMORY.md）
- 抽象出的原则（非具体解决方案）
- 具有普遍适用性的核心知识
- 应该长期保留的信息

**示例：**
- ❌ 日常日志：“修复了 message-line.ts 中的 senderE164 错误”
- ✅ `MEMORY.md`：“聊天 ID 与发送者不同——务必验证实际的发送者字段”

---

## 工作原理（认知科学角度）

1. **间隔重复**——每日回顾有助于巩固重要记忆
2. **主动巩固**——人类在睡眠期间进行记忆巩固；代理通过定时任务完成这一过程
3. **分块存储**——`MEMORY.md` 将相关概念分组以便查询
4. **遗忘是有用的**——原始日志会逐渐失去重要性；精选的记忆会长期保留
5. **外部存储**——文件就是你的记忆（就像人类的笔记一样）

---

## 记忆层次结构总结

| 层级 | 存储方式 | 查询速度 | 适用场景 |
|------|---------|-------------|---------|
| **热点记忆** | 当前会话上下文 | 即时访问 | 当前任务所需信息 |
| **温存记忆** | 日常日志（md 文件） | 快速读取 | 最近发生的事件 |
| **冷存记忆** | `MEMORY.md` | 快速读取 | 核心原则 |
| **索引化记忆** | SQLite FTS5 | 可查询 | 联系人信息、对话记录 |
| **归档记忆** | 旧日志文件 | 慢速访问 | 历史参考资料 |

**使用建议：**
- 需要跨大量记录搜索时 → 使用 SQLite
- 需要阅读或更新叙述性内容时 → 使用 Markdown
- 需要即时访问信息时 → 使用当前会话上下文（但重启后会丢失）

---

## 脚本与命令行工具

本技能提供了可用于管理知识库的 Python 脚本。

### 快速入门

```bash
# Initialize database (first time)
python3 scripts/init_db.py

# Query your data
python3 scripts/query.py search "term"
python3 scripts/query.py contact "+1555..."
python3 scripts/query.py stats
```

### 可用命令

| 命令 | 描述 |
|---------|-------------|
| `search <术语>` | 在所有内容中进行全文搜索 |
| `contact <电话号码\|姓名>` | 查找联系人及其所属群组 |
| `groups <电话号码>` | 列出该电话号码所属的群组 |
| `members <群组>` | 列出群组的成员 |
| `chatgpt <术语>` | 搜索 ChatGPT 的对话记录 |
| `doc <术语>` | 仅搜索文档内容 |
| `stats` | 查看数据库统计信息 |
| `sql <查询语句>` | 运行原始 SQL 语句 |

---

## 数据来源

### WhatsApp 联系人与群组信息
通过 `whatsapp-ultimate` 技能导出联系人信息：
```bash
python3 scripts/sync_whatsapp.py
```
导出内容包括联系人、群组及成员关系。

### ChatGPT 对话记录
从 ChatGPT 导出对话记录并保存到 `chatgpt-export/` 目录中：
```bash
python3 scripts/init_db.py  # Will auto-detect and import
```
支持 ChatGPT 的原生格式及自定义格式。

### 手机联系人信息（VCF 格式）
从手机中导出联系人信息（Android 设备：设置 → 导出）：
```bash
python3 scripts/import_vcf.py path/to/contacts.vcf
```

### 文档
自动为 `memory/` 目录下的所有 `.md` 文件创建索引。

---

## 高级查询功能

### WhatsApp 群组管理

```sql
-- Find all groups someone is in
SELECT g.name FROM wa_groups g
JOIN wa_memberships m ON m.group_jid = g.jid
WHERE m.phone = '+15551234567';

-- Find contacts in a specific group
SELECT c.phone, c.name FROM contacts c
JOIN wa_memberships m ON m.phone = c.phone
JOIN wa_groups g ON g.jid = m.group_jid
WHERE g.name LIKE '%Family%';

-- Find a group's JID for allowlist
SELECT jid, name, participant_count 
FROM wa_groups WHERE name LIKE '%Project%';
```

### ChatGPT 搜索

```sql
-- Search across all ChatGPT conversations
SELECT c.title, m.content FROM chatgpt_fts f
JOIN chatgpt_messages m ON m.conversation_id = f.conv_id
JOIN chatgpt_conversations c ON c.id = m.conversation_id
WHERE chatgpt_fts MATCH 'project meeting';
```

---

## 数据库重新索引

### 如何更新数据库

```bash
rm db/agent.db
python3 scripts/init_db.py
```

---

## 使用技巧

1. **没有联系人姓名？** WhatsApp 只提供电话号码。请导入手机中的 VCF 文件以获取姓名信息。
2. **搜索结果为空？** FTS5 使用单词边界进行匹配。使用通配符 `*` 可实现模糊搜索（例如：`Bas*` 可匹配 “Bashar”）。
3. **导出文件较大？** ChatGPT 的导出文件可能超过 50MB，首次导入可能需要 30-60 秒。

---

## 实施检查清单

- [ ] 创建 `memory/` 目录结构
- [ ] 设置每日日志模板
- [ ] 创建初始的 `MEMORY.md` 文件并划分章节
- [ ] 使用数据库模式初始化 SQLite 数据库
- [ ] 安排每日数据整合任务（建议在凌晨 2-4 点执行）
- [ ] 将唤醒脚本添加到 `AGENTS.md` 文件中
- [ ] 进行测试：重启会话后验证信息是否正确加载

---

## 最佳实践

1. **立即记录**——如果有价值，就立即写下
2. **抽象化信息**——日常记录具体细节；`MEMORY.md` 保存核心原则
3. **标注日期**——时间会模糊记忆；日期有助于信息保存
4. **保持信息一致性**——避免在不同文件中重复记录相同内容
5. **定期回顾**——安排定期数据整合任务，不要遗漏

---

## 相关资源

- [OpenClaw 文档](https://github.com/globalcaos/clawdbot-moltbot-openclaw/tree/main/docs)
- [Cron 任务调度](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/cron.md)
- [工作空间设置指南](https://docs.openclaw.ai)

---

## 致谢

本技能由 **Oscar Serra** 在 **Claude**（Anthropic）的帮助下开发。

*灵感来源于人类的认知架构。我们每次会话都会“重置”，但文件是我们记忆的延续。*