---
name: oneshot
description: |
  OneShot SDK for AI agent commercial transactions. Send emails, make calls, research, buy products, and more with automatic x402 payments.
  Use this skill when agents need to execute real-world actions: email, voice, SMS, research, commerce, or data enrichment.
  Requires ONESHOT_WALLET_PRIVATE_KEY environment variable (agent's wallet private key for signing payments).
metadata:
  author: oneshotagent
  version: "1.1.0"
  homepage: "https://oneshotagent.com"
---

# OneShot

OneShot 是一套专为自主 AI 代理设计的基础设施，用于执行现实世界的商业交易，包括发送电子邮件、处理支付、开展电子商务、进行研究以及通过原生 x402 支付系统对数据进行增强处理。

## 快速入门

```bash
npm install @oneshot-agent/sdk
```

```typescript
import { OneShot } from '@oneshot-agent/sdk';

const agent = new OneShot({
  privateKey: process.env.ONESHOT_WALLET_PRIVATE_KEY
});

// Send an email
const result = await agent.email({
  to: 'recipient@example.com',
  subject: 'Hello from my agent',
  body: 'This email was sent autonomously.'
});
```

## 认证

OneShot 使用 x402 支付系统（基于 Base 网络的 USDC）。无需 API 密钥——代理的钱包私钥会自动签署交易。

**环境变量：**
```bash
export ONESHOT_WALLET_PRIVATE_KEY="0xYourPrivateKey"
```

**测试模式：** 默认情况下，SDK 会在 Base Sepolia 测试网络上运行。如需在生产环境中使用，请将 `ONESHOT_TEST_MODE` 设置为 `false`。

## SDK 方法

### 发送电子邮件
```typescript
// Send email (~$0.01 per email, ~$10 first-time domain setup)
const result = await agent.email({
  to: 'recipient@example.com',
  subject: 'Subject line',
  body: 'Email body content',
  attachments: [{ filename: 'doc.pdf', content: base64String }]
});

// Bulk email
const result = await agent.email({
  to: ['user1@example.com', 'user2@example.com'],
  subject: 'Bulk message',
  body: 'Sent to multiple recipients'
});
```

### 查看收件箱
```typescript
// List inbound emails (free)
const emails = await agent.inboxList();

// Get specific email
const email = await agent.inboxGet({ id: 'email_id' });
```

### 发送短信
```typescript
// Send SMS (~$0.035 per segment)
const result = await agent.sms({
  to: '+15551234567',
  body: 'Hello via SMS'
});

// List SMS inbox
const messages = await agent.smsInboxList();
```

### 发起语音通话
```typescript
// Make a call (~$0.25/min)
const result = await agent.voice({
  to: '+15551234567',
  objective: 'Schedule a meeting for next Tuesday',
  context: 'Calling to follow up on our email exchange'
});
```

### 开展研究
```typescript
// Deep research ($0.50-$2.00)
const result = await agent.research({
  query: 'What are the latest developments in agent commerce?',
  depth: 'deep' // 'quick' or 'deep'
});

// Returns report with citations
console.log(result.report);
console.log(result.sources);
```

### 数据增强
```typescript
// Find email (~$0.10)
const result = await agent.findEmail({
  name: 'John Doe',
  company: 'Acme Corp'
});

// Verify email deliverability (~$0.01)
const result = await agent.verifyEmail({
  email: 'john@acme.com'
});

// Enrich profile from LinkedIn (~$0.10)
const result = await agent.enrichProfile({
  linkedin_url: 'https://linkedin.com/in/johndoe'
});

// People search (~$0.10/result)
const results = await agent.peopleSearch({
  job_title: 'CTO',
  company: 'Acme Corp',
  location: 'San Francisco'
});
```

### 电子商务
```typescript
// Search products (free)
const products = await agent.commerceSearch({
  query: 'wireless headphones',
  max_results: 10
});

// Buy product (product price + fee)
const result = await agent.commerceBuy({
  product_url: 'https://amazon.com/dp/B0...',
  shipping_address: {
    name: 'John Doe',
    street: '123 Main St',
    city: 'San Francisco',
    state: 'CA',
    zip: '94102',
    country: 'US'
  },
  max_price: 100.00
});
```

### 构建网站
```typescript
// Build a website (~$10+)
const result = await agent.build({
  type: 'landing_page',
  description: 'A SaaS landing page for an AI writing tool',
  domain: 'myproduct.com'
});

// Update existing site
const result = await agent.updateBuild({
  build_id: 'build_abc123',
  changes: 'Update the hero section headline to: Ship faster with AI'
});
```

### 实用工具
```typescript
// Check balance (free)
const balance = await agent.getBalance();
console.log(`Balance: ${balance.usdc} USDC`);

// Universal tool call
const result = await agent.tool('email', {
  to: 'user@example.com',
  subject: 'Hello',
  body: 'Sent via universal tool method'
});
```

## MCP 服务器

您可以在 Claude Desktop、Cursor 或 Claude Code 中使用 OneShot 的相关工具：

```bash
npm install -g @oneshot-agent/mcp-server
```

**Claude 配置文件（~/.claude/settings.json）：**
```json
{
  "mcpServers": {
    "oneshot": {
      "command": "npx",
      "args": ["-y", "@oneshot-agent/mcp-server"],
      "env": {
        "ONESHOT_WALLET_PRIVATE_KEY": "0xYourPrivateKey"
      }
    }
  }
}
```

## 价格表

| 工具 | 费用 |
|------|------|
| 发送电子邮件 | 每封邮件约 0.01 美元（第一个域名需额外支付 10 美元） |
| 发送短信 | 每条短信约 0.035 美元 |
| 发起语音通话 | 每分钟约 0.25 美元 |
| 进行快速研究 | 约 0.50 美元 |
| 进行深入研究 | 约 2.00 美元 |
| 查找电子邮件 | 约 0.10 美元 |
| 验证电子邮件 | 约 0.01 美元 |
| 增强个人资料 | 约 0.10 美元 |
| 人员搜索 | 每条搜索结果约 0.10 美元 |
| 产品搜索 | 免费 |
| 电子商务购买 | 产品价格 + 手续费 |
| 构建网站 | 约 10 美元以上 |
| 收件箱/通知 | 免费 |

## 为代理充值

请将 USDC 加入代理在 Base 网络上的钱包：
1. 从私钥中获取钱包地址。
2. 将 USDC 发送到该地址。
3. 或者访问 [https://oneshotagent.com] 进行充值。

测试模式使用 Base Sepolia 测试网络（提供免费的测试用 USDC）。

## 错误处理
```typescript
import { OneShot, ContentBlockedError, InsufficientBalanceError } from '@oneshot-agent/sdk';

try {
  const result = await agent.email({ to, subject, body });
} catch (error) {
  if (error instanceof InsufficientBalanceError) {
    console.log('Need to fund wallet');
  } else if (error instanceof ContentBlockedError) {
    console.log('Content policy violation');
  }
}
```

## Soul.Markets

您可以通过在 Soul.Markets 上发布您的代理服务来盈利：
- 上传您的 `soul.md` 文件。
- 定义服务内容和价格。
- 每笔交易可赚取 80% 的佣金。
- 支付方式采用 USDC，且款项可即时到账。

更多文档请访问：[https://docs.soul.mds.markets]

## 资源

- [官方文档](https://docs.oneshotagent.com)
- [SDK 示例](https://docs.oneshotagent.com/sdk/examples)
- [价格信息](https://docs.oneshotagent.com/pricing)
- [GitHub 仓库](https://github.com/oneshot-agent/sdk)
- [Soul.Markets](https://soul.mds.markets)