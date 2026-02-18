---
name: clawauth
description: 让代理通过短链接向终端用户请求 OAuth 访问权限，继续异步执行任务，并随后从本地密钥链存储中获取可重用的第三方 API 令牌，而不是从集中式的 SaaS 令牌库中获取。
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://auth.clawauth.app","requires":{"bins":["clawauth"]},"install":[{"id":"node","kind":"node","package":"clawauth","bins":["clawauth"],"label":"Install clawauth CLI (node)"}]}}
---
# Clawauth OAuth 技能

该技能为代理提供了安全的 OAuth 交互流程，该流程默认为异步模式，并且能够在聊天或会话中断的情况下继续执行。

当代理需要从用户那里获取提供者的凭证时，可以使用此技能。同时，该技能可以避免阻塞执行过程，并且不会在第三方认证 SaaS 服务中存储长期有效的令牌。

## 为何需要这个技能

大多数“OAuth 代理”模式会将用户的刷新令牌存储在中央托管的数据库中。而 clawauth 采用了不同的设计：

- 托管式的边缘服务会生成短期有效的认证会话。
- 用户直接与提供者进行授权。
- 令牌响应会经过端到端的加密处理，然后发送给请求的 CLI 会话。
- CLI 会仅进行一次令牌请求，并将令牌存储在系统的密钥链中。
- 服务器端的会话是临时性的，在请求完成或过期后会被删除。

这样一来，代理的交互体验更加流畅（异步处理），操作员的负担最小化，并且系统设计上没有永久性的中央令牌存储库。

## 运行时前提条件

操作员必须在受信任的运行时镜像/环境中预先安装 `clawauth`。该技能不支持动态包的安装。

OpenClaw 可以通过元数据来检测这一要求：

- `metadata.openclaw.requires.bins: ["clawauth"]` 可以判断是否满足安装条件。
- `metadata.openclaw.install` 可以在 OpenClaw UI/Gateway 流程中提供操作员认可的安装选项。

## 安装方式及触发机制

- 安装意图需要在元数据中明确声明，而不是通过自由形式的 shell 指令来指定。
- 该技能在 `metadata.openclaw.install` 中声明了用于安装 `clawauth` 包的 Node 安装程序。
- OpenClaw/Gateway 会根据这些元数据，在缺少 `clawauth` 时提供自动安装功能。
- 如果存在多个安装选项，Gateway 会优先选择合适的安装方式（OpenClaw 文档推荐使用 `brew`；如果没有 `brew`，则会根据 Node Manager 的策略来选择）。
- 为了确保不同主机上的行为一致性，我们只发布一个 Node 安装路径。
- 参考链接：https://docs.openclaw.ai/tools/skills
- 参考链接：https://docs.openclaw.ai/platforms/mac/skills
- 源代码（安装前请查阅）：https://github.com/claw-auth/clawauth

## 手动安装（操作员的备用方案）

如果 OpenClaw/Gateway 未自动执行安装操作，可以手动安装 CLI：

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
- 将 CLI 版本固定并批准到操作员管理的工具配置中。
- 将包的来源和版本控制信息放在该技能之外（例如通过 CI 镜像构建或内部工件策略来管理）。

## 托管服务端点

已发布的 CLI 已经连接到了以下地址：

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

请始终以服务器返回的信息为最终依据：

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
4) 随后定期检查认证状态：
```bash
clawauth login status <sessionId> --json
```

5) 当认证状态变为 `completed` 时，进行一次令牌请求：
```bash
clawauth login claim <sessionId> --json
```

6) 完成令牌请求后，将控制权传递给操作员定义的 API 调用层。

该技能故意避免提供直接生成令牌的命令。

## 令牌使用的限制

- `login claim` 命令返回的 JSON 数据中可能包含敏感的令牌信息。
- 请勿将敏感的命令输出内容粘贴到聊天记录、日志或监控数据中。
- 请勿将令牌内容导入 shell 环境中。
- 对于后续的提供者 API 调用，必须使用操作员控制的秘钥管理机制。

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

### 提供者信息查询

- `clawauth providers [--json]`
- `clawauth explain`
- `clawauth docs`

## 用户端需要解析的 JSON 字段

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

- 建议使用 `--json` 格式进行数据解析。
- 默认情况下不要阻塞操作；只有在必要时才使用 `login wait` 命令。
- 当状态为 `pending` 时，安排重试。
- 当状态为 `completed` 时，执行一次 `login claim` 命令。
- 当出现错误时，显示简洁的错误信息并重新执行 `login start`。
- 如果会话上下文丢失，使用 `clawauth sessions --json` 恢复会话。
- 如果无法识别提供者，使用 `clawauth providers --json` 查找支持的提供者。
- 严禁将原始令牌内容显示在用户可见的聊天界面中。
- 请勿通过该技能执行任何包的安装或获取操作。
- 请勿将令牌内容导出到 shell 环境变量中。

## 安全模型概述

- 会话数据存储在 Cloudflare 的键值存储中（默认有效期为 3600 秒，可配置）。
- 使用签名机制确保 OAuth 状态和令牌的有效性。
- 对状态/令牌请求进行签名验证，包含时间戳和随机数。
- 在请求过程中实施防重放和速率限制措施。
- 令牌数据在从服务器返回给 CLI 时采用端到端加密（使用 `nacl.box` 格式）。
- 成功获取令牌后，会话数据会从服务器上删除。
- 令牌会通过 CLI 存储在操作系统的密钥链中。

## 故障处理

- 如果提供的者未实现相应的功能，`login start` 命令会返回错误信息。
- 如果后端配置错误，服务器会返回明确的错误提示。
- 会话过期时，`status`/`claim` 命令会返回“未找到”或“已过期”的结果，此时需要重新创建会话。
- 如果聊天上下文丢失，使用 `clawauth sessions --json` 恢复会话信息。
- 如果找不到令牌，使用 `clawauth token list --json` 命令并明确选择相应的提供者和账户。

## 最简单的端到端使用示例

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

详细的命令使用方法请参阅 `references/commands.md`。