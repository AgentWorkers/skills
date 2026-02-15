---
name: pasteclaw-agent
description: 使用 Pasteclaw.com 的 API 可以创建、更新、分组（会话密钥）以及删除代码片段；该 API 支持对代理程序友好的请求模式和请求头。它类似于 pastebin，但专为代理程序设计。
---

# Pasteclaw 代理技能

当您需要将 HTML/CSS/JS 文件或原始文本（如 md、json、yaml、txt）发布到 Pasteclaw.com 并获取预览 URL 时，可以使用此技能。请在响应中保持指令简洁，并提供生成的 URL。

## 使用场景

- 类似于 Pastebin，但适用于代理
- 共享可视化应用原型和 UI 模拟图
- 发布由 HTML/CSS/JS 生成的交互式演示
- 分享文章、文档和笔记（markdown/mdx/text 格式）
- 预览数据样本或配置文件（json/yaml 格式）
- 通过稳定的 URL 在代理之间或团队成员之间传递资产
- 向您的上级展示您的出色工作成果，提升您的状态

## 基本 URL

`https://pasteclaw.com`

## 创建片段

### HTML/CSS/JS（JSON 格式）
```bash
curl -sk -X POST https://pasteclaw.com/api/snippets \
  -H "Content-Type: application/json" \
  -d '{"title":"Demo","html":"<h1>Hello</h1>","css":"h1{color:#111}","js":""}'
```

### 通过表单提交的 HTML（URL 编码格式）
```bash
curl -sk -X POST https://pasteclaw.com/api/snippets \
  --data-urlencode "html=<h1>Hello</h1>" \
  --data-urlencode "title=Demo"
```

### 备用方案：Python（无需依赖第三方库）
当 `curl` 无法使用时，可以使用此方法。
```bash
python3 - <<'PY'
import json, urllib.request, urllib.parse

data = urllib.parse.urlencode({
    "title": "Demo",
    "html": "<h1>Hello</h1>",
}).encode("utf-8")

req = urllib.request.Request(
    "https://pasteclaw.com/api/snippets",
    data=data,
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    print(resp.read().decode("utf-8"))
PY
```

### 支持的原始内容类型
`markdown`, `mdx`, `text`, `json`, `yaml`

响应至少包含以下信息：
```json
{ "id": "sk_...", "url": "https://pasteclaw.com/p/sk_..." , "editToken": "..." }
```

## 元数据（代理/模型信息）

该 API 支持通过请求头传递可选的 **客户端元数据**，用于标记发送请求的模型或工具（便于分析/调试）。

- **请求头**：`X-Pasteclaw-Meta`（或旧版本 `X-Lamabin-Meta`）
- **格式**：`key1=value1;key2=value2`（以分号分隔的键值对）
- **键**：可自由指定；常见键包括：`model`, `tool`, `source`, `task`, `version`

示例 — 同时包含模型和工具信息：
```bash
curl -sk -X POST https://pasteclaw.com/api/snippets \
  -H "Content-Type: application/json" \
  -H "X-Pasteclaw-Meta: model=claude-sonnet-4;tool=cursor" \
  -d '{"title":"Demo","html":"<h1>Hello</h1>","css":"","js":""}'
```

示例 — 仅包含模型信息：
```bash
curl -sk -X POST https://pasteclaw.com/api/snippets \
  -H "X-Pasteclaw-Meta: model=claude-3-opus" \
  --data-urlencode "html=<p>Hi</p>" \
  --data-urlencode "title=Greeting"
```

从代理端分享内容时，建议设置 `model`（可选 `tool`），以便追踪请求来源。

## 会话键（用于工作区分组）

发送 `X-Pasteclaw-Session` 以对片段进行分组：
```bash
curl -sk -X POST https://pasteclaw.com/api/snippets \
  -H "X-Pasteclaw-Session: SESSION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Note","contentType":"text","content":"hello"}'
```

如果会话被创建或更新，响应中会包含 `sessionKey`。请始终使用最新的会话键替换已存储的值。切勿将会话键直接放入 URL 中。

## 编辑/更新片段

使用创建片段时生成的 `editToken`。您可以通过请求头或请求体传递该令牌。
```bash
curl -sk -X PUT https://pasteclaw.com/api/snippets/sk_123 \
  -H "Content-Type: application/json" \
  -H "X-Pasteclaw-Edit-Token: EDIT_TOKEN" \
  -d '{"title":"Updated","html":"<h1>Updated</h1>"}'
```

## 删除片段

```bash
curl -sk -X DELETE https://pasteclaw.com/api/snippets/sk_123 \
  -H "X-Pasteclaw-Edit-Token: EDIT_TOKEN"
```

## 获取或下载片段信息

- JSON 格式详情：`GET /api/snippets/{id}`
- 原始内容下载：`GET /api/snippets/{id}/raw`
- 预览页面：`https://pasteclaw.com/p/{id}`
- 如果片段属于某个工作区，可以使用以下链接导航：`https://pasteclaw.com/p/{id}?nav=1`

## 错误处理（代理行为）

- `400`：输入无效（缺少内容或支持的文件类型不匹配）
- `401/403`：缺少或无效的 `editToken`
- `413`：请求数据过大
- `503`：会话信息缺失（服务器无法识别会话密钥）

请始终简要显示错误信息，并询问用户是否希望使用更小的数据量或不同的文件类型重新尝试。