---
name: ogment
description: 通过 Ogment 安全地访问业务集成（SaaS、API、数据）。当用户需要查询、创建、更新或管理外部系统（如 Salesforce、Notion、Slack、数据库或任何连接的服务器）中的数据时，请使用此功能。
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["ogment"]},"install":[{"id":"npm","kind":"node","package":"ogment","bins":["ogment"],"label":"Install Ogment CLI (npm)"}]}}
---

# Ogment

Ogment 通过一个统一的命令行界面（CLI）为您提供对业务集成（包括 SaaS 工具、内部 API 和数据）的安全访问。用户的凭据永远不会离开 Ogment。Ogment 会生成具有特定工具权限的可撤销令牌，并确保所有操作都经过人工审批流程。

## 设置（只需一次）

如果 `ogment` 未安装，或者任何命令出现 “not logged in” 的错误，请按照以下步骤操作：

1. 安装：`npm install -g ogment`
2. 要求用户在终端中运行 `ogment login`（这将打开浏览器进行 OAuth 登录，无需传递任何参数）
3. 登录过程仅需要执行一次。认证成功后，所有服务器和工具都将自动可供使用。

## 命令

**发现服务器：**
```bash
ogment servers --json
```
返回所有组织中可用的服务器列表。

**查看服务器上的工具：**
```bash
ogment servers <server-path> --json
```
返回工具的完整列表，包括工具名称、描述和输入格式。

**调用工具：**
```bash
ogment call <server-path> <tool-name> '<json-args>'
```
返回 JSON 格式的结果。参数必须是一个 JSON 字符串。对于不需要参数的工具，可以省略参数。

## 工作流程

请按照以下步骤操作：

1. 运行 `ogment servers --json` 以发现可用的服务器。
2. 选择与用户需求相关的服务器。
3. 运行 `ogment servers <服务器路径> --json` 以查看该服务器上的工具列表。
4. 使用 `ogment call <服务器> <工具> '<参数>'` 调用相应的工具。
5. 解析 JSON 响应并将结果呈现给用户。
6. 如果用户需要使用其他集成服务，请返回步骤 1。

## 示例

```bash
# Discover all servers
ogment servers --json

# Inspect tools on a server
ogment servers salesforce --json

# Query data
ogment call salesforce query_accounts '{"limit":5}'
ogment call notion search '{"query":"Q1 roadmap"}'
ogment call data-warehouse run_query '{"sql":"SELECT * FROM orders LIMIT 10"}'

# Create records
ogment call salesforce create_record '{"type":"Contact","fields":{"Name":"Jane Doe","Email":"jane@example.com"}}'

# Health check (no args)
ogment call my-api get__health
```

## 错误处理

- **“not logged in”**：要求用户在终端中运行 `ogment login`。
- **“server not found”**：运行 `ogment servers --json` 以查看可用的服务器。
- **返回审批链接**：该工具需要人工审批。将审批链接显示给用户并请求他们进行审批，然后重试工具调用。
- **401/认证错误**：令牌可能已过期。请要求用户先运行 `ogment logout`，然后再运行 `ogment login`。

## 重要提示：

- 发现服务器和工具时，请务必使用 `--json` 标志。
- `ogment call` 默认会返回 JSON 格式的结果，因此无需额外添加 `--json` 标志。
- `ogment call` 的参数必须是一个 JSON 字符串。
- 请勿存储或记录令牌信息——Ogment 会在服务器端处理所有凭据。
- 每次工具调用都会经过 Ogment 的认证、权限检查并记录日志。