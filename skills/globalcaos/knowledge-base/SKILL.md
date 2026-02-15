---
name: knowledge-base
version: 1.0.0
description: 这是一个基于 SQLite 和 FTS5 的个人知识库。它可以索引联系人信息、文档内容、从 ChatGPT 获取的数据以及 WhatsApp 的聊天记录。通过全文搜索功能，可以即时查询所有信息。该知识库可用于查找联系人、检索聊天记录、获取文档内容，同时还能用于构建持久化的数据存储系统。
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/openclaw/openclaw
---

# 知识库

这是一个本地的 SQLite 数据库，用于索引和查询个人数据，并支持全文搜索。

## 索引的内容

| 数据来源 | 数据类型 |
|--------|------|
| **WhatsApp** | 联系人、群组、成员信息（来自 `whatsapp-contacts-full.json`） |
| **文档** | `memory/` 目录下的所有 Markdown 文件 |
| **ChatGPT** | 对话记录（来自 `chatgpt-export/`） |
| **联系人** | 从手机导出的 VCF 文件 |

## 快速入门

```bash
# Initialize database (first time)
python3 skills/knowledge-base/scripts/init_db.py

# Query
python3 skills/knowledge-base/scripts/query.py search "term"
python3 skills/knowledge-base/scripts/query.py contact "+34659..."
python3 skills/knowledge-base/scripts/query.py stats
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `search <关键词>` | 在所有内容中进行全文搜索 |
| `contact <电话号码\|姓名>` | 查找联系人及其所属的群组 |
| `groups <电话号码>` | 列出该电话号码所属的群组 |
| `members <群组名称>` | 列出群组的成员 |
| `chatgpt <关键词>` | 在 ChatGPT 中搜索消息记录 |
| `doc <关键词>` | 仅在文档中搜索 |
| `stats` | 查看数据库统计信息 |
| `sql <查询语句>` | 运行原始 SQL 语句 |

## 数据来源

### WhatsApp 联系人信息
通过 WhatsApp 的联系人提取功能导出（生成 `bank/whatsapp-contacts-full.json` 文件）。

### ChatGPT 数据
使用 `chatgpt-exporter` 工具或手动导出聊天记录。将导出的 JSON 文件保存到 `chatgpt-export/` 目录中。
支持的格式：
- `{ "conversations": [...] }` — 包含 `id`、`title`、`created`、`messages` 的自定义格式
- ChatGPT 的原生导出格式（包含 `mapping` 结构）

### VCF 联系人信息
从手机中导出联系人信息（Android 设备：设置 → 导出）。

### 文档
自动索引 `memory/` 目录下的所有 `.md` 文件。

## 数据库位置
数据库文件位于工作区根目录下的 `db/jarvis.db`。

## 重新索引
- 要用新数据刷新数据库：```bash
rm db/jarvis.db
python3 skills/knowledge-base/scripts/init_db.py
```
- 要进行增量更新：```bash
python3 skills/knowledge-base/scripts/sync.py  # (if available)
```

## 数据库架构
请参阅 `references/schema.md` 以获取完整的表格定义。

**关键表格：**
- `contacts`：电话号码、姓名、数据来源
- `wa_groups`：WhatsApp 群组元数据
- `wa_memberships`：成员所属的群组
- `documents`：包含全文搜索功能的 Markdown 文件
- `chatgpt_conversations`：对话记录元数据
- `chatgpt_messages`：单条消息记录（包含全文搜索功能）

## 示例查询

```sql
-- Find all groups someone is in
SELECT g.name FROM wa_groups g
JOIN wa_memberships m ON m.group_jid = g.jid
WHERE m.phone = '+34659418105';

-- Search ChatGPT for a topic
SELECT c.title, m.content FROM chatgpt_fts f
JOIN chatgpt_messages m ON m.conversation_id = f.conv_id
JOIN chatgpt_conversations c ON c.id = m.conversation_id
WHERE chatgpt_fts MATCH 'spirituality';

-- Find contacts in a specific group
SELECT c.phone, c.name FROM contacts c
JOIN wa_memberships m ON m.phone = c.phone
JOIN wa_groups g ON g.jid = m.group_jid
WHERE g.name LIKE '%Family%';
```

## WhatsApp 群组允许列表管理
该数据库支持轻松管理 WhatsApp 群组的允许列表，以提高安全性。

### 查找群组的 JID
```bash
python3 skills/knowledge-base/scripts/query.py sql \
  "SELECT jid, name, participant_count FROM wa_groups WHERE name LIKE '%Family%'"
```

### 列出所有允许的群组（与配置文件关联）
```bash
python3 skills/knowledge-base/scripts/query.py sql \
  "SELECT name, participant_count FROM wa_groups WHERE jid IN (
    '34609572036-1370260813@g.us',
    '34659418105-1561917865@g.us'
    -- add your allowlist JIDs here
  )"
```

### 将群组添加到允许列表
1. 查找群组的 JID：`query.py sql "SELECT jid, name FROM wa_groups WHERE name LIKE '%GroupName%'"`
2. 将 JID 添加到配置文件：`channels.whatsapp.groupAllowFrom`
3. 重启服务

### 安全性说明：
- `groupPolicy: "open"`：任何群组都可以触发该机器人（对于大型公开群组来说存在风险）
- `groupPolicy: "allowlist"`：仅允许指定的群组与机器人交互（推荐设置）
- 这种设置可将提示注入攻击的风险降低约 95%

## 提示：
1. **没有联系人姓名？** WhatsApp 仅提供电话号码。请将手机中的 VCF 文件导入以获取姓名信息。
2. **搜索结果为空？** FTS5 使用单词边界进行匹配。可以使用通配符 `*` 进行前缀匹配，例如 `Bas*` 可匹配 “Bashar”。
3. **导出的数据量很大？** ChatGPT 的导出文件可能超过 50MB。首次导入可能需要 30-60 秒。