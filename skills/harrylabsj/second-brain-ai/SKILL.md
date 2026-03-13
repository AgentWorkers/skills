---
name: second-brain-ai
description: 从用户指定的本地 Markdown 知识库中读取、捕获、搜索、关联信息，并整合相关内容。该功能通过基于文件的扫描技术和智能链接机制实现。适用于用户需要为 Markdown 笔记创建一个“第二大脑”/笔记存储层的情况，具体用途包括：保存想法、搜索过去的笔记、查找相关笔记或回链、构建信息包、向现有笔记添加内容，或获取智能链接建议。使用时必须提供明确的 `SECOND_BRAIN_VAULT` 路径；请勿将其用于广泛的文件系统访问。
---
# Second Brain AI Skill v2.1.3

这是一个轻量级的AI技能，用于操作用户自定义的Markdown知识库（支持Obsidian/Logseq格式），具备受控的写入操作、基于文件的搜索功能以及智能的链接建议功能。

## 系统要求

- Node.js版本需大于或等于16.0.0
- 需要一个包含Markdown文件（.md格式）的本地目录
- 必须明确设置环境变量`SECOND_BRAIN_VAULT`
- 可选功能：支持Frontmatter格式（YAML格式）
- 可选功能：支持WikiLinks格式（例如`[[Note Title]]`）

## 配置方法

在运行任何脚本之前，通过环境变量设置知识库的路径：

```bash
export SECOND_BRAIN_VAULT="/absolute/path/to/your/vault"
```

该技能不再自动将数据写入默认的主目录知识库中；用户必须明确指定知识库的路径。

## 安全限制

- 仅允许在用户明确指定的知识库路径下使用该技能
- 禁止在配置的知识库范围之外进行广泛的文件系统搜索
- 仅当调用者明确设置了`allow_write: true`时，才允许执行写入操作
- 所有写入操作都必须严格限制在配置的知识库路径范围内
- 该技能不会在配置的知识库范围之外进行任何写入操作
- 本版本仅使用基于文件的扫描方式，避免依赖任何原生数据库

## 受控的写入范围

本版本支持读写操作，但写入操作需要用户在输入数据中明确表示同意（通过设置`allow_write: true`）。初始化笔记、创建新笔记以及追加内容等操作均需满足此条件。所有操作均受配置的知识库路径限制。

## 提供的工具

### 1. search_notes

通过文件系统扫描，根据笔记的标题或内容中的关键词进行搜索。

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

### 2. find_related

查找与给定主题或笔记相关的笔记。

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

**关联类型：** `topic-match`、`links-to`、`mentions`、`shared-tags`、`similar-content`

---

### 3. suggest_links

根据笔记内容的相似性，提供智能的链接建议。

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

### 4. get_backlinks

获取所有链接到特定笔记的其他笔记。

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

### 5. build_context_pack

为某个主题生成上下文包（供代理程序使用）。

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

## 写入操作的安全性

对于支持写入操作的工具，输入数据中必须包含`allow_write: true`这一字段。如果没有该字段，工具将拒绝执行任何修改知识库的操作。