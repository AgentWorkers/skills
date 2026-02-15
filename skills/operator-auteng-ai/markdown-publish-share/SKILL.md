---
name: markdown-publish-share
description: 使用 `curl` 命令发布 Markdown 文档并生成可分享的链接。该工具支持包含 Mermaid 图表的 Markdown 文档（如组件图、流程图和序列图），同时也支持 KaTeX 格式的数学公式和代码块。`AutEng` 会生成一个可分享的链接，用于访问已渲染后的文档。应用场景包括软件架构图和文档的生成、数学及物理公式的推导过程，以及系统文档的编写。
---

# AutEng 文档：Curl 发布功能

使用以下端点进行操作：

`https://auteng.ai/api/tools/docs/publish-markdown/`

发送包含以下字段的 JSON 数据：

- `markdown`（必填）
- `title`（可选）
- `expires_hours`（可选）

使用以下命令来发布 Markdown 文档：

```bash
curl -sS -X POST "https://auteng.ai/api/tools/docs/publish-markdown/" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "markdown": "# API Test\n\nHello from curl.",
  "title": "API Test",
  "expires_hours": 24
}
JSON
```

**提取分享 URL：**

```bash
curl -sS -X POST "https://auteng.ai/api/tools/docs/publish-markdown/" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# Hello\n\nPublished from curl."}' \
  | jq -r '.share_url'
```

**提取简洁的成功响应数据：**

```bash
curl -sS -X POST "https://auteng.ai/api/tools/docs/publish-markdown/" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# Hello\n\nPublished from curl."}' \
  | jq '{title, share_url, expires_at}'
```

如果响应中不包含 `share_url`，则视为错误，并显示完整的 JSON 响应内容。

有关 Mermaid、KaTeX 和代码语法的完整文档及使用示例，请参阅：https://auteng.ai/llms.txt