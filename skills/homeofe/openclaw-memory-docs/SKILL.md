---
name: openclaw-memory-docs
description: "OpenClaw插件：专为文档级内存管理设计，支持显式数据捕获功能，提供本地可搜索的数据存储空间，并具备安全的数据编辑（redaction）机制。"
---
# openclaw-memory-docs

这是一个**OpenClaw Gateway插件**（而非代理技能），它提供了一个保守的、易于审计的内存存储解决方案。

该插件专为项目文档和需要长期保存的笔记设计，注重以下特点：
- 对存储内容的明确控制；
- 防止机密信息被意外存储；
- 采用确定性的、以本地数据为主的数据存储策略。

## 功能介绍

- 提供了一个控制命令：`/remember-doc <text>`，用于保存文档内容；
- 提供了一个搜索工具：`docs_memory_search({ query, limit })`，用于查找文档；
- 将数据存储在本地的**JSONL文件**中（每行存储一条记录）；
- 使用确定性的本地数据存储机制，实现无需外部服务即可进行语义搜索的功能；
- 支持对常见的机密信息（如API密钥、令牌、私钥等）进行自动遮蔽处理。

## 安装方法

### 在ClawHub中安装
```bash
clawhub install openclaw-memory-docs
```

### 开发者使用说明
```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-memory-docs
openclaw gateway restart
```

## 使用规范

### 保存文档

使用`/remember-doc`命令来保存任何属于文档级别的内容，并确保这些内容具有稳定性。

示例：
```
/remember-doc Dubai: decide A vs B, then collect facts, then prepare a tax advisor briefing.
```

插件会保存文档内容并返回确认信息。如果检测到机密信息，会对其进行遮蔽处理，但仍会保存遮蔽后的版本。

### 搜索文档

调用`docs_memory_search()`工具进行搜索，该工具会返回包含搜索结果及其相关文本片段的列表。

## 配置选项
```json
{
  "plugins": {
    "entries": {
      "openclaw-memory-docs": {
        "enabled": true,
        "config": {
          "storePath": "~/.openclaw/workspace/memory/docs-memory.jsonl",
          "dims": 256,
          "redactSecrets": true,
          "defaultTags": ["docs"]
        }
      }
    }
  }
}
```

### 注意事项

- 该插件**不**自动捕获用户输入的消息；
- 如果需要自动捕获消息，请使用`openclaw-memory-brain`插件。