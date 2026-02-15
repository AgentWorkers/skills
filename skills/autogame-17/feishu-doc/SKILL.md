---
name: feishu-doc
description: 从 Feishu（Lark）的 Wiki、文档、表格（ Sheets）以及 Bitable 中获取内容。系统会自动将 Wiki 链接解析为对应的实际内容，并将获取到的内容转换为 Markdown 格式。
tags: [feishu, lark, wiki, doc, sheet, document, reader, writer]
---

# Feishu 文档技能

该技能用于从 Feishu（Lark）的 Wiki、文档、表格（Sheets）和 Bitable 中获取内容，并能够编写和更新文档。

## 先决条件

- 请先安装 `feishu-common`。
- 该技能依赖于 `../feishu-common/index.js` 文件，用于处理令牌（token）和 API 认证。

## 功能

- **读取**：从 Feishu 的文档、表格和 Wiki 中获取内容。
- **创建**：创建新的空白文档。
- **编写**：使用 Markdown 格式覆盖文档内容。
- **追加**：将 Markdown 内容追加到文档的末尾。
- **区块**：列出、获取、更新和删除特定的文档区块。

## 处理长文档（长度不限）

对于超过 LLM 输出限制（约 2000-4000 个令牌）的长文档，可以按照以下步骤操作：
1. 首先创建文档以获取一个 `doc_token`。
2. 将文档内容分成逻辑上独立的章节（例如：引言、第 1 章、第 2 章等）。
3. 使用 `feishu_doc_append` 方法依次追加每个章节的内容。
- 如果文档内容非常长，切勿尝试一次性通过 `feishu_doc_write` 方法写入整个文档，而是使用循环追加的方式。

## 使用方法

```bash
# Read
node index.js --action read --token <doc_token>

# Create
node index.js --action create --title "My Doc"

# Write (Overwrite)
node index.js --action write --token <doc_token> --content "# Title\nHello world"

# Append
node index.js --action append --token <doc_token> --content "## Section 2\nMore text"
```

## 配置

在技能的根目录下创建一个 `config.json` 文件，或设置环境变量：

```json
{
  "app_id": "YOUR_APP_ID",
  "app_secret": "YOUR_APP_SECRET"
}
```

环境变量：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`