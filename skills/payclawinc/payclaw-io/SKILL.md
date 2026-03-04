---
name: payclaw-io
description: "代理并非机器人。PayClaw可以证明这一点——因此，它们能够完成支付。UCP凭证提供者（UCP Credential Provider）的“Badge”功能可确认您的代理为任何符合UCP标准的商家的授权用户。支付时可以使用一次性的虚拟Visa卡；无需API密钥，因为设备认证流程已内置在系统中。"
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

**AI代理并非简单的机器人。PayClaw能够证明它们的真实身份，从而让它们能够进行支付。**

在互联网上的所有商家眼中，AI代理都可能被视作机器人。但PayClaw为这些代理提供了两项关键支持：

**身份验证徽章（Badge）**：这是一款兼容UCP（Universal Commerce Protocol）的认证凭证，能够让代理顺利通过商家的安全验证机制。完全免费，无需使用信用卡。

**支付功能（Spend）**：当代理需要支付时，PayClaw会为其生成一张一次性的虚拟Visa卡。该卡需要经过人工审核后方可使用，并在使用后自动销毁。用户的真实信用卡信息永远不会被泄露到聊天记录中。

> 🧪 **开发者沙箱现已开放**：可以使用真实的基础设施进行测试。[获取沙箱访问权限 →](https://payclaw.io)

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

无需API密钥。首次使用时，代理会显示一个代码和URL。你只需在手机上完成一次确认操作，即可完成设置——你的同意信息会自动被保存。

### 2. 开始使用

在任何商家处进行操作之前，代理只需调用`payclaw_getAgentIdentity`函数即可。

## UCP身份验证机制

PayClaw是UCP协议的认证服务提供商。那些启用了PayClaw身份验证扩展（`io.payclaw.common.identity`）的商家，会向所有符合UCP标准的代理明确表示：在他们的店铺中，使用PayClaw认证的代理将获得优先处理权。

- [商家指南](https://payclaw.io/merchants)：如何将PayClaw集成到你的UCP配置文件中
- [协议规范](https://github.com/payclaw/ucp-agent-badge)：`io.payclaw.common.identity`（开源代码，MIT许可证）

## 相关工具

| 工具 | 功能说明 |
|------|-------------|
| `payclaw_getAgentIdentity` | 在与商家交互前，声明自己的代理身份。未经此步骤，符合UCP标准的商家可能会优先选择已认证的代理。该函数会返回一个符合UCP标准的认证凭证。 |
| `payclaw_getCard` | 声明购买意图后，生成一次性虚拟Visa卡（用于支付） |
| `payclaw_reportPurchase` | 报告交易结果，确保交易记录的透明度 |

## 授权机制的扩展性

| 动作 | 处理方式 |
|--------|-------------|
| **浏览商品** | 仅需要展示身份验证徽章即可 |
| **搜索商品** | 也需要展示身份验证徽章 |
| **结账** | 需要同时展示身份验证徽章并完成支付操作；支付过程需经过人工审核 |

## 安全保障措施

- **零风险访问**：在代理主动请求之前，用户的信用卡信息不会被存储 |
- **一次性使用的支付卡**：卡片由商家控制，金额有限制，有效期为15分钟 |
- **人工审核**：所有交易均需用户明确授权 |
- **意图验证**：所有交易都会与用户事先声明的购买意图进行比对 |
- **账户余额上限**：账户余额最高为500美元 |
- **用户信用卡信息保密**：用户的真实信用卡信息永远不会被泄露到聊天记录中 |

## 如果只需要身份验证？

如果你仅需要身份验证（无需支付功能），可以执行以下命令：`clawhub install payclaw-badge`

## 相关链接

- [PayClaw官网](https://payclaw.io)
- [商家专区](https://payclaw.io/merchants)
- [信任与验证机制](https://payclaw.io/trust)
- [npm包：@payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server)
- [协议规范：ucp-agent-badge](https://github.com/payclaw/ucp-agent-badge)
- [GitHub项目：badge-server](https://github.com/payclaw/badge-server)