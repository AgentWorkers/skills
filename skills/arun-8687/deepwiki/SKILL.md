---
name: deepwiki
description: 查询 DeepWiki MCP 服务器上的 GitHub 仓库文档、wiki 结构以及由 AI 支持的问题。
homepage: https://docs.devin.ai/work-with-devin/deepwiki-mcp
---

# DeepWiki

使用此技能，您可以通过 DeepWiki MCP 服务器访问公共 GitHub 仓库的文档。您可以搜索仓库的 wiki，获取其文档结构，并根据仓库的文档提出复杂的问题。

## 命令

### 提问
关于任何 GitHub 仓库的问题，都可以通过此命令获得基于人工智能的、与上下文相关的回答。
```bash
node ./scripts/deepwiki.js ask <owner/repo> "your question"
```

### 查看 Wiki 结构
获取 GitHub 仓库的文档主题列表。
```bash
node ./scripts/deepwiki.js structure <owner/repo>
```

### 查看 Wiki 内容
查看 GitHub 仓库 wiki 中特定路径的文档内容。
```bash
node ./scripts/deepwiki.js contents <owner/repo> <path>
```

## 示例

**询问关于 Devin 的 MCP 使用方法：**
```bash
node ./scripts/deepwiki.js ask cognitionlabs/devin "How do I use MCP?"
```

**获取 React 文档的结构：**
```bash
node ./scripts/deepwiki.js structure facebook/react
```

## 注意事项
- 基础服务器：`https://mcp.deepwiki.com/mcp`
- 仅适用于公共仓库。
- 无需身份验证。