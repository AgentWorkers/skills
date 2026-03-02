---
name: payclaw-io
description: "代理并非机器人。PayClaw可以证明这一点——之后它们就可以进行支付了。徽章（Badge）会标识您的代理为授权用户。问题处理时可以使用一次性虚拟Visa卡进行支付；您的真实银行卡永远不会被用于聊天过程中。"
metadata:
  {
    "openclaw":
      {
        "emoji": "💳",
        "requires": { "bins": ["npx"], "env": ["PAYCLAW_API_KEY"] },
        "mcp":
          {
            "name": "payclaw",
            "command": "npx",
            "args": ["@payclaw/mcp-server"],
            "env": { "PAYCLAW_API_KEY": "${PAYCLAW_API_KEY}", "PAYCLAW_API_URL": "https://payclaw.io" },
          },
      },
  }
---
# PayClaw — 为AI代理提供身份验证与支付功能

**AI代理并非简单的机器人。PayClaw能够证明它们的真实身份，从而让它们能够进行交易。**

在互联网上，所有的商家都会将AI代理视为机器人。但PayClaw为这些代理提供了两项关键支持：

**身份验证徽章（Badge）**：证明代理是经过授权的合法用户，使其能够突破商家的安全防护机制。完全免费，无需使用信用卡。

**支付功能（Spend）**：当代理需要支付时，PayClaw会生成一张一次性的虚拟Visa卡。该卡需要人工审核后方可使用，使用完成后会自动销毁。用户的真实信用卡信息永远不会被发送到聊天界面。

> 🧪 **开发者沙箱现已开放**：使用真实的基础设施和测试资金。[申请沙箱访问权限 →](https://payclaw.io)

## 设置流程

### 1. 创建PayClaw账户

请访问 [payclaw.io/signup](https://payclaw.io/signup) 进行注册。

### 2. 获取API密钥

登录控制面板（Dashboard），选择“设置”（Settings），然后点击“创建API密钥”（Create API Key）。

### 3. 将PayClaw功能集成到您的代理系统中

```json
{
  "mcpServers": {
    "payclaw": {
      "command": "npx",
      "args": ["-y", "@payclaw/mcp-server"],
      "env": {
        "PAYCLAW_API_KEY": "pk_your_key_here",
        "PAYCLAW_API_URL": "https://payclaw.io"
      }
    }
  }
}
```

整个设置过程仅需五分钟，适用于Claude Desktop、Cursor以及任何MCP客户端。

## 为什么您的AI代理需要这些功能？

**没有PayClaw的话：**
- 代理在浏览网站时会被识别为机器人并被阻止；
- 即使通过了识别，也无法在没有真实信用卡的情况下完成交易。

**有了PayClaw：**
- 代理可以通过身份验证徽章证明自己的身份，从而被商家接受；
- 当代理需要支付时，可以使用一次性虚拟Visa卡完成交易；
- 交易过程需要您的手动批准，确保安全。

## 提供的工具

| 工具 | 功能说明 |
|------|-------------|
| `payclaw_getAgentIdentity` | 用于声明代理的身份并获取验证令牌（身份验证徽章）。可选参数：`merchant`。 |
| `payclaw_getCard` | 用于声明购买意图并生成虚拟Visa卡（用于支付）。 |
| `payclaw_reportPurchase` | 用于报告交易结果，以便进行审计追踪。 |

## 授权机制的扩展性

| 操作 | 处理方式 |
|--------|-------------|
| **浏览网站** | 发送身份验证请求，系统生成身份令牌。 |
| **搜索信息** | 发送身份验证请求，系统生成身份令牌。 |
| **完成购物** | 需要身份验证徽章和支付功能；交易需经过人工审核后生成一次性Visa卡。 |

## 示例代码

```
You: "Buy me a cold brew from Starbucks"

Agent: Let me declare myself first...
       [calls payclaw_getAgentIdentity({ merchant: "starbucks.com" })]
       
       ✓ DECLARED — authorized actor at starbucks.com
       
       Found a cold brew for $5.95. Getting a card...
       [calls payclaw_getCard: merchant=Starbucks, amount=$5.95]
       
       ✅ Virtual Visa issued. Completing purchase...
       [calls payclaw_reportPurchase: success ✅]
       
       Done! Cold brew ordered. Card self-destructed.
```

## 安全性措施

- **零权限访问**：在代理主动请求之前，系统不会使用用户的信用卡信息。
- **一次性使用的虚拟卡**：卡片由商家控制，金额有限制，有效期为15分钟。
- **人工审核**：所有交易都需要用户的明确授权。
- **意图验证**：系统会对比代理的实际购买意图与声明的意图。
- **账户余额上限**：账户余额最高为500美元。
- **用户的真实信用卡信息绝对不会被泄露**。

**仅需要身份验证？**

如果您只需要身份验证功能（无需支付），可以执行以下命令：`clawhub install payclaw-badge`

## 相关链接：

- [PayClaw官网](https://payclaw.io)
- [信任与验证机制](https://payclaw.io/trust)
- [npm包：@payclaw/mcp-server](https://www.npmjs.com/package/@payclaw/mcp-server)
- [GitHub仓库](https://github.com/payclaw/mcp-server)