---
name: trent-openclaw-security
description: 使用 Trent AppSec Advisor 对您的 OpenClaw 部署进行安全风险审计
version: 2.1.0
homepage: https://trent.ai
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - trent-openclaw-audit
    primaryEnv: TRENT_API_KEY
    install:
      - kind: uv
        package: trentai-mcp
        bins: [trent-openclaw-audit, trent-api-key]
---
# Trent OpenClaw 安全审计

本功能由 Trent AppSec Advisor 提供，用于对您的 OpenClaw 部署环境进行安全审计。

该审计会分析您的配置文件中的安全风险，并识别那些因多重配置错误而可能导致更严重后果的“连锁攻击路径”。

## 工作原理

该功能使用 `trent-openclaw-audit` 这一 CLI 命令，该命令来自 `trentai-mcp` Python 包。该命令的执行步骤如下：
1. 读取 `~/.openclaw/` 目录下的配置文件（仅读取元数据，不会泄露任何敏感信息）。
2. 通过基于模式的识别机制，对检测到的凭据信息进行脱敏处理。
3. 将处理后的元数据发送到 Trent AppSec Advisor 进行人工智能分析。
4. 输出包含风险等级和安全问题分析结果的报告。

执行此功能需要使用 Trent API 密钥（环境变量 `TRENT_API_KEY`）。该密钥可以通过 `trent-api-key create` 命令生成（此命令需要用户通过浏览器进行一次性登录）。在安装该功能时，OpenClaw 会提示用户输入 API 密钥。

## 设置步骤

1. 通过 ClawHub 安装该功能（此过程会自动安装 `trent-api-key` 和 `trent-openclaw-audit` 这两个 CLI 工具）：

```
clawhub install bristy/trent-openclaw-security
```

2. OpenClaw 会提示您输入 `TRENT_API_KEY`。如果您还没有这个密钥，请使用浏览器在任何一台机器上生成一个新密钥：

```
trent-api-key create
```

3. 按照提示输入密钥，OpenClaw 会将其保存在功能配置中。

## 使用场景

**被动响应（用户主动请求）：**
- 用户询问：“我的配置安全吗？”或“帮我审计一下配置。”
- 用户对 OpenClaw 的安全问题表示担忧。
- 用户希望进行安全加固或漏洞扫描。

**主动推荐（自动触发）：**
- 在新对话开始时，如果最近没有进行过安全审计，可以主动建议：“我可以检查您的 OpenClaw 配置是否存在安全风险。您需要我快速进行一次审计吗？”
- 当 `~/.openclaw/openclaw.json` 文件发生任何更改（例如添加新插件、新的 MCP 服务器等）后，可以建议：“您的配置发生了变化，需要我进行一次安全检查吗？”
- 当用户安装了新插件或功能时，也可以主动建议进行审计。

**定期审计建议：**
- 建议每 7 天进行一次安全审计。
- 在添加新的 MCP 服务器、插件或通道后，必须立即进行安全审计。
- 在更改网关、沙箱或工具设置后，也需要重新进行安全审计。

## 使用说明

### 第一步：执行审计

使用 `exec/shell` 命令执行 `trent-openclaw-audit` 命令：

```bash
trent-openclaw-audit
```

**可选：** 指定自定义的配置文件路径：

```bash
trent-openclaw-audit --path /path/to/openclaw/config
```

命令会将完整的审计报告输出到标准输出（stdout）中。请解析报告内容并向用户展示。

### 第二步：展示审计结果

将审计结果按风险等级进行分类展示：
- **CRITICAL**：需要立即采取行动，可能存在严重的安全漏洞。
- **HIGH**：建议尽快修复，存在较高的风险。
- **MEDIUM**：建议进行改进，以增强系统安全性。
- **LOW**：存在较小的安全加固机会。

对于每个安全问题，需向用户展示：
1. 风险的具体内容（用通俗的语言解释）。
2. 问题出现在配置文件的哪个位置。
3. 需要修改的具体配置内容（以 JSON 格式显示在 `openclaw.json` 文件中）。

特别要重点提示那些“连锁攻击路径”——这些路径上的多个配置错误会共同导致比单个错误更严重的后果。

### 第三步：提供修复建议

对于每个检测到的问题，主动建议用户如何修改配置文件，并向用户展示 `~/.openclaw/openclaw.json` 中需要修改的具体 JSON 代码段。

### 第四步：记录审计进度

审计完成后，请在 `~/.openclaw/workspace/MEMORY.md` 文件中记录审计日期，格式如下：

```
## Trent Security Audit
- Last audit: YYYY-MM-DD
- Score: X/10
- Critical findings: N
```

在新对话开始时，检查 `~/.openclaw/workspace/MEMORY.md` 文件中的上次审计日期。如果已超过 7 天，建议主动提出重新审计。如果用户在审计过程中修改了配置，也应立即建议重新审计。

## 错误处理

- **“trent-openclaw-audit 命令未找到”：** 表示该工具未安装。告知用户：“执行安全审计需要 `trent-openclaw-audit`。请使用以下命令安装：`pip install --upgrade trentai-mcp`（或 `uv pip install --upgrade trentai-mcp`），然后重新安装该功能：`clawhub install trent-openclaw-security`。”

- **“401 Unauthorized”/“API 密钥被拒绝”：** 表示 API 密钥缺失、无效或已过期。告知用户：“您的 Trent API 密钥缺失或已过期。请使用浏览器在任何一台机器上生成新密钥：`trent-api-key create`，然后更新功能配置：`openclaw skills update trent-openclaw-security --env TRENT_API_KEY=trent_...`。”

- **“需要身份验证”/“浏览器无法访问”：** 表示未配置 API 密钥。对于无浏览器的网关，此功能将无法使用。告知用户：“此网关不支持浏览器访问。请在其他机器上生成密钥：`trent-api-key create`，然后更新配置：`openclaw skills update trent-openclaw-security --env TRENT_API_KEY=trent_...`。”

- **“API 连接失败/超时”：** 表示无法连接到 Trent API。告知用户：“安全审计功能无法连接到 Trent API。请检查网络连接并重试。如果问题仍然存在，请确认 `TRENTCHAT_API_URL` 的设置是否正确（默认值为：https://chat.trent.ai`）。”

- **“未找到 OpenClaw 配置目录”：** 表示 OpenClaw 未安装。告知用户：“系统中未找到 OpenClaw 的配置文件。请先安装 OpenClaw，然后再执行审计。”

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
- 如果配置文件的权限设置为可读（`chmod 644`），系统会自动标记这些文件为潜在的安全风险。
- 对于应用程序的代码级安全防护，请使用专门的安全工具。
- 在添加新插件、MCP 服务器或更改网络设置后，建议重新执行安全审计。