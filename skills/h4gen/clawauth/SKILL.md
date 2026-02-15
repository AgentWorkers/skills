---
name: clawauth
description: Secure delegated OAuth for agents: request user approval, hand off a short auth link, then claim provider access tokens for direct third-party API calls without a central SaaS token vault.
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://auth.clawauth.app"}}
---

# Clawauth OAuth 技能

该技能为代理提供了安全的 OAuth 接口，支持异步操作，并且能够在聊天或会话中断的情况下继续执行。当代理需要从用户那里获取提供者的凭证时，可以使用该技能；同时，该技能能够避免阻塞执行过程，并且不会将长期有效的令牌存储在第三方认证 SaaS 服务上。

## 为什么需要这个技能

大多数“OAuth 网关”模式会将用户的刷新令牌存储在中央托管的数据库中，但 clawauth 采用了不同的设计：

- 托管式边缘服务生成短期有效的认证会话。
- 用户直接与提供者进行授权。
- 令牌响应会经过端到端的加密处理，然后发送给请求的 CLI 会话。
- CLI 仅进行一次令牌请求，并将令牌存储在系统的密钥链中。
- 服务器端的会话是临时性的，在请求完成或令牌过期后会被删除。

这样一来，代理可以享受到异步的用户体验，操作员的负担最小化，并且系统设计上没有永久性的中央令牌存储库。

## 代理如何获取令牌

代理必须能够运行 `clawauth` 命令。可以使用以下方法之一来获取令牌：

1) 无需安装即可使用：
   ```bash
npx clawauth --help
```

2) 全局安装：
   ```bash
npm i -g clawauth
clawauth --help
```

3) 项目本地安装：
   ```bash
npm i clawauth
npx clawauth --help
```

4) 操作员可以通过运行时/工具策略来强制使用特定版本的 `clawauth`。

如果找不到 `clawauth`，可以使用 `npx clawauth ...` 或者操作员批准的固定版本。

## 托管服务端点

已发布的 CLI 已经连接到以下地址：
- `https://auth.clawauth.app`

代理在正常使用托管服务时，不需要设置 `CLAWAUTH_WORKER_URL`。

## 支持的提供者

当前支持的提供者包括：
- notion
- github
- discord
- linear
- airtable
- todoist
- asana
- trello
- dropbox
- digitalocean
- slack
- gitlab
- reddit
- figma
- spotify
- bitbucket
- box
- calendly
- fathom
- twitch

请始终以服务器返回的信息为准：

```bash
clawauth providers --json
```

## 标准的异步流程（非阻塞式）

1) 启动认证流程并立即返回结果：
   ```bash
clawauth login start <provider> --json
```

2) 提取 `shortAuthUrl` 并将其发送给用户。
3) 继续执行其他任务，不要阻塞当前操作。
4) 后续通过轮询或检查来获取认证状态：
   ```bash
clawauth login status <sessionId> --json
```

5) 当认证状态变为 `completed` 时，进行一次令牌请求：
   ```bash
clawauth login claim <sessionId> --json
```

6) 稍后使用存储的令牌：
   ```bash
clawauth token get <provider> --json
clawauth token env <provider>
```

只有在下游命令明确需要在同一进程中使用环境变量时，才使用 `token env`。

## 命令映射

### 登录流程

- `clawauth login start [provider] [--ttl <seconds>] [--scope <scope>] [--json]`
- `clawauth login status <sessionId> [--json]`
- `clawauth login claim <sessionId> [--json]`
- `clawauth login wait <sessionId> [--timeout <ms>] [--interval <ms>] [--json]`

### 会话管理

- `clawauth sessions [--json]`
- `clawauth session-rm <sessionId> [--json]`

### 令牌访问

- `clawauth token list [--json]`
- `clawauth token get [provider] [--json]`
- `clawauth token env [provider] [--json]`

### 提供者信息查询与文档

- `clawauth providers [--json]`
- `clawauth explain`
- `clawauth docs`

## 代理应解析的 JSON 字段

### `login start --json`

- `provider`
- `sessionId`
- `expiresIn`
- `shortAuthUrl`
- `authUrl`
- `statusCommand`
- `claimCommand`

### `login status --json`

- `status` (`pending | completed | error`)
- `provider`
- `error`

### `login claim --json`

- `status` (`pending | completed | error`)
- `provider`
- `tokenData`
- `storedInKeychain`
- `keychainService`
- `keychainAccount`

### `token get --json`

- `action`
- `account`
- `token.provider`
- `token.access_token`
- `token.refresh_token`
- `token.token_type`
- `token_saved_at`

## 代理的行为规则

- 建议使用 `--json` 格式进行命令解析。
- 默认情况下不要阻塞执行；仅在必要时使用 `login wait`。
- 当认证状态为 `pending` 时，安排重试。
- 当认证状态为 `completed` 时，执行一次 `login claim`。
- 如果会话上下文丢失，使用 `clawauth sessions --json` 恢复会话信息。
- 如果无法识别提供者，使用 `clawauth providers --json` 查找支持的提供者。
- 绝不要将原始令牌显示在用户可见的聊天界面中。
- 在自主执行过程中，不要使用 `npx ...@latest`。
- 除非确实需要用于当前的 API 调用，否则避免在整个 shell 环境中导出令牌。

## 安全模型概述

- 会话数据存储在 Cloudflare 的键值存储（KV）中（默认过期时间为 3600 秒，可配置）。
- 使用签名机制来确保 OAuth 状态和令牌的有效性。
- 对状态请求和令牌请求进行签名验证，包含时间戳和随机数（nonce）。
- 在轮询过程中提供防重放和速率限制保护。
- 从回调到 CLI 的令牌数据会经过端到端的加密处理（使用 `nacl.box`）。
- 成功获取令牌后，会话数据会从服务器端删除。
- 令牌通过 CLI 存储在操作系统的密钥链中。

## 故障处理

- 如果提供的者未实现相应的功能，`login start` 命令会返回错误信息。
- 如果后端配置错误，服务器会返回明确的错误提示（如“缺少密钥或配置信息”）。
- 会话过期时，`status`/`claim` 命令会返回“未找到”或“已过期”的错误信息，此时需要重新开始会话。
- 如果会话上下文丢失，使用 `clawauth sessions --json` 恢复会话信息。
- 如果找不到令牌，使用 `clawauth token list --json` 并明确选择相应的提供者和账户。

## 最简单的端到端使用示例

```bash
# 1) Start
clawauth login start notion --json

# 2) Share shortAuthUrl with user (from JSON output)

# 3) Later check
clawauth login status <sessionId> --json

# 4) Claim when completed
clawauth login claim <sessionId> --json

# 5) Use token
clawauth token get notion --json
```

## 参考资料

有关完整的命令示例，请参阅 `references/commands.md`。