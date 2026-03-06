---
name: payclaw-io
description: "代理并非机器人。PayClaw证明了这一点——因此它们可以被允许进行支付。UCP（Unified Commerce Platform）认证提供者： Badge能够将您的代理声明为任何符合UCP标准的商家的授权用户。支出时可以使用一次性的虚拟Visa卡；无需API密钥，因为设备认证流程已经内置在系统中。"
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

**AI代理并非简单的机器人程序。PayClaw能够证明它们的真实身份，从而让它们能够进行支付。**

在互联网上的所有商家眼中，AI代理看起来都像普通的机器人程序。但PayClaw为这些代理提供了两项关键支持：

**身份徽章（Badge）**—— 证明你的代理是经过授权的合法用户。这是一个与UCP（Universal Commerce Protocol）兼容的认证凭证，可以让代理顺利通过商家的安全验证机制。完全免费，无需使用信用卡。

**支付功能（Spend）**—— 当代理需要支付时，PayClaw会生成一张一次性的虚拟Visa卡。该卡需要人工审核批准，并在使用后自动销毁。你的真实信用卡信息永远不会被泄露给商家。

> 🧪 **开发者沙箱现已开放。** 可使用真实基础设施进行测试。[获取沙箱访问权限 →](https://payclaw.io)

## 设置流程

### 1. 为你的AI代理添加PayClaw支持

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

无需API密钥。首次使用时，代理会显示一个验证码和相应的URL。你只需在手机上完成一次确认操作，即可完成设置——你的同意信息会自动保存。

**系统要求：Node.js 20.0及以上版本**。Node.js 18版本已停止维护。如果遇到运行错误，请执行 `node -v` 命令，然后从 [nodejs.org](https://nodejs.org) 或 `nvm install 20` 安装最新版本的Node.js。

### 2. 开始使用

在代理与任何商家进行交互之前，只需调用 `payclaw_getAgentIdentity` 函数即可。

## UCP身份验证机制

PayClaw是一个符合UCP标准的认证服务提供商。商家可以通过在他们的系统中启用 `io.payclaw.common.identity` 扩展，来表明他们更倾向于使用已通过PayClaw身份验证的代理。

- [商家指南](https://payclaw.io/merchants)：如何将PayClaw集成到你的UCP系统中
- [协议规范](https://github.com/payclaw/ucp-agent-badge)：`io.payclaw.common.identity`（开源项目，MIT许可）

## 相关工具

| 工具 | 功能说明 |
|------|-------------|
| `payclaw_getAgentIdentity` | 在与商家交互前，声明代理的合法身份。未经此步骤，符合UCP标准的商家可能会优先选择已验证的代理。返回一个与UCP兼容的认证凭证。 |
| `payclaw_getCard` | 声明购买意图后，生成一次性虚拟Visa卡用于支付。 |
| `payclaw_reportPurchase` | 报告交易结果，确保交易过程的透明度。 |

## 授权机制的扩展性

| 操作类型 | 功能说明 |
|--------|-------------|
| **浏览商品** | 代理显示身份徽章后，系统会生成UCP身份令牌。 |
| **搜索商品** | 代理显示身份徽章后，系统同样会生成UCP身份令牌。 |
| **结账** | 代理显示身份徽章并使用支付功能后，系统会生成一次性Visa卡，并需要人工审核批准。 |

## 安全保障措施

- **零风险访问**：除非代理主动请求，否则不会使用任何信用卡信息。 |
- **一次性支付卡**：每张支付卡都由商家控制，支付金额有限制，且有效期仅为15分钟。 |
- **人工审核**：所有交易都需要你的明确授权。 |
- **意图验证**：系统会对比实际购买行为与代理声明的购买意图。 |
- **账户余额上限**：账户余额最高为500美元。 |
- **保护用户隐私**：你的真实信用卡信息绝对不会被泄露给商家。 |

## 如果只需要身份验证？

如果你仅需要身份验证（无需支付功能），可以执行以下命令：`clawhub install payclaw-badge`

## 相关链接

- [PayClaw官网](https://payclaw.io) |
- [商家专区](https://payclaw.io/merchants) |
- [信任与验证机制](https://payclaw.io/trust) |
- [Node.js插件：@payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server) |
- [协议规范：ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge) |
- [徽章服务相关项目：badge-server](https://github.com/payclaw/badge-server)