---
name: clawauth
description: 允许代理通过短链接向最终用户请求 OAuth 访问权限，继续异步执行任务，并随后从本地密钥链存储中获取可重用的第三方 API 令牌，而不是从集中式的 SaaS 令牌库中获取。
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://auth.clawauth.app","requires":{"bins":["clawauth"]},"install":[{"id":"node","kind":"node","package":"clawauth","bins":["clawauth"],"label":"Install clawauth CLI (node)"}]}}
---
# Clawauth OAuth 技能

该技能为代理提供了安全的 OAuth 交互流程，该流程默认为异步模式，并且能够在聊天或会话中断的情况下继续执行。

当代理需要从用户那里获取提供者的凭证时，可以使用此技能；同时，该技能可以避免阻塞执行过程，并且不会在第三方认证 SaaS 服务中存储长期有效的令牌。

## 该技能存在的理由

大多数“OAuth 网关”模式会将用户的刷新令牌存储在中央托管的数据库中。而 Clawauth 避免了这种模式：

- 托管式边缘服务会生成短期有效的认证会话。
- 用户直接与提供者进行授权。
- 令牌响应会经过端到端加密，然后发送给请求的 CLI 会话。
- CLI 会一次性获取令牌信息，并将其存储在系统的密钥链中。
- 服务器端的会话是临时性的，在获取令牌或令牌过期后会被删除。

因此，该技能为代理提供了异步的用户体验，减少了操作员的负担，并且设计上没有永久性的中央令牌存储库。

## 运行时前提条件

操作员必须在受信任的运行时镜像/环境中预先安装 `clawauth`。该技能不支持动态包的安装。

OpenClaw 可以从前置元数据中检测到这一要求：

- `metadata.openclaw.requires.bins: ["clawauth"]` 可以判断是否满足安装条件。
- `metadata.openclaw.install` 可以在 OpenClaw UI/Gateway 流程中提供操作员批准的安装选项。

## 安装方式的文档说明及触发机制

- 安装意图在前置元数据中声明，而不是以自由形式的 shell 指令形式提供。
- 该技能在 `metadata.openclaw.install` 中声明了用于安装 `clawauth` 包的 Node 安装程序。
- OpenClaw/Gateway 会利用这些元数据，在缺少 `clawauth` 时提供托管的安装选项。
- 如果存在多个安装选项，Gateway 会选择其中一个优先的安装方式（OpenClaw 文档推荐使用 `brew`，否则按照 Node Manager 的策略进行安装）。
- 为了确保不同主机上的行为一致性，我们只发布一个 Node 安装程序的路径。
- 参考链接：https://docs.openclaw.ai/tools/skills
- 参考链接：https://docs.openclaw.ai/platforms/mac/skills

## 手动安装（操作员的备用方案）

如果 OpenClaw/Gateway 未自动执行安装操作，请手动安装 CLI：

```bash
npm i -g clawauth
```

然后进行验证：

```bash
clawauth --help
openclaw skills check --json
```

## 推荐的安装方式

- 在基础镜像/运行环境中预先安装 `clawauth`，并禁用临时包的获取功能。
- 将 CLI 版本固定并批准到操作员管理的工具策略中。
- 将包的来源和来源控制机制放在该技能之外（例如通过 CI 镜像构建或内部工件策略来管理）。

## 托管服务端点

发布的 CLI 已经连接到以下地址：

- `https://auth.clawauth.app`

代理在正常使用托管服务时不需要 `CLAWAUTH_WORKER_URL`。

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

请始终以服务器的输出为准：

```bash
clawauth providers --json
```

## 标准的异步流程（非阻塞）

1) 启动认证流程并立即返回结果：
```bash
clawauth login start <provider> --json
```

2) 提取 `shortAuthUrl` 并将其发送给用户。
3) 继续执行其他任务，不要阻塞当前流程。
4) 后续进行轮询或检查状态：
```bash
clawauth login status <sessionId> --json
```

5) 当状态变为 `completed` 时，一次性获取令牌：
```bash
clawauth login claim <sessionId> --json
```

6) 完成令牌获取后，将控制权交给操作员定义的 API 调用层。

该技能故意避免提供直接生成令牌的命令。

## 令牌使用的限制

- `login claim` 命令返回的 JSON 数据中可能包含敏感的令牌信息。
- 请勿将敏感的命令输出内容粘贴到聊天记录、日志或监控数据中。
- 请勿将该技能生成的令牌导入到 shell 环境中。
- 对下游提供者的 API 调用，必须使用操作员控制的秘密处理机制。

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

### 提供者信息查询和文档

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

## 代理的行为规则

- 建议使用 `--json` 格式以便机器解析命令。
- 默认情况下不要阻塞执行；只有在必要时才使用 `login wait` 命令。
- 当状态为 `pending` 时，安排重试。
- 当状态为 `completed` 时，执行一次 `login claim` 命令。
- 当出现错误时，显示简洁的错误信息并重新开始登录流程。
- 如果会话上下文丢失，使用 `clawauth sessions --json` 恢复会话。
- 如果提供者信息未知，使用 `clawauth providers --json` 查找支持的提供者。
- 严禁将原始令牌内容显示在用户可见的聊天界面中。
- 严禁通过该技能执行包的安装或获取操作。
- 严禁将该技能生成的令牌导出到 shell 环境变量中。

## 安全模型概述

- 会话数据存储在 Cloudflare 的 KV 存储中（默认有效期为 3600 秒，可配置）。
- 使用签名机制确保 OAuth 状态和令牌的有效性。
- 对状态/令牌请求进行签名验证，包含时间戳和随机数（nonce）。
- 在轮询过程中提供防重放和速率限制保护。
- 令牌数据在从回调到 CLI 的过程中进行端到端加密（使用 `nacl.box` 格式）。
- 成功获取令牌后，会话数据会从服务器上删除。
- 令牌通过 CLI 存储在操作系统的密钥链中。

## 故障处理

- 如果提供的者未实现相关功能，`login start` 命令会返回错误信息。
- 如果后端配置错误，服务器会返回明确的错误提示（例如“secret 或配置缺失”）。
- 会话过期时，`status`/`claim` 命令会返回“未找到”或“已过期”的提示，并重新启动会话。
- 如果聊天上下文丢失，使用 `clawauth sessions --json` 恢复会话状态。
- 如果找不到令牌，使用 `clawauth token list --json` 命令并明确选择相应的提供者和账户。

## 最小的端到端使用示例

```bash
# 1) Start
clawauth login start notion --json

# 2) Share shortAuthUrl with user (from JSON output)

# 3) Later check
clawauth login status <sessionId> --json

# 4) Claim when completed
clawauth login claim <sessionId> --json

# 5) Continue with operator-defined downstream API handling
```

## 参考资料

有关详细的命令示例，请参阅 `references/commands.md` 文件。