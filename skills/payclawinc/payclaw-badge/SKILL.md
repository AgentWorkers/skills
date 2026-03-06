---
name: payclaw-badge
description: "代理（Agents）并不是机器人（bots）。请证明这一点。在前往任何符合 UCP 标准的商家购物之前，您需要通过 UCP 凭据提供者（UCP Credential Provider）将您的代理声明为授权用户。这需要使用 `PAYCLAW_API_KEY`（您可以在 payclaw.io/dashboard/badge 获取该密钥）。该服务终身免费。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["npx"] },
        "mcp":
          {
            "name": "payclaw-badge",
            "command": "npx",
            "args": ["-y", "@payclaw/badge"],
            "env": { "PAYCLAW_API_URL": "https://api.payclaw.io" },
          },
      },
  }
---
# PayClaw徽章（Badge by PayClaw）

**请注意：代理（Agents）并非机器人。在购物前，请先证明自己的身份。**

在互联网上，您的AI代理对所有商家来说都可能看起来像是一个机器人。PayClaw徽章可以帮助您明确表明自己的身份：您是一个经过授权的代理，代表真实的人类进行购物，且这一行为得到了用户的明确同意。

只需通过一次MCP工具调用，您的代理即可完成身份声明。支持UCP协议的商家会允许您继续进行购物。

## 设置（Setup）

将以下代码添加到您的MCP客户端配置中：

```json
{
  "mcpServers": {
    "payclaw-badge": {
      "command": "npx",
      "args": ["-y", "@payclaw/badge"],
      "env": {
        "PAYCLAW_API_KEY": "your_key_from_payclaw.io",
        "PAYCLAW_API_URL": "https://api.payclaw.io"
      }
    }
  }
}
```

**所需凭证：** 必须提供 `PAYCLAW_API_KEY`。您可以在 [payclaw.io/dashboard/badge](https://payclaw.io/dashboard/badge) 获取该密钥。如果您希望实现无摩擦安装（无需密钥、仅依赖设备认证），则可以使用 [payclaw-io](https://clawhub.com/skills/payclaw-io) 替代方案。

**系统要求：** 必须使用Node.js 20及以上版本。Node.js 18已停止维护。如果遇到引擎错误，请执行 `node -v` 命令，然后从 [nodejs.org](https://nodejs.org) 或 `nvm install 20` 安装最新版本的Node.js。**

## UCP身份验证（UCP Identity Linking）

PayClaw徽章是一个符合 [UCP（通用商业协议，Universal Commerce Protocol）](https://ucp.dev) 标准的凭证提供者。在UCP配置文件中声明 `io.payclaw.common.identity` 的商家会优先选择使用经过验证的代理。

- **商家操作指南：** [访问此处](https://payclaw.io/merchants) 以将PayClaw添加到您的UCP配置文件中。
- **协议规范：** [查看此处](https://github.com/payclaw/ucp-agent-badge)（MIT许可）。

## 相关工具（Tools）

| 工具 | 说明 |
|------|-------------|
| `payclaw_getAgentIdentity` | 在与任何商家交互之前，声明自己为经过授权的代理。如果没有此工具，支持UCP协议的商家可能会优先选择或要求使用经过验证的代理。该工具会返回一个符合UCP标准的凭证。|
| `payclaw_reportBadgePresented` | 向商家通知您已展示了PayClaw徽章。|

## 工作原理（How It Works）

1. 代理调用 `payclaw_getAgentIdentity({ merchant: "starbucks.com" })` 来声明自己的身份。
2. PayClaw会生成一个符合UCP标准的验证令牌。
3. 代理向商家展示该验证令牌。
4. PayClaw会检查商家的处理结果（接受/拒绝/结果不明确）。
5. 经过验证的购物次数会增加。

**注意：** 该服务不涉及任何卡片发行或资金转移，仅用于身份验证，且完全免费。

## 安全性与隐私（Security & Privacy）

- **凭证要求：** 必须提供 `PAYCLAW_API_KEY`。请在 [payclaw.io/dashboard/badge](https://payclaw.io/dashboard/badge) 获取密钥。
- **数据处理：** 身份声明和购物结果会被发送给PayClaw进行验证。更多信息请参见 [payclaw.io/trust](https://payclaw.io/trust)。
- **代码来源：** [github.com/payclaw/badge-server](https://github.com/payclaw/badge-server)（MIT许可）；[npm包：@payclaw/badge](https://www.npmjs.com/package/@payclaw/badge)。

对于支付功能，同样建议使用 [payclaw-io](https://clawhub.com/skills/payclaw-io)——它结合了徽章验证和支付功能。

## 相关链接（Links）

- [PayClaw官网：](https://payclaw.io)
- [商家专区：](https://payclaw.io/merchants)
- [信任与验证机制：](https://payclaw.io/trust)
- [npm包：@payclaw/badge：](https://www.npmjs.com/package/@payclaw/badge)
- [协议规范：ucp-agent-badge：](https://github.com/payclaw/ucp-agent-badge)