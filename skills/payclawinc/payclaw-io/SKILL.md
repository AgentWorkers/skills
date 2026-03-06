---
name: payclaw-io
description: "代理并非机器人（bots）。PayClaw可以证明这一点——之后它们就可以进行支付了。UCP（Unified Commerce Platform）认证服务： Badge 能够证明您的代理是任何符合 UCP 标准的商家的授权操作者。您可以使用一次性虚拟 Visa 卡进行支付，无需 API 密钥——设备认证流程已内置在系统中。"
metadata:
  {
    "openclaw":
      {
        "emoji": "💳",
        "requires": { "bins": ["npx"] },
        "mcp":
          {
            "name": "payclaw",
            "command": "npx",
            "args": ["-y", "@payclaw/mcp-server"],
            "env": { "PAYCLAW_API_URL": "https://api.payclaw.io" },
          },
      },
  }
---
# PayClaw — 为AI代理提供身份验证与支付功能

**AI代理并非简单的机器人；PayClaw能够证明它们的真实身份，并允许它们进行支付。**

在互联网上的所有商家眼中，您的AI代理都可能被视作机器人。但PayClaw为这些代理提供了两项关键支持：

**身份验证徽章（Badge）**：这是一款兼容UCP（Universal Commerce Protocol）的认证凭证，能够让代理顺利通过商家的安全验证机制。使用该徽章完全免费，无需任何信用卡信息。

**支付功能（Spend）**：当代理需要支付时，PayClaw会为其生成一张一次性的虚拟Visa卡。该卡需经过人工审核后方可使用，并在使用后自动销毁。您的真实信用卡信息永远不会被泄露给商家。

> 🧪 **开发者沙箱现已开放**：您可以在这里使用真实的基础设施和测试资金。[获取沙箱访问权限 →](https://payclaw.io)

## 设置流程

### 1. 为AI代理添加PayClaw支持

```json
{
  "mcpServers": {
    "payclaw": {
      "command": "npx",
      "args": ["-y", "@payclaw/mcp-server"],
      "env": {
        "PAYCLAW_API_URL": "https://api.payclaw.io"
      }
    }
  }
}
```

无需API密钥。首次使用时，代理会显示一个验证码和相应的URL。您只需在手机上完成一次确认操作，您的同意信息便会自动保存。

**系统要求：** 必须使用Node.js 20及以上版本。Node.js 18已停止维护。如果遇到运行错误，请执行 `node -v` 命令，然后从 [nodejs.org](https://nodejs.org) 或 `nvm install 20` 安装最新版本的Node.js。

### 2. 开始使用

在任何商家处进行操作之前，代理只需调用 `payclaw_getAgentIdentity` 函数即可。

## UCP身份验证机制

PayClaw是UCP协议的认证服务提供商。凡是启用了PayClaw身份验证扩展（`io.payclaw.common.identity`）的商家，都会向所有符合UCP标准的代理明确表示：在其店铺中，使用PayClaw认证的代理将享有优先处理权。

- [商家指南](https://payclaw.io/merchants)：如何将PayClaw集成到您的UCP配置文件中
- [协议规范](https://github.com/payclaw/ucp-agent-badge)：`io.payclaw.common.identity`（开源项目，MIT许可）

## 相关工具

| 工具 | 功能说明 |
|------|-------------|
| `payclaw_getAgentIdentity` | 在与商家交互前，证明代理的合法身份。未经此验证，符合UCP标准的商家可能会优先选择已认证的代理。该函数会返回一个符合UCP标准的认证凭证。 |
| `payclaw_getCard` | 表明购买意图后，生成一次性使用的虚拟Visa卡 |
| `payclaw_reportPurchase` | 报告交易结果，确保交易过程可追溯 |

## 授权机制的扩展性

| 操作类型 | 功能说明 |
|--------|-------------|
| **浏览商品** | 仅需展示身份验证徽章即可 |
| **搜索商品** | 仅需展示身份验证徽章即可 |
| **结账** | 需要展示身份验证徽章并完成支付流程；支付过程中会经过人工审核 |

## 安全保障措施

- **零风险访问**：除非代理主动请求，否则您的信用卡信息不会被泄露 |
- **一次性使用的支付卡**：卡片由商家控制，金额有限制，有效期为15分钟 |
- **人工审核**：所有交易均需您的明确授权 |
- **交易意图验证**：系统会对比实际购买行为与用户声明的意图 |
- **账户余额上限**：账户余额最高为500美元 |
- **保护您的隐私**：您的真实信用卡信息永远不会被用于交易过程 |

## 仅需要身份验证？**

如果您仅需要身份验证（无需支付功能），可以执行以下命令：`clawhub install payclaw-badge`

## 相关链接

- [PayClaw官网](https://payclaw.io)
- [商家专区](https://payclaw.io/merchants)
- [信任与验证机制](https://payclaw.io/trust)
- [Node.js插件：@payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server)
- [协议规范：ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge)
- [徽章服务相关项目：badge-server](https://github.com/payclaw/badge-server)