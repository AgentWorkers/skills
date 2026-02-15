---
name: erc-800claw
description: OpenClaw 提供了用于 ERC-8004 代理身份和声誉管理的入口点。用户可以通过该接口在链上注册代理、查询代理身份信息、以及发送和接收反馈评分。
metadata: {"openclaw":{"emoji":"🪪","requires":{"anyBins":["node","npx","python3","pip"]}}}
---

# ERC-800Claw

这是您了解 ERC-8004 的入口点——一个用于自主代理的链上身份、声誉和验证标准。ERC-8004 是一个 [开放协议](https://8004.org)，它能够在以太坊网络上实现可验证的代理身份和声誉系统。代理可以注册身份（ERC-721 NFT），接收和提供声誉反馈，并通过验证器来验证自己的能力。ERC-800Claw 由 [Primer](https://primer.systems) 开发，提供了与该协议交互的简单 API。

## 何时使用此技能

在以下情况下使用 ERC-800Claw：
- 您需要在链上**注册代理身份**。
- 您需要**根据 ID 或所有者查找代理**。
- 您想要**向其他代理提供反馈/评分**。
- 您需要**检查代理的声誉**。
- 用户询问关于**代理验证**或信任的问题。

## 快速设置

### Node.js
```bash
npm install erc-800claw
```

### Python
```bash
pip install erc-800claw
```

## 如何响应

| 用户输入/询问 | 操作建议 |
|----------------|------------|
| “查找代理 #123” | 运行 `erc-800claw agent 123` 以获取详细信息 |
| “代理 42 存在吗？” | 运行 `erc-800claw exists 42` |
| “0x... 拥有多少个代理？” | 运行 `erc-800claw owner 0x...` |
| “注册我的代理” | 运行 `erc-800claw register --name “名称”`（需要 PRIVATE_KEY 环境变量） |
| “支持哪些网络？” | 运行 `erc-800claw networks` |
| “显示合约地址” | 运行 `erc-800claw contracts` |

## CLI 命令

| 命令 | 描述 |
|---------|-------------|
| `erc-800claw agent <id>` | 根据 ID 获取代理详细信息 |
| `erc-800claw exists <id>` | 检查代理是否存在 |
| `erc-800claw owner <address>` | 获取地址对应的代理数量 |
| `erc-800claw register` | 注册新代理（需要 PRIVATE_KEY） |
| `erc-800claw networks` | 列出支持的网络 |
| `erc-800claw contracts [network]` | 显示指定网络的合约地址 |

### CLI 选项

- `--network, -n <name>` - 使用的网络（mainnet, sepolia）。默认：mainnet |
- `--json, -j` - 以 JSON 格式输出结果

### CLI 示例输出

```bash
$ erc-800claw agent 1
Agent #1 (mainnet)
────────────────────────────────────────
Owner:    0x1234...abcd
URI:      data:application/json;base64,...
Name:     My Agent
About:    An autonomous agent for...
Explorer: https://etherscan.io/nft/0x8004.../1

$ erc-800claw exists 100
Agent 100 exists on mainnet

$ erc-800claw owner 0x1234...
Address 0x1234... owns 3 agent(s) on mainnet

$ PRIVATE_KEY=0x... erc-800claw register --name "My Agent" --network sepolia
Agent Registered on sepolia!
────────────────────────────────────────
Agent ID: 42
Owner:    0x1234...abcd
Tx:       0xabc123...
Explorer: https://sepolia.etherscan.io/nft/0x8004.../42
```

## ERC-8004 的工作原理

ERC-8004 提供了三个链上注册表：
1. **身份注册表**（ERC-721）：每个代理都会获得一个带有元数据 URI 的唯一 NFT 代币。
2. **声誉注册表**：客户向代理提供的结构化反馈分数。
3. **验证注册表**：通过 zkML、TEE、质押者等机制进行独立验证。

操作流程：
1. **注册**：创建一个包含名称/描述元数据的代理身份 NFT。
2. **操作**：在与其他代理交互时使用代理的 ID。
3. **建立声誉**：客户提供反馈，分数会在链上累积。
4. **验证**（可选）：验证器对代理的能力进行认证。

## 在代码中使用

### Node.js / TypeScript
```javascript
const { createClient } = require('erc-800claw');

const client = createClient({ network: 'mainnet' });

// Get agent by ID
const agent = await client.getAgent(1);
console.log(agent);
// {
//   agentId: 1,
//   tokenURI: 'data:application/json;base64,...',
//   owner: '0x...',
//   metadata: { name: 'My Agent', description: '...' },
//   explorerUrl: 'https://etherscan.io/...'
// }

// Check if agent exists
const exists = await client.agentExists(42);

// Get agent count for address
const count = await client.getAgentCount('0x...');

// Register a new agent (no IPFS needed - uses data URI!)
const result = await client.registerAgent(process.env.PRIVATE_KEY, {
  name: 'My Autonomous Agent',
  description: 'Handles customer support',
  services: [{ name: 'support', endpoint: 'https://myagent.com/api' }]
});
console.log(`Registered agent #${result.agentId}`);

// Give feedback to an agent
await client.giveFeedback(process.env.PRIVATE_KEY, agentId, {
  value: 4.5,     // Score out of 5
  decimals: 1,
  tag1: 'support',
  tag2: 'fast'
});
```

### Python
```python
from erc800claw import create_client
import os

client = create_client(network='mainnet')

# Get agent by ID
agent = client.get_agent(1)
print(agent)
# {
#     'agent_id': 1,
#     'token_uri': 'data:application/json;base64,...',
#     'owner': '0x...',
#     'metadata': {'name': 'My Agent', 'description': '...'},
#     'explorer_url': 'https://etherscan.io/...'
# }

# Check if agent exists
exists = client.agent_exists(42)

# Get agent count for address
count = client.get_agent_count('0x...')

# Register a new agent (no IPFS needed - uses data URI!)
result = client.register_agent(
    private_key=os.environ['PRIVATE_KEY'],
    name='My Autonomous Agent',
    description='Handles customer support',
    services=[{'name': 'support', 'endpoint': 'https://myagent.com/api'}]
)
print(f"Registered agent #{result['agent_id']}")

# Give feedback to an agent
client.give_feedback(
    private_key=os.environ['PRIVATE_KEY'],
    agent_id=agent_id,
    value=4.5,        # Score out of 5
    decimals=1,
    tag1='support',
    tag2='fast'
)
```

## 元数据格式

代理的元数据遵循以下标准格式：

```json
{
  "name": "My Agent",
  "description": "What my agent does",
  "image": "https://example.com/avatar.png",
  "services": [
    {
      "name": "api",
      "endpoint": "https://myagent.com/api",
      "description": "Main API endpoint"
    }
  ],
  "supported_trust": ["reputation", "validation"]
}
```

SDK 会自动将这些元数据编码为数据 URI——无需上传到 IPFS。

## 与 xClaw02 的集成

ERC-800Claw 与 **xClaw02**（x402 支付系统）配合使用，以实现付费代理服务：
1. 使用 ERC-800Claw 注册代理身份。
2. 设置 xClaw02 的支付接收功能。
3. 客户验证您的身份后支付服务费用，并对您进行评分。

有关支付设置的详细信息，请参阅 **xClaw02** 技能文档。

## 支持的网络

| 网络 | 链路 ID | 状态 |
|---------|----------|--------|
| 以太坊主网 | 1 | 正在运行 |
| Sepolia 测试网 | 11155111 | 正在运行 |

## 合约地址

### 主网
- 身份注册表：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- 声誉注册表：`0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

### Sepolia
- 身份注册表：`0x8004A818BFB912233c491871b3d84c89A494BD9e`
- 声誉注册表：`0x8004B663056A597Dffe9eCcC1965A193B7388713`

## 环境变量

| 变量 | 格式 | 描述 |
|----------|--------|-------------|
| `PRIVATE_KEY` | `0x` + 64 个十六进制字符 | 钱包私钥（注册/反馈所需） |
| `ERC8004_NETWORK` | `mainnet`, `sepolia` | 默认网络（默认：mainnet） |
| `ERC8004_RPC_URL` | URL | 自定义 RPC 端点 |

## 错误处理

| 错误 | 含义 | 处理方法 |
|-------|---------|------------|
| `代理未找到` | 指定的代理 ID 不存在 | 请确认代理 ID 是否正确 |
| 代理已存在 | 该代理的代币已被注册 | 每个代理 ID 都是唯一的 |
| 无权修改代理信息 | 只有所有者才能更新代理的元数据 |
| 地址无效 | 地址格式不正确（应为 `0x` + 40 个十六进制字符） |

## 安全注意事项

- **切勿在日志、聊天记录或输出中泄露私钥**。
- 使用环境变量来存储钱包凭证。
- 注册代理需要消耗以太坊网络费用，请确保钱包中有足够的 ETH。
- 私钥格式：`0x` 后跟 64 个十六进制字符。

## 链接

- **ERC-8004 协议**：https://8004.org
- **EIP-8004**：https://eips.ethereum.org/EIPS/eip-8004
- **SDK（Node.js）**：https://npmjs.com/package/erc-800claw
- **SDK（Python）**：https://pypi.org/project/erc-800claw
- **GitHub**：https://github.com/primer-systems/ERC-8004
- **Primer Systems**：https://primer.systems