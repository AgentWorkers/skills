---
name: evc-team-relay
version: 1.1.2
description: >
  **技能说明：**  
  能够读写存储在 EVC Team Relay 协作仓库中的 Obsidian 笔记。适用于以下场景：  
  - 从共享的 Obsidian 仓库中读取笔记内容；  
  - 创建或更新文档；  
  - 列出可用的共享文件夹和文档；  
  - 在共享仓库内容中进行搜索。  
  **工作原理：**  
  EVC Team Relay 将文档以 Yjs CRDT（Cyclic Redundant Data Tree）格式进行存储。本技能提供了 REST 接口，用于读取和写入这些文档的文本内容。
metadata:
  openclaw:
    requires:
      env:
        - RELAY_CP_URL
        - RELAY_EMAIL
        - RELAY_PASSWORD
      bins:
        - curl
        - jq
    primaryEnv: RELAY_CP_URL
    homepage: https://github.com/entire-vc/evc-team-relay
---
# EVC Team Relay

这是一个REST API，用于通过EVC Team Relay读写Obsidian文档库中的文件。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `RELAY_CP_URL` | 是 | 控制平面URL，例如 `https://cp.tr.entire.vc` |
| `RELAY_EMAIL` | 是 | 用于身份验证的用户邮箱 |
| `RELAY_PASSWORD` | 是 | 用户密码 |
| `RELAY_TOKEN` | 否 | JWT令牌（通过 `export RELAY_TOKEN=$(scripts/auth.sh)` 设置） |

## 快速入门

```bash
# 1. Authenticate — get a JWT token (stored in env var, not visible in ps)
export RELAY_TOKEN=$(scripts/auth.sh)

# 2. List shares to find available documents
scripts/list-shares.sh

# 3. Read a file from a folder share BY PATH (most common)
scripts/read-file.sh <folder_share_id> "Marketing/plan.md"

# 4. Create or update a file in a folder share
scripts/upsert-file.sh <folder_share_id> "note.md" "# Content"

# 5. List all files in a folder share
scripts/list-files.sh <folder_share_id>

# 6. Delete a file from a folder share
scripts/delete-file.sh <folder_share_id> "old-note.md"

# 7. Read a doc share (single document, share_id = doc_id)
scripts/read.sh <share_id>

# 8. Write to a doc share
scripts/write.sh <share_id> <share_id> "# Updated content"
```

所有脚本都支持通过 `RELAY_TOKEN` 环境变量传递令牌（推荐方式），或者作为第一个CLI参数传递（向后兼容）。

## 两种共享类型

| 共享类型 | 文档共享 | 文件夹共享 |
|--|-----------|--------------|
| **包含** | 单个文档 | 多个文件 |
| **doc_id** | 与 `share_id` 相同 | 每个文件都有自己的 `doc_id`（在文件夹元数据中） |
| **读取** | `read.sh <share_id>` | **`read-file.sh <share_id> "path/to/file.md"`** |
| **写入** | `write.sh <share_id> <content>` | **`upsert-file.sh <share_id> "path" <content>`** |
| **删除** | 不适用 | `delete-file.sh <share_id> "path"` |

**大多数共享类型是文件夹共享。** 使用 `read-file.sh` 和 `upsert-file.sh` — 它们会自动处理路径解析。

> **警告**：`write.sh` 不适用于文件夹共享 — 它会写入内容，但不会在文件夹元数据中注册文件，因此Obsidian无法识别该文件。该脚本会检测到文件夹共享并返回错误。

## 脚本参考

| 脚本 | 用途 | 参数 |
|--------|---------|------|
| `auth.sh` | 获取JWT令牌 | — |
| `list-shares.sh` | 列出所有共享 | `[kind] [owned_only]` |
| `list-files.sh` | 列出文件夹共享中的文件 | `<share_id>` |
| **`read-file.sh`** | **按路径读取文件（文件夹共享）** | `<share_id> <file_path>` |
| `read.sh` | 按 `doc_id` 读取 | `<share_id> [doc_id]` |
| **`upsert-file.sh`** | **创建/更新文件（文件夹共享）** | `<share_id> <file_path> <content>` |
| `write.sh` | 按 `doc_id` 写入文件（仅适用于文档共享） | `<share_id> <doc_id> <content>` |
| `delete-file.sh` | 从文件夹共享中删除文件 | `<share_id> <file_path>` |
| `create-file.sh` | 创建新文件（底层操作） | `<share_id> <file_path> <content>` |

****粗体表示推荐用法。** 所有脚本都使用 `RELAY_TOKEN` 环境变量（或接受令牌作为第一个参数）。**

## 身份验证

所有API调用都需要一个Bearer JWT令牌。可以通过登录来获取令牌：

```bash
curl -s -X POST "$RELAY_CP_URL/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "'$RELAY_EMAIL'", "password": "'$RELAY_PASSWORD'"}' \
  | jq -r '.access_token'
```

响应：
```json
{
  "access_token": "eyJ...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

在后续的所有请求中，将 `access_token` 作为 `Authorization: Bearer <token>` 头部字段使用。

当令牌过期（1小时后），需要重新获取令牌：
```bash
curl -s -X POST "$RELAY_CP_URL/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "'$REFRESH_TOKEN'"}'
```

## 列出共享资源

共享资源是访问的基本单位 — 每个共享资源对应Obsidian文档库中的一个文档或文件夹。

```bash
curl -s "$RELAY_CP_URL/v1/shares" \
  -H "Authorization: Bearer $TOKEN" | jq
```

响应（数组格式）：
```json
[
  {
    "id": "a1b2c3d4-...",
    "kind": "doc",
    "path": "Projects/meeting-notes.md",
    "visibility": "private",
    "is_owner": true,
    "user_role": null,
    "web_published": false
  },
  {
    "id": "e5f6g7h8-...",
    "kind": "folder",
    "path": "Projects/",
    "visibility": "private",
    "is_owner": false,
    "user_role": "editor"
  }
]
```

关键字段：
- **`id`** — 共享资源的UUID，在所有操作中用作 `share_id` |
- **`kind`** — `doc`（单个文件）或 `folder`（文件夹） |
- **`path`** — Obsidian文档库中的相对路径 |
- **`user_role`** — `viewer`（只读）、`editor`（读写）或 `null`（所有者） |

过滤选项：`?kind=doc`、`?owned_only=true`、`?member_only=true`、`?skip=0&limit=50`。

## 列出文件夹共享中的文件

```bash
scripts/list-files.sh <share_id>
```

响应：
```json
{
  "doc_id": "e5f6g7h8-...",
  "files": {
    "meeting-notes.md": {"doc_id": "abc123-...", "type": "markdown"},
    "project-plan.md": {"doc_id": "def456-...", "type": "markdown"}
  }
}
```

每个键表示文件在文件夹中的路径。`doc_id` 字段用于内容操作。对于内容请求，`share_id` 总是文件夹共享的ID。

> **注意**：API响应使用 `id` 作为字段名。这与 `doc_id` 是相同的 — 在需要使用 `doc_id` 的地方都可以使用 `id`。

## 读取文件

### 按路径读取（推荐用于文件夹共享）

```bash
scripts/read-file.sh <folder_share_id> "Marketing/plan.md"
```

该脚本会内部将路径解析为 `doc_id` 并返回结果：
```json
{
  "doc_id": "abc123-...",
  "content": "# Marketing Plan\n\nContent here...",
  "format": "text",
  "path": "Marketing/plan.md"
}
```

### 按 `doc_id` 读取（底层操作）

```bash
scripts/read.sh <share_id> [doc_id] [key]
```

对于文档共享，可以省略 `doc_id`（默认使用 `share_id`）。对于文件夹共享，需要使用 `list-files.sh` 获取文件的 `doc_id`。

## 写入文件

### 文件夹共享 — 使用 `upsert-file.sh`

```bash
# Create or update — auto-detects which operation is needed
scripts/upsert-file.sh <folder_share_id> "note.md" "# Updated content"

# Pipe content from stdin
echo "# Content" | scripts/upsert-file.sh <folder_share_id> "note.md" -
```

响应中包含一个 `operation` 字段：`"created"` 或 `"updated"`。

### 文档共享 — 使用 `write.sh`

```bash
scripts/write.sh <share_id> <share_id> "# Updated Notes"
```

> **注意**：`write.sh` 不支持文件夹共享 — 如果你意外地传递了文件夹共享的ID，它会检测到这一点并返回错误，提示你使用 `upsert-file.sh`。

## 常见工作流程

### 按路径读取特定笔记（最常见）

```bash
# If you know the folder share_id:
scripts/read-file.sh <folder_share_id> "Marketing/docs/plan.md"

# If you need to find the share first:
scripts/list-shares.sh  # find the folder share
scripts/read-file.sh <share_id> "path/to/file.md"
```

### 创建或更新文件

```bash
# Always works, whether the file exists or not
scripts/upsert-file.sh <folder_share_id> "note.md" "# Content"
```

### 删除文件

```bash
scripts/delete-file.sh <folder_share_id> "old-note.md"
```

## 错误代码

| 状态码 | 含义 |
|--------|---------|
| 400 | `share_id` 格式无效 |
| 401 | 令牌缺失或过期 — 请重新登录 |
| 403 | 权限不足（仅限查看者尝试写入，或非成员） |
| 404 | 共享资源或文件未找到（检查路径拼写，可以使用 `list-files.sh` 验证） |
| 422 | 缺少必需字段（`share_id`、`content`） |
| 502 | 中继服务器不可用 — 请稍后重试 |

## 术语说明

| 术语 | 含义 |
|------|---------|
| `share_id` | 共享资源的UUID（文档或文件夹的标识符）。在所有请求中用于访问控制检查。 |
| `doc_id` | 单个文档的UUID。对于文档共享，与 `share_id` 相同；对于文件夹共享，每个文件都有自己的 `doc_id`。 |
| `id` | 与 `doc_id` 同义 — API响应中的字段名。两者可以互换使用。 |
| `file_path` | 文件夹共享中的相对路径（例如 `"Marketing/plan.md"`）。 |

## 参考资料

- `references/api.md` — 完整的API参考文档，包含所有端点信息