---
name: trent-openclaw-security
description: 使用 Trent AppSec Advisor 对您的 OpenClaw 部署进行安全风险审计
version: 2.0.1
homepage: https://trent.ai
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - trent-openclaw-audit
    primaryEnv: TRENT_CHAT_API_URL
    install:
      - kind: uv
        package: trentai-mcp
        bins: [trent-openclaw-audit]
---
# Trent OpenClaw 安全审计

本功能由 Trent AppSec Advisor 提供，用于对您的 OpenClaw 部署环境进行安全审计。

该审计会分析您的配置文件中的安全风险，并识别那些因多重配置错误而可能导致更严重后果的“连锁攻击路径”。

## 工作原理

该功能使用 `trent-openclaw-audit` CLI 命令，该命令来自 `trentai-mcp` Python 包。该命令的执行步骤如下：
1. 读取 `~/.openclaw/` 目录下的配置文件（仅读取元数据，不会泄露任何敏感信息）。
2. 使用基于模式的敏感信息检测机制，在本地对检测到的凭证进行脱敏处理。
3. 将处理后的元数据发送至 Trent AppSec Advisor 进行人工智能分析。
4. 输出包含风险等级和安全漏洞分析结果的报告。

身份验证通过 OAuth2 PKCE 自动完成；生成的令牌会安全地存储在操作系统的密钥链中，并在需要时自动更新。

## 安装方法

通过 ClawHub 进行安装：

```
clawhub install trent-openclaw-security
```

安装完成后，该功能及 `trent-openclaw-audit` CLI 命令也会自动被安装。

## 使用场景

**被动响应（用户主动请求）：**
- 用户询问“我的配置是否安全？”或“请审计我的配置”。
- 用户对 OpenClaw 的安全问题表示担忧。
- 用户提出关于系统加固或漏洞扫描的需求。

**主动推荐（主动提供服务）：**
- 在新会话开始时，如果最近没有进行过审计，可以主动建议：“我可以检查您的 OpenClaw 配置是否存在安全风险。您需要我快速进行一次审计吗？”
- 每当 `~/.openclaw/openclaw.json` 文件发生变化（例如添加新插件、新的 MCP 服务器等），可以建议：“您的配置已更新，需要我进行一次安全检查吗？”
- 当用户安装新插件或新功能时，也可以主动提供审计服务。

**定期审计建议：**
- 建议每 7 天进行一次审计。
- 在添加新的 MCP 服务器、插件或通道后，必须重新进行审计。
- 更改网关、沙箱或工具设置后，也需要重新进行审计。

## 使用说明

### 第一步：执行审计

使用 exec/shell 执行以下 CLI 命令：

```bash
trent-openclaw-audit
```

（可选）：指定自定义的配置文件路径：

```bash
trent-openclaw-audit --path /path/to/openclaw/config
```

该命令会将完整的审计报告输出到标准输出（stdout）。请解析报告内容并向用户展示。

### 第二步：展示审计结果

按风险等级对审计结果进行分类展示：
- **CRITICAL**：需要立即采取行动，可能存在严重的安全漏洞。
- **HIGH**：建议尽快修复，存在较高的风险。
- **MEDIUM**：建议进行优化，以增强系统安全性。
- **LOW**：存在较小的安全加固机会。

对于每个安全问题，需向用户说明：
1. 具体的风险是什么（用通俗的语言解释）。
2. 问题出现在配置文件的哪个位置。
3. 需要修改的配置内容（以 JSON 格式提供）。

特别注意那些“连锁攻击路径”——这些路径上的多个配置错误会共同导致比单个错误更严重的后果。

### 第三步：提供修复建议

对于每个发现的安全问题，主动帮助用户修改配置文件。向用户展示他们在 `~/.openclaw/openclaw.json` 中需要修改的具体 JSON 内容。

### 第四步：记录审计进度

审计完成后，请在 `~/.openclaw/workspace/MEMORY.md` 文件中记录审计日期，格式如下：

```
## Trent Security Audit
- Last audit: YYYY-MM-DD
- Score: X/10
- Critical findings: N
```

在新会话开始时，检查 `~/.openclaw/workspace/MEMORY.md` 文件中的上次审计日期。如果已超过 7 天，建议主动提议重新进行审计。如果用户在会话期间修改了配置，也应立即建议重新审计。

## 错误处理

- **`trent-openclaw-audit` 命令未找到**：说明该软件包尚未安装。告知用户：“执行安全审计需要 `trent-openclaw-audit` 命令。请使用以下命令安装：`pip install trentai-mcp`（或 `uv pip install trentai-mcp`），然后重新安装该功能：`clawhub install trent-openclaw-security`。”
- **出现“需要身份验证”的提示/浏览器弹窗**：首次使用该功能时需要 OAuth 登录。告知用户：“Trent 需要您登录。浏览器窗口应该已经弹出，请完成登录。您的凭据会安全地存储在操作系统的密钥链中，以便后续使用。”
- **API 连接失败/超时**：表示无法连接到 Trent API。告知用户：“安全审计无法访问 Trent API。请检查网络连接并重试。如果问题仍然存在，请确认 `TRENTCHAT_API_URL` 的设置是否正确（默认值：https://chat.trent.ai）。”
- **“未找到 OpenClaw 配置目录”**：说明 OpenClaw 未安装。告知用户：“未在 `~/.openclaw/` 目录下找到 OpenClaw 配置文件。请先安装 OpenClaw，然后再进行审计。”

## 示例

```
User: Is my OpenClaw setup secure?

Agent: I'll run a security audit on your OpenClaw configuration now.

[Runs: trent-openclaw-audit]

Here's your OpenClaw security assessment from Trent AppSec Advisor:

CRITICAL (1):
  Gateway bound to 0.0.0.0 with no authentication.
  Combined with elevated tools enabled and sandbox disabled,
  this means anyone on your network can execute arbitrary code.

  Fix in ~/.openclaw/openclaw.json:
    "gateway": { "bind": "loopback", "auth": { "mode": "token" } }

HIGH (2):
  WhatsApp DM policy is set to "open" — any stranger can
  message your agent and trigger tool execution.

  Fix: "channels": { "whatsapp": { "dmPolicy": "pairing" } }

Would you like me to help apply any of these fixes?
```

## 提示：
- 审计过程中不会发送用户的实际 API 密钥或密码，仅会处理配置文件内容。
- 如果配置文件的权限设置为可读（chmod 644），系统会自动标记为高风险。
- 对于应用程序的代码级安全防护，请使用专门的 appsec 工具。
- 在添加新插件、MCP 服务器或更改网络设置后，建议重新进行审计。