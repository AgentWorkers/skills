---
name: granola
description: **访问 Granola AI 会议记录**  
- 支持 CSV 文件导入功能；  
- 可获取共享的会议记录；  
- 为即将推出的 API 支持做好准备（MCP）。
homepage: https://granola.ai
metadata: {"clawdbot":{"emoji":"🥣","requires":{}}}
---

# Granola

您可以访问您的 [Granola](https://granola.ai) 会议记录。Granola 是专为需要连续参加会议的人设计的智能笔记工具。

## 当前功能

### 1. CSV 导出/导入
Granola 允许将历史会议记录导出为 CSV 格式。该功能可以解析并搜索这些导出的文件。

```bash
# Parse a Granola CSV export
python3 {baseDir}/scripts/csv_import.py --file ~/Downloads/granola_export.csv

# Search parsed notes
python3 {baseDir}/scripts/csv_import.py --file ~/Downloads/granola_export.csv --search "quarterly review"
```

### 2. 共享笔记的获取
当您分享 Granola 中的笔记时，会生成一个公共 URL。该功能可以获取并解析这些共享的笔记。

```bash
# Fetch a shared note
python3 {baseDir}/scripts/fetch_shared.py --url "https://share.granola.ai/..."
```

### 3. MCP 集成（即将推出）
Granola 正在开发官方的 MCP（Model Context Protocol）支持，以便 AI 代理能够访问共享的会议记录。功能上线后：

```json
{
  "mcpServers": {
    "granola": {
      "command": "granola-mcp",
      "args": ["--api-key", "YOUR_KEY"]
    }
  }
}
```

## 如何从 Granola 中导出笔记

1. 打开 Granola 应用程序
2. 转到 **设置 → 个人资料**
3. 点击 **生成 CSV 文件**
4. CSV 文件将通过电子邮件发送给您（可能需要几个小时）

注意：CSV 导出仅包含 30 天之前的笔记，并不包含完整的会议记录文本。

## 使用示例

**导入和搜索会议记录：**
```
"Search my Granola notes for anything about the product roadmap"
"What did we discuss in last month's board meeting?"
"Find action items from my 1:1s"
```

**MCP 功能可用时：**
```
"What meetings did I have this week?"
"Summarize my meeting with John yesterday"
"What are my action items from today?"
```

## 开发计划

- [x] CSV 文件的解析功能
- [x] 共享笔记的获取功能
- [ ] MCP 集成（等待 Granola 正式发布）
- [ ] 完整的 API 访问功能（待发布）

## 链接

- [Granola 帮助中心](https://help.granola.ai)
- [导出文档](https://help.granola.ai/article/exporting-notes)
- [Granola 官网](https://granola.ai)