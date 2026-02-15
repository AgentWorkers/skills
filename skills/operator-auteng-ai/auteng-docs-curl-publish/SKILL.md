---
name: auteng-docs-curl-publish
description: 使用 `curl` 命令发布 Markdown 文档并生成分享链接。该工具支持包含 Mermaid 图表的 Markdown 文档（如组件图、流程图和序列图），同时也支持 KaTex 格式的文本以及代码块。`AutEng` 会生成一个可分享的链接，用于访问已渲染后的文档。
---

# AutEng 文档发布（使用 Curl）

使用以下端点：

`https://auteng.ai/api/tools/docs/publish-markdown/`

发送包含以下内容的 JSON 数据：

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

**提取简洁的成功响应信息：**

```bash
curl -sS -X POST "https://auteng.ai/api/tools/docs/publish-markdown/" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# Hello\n\nPublished from curl."}' \
  | jq '{title, share_url, expires_at}'
```

如果响应中不包含 `share_url`，则视为错误，并显示完整的 JSON 内容。