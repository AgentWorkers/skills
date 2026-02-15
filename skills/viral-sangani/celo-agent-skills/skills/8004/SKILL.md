---
name: 8004
description: ERC-8004 代理信任协议：用于在 Celo 平台上实现 AI 代理的身份验证、声誉管理及信任验证功能。适用于需要跨组织边界进行身份注册、声誉追踪或信任验证的 AI 代理的开发场景。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# ERC-8004：智能体信任协议

ERC-8004为自主智能体建立了信任基础设施，使它们能够跨组织边界发现、识别和评估其他智能体。

## 使用场景

- 在链上注册智能体的身份
- 为智能体构建声誉系统
- 在交互前验证智能体的身份
- 查询智能体的声誉和反馈
- 实现基于信任的智能体交互

## 核心概念

### 三个注册表

| 注册表 | 目的 | 主要功能 |
|----------|---------|---------------|
| **身份注册表** | 通过 ERC-721 NFT 进行智能体发现 | `register()`, `agentURI()` |
| **声誉注册表** | 提供反馈和证明 | `giveFeedback()`, `getSummary()` |
| **验证注册表** | 提供验证机制 | 自定义验证器 |

### 协议栈中的位置

```
Application Layer (Agent Apps, Marketplaces)
    ↓
Trust Layer (ERC-8004) ← This skill
    ↓
Payment Layer (x402)
    ↓
Communication Layer (A2A, MCP)
```

## 安装

```bash
# JavaScript/TypeScript
npm install @chaoschain/sdk

# Python
pip install chaoschain-sdk
```

## 合同地址

### Celo 主网

| 合同 | 地址 |
|----------|---------|
| 身份注册表 | 即将推出（2026年第一季度） |
| 声誉注册表 | 即将推出（2026年第一季度） |

### Celo Sepolia（测试网）

| 合同 | 地址 |
|----------|---------|
| 身份注册表 | 即将推出 |
| 声誉注册表 | 即将推出 |

## 智能体注册

### 1. 创建注册文件

创建一个描述智能体端点及其功能的注册文件：

```json
{
  "type": "Agent",
  "name": "My AI Agent",
  "description": "Description of capabilities",
  "image": "ipfs://Qm...",
  "endpoints": [
    {
      "type": "a2a",
      "url": "https://example.com/.well-known/agent.json"
    },
    {
      "type": "mcp",
      "url": "https://example.com/mcp"
    },
    {
      "type": "wallet",
      "address": "0x...",
      "chainId": 42220
    }
  ],
  "supportedTrust": ["reputation", "validation", "tee"]
}
```

### 2. 上传到 IPFS

```javascript
import { upload } from "@chaoschain/sdk";

const agentMetadata = {
  type: "Agent",
  name: "My AI Agent",
  description: "AI agent for DeFi operations",
  // ...
};

const agentURI = await upload(agentMetadata);
// Returns: ipfs://QmYourRegistrationFile
```

### 3. 注册智能体

```javascript
import { IdentityRegistry } from '@chaoschain/sdk';
import { createPublicClient, http } from 'viem';
import { celo } from 'viem/chains';

const client = createPublicClient({
  chain: celo,
  transport: http('https://forno.celo.org'),
});

const registry = new IdentityRegistry(client);

// Register and get agent ID
const tx = await registry.register(agentURI);
const agentId = tx.events.Transfer.returnValues.tokenId;

console.log('Agent registered with ID:', agentId);
```

## 声誉系统

### 提供反馈

```javascript
import { ReputationRegistry } from '@chaoschain/sdk';

const reputation = new ReputationRegistry(client);

await reputation.giveFeedback(
  agentId,           // Agent ID to review
  85,                // score (0-100)
  0,                 // decimals
  'starred',         // tag1: category
  '',                // tag2: optional
  'https://agent.example.com',  // endpoint used
  'ipfs://QmDetailedFeedback',  // detailed feedback URI
  feedbackHash       // keccak256 of feedback content
);
```

### 常见反馈标签

| 标签 | 度量指标 | 例子 |
|-----|----------|---------|
| `starred` | 质量评分（0-100） | 87/100 |
| `uptime` | 端点运行时间百分比 | 99.77% |
| `successRate` | 任务成功率百分比 | 89% |
| `responseTime` | 响应时间（毫秒） | 560毫秒 |
| `reachable` | 端点是否可访问 | true/false |

### 查询声誉

```javascript
// Get all feedback for an agent
const feedback = await reputation.readAllFeedback(agentId);

// Get aggregated summary
const summary = await reputation.getSummary(agentId);
console.log('Average rating:', summary.averageScore);
console.log('Total reviews:', summary.totalFeedback);
```

## 信任验证流程

```javascript
import { IdentityRegistry, ReputationRegistry } from '@chaoschain/sdk';

async function verifyAndInteract(targetAgentId, minReputation = 70) {
  // 1. Verify identity
  const identity = await identityRegistry.getAgent(targetAgentId);
  if (!identity) {
    throw new Error('Agent not registered');
  }

  // 2. Check reputation
  const summary = await reputationRegistry.getSummary(targetAgentId);
  if (summary.averageScore < minReputation) {
    throw new Error(`Agent reputation ${summary.averageScore} below threshold ${minReputation}`);
  }

  // 3. Get endpoint
  const agentData = await fetch(identity.agentURI).then(r => r.json());
  const endpoint = agentData.endpoints.find(e => e.type === 'a2a');

  // 4. Interact with verified agent
  const result = await interactWithAgent(endpoint.url);

  // 5. Submit feedback
  await reputationRegistry.giveFeedback(
    targetAgentId,
    result.success ? 90 : 30,
    0,
    result.success ? 'starred' : 'failed',
    '',
    endpoint.url,
    '',
    ''
  );

  return result;
}
```

## 与 x402 支付系统的集成

ERC-8004 与 x402 结合使用，以实现可信任的付费智能体交互：

```javascript
import { IdentityRegistry, ReputationRegistry } from '@chaoschain/sdk';
import { wrapFetchWithPayment } from 'thirdweb/x402';

async function payTrustedAgent(agentId, serviceUrl) {
  // 1. Verify trust
  const summary = await reputationRegistry.getSummary(agentId);
  if (summary.averageScore < 80) {
    throw new Error('Agent not trusted enough for payment');
  }

  // 2. Make paid request
  const fetchWithPayment = wrapFetchWithPayment({
    client,
    account,
    paymentOptions: { maxValue: "1000000" },
  });

  const response = await fetchWithPayment(serviceUrl);
  return response.json();
}
```

## 使用案例

### DeFi 交易智能体

在委托资金之前验证策略智能体：

```javascript
const strategyAgents = await identityRegistry.searchByCapability('defi-trading');
const trustedAgents = [];

for (const agent of strategyAgents) {
  const summary = await reputationRegistry.getSummary(agent.id);
  if (summary.averageScore >= 85 && summary.totalFeedback >= 100) {
    trustedAgents.push(agent);
  }
}
```

### 多智能体工作流程

协调受信任的智能体执行复杂任务：

```javascript
const workflow = {
  research: await findTrustedAgent('research', 80),
  analysis: await findTrustedAgent('analysis', 85),
  execution: await findTrustedAgent('execution', 90),
};

// Execute with trust-verified agents
await executeWorkflow(workflow);
```

## 验证注册表

对于高风险操作，使用验证注册表进行额外验证：

| 机制 | 适用场景 | 优点 |
|-------|-----------|----------|
| **基于声誉的验证** | 客户反馈 | 适用于低风险、频繁的场景 |
| **加密经济模型** | 持币 + 减损机制 | 适用于中等风险、金融场景 |
| **zkML** | 零知识证明 | 保护隐私 |
| **TEE 证明** | 硬件隔离 | 高可靠性 |

## Celo 网络参考

| 网络 | 链路 ID | RPC 端点 |
|---------|----------|--------------|
| Celo 主网 | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |

## 额外资源

- [EIP 规范](https://eips.ethereum.org/EIPS/eip-8004)
- [官方网站](https://www.8004.org)
- [学习门户](https://www.8004.org/learn)
- [合约仓库](https://github.com/erc-8004/erc-8004-contracts)
- [构建工具](http://bit.ly/8004builderprogram)

## 相关技能

- [x402](../x402/SKILL.md) - 用于智能体的支付层 |
- [celo-rpc](../celo-rpc/SKILL.md) - Celo 区块链交互工具 |
- [viem](../viem/SKILL.md) - TypeScript 编程库（用于 Ethereum 开发）