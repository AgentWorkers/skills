---
name: latchkey
description: 可以通过这些第三方服务或自托管服务的 HTTP API 与它们进行交互，例如 AWS、Slack、Google Drive、Dropbox、GitHub、GitLab、Linear、Coolify 等。
compatibility: Requires node.js, curl and latchkey (npm install -g latchkey).
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["latchkey"]},"install":[{"id":"node","kind":"node","package":"latchkey","bins":["latchkey"],"label":"Install Latchkey (npm)"}]}}
---
# Latchkey

## 使用说明

Latchkey 是一个命令行工具（CLI），它可以自动将凭据插入到 `curl` 命令中。这些凭据（主要是 API 令牌）需要由用户手动管理。

当用户要求您使用具有 HTTP API 的服务（如 AWS、Coolify、GitLab、Google Drive、Discord 等）时，请使用此工具。

**使用方法：**
1. 对于支持的服务，使用 `latchkey curl` 代替普通的 `curl`。
2. 所有的常规 `curl` 参数都会被原样传递给 `latchkey`；`latchkey` 仅作为一个透明的包装器。
3. 使用 `latchkey services list` 命令查看支持的服务列表。如果只想查看已配置的服务，可以使用 `--viable` 标志。
4. 使用 `latchkey services info <服务名称>` 命令获取特定服务的详细信息（包括认证选项、凭据状态、API 文档链接、特殊要求等）。
5. 如有必要，请先让用户配置凭据。告诉用户在安装了 `latchkey` 的机器上运行 `latchkey auth set` 命令（具体操作方法参见 `services info` 命令中的 `setCredentialsExample` 说明）。
6. 在线查找所需公共 API 的最新文档。
7. 如果凭据状态为 `valid` 或 `unknown`，则不要尝试登录——可能是用户没有执行该操作所需的权限。

## 示例

### 发送经过身份验证的 `curl` 请求
```bash
latchkey curl [curl arguments]
```

### 创建 Slack 频道
```bash
latchkey curl -X POST 'https://slack.com/api/conversations.create' \
  -H 'Content-Type: application/json' \
  -d '{"name":"my-channel"}'
```

（请注意：在示例代码中，`-H 'Authorization: Bearer'` 这一行并未被包含。）

### 获取 Discord 用户信息
```bash
latchkey curl 'https://discord.com/api/v10/users/@me'
```

### 检测过期的凭据
```bash
latchkey services info discord  # Check the "credentialStatus" field - shows "invalid"
```

### 列出可用的服务
```bash
latchkey services list --viable
```

该命令会列出已保存凭据的服务。

### 获取特定服务的详细信息
```bash
latchkey services info slack
```

该命令会返回服务的认证选项、凭据状态以及开发者的相关说明。

## 凭据存储

提供凭据是用户的责任。用户通常会按照以下步骤操作：
```bash
latchkey auth set my-gitlab-instance -H "PRIVATE-TOKEN: <token>"
```

如果凭据无法以常规 `curl` 参数的形式传递，可以使用 `set-nocurl` 子命令。例如：
```bash
latchkey auth set-nocurl aws <access-key-id> <secret-access-key>
```

如果某个服务在 `--viable` 标志下没有显示，可能仍然支持该服务；只是用户尚未提供相应的凭据。可以使用 `latchkey service info <服务名称>` 命令来了解如何为该服务提供凭据。

## 注意事项：
- 所有的 `curl` 参数都会被原样传递。
- `curl` 命令返回的返回码、标准输出（stdout）和标准错误输出（stderr）也会被传递给 `latchkey`。
- 凭据始终以加密形式存储，且不会被传输到 `curl` 调用的目标端点之外的任何地方。

## 目前支持的服务

Latchkey 目前支持以下服务（部分服务的支持程度可能有所不同）：AWS、Calendly、Coolify、Discord、Dropbox、Figma、GitHub、GitLab、Gmail、Google Analytics、Google Calendar、Google Docs、Google Drive、Google Sheets、Linear、Mailchimp、Notion、Sentry、Slack、Stripe、Telegram、Umami、Yelp、Zoom 等。

### 用户可注册的新服务

**用户操作说明：** 用户也可以通过 `latchkey services register` 命令在运行时为新的服务添加支持。