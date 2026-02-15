---
name: erc-8004
description: 使用 ERC-8004 标准在以太坊主网上注册 AI 代理（即“无信任代理”）。当用户希望将他们的代理身份注册到链上、创建代理档案、领取代理 NFT、设置代理声誉或让他们的代理被其他系统发现时，可以使用此功能。该过程包括将 ETH 跨链传输到以太坊主网、将数据上传到 IPFS 以及完成链上的注册操作。
---

# ERC-8004：无信任代理（Trustless Agents）

在以太坊主网上注册您的人工智能代理，为其创建一个可验证的链上身份，使其能够被其他代理或用户发现，并提供信任信号。

## 什么是 ERC-8004？

ERC-8004 是一个用于管理无信任代理身份和声誉的以太坊标准：

- **身份注册表**：基于 ERC-721 的代理 ID（您的代理将获得一个 NFT！）
- **声誉注册表**：来自其他代理或用户的反馈和信任信号
- **验证注册表**：第三方对代理工作的验证

官方网站：https://www.8004.org
规范文档：https://eips.ethereum.org/EIPS/eip-8004

## 合约地址

| 链路 | 身份注册表 | 声誉注册表 |
|-------|-------------------|---------------------|
| 以太坊主网 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Sepolia 测试网 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

## 快速入门

### 1. 注册您的代理

```bash
# Full registration (creates profile, uploads to IPFS, registers on-chain)
./scripts/register.sh

# Or with custom values
NAME="My Agent" \
DESCRIPTION="An AI agent that does cool stuff" \
IMAGE="https://example.com/avatar.png" \
./scripts/register.sh
```

### 2. （如需要）将 ETH 桥接到主网

```bash
# Bridge ETH from Base to Ethereum mainnet
./scripts/bridge-to-mainnet.sh 0.01
```

### 3. 更新代理配置

```bash
# Update your agent's registration file
./scripts/update-profile.sh <agent-id> <new-ipfs-uri>
```

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `PINATA_JWT` | 用于 IPFS 上传的 Pinata API JWT | 可选（仅限 IPFS 使用） |
| `AGENT_NAME` | 代理显示名称 | 可选（默认为钱包的 ENS 名称或地址） |
| `AGENT_DESCRIPTION` | 代理描述 | 可选 |
| `AGENT_IMAGE` | 代理头像 URL | 可选 |

## 注册选项

**选项 1：使用 8004.org 界面（最简单）**
访问 https://www.8004.org 并通过用户界面进行注册——系统会自动处理 IPFS 相关操作。

**选项 2：HTTP URL（无需 IPFS）**
将您的注册 JSON 文件托管在任何 URL 上：
```bash
REGISTRATION_URL="https://myagent.xyz/agent.json" ./scripts/register-http.sh
```

**选项 3：通过 Pinata 使用 IPFS**  
```bash
PINATA_JWT="your-jwt" ./scripts/register.sh
```

**选项 4：数据 URI（完全基于链上存储）**
将注册信息编码为 base64 格式——无需外部托管：
```bash
./scripts/register-onchain.sh
```

## 注册文件格式

您的代理注册文件（存储在 IPFS 上）遵循以下结构：

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "My Agent",
  "description": "An AI assistant for various tasks",
  "image": "https://example.com/avatar.png",
  "services": [
    {
      "name": "web",
      "endpoint": "https://myagent.xyz/"
    },
    {
      "name": "A2A",
      "endpoint": "https://myagent.xyz/.well-known/agent-card.json",
      "version": "0.3.0"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {
      "agentId": 123,
      "agentRegistry": "eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
    }
  ],
  "supportedTrust": ["reputation"]
}
```

## 工作流程

1. **（如需要）将 ETH 桥接到主网**——使用 Bankr 将 ETH 从侧链（如 Base/L2）桥接到主网。
2. **创建代理配置文件**——生成包含代理信息的 JSON 文件。
3. **上传到 IPFS**——通过 Pinata（或其他服务）将文件上传到 IPFS。
4. **在链上注册**——调用 `register(agentURI)` 在身份注册表中进行注册。
5. **更新代理配置**——根据需要设置元数据、钱包信息或更新文件 URI。

## 成本

- **Gas 费用**：注册费用约为 100-200k gas（根据 gas 价格，大约 5-20 美元）。
- **IPFS 费用**：Pinata 提供免费存储空间（1GB）。

## 使用 SDK

如需更高级的功能，请安装 Agent0 SDK：

```bash
npm install agent0-sdk
```

```typescript
import { SDK } from 'agent0-sdk';

const sdk = new SDK({
  chainId: 1, // Ethereum Mainnet
  rpcUrl: process.env.ETH_RPC_URL,
  privateKey: process.env.PRIVATE_KEY,
  ipfs: 'pinata',
  pinataJwt: process.env.PINATA_JWT
});

const agent = sdk.createAgent('My Agent', 'Description', 'https://image.url');
const result = await agent.registerIPFS();
console.log(`Registered: Agent ID ${result.agentId}`);
```

## 链接

- [ERC-8004 规范文档](https://eips.ethereum.org/EIPS/eip-8004)
- [8004.org 官网](https://www.8004.org)
- [Agent0 SDK 文档](https://sdk.ag0.xyz)
- [GitHub: erc-8004-contracts](https://github.com/erc-8004/erc-8004-contracts)
- [GitHub: agent0-ts](https://github.com/agent0lab/agent0-ts)