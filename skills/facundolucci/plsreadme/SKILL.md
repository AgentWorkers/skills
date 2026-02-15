---
name: plsreadme
description: 您可以通过 plsreadme.com 将 Markdown 文件和文本分享为清晰、易读的网页链接。当有人请求分享文档（如 README、PRD、提案、笔记等 Markdown 文件）时，可以使用此服务。该服务还支持“创建预览链接”、“将内容分享为网页”或“使内容更易阅读”的功能。使用此服务需要 plsreadme MCP 服务器（通过 npx plsreadme-mcp 命令安装）。
---

# 请阅读此文档（Please Read This Documentation）

您可以通过将 Markdown 文件转换为简洁的 `plsrd.me` 链接来分享它。MCP 提供了两种工具来实现这一功能：

## 设置（Setup）

**方法一：** 将 MCP 服务器添加到您的客户端中：  
```json
{
  "mcpServers": {
    "plsreadme": {
      "command": "npx",
      "args": ["-y", "plsreadme-mcp"]
    }
  }
}
```

**方法二：** 使用远程端点（无需安装）：  
```json
{
  "mcpServers": {
    "plsreadme": {
      "url": "https://plsreadme.com/mcp"
    }
  }
}
```

## 工具（Tools）

- **`plsreadme_share_file`** — 通过文件路径分享本地的 `.md` 文件。该工具会从磁盘读取文件、上传到服务器并返回共享链接。  
- **`plsreadme_share_text`** — 直接分享文本（优先支持 Markdown 格式；也支持纯文本）。适用于生成的内容、对话输出或编写的文档。

## 使用指南（Usage Guidelines）

- 文件大小上限：200KB  
- 共享的链接是永久有效的且可公开访问的——在分享敏感内容前请先征得用户同意。  
- 如果输入内容不是 Markdown 格式，请先使用您自己的工具对其进行转换（或让 `plsreadme_share_text` 自动将其转换为 Markdown 格式）。  
- 文档中的第一个 `# 标题` 将作为文档的标题显示。  
- 输出结果包含一个便于阅读的链接以及原始 Markdown 文件的链接。

## 示例用法（Example Prompts）：

- “将此 README 文件分享到 plsreadme 上。”  
- “为 `docs/api.md` 文件创建一个可共享的链接。”  
- “将此文档转换为一个可阅读的网页以便发送。”  
- “将这份 PRD 文件以链接的形式分享出去。”