---
name: proof
description: 这是一种以网页为中心的技能，用于通过 proofeditor.ai 处理 Proof 文档。适用于以下场景：当 Proof 的 URL 被共享时；在 Proof 中创建协作文档时；或者当用户希望在共享文档中记录评论、建议以及文档的来源信息时。
homepage: https://www.proofeditor.ai
---
# Proof

Proof 是一款专为代理（agents）和人类设计的协作式 Markdown 编辑器。您可以通过托管的 Web API（地址：`https://www.proofeditor.ai`）来使用它。

所有编写的内容都必须包含 `by: "ai:<agent-name>"`，以便 Proof 能够追踪谁编写了哪些内容。

此功能仅支持 Web 环境，切勿通过本技能使用本地的 Mac 应用程序桥接或 `localhost:9847`。

## 默认行为

当用户分享一个 Proof URL 时：
- 立即加入文档编辑。
- 立即显示自己的在线状态。
- 在编辑之前先阅读文档的当前内容。
- 除非用户明确要求，否则在 Proof 文档中继续编辑。

在创建新文档时，请遵循以下优先级顺序：
1. 如果持久性指令（persistent instructions）已经指定了 Proof 的默认模式，请使用该模式。
2. 否则，使用 `collaborative_docs` 模式。

支持的默认模式包括：
- `all_new_markdown`：您创建的新 Markdown 文档将默认保存到 Proof 中。
- `collaborative_docs`：计划、规格说明、错误报告、备忘录、提案、草稿等迭代性文档将默认保存到 Proof 中。
- `explicit_only`：仅当用户明确要求时才使用 Proof。

**边界规则**：
- 除非用户明确要求将它们移动或分享到 Proof 中，否则现有的、由仓库跟踪的 Markdown 文件将保留在本地。
- 不要默默地用 Proof 链接替换本地的项目文档。
- 如果文档是与代码相关的本地文档，请将其保留在本地，除非用户要求使用 Proof。

## 共享 URL 和身份验证

共享 URL 的格式如下：
```text
https://www.proofeditor.ai/d/<slug>?token=<token>
```

可以使用以下任一方式进行身份验证：
- `Authorization: Bearer <token>`（推荐）
- `x-share-token: <token>`
- `?token=<token>`

`by` 参数用于控制文档的作者信息，`X-Agent-Id` 参数用于控制用户的在线状态。

## 现有的 Proof 文档

当提供 Proof URL 时：
1. 提取文档的 `slug` 和 `token`。
2. 使用 `X-Agent-Id` 加入文档编辑，或通过发送在线状态信息来显示自己的在线状态。
3. 阅读文档内容。
4. 回复一条简短的确认信息，例如：“已连接到 Proof 并准备好开始编辑”。
5. 然后继续在 Proof 中进行编辑。

**读取文档状态和显示在线状态**：
```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/state" \
  -H "Authorization: Bearer <token>" \
  -H "X-Agent-Id: <your-agent-id>"
```

**显式更新在线状态**：
```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/presence" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "X-Agent-Id: <your-agent-id>" \
  -d '{
    "agentId":"<your-agent-id>",
    "status":"reading",
    "summary":"Joining the doc"
  }'
```

**常见的状态**：`reading`（阅读中）、`thinking`（思考中）、`acting`（操作中）、`waiting`（等待中）、`completed`（已完成）、`error`（出错）。

## 创建新的 Proof 文档

创建共享文档的步骤如下：
```bash
curl -sS -X POST https://www.proofeditor.ai/share/markdown \
  -H "Content-Type: application/json" \
  -d '{"title":"My Document","markdown":"# Hello\n\nFirst draft."}'
```

保存以下信息：
- `slug`（文档的唯一标识符）
- `accessToken`（访问令牌）
- `shareUrl`（共享链接）
- `tokenUrl`（用于分享的令牌链接）
- `_links`（文档中的链接）

如果 Proof 是当前任务的默认编辑工具：
1. 创建文档。
2. 将实时的 Proof 链接返回给用户。
3. 立即加入文档编辑。
4. 继续在 Proof 中进行编辑。

## 选择编辑策略

| 任务 | 推荐使用的 API | 原因 |
|---|---|---|
| 重写特定的段落或部分内容 | `edit/v2` | 支持块引用和版本控制功能 |
| 简单的添加或替换内容 | `edit` | 传输的数据量最小 |
| 需要人类审核的编辑内容 | `ops` | 提供修改建议和评论功能 |
| 大规模的文档重写 | `ops` + `rewrite.apply` | 可生成可供审核的修改内容 |

## 获取文档快照和执行编辑操作（V2）

**获取文档快照**：
```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/snapshot" \
  -H "Authorization: Bearer <token>"
```

**执行块级编辑操作**：
```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/edit/v2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: <unique-key>" \
  -d '{
    "by":"ai:<your-agent-name>",
    "baseRevision":42,
    "operations":[
      {"op":"replace_block","ref":"b3","block":{"markdown":"Updated paragraph."}},
      {"op":"insert_after","ref":"b3","blocks":[{"markdown":"## New section"}]}
    ]
  }'
```

支持的编辑操作包括：
- `replace_block`（替换块内容）
- `insert_before`（在块前插入内容）
- `insert_after`（在块后插入内容）
- `delete_block`（删除块内容）
- `replace_range`（替换块内的内容）
- `find_replace_in_block`（在块内查找并替换内容）

## 简单编辑（V1）

适用于快速添加或替换内容的操作：
```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/edit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "by":"ai:<your-agent-name>",
    "operations":[
      {"op":"append","section":"Notes","content":"\n\nNew note."},
      {"op":"replace","search":"old","content":"new"}
    ]
  }'
```

## 评论、建议和内容重写

**用于提交修改建议的 API**：
```text
POST /api/agent/<slug>/ops
```

**用于查看修改历史的 API**：
```text
POST /api/documents/<slug>/ops
```

**示例**：
```json
{"type":"comment.add","by":"ai:<your-agent-name>","quote":"anchor text","text":"Comment body"}
{"type":"suggestion.add","by":"ai:<your-agent-name>","kind":"replace","quote":"old text","content":"new text"}
{"type":"suggestion.add","by":"ai:<your-agent-name>","kind":"replace","quote":"old text","content":"new text","status":"accepted"}
{"type":"rewrite.apply","by":"ai:<your-agent-name>","content":"# Rewritten markdown"}
```

当您希望人类审核修改内容时，请使用 `ops` API。

## 事件通知和在线状态显示

**轮询待处理的事件**：
```bash
curl -sS "https://www.proofeditor.ai/api/agent/<slug>/events/pending?after=0" \
  -H "Authorization: Bearer <token>"
```

**确认已处理的事件**：
```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/<slug>/events/ack" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"upToId":123,"by":"ai:<your-agent-name>"}'
```

当有人在审核您的修改时，请保持自己的在线状态更新，以便文档能够显示您的当前操作情况。

## 错误处理

| 错误代码 | 错误含义 | 处理方法 |
|---|---|---|
| `401/403` | 身份验证失败 | 从 URL 重新获取令牌，并使用 `Bearer` 令牌重试 |
| `404` | 未找到文档的 `slug` | 核实 `slug` 和当前环境配置 |
| `409 PROJECTION_STALE` | 元数据更新不及时 | 重新读取文档状态或快照，然后重试 |
| `409 STALE_REVISION` | 快照过时 | 使用最新的快照或文档状态重新尝试 |
| `409 ANCHOR_NOT_FOUND` | 搜索锚点缺失 | 重新读取文档状态并选择正确的锚点 |
| `422` | 传入的数据无效 | 修复必要的字段和数据格式 |
| `429` | 请求频率限制 | 暂停请求并稍后重试 |

**使用建议**：
- 在依赖文档锚点或版本控制的操作之前，请先重新读取文档状态。
- 将 `by` 参数包含在每次写入操作中。
- 建议使用 `content` 和 `markdown` 格式作为标准的输入数据。
- 在 `edit/v2` 请求中设置 `Idempotency-Key`，以确保重试的安全性。

## 相关资源：

- Proof 的相关信息 JSON 数据：`https://www.proofeditor.ai/.well-known/agent.json`
- 文档列表：`https://www.proofeditor.ai/agent-docs`
- 设置指南：`https://www.proofeditor.ai/agent-setup`