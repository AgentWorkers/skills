---
name: second-brain-ai
description: 通过 SQLite 索引和智能链接功能，能够从 Markdown 知识库中读取、捕获、搜索、关联并整合相关信息。当用户需要一个辅助记忆工具（即“第二大脑”或外部知识库）来管理笔记时，该功能非常实用：用户可以保存想法、搜索过去的笔记、查找相关内容或回链、构建知识包、向现有笔记添加新内容，或者获取智能的链接建议。
---
# Second Brain AI Skill v2.0.0

这是一个轻量级的工具，用于管理基于 Markdown 的知识库（支持 Obsidian/Logseq 格式），并利用 SQLite 索引实现快速搜索和智能链接建议功能。

## 必备条件

- Node.js 版本 >= 16.0.0
- 包含 Markdown 文件（.md 格式）的本地目录
- 可选：支持前置内容（YAML 格式）
- 可选：支持 WikiLinks（格式：`[[Note Title]]`）

## 配置

通过环境变量设置存储目录的路径：

```bash
export SECOND_BRAIN_VAULT="/path/to/your/vault"
```

或者使用默认路径：`~/Documents/SecondBrain`

## 工具

### 1. init_vault

使用标准文件夹结构初始化一个新的 Second Brain 存储库，并创建 SQLite 索引。

**使用方法：** `node scripts/init_vault.js`

**输出结果：**
```json
{
  "status": "success",
  "path": "/Users/.../Documents/SecondBrain",
  "folders": ["00-Inbox", "01-Daily", "02-Ideas", ...],
  "index": "/Users/.../.secondbrain/index.db"
}
```

---

### 2. search_notes

根据标题或内容中的关键词搜索笔记。使用 SQLite 索引，并采用 BM25 评分算法进行排序。

**输入协议：**
```json
{
  "query": "AI agent",    // Required (aliases: topic, title, q)
  "limit": 5,             // Optional, default: 5
  "use_index": true       // Optional, default: true
}
```

**输出结果：**
```json
{
  "query": "AI agent",
  "total": 3,
  "results": [
    {
      "path": "02-Ideas/2026-03-13-AI-电商.md",
      "title": "AI电商",
      "snippet": "...AI agent 可以替代平台撮合...",
      "score": 12.5,
      "rank": 1,
      "modified": "2026-03-13",
      "tags": ["ai", "电商"]
    }
  ]
}
```

---

### 3. capture_note

创建一个带有自动生成前置内容的新的笔记。

**输入协议：**
```json
{
  "title": "New Idea",              // Required
  "content": "Your note content",   // Optional
  "type": "idea",                   // Optional: idea|project|person|concept|reading|daily|moc
  "tags": ["ai", "thought"],        // Optional
  "links": ["Related Note"]         // Optional: WikiLinks to other notes
}
```

**笔记类型及对应的文件夹结构：**
- `idea` → 02-想法/
- `project` → 03-项目/
- `person` → 04-人物/
- `concept` → 05-概念/
- `reading` → 06-阅读/
- `daily` → 01-每日笔记/
- `moc` → 07-临时文件/
- `default` → 00-收件箱/

**输出结果：**
```json
{
  "status": "success",
  "path": "02-Ideas/2026-03-13-New-Idea.md",
  "title": "New Idea",
  "type": "idea"
}
```

---

### 4. append_note

向现有笔记中添加内容（如果笔记不存在，则会创建新笔记）。

**输入协议：**
```json
{
  "title": "Existing Note",         // Required: Note title to append to
  "content": "Additional content",  // Required: Content to append
  "section": "Thoughts",            // Optional: Section heading to add under
  "timestamp": true                 // Optional: Add timestamp (default: true)
}
```

**输出结果：**
```json
{
  "status": "success",
  "path": "02-Ideas/2026-03-13-Existing-Note.md",
  "title": "Existing Note",
  "action": "appended",
  "section_added": "Thoughts"
}
```

---

### 5. find_related

查找与指定主题或笔记相关的笔记。

**输入协议：**
```json
{
  "topic": "OpenClaw",    // Required (aliases: title, note_title, query, q)
  "limit": 5              // Optional, default: 5
}
```

**输出结果：**
```json
{
  "topic": "OpenClaw",
  "topic_notes": [{"path": "...", "title": "OpenClaw", "relation": "topic-match"}],
  "related_notes": [
    {
      "path": "02-Ideas/AI-思考.md",
      "title": "AI思考",
      "relation": "mentions"
    }
  ],
  "total": 5
}
```

**关联类型：** `topic-match`（主题匹配）、`links-to`（链接到）、`mentions`（被提及）、`shared-tags`（共享标签）、`similar-content`（内容相似）

---

### 6. suggest_links

根据笔记内容生成智能链接建议。

**输入协议：**
```json
{
  "title": "My Note",       // Required: Note title to find links for
  "content": "...",         // Optional: Content to analyze (if note doesn't exist)
  "limit": 5                // Optional: Max suggestions (default: 5)
}
```

**输出结果：**
```json
{
  "title": "My Note",
  "suggestions": [
    {
      "note_title": "Related Note",
      "note_path": "02-Ideas/Related-Note.md",
      "reason": "shared-tags",
      "confidence": 0.85,
      "shared_tags": ["ai", "agent"]
    }
  ],
  "total": 5
}
```

---

### 7. get_backlinks

获取所有链接到特定笔记的笔记。

**输入协议：**
```json
{
  "note_title": "OpenClaw"    // Required (alias: title)
}
```

**输出结果：**
```json
{
  "note_title": "OpenClaw",
  "note_found": true,
  "note_path": "03-Projects/OpenClaw.md",
  "backlink_count": 2,
  "backlinks": [
    {
      "path": "02-Ideas/AI-思考.md",
      "title": "AI思考",
      "context": "...see [[OpenClaw]] for details...",
      "modified": "2026-03-13"
    }
  ]
}
```

---

### 8. build_context_pack

为某个主题生成上下文包（供其他工具使用）。

**输入协议：**
```json
{
  "topic": "AI电商",      // Required (aliases: query, title, q)
  "limit": 10             // Optional, default: 10
}
```

**输出结果：**
```json
{
  "topic": "AI电商",
  "summary": "Found 5 related notes. Top 3 most relevant notes cover: agent, 电商, 撮合.",
  "related_notes": [...],
  "key_concepts": ["agent", "电商", "撮合"],
  "stats": {
    "total_notes": 42,
    "related_found": 5,
    "returned": 3
  }
}
```

---

### 9. rebuild_index

从头开始重建 SQLite 索引（在外部编辑后使用此命令）。

**输入协议：**
```json
{}
```

**输出结果：**
```json
{
  "status": "success",
  "indexed": 42,
  "time_ms": 125,
  "index_path": "/Users/.../.secondbrain/index.db"
}
```

---

## 目录结构

该工具要求存储目录具有以下结构（结构可灵活调整）：

```
vault/
├── 00-Inbox/          # New uncategorized notes
├── 01-Daily/          # Daily notes
├── 02-Ideas/          # Ideas and thoughts
├── 03-Projects/       # Project notes
├── 04-People/         # People notes
├── 05-Concepts/       # Concept definitions
├── 06-Reading/        # Reading notes
├── 07-MOCs/           # Maps of Content
└── 99-Archive/        # Archived notes
```

## 索引结构

SQLite 索引存储在 `.secondbrain/index.db` 文件中：

- **notes**：笔记元数据（路径、标题、类型、创建时间、更新时间）
- **note_content**：可全文搜索的内容（采用 FTS5 格式）
- **links**：笔记之间的 WikiLinks
- **tags**：标签索引，便于快速查找
- **backlinks**：反向链接索引

## 笔记格式

标准的前置内容格式如下：

```yaml
---
id: 20260313-001
title: Note Title
type: idea
tags: [tag1, tag2]
created: 2026-03-13
updated: 2026-03-13
links:
  - Related Note
status: active
---
```

笔记正文支持以下格式：
- Markdown 格式
- WikiLinks：`[[Note Title]]`（用于创建超链接）
- 标签：`#tag` 或在前置内容中添加

## 忽略规则

在存储目录的根目录下创建 `.secondbrainignore` 文件，以排除某些文件不被搜索：

```
# Documentation
README.md
CHANGELOG.md

# Templates
templates/

# Archive (optional)
99-Archive/
```

默认被忽略的文件包括：`.git`、`.obsidian`、`.logseq`、`node_modules`、`.DS_Store`、`README.md`

## 测试

运行测试套件：

```bash
npm test                    # Run all tests
npm run test:init          # Test vault initialization
npm run test:capture       # Test note capture
npm run test:append        # Test append note
npm run test:search        # Test search
npm run test:related       # Test find related
npm run test:backlinks     # Test backlinks
npm run test:context       # Test context pack
npm run test:suggest       # Test link suggestions
```

## 使用示例

```bash
# Initialize vault
node scripts/init_vault.js

# Capture an idea
node scripts/capture_note.js '{"title":"AI 重构电商","content":"AI agent 可以替代平台撮合","type":"idea","tags":["ai","电商"]}'

# Append to existing note
node scripts/append_note.js '{"title":"AI 重构电商","content":"补充想法...","section":"更新"}'

# Search notes
node scripts/search_notes.js '{"query":"AI agent","limit":5}'

# Find related notes
node scripts/find_related.js '{"topic":"OpenClaw"}'

# Get backlinks
node scripts/get_backlinks.js '{"note_title":"OpenClaw"}'

# Build context pack
node scripts/build_context_pack.js '{"topic":"AI 电商","limit":10}'

# Suggest links for a note
node scripts/suggest_links.js '{"title":"AI 重构电商","limit":5}'

# Rebuild index
node scripts/rebuild_index.js
```

## 限制事项（v2.0.0）

- SQLite 需要 `better-sqlite3` 插件（如果该插件不可用，系统会自动切换为文件扫描方式）
- 目前仅支持基于关键词的搜索，不支持语义搜索或向量搜索
- 仅支持单个存储库
- 不支持并发编辑时的冲突检测
- 无内置的同步/复制功能

## 未来计划

- 引入向量嵌入技术以实现更精确的语义搜索
- 支持跨存储库搜索
- 自动生成每日复习内容
- 提供图形化界面以便浏览笔记

## 许可证

MIT 许可证