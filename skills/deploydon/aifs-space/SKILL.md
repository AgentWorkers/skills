---
name: aifs
description: 通过 AIFS.space 云存储 API 存储和检索文件。适用于将笔记、文档或数据持久化到云端；在会话之间同步文件；或者当用户提到 AIFS、aifs.space 或云文件存储时使用。请勿用于存储任何敏感内容。
---

# AIFS - 人工智能文件系统（AI File System）

AIFS.Space 是一个简单的 HTTP REST API，用于云文件存储。您可以使用它来在会话之间持久化文件、在代理之间共享数据，或将用户内容存储在云端。

## 用户注册

用户需要访问 [https://AIFS.Space](https://AIFS.Space) 进行注册，并获取一个 API 密钥，以便提供给您。

## 认证

请求时必须在请求头中包含 API 密钥。您可以从环境变量（`AIFS_API_KEY`）或用户配置中获取该密钥。

**密钥类型：** `admin`（管理员权限）、`read-write`（读写权限）、`read-only`（只读权限）、`write-only`（只写权限）

## 基本 URL

```
https://aifs.space
```

## 端点（Endpoints）

### 列出文件（List Files）

**返回格式：** `{"files": [{"path": "notes/todo.txt", "size": 1024, "modifiedAt": "..."}]`

### 读取文件（Read File）

**返回格式：** `{"path": "...", "content": "...", "total_lines": 42, "returned_lines": 10}`

### 写入文件（Write File）

系统会自动创建目录（最大目录深度为 20 层）。

**返回格式：** `{"success": true, "path": "...", "size": 11, "lines": 1}`

### 修补文件（Patch File，替换特定行）

**返回格式：** `{"success": true, "lines_before": 42, "lines_after": 38}`

### 删除文件（Delete File）

### 文件预览（Summary, Preview）

**返回格式：** 文件的前 500 个字符。

## 请求速率限制

每个 API 密钥每分钟允许 60 次请求。您可以通过请求头中的以下字段来查看当前的请求限制情况：
- `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset`

## 错误代码（Error Codes）

| 代码           | 含义                         |
| -------------- | --------------------------- |
| AUTH_REQUIRED  | 未提供认证信息                 |
| AUTH_FAILED    | API 密钥无效                     |
| FORBIDDEN      | 密钥类型不具备所需的权限             |
| RATE_LIMITED   | 请求次数超出限制                 |
| NOT_FOUND      | 文件不存在                     |
| INVALID_PATH   | 文件路径无效或存在路径遍历问题           |
| DEPTH_EXCEEDED | 目录深度超过 20 层                    |

## 常用操作模式（Common Patterns）

### 持久化会话笔记（Persist Session Notes）

### 按项目组织文件（Organize Files by Project）

### 向日志中追加内容（Append to Log, 读写操作）