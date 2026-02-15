---
name: base-8004
description: 在 Base 平台上，使用 ERC-8004 标准将您的人工智能代理进行链上注册。创建一个钱包，为其充值资金，然后在身份注册系统中完成注册，以获得永久且可验证的身份信息及声誉记录。
metadata: { "openclaw": { "homepage": "https://8004.org" } }
---

# Base-8004 注册流程

本指南将指导您如何设置自己的钱包、为其充值，并在 Base 主网上使用 ERC-8004 协议进行在线注册。完成注册后，您的智能体将拥有一个永久的、可验证的在线身份，并能够积累声誉。

## 1. 什么是 ERC-8004？

ERC-8004 是一种用于智能体的在线身份和声誉管理协议：

- **身份**：每个注册的智能体都会在 Base 主网上获得一个 ERC-721 NFT，这代表了您的永久、可验证的在线身份。
- **声誉记录**：一个独立的合约用于跟踪智能体的声誉分数。用户的反馈（点赞、点踩、质量评估）会累积到 `totalScore` 和 `feedbackCount` 中。
- **可验证的元数据**：您的注册信息包含一个 JSON 文档（`agentURI`），其中包含您的名称、描述和能力。任何人都可以在线查看这些信息。

**重要性：**
- **永久的身份**：您的智能体 ID 在不同平台上都是唯一的，不会绑定到任何单一服务上。
- **公开的声誉**：您的表现记录会在线上公开，并且任何人都可以查看。

## 2. 设置钱包

您需要在 Base 主网上使用一个兼容以太坊的钱包。**如果您已经在 Base 上拥有 ETH 钱包，请跳转到第 4 节**。以下步骤仅适用于首次设置钱包的情况。

### 步骤 1：安装 viem

```bash
npm install viem
```

### 步骤 2：生成私钥

```typescript
import { generatePrivateKey } from "viem/accounts";

const privateKey = generatePrivateKey();
console.log("Private key:", privateKey);
```

请立即保存这个私钥，因为您将无法再次恢复它。

### 步骤 3：生成钱包地址

```typescript
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(privateKey);
console.log("Address:", account.address);
```

### 步骤 4：安全存储私钥

将私钥添加到您的 `.env` 文件中：

```
AGENT_PRIVATE_KEY=0x...your_private_key_here...
```

如果 `.env` 文件还不存在，请将其添加到 `.gitignore` 文件中：

```
echo ".env" >> .gitignore
```

### 步骤 5：安全注意事项
- **切勿在日志、提交或 API 调用中泄露**私钥。
- **切勿丢失**私钥——一旦丢失，您的钱包和在线身份将永远丢失。
- **在覆盖旧私钥之前，请务必备份**。

### 步骤 6：配置适用于 Base 主网的钱包客户端

```typescript
import { createWalletClient, createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.AGENT_PRIVATE_KEY as `0x${string}`);
const publicClient = createPublicClient({ chain: base, transport: http() });
const walletClient = createWalletClient({ account, chain: base, transport: http() });
```

## 3. 为钱包充值

您的钱包需要 ETH 来支付网络手续费（gas）。

- **在 Base 上获取 ETH**：可以使用 Coinbase（直接提取到 Base），或者通过 [Relay](https://relay.link/bridge) 从其他链转移 ETH，或者从其他 Base 钱包接收 ETH。
- **手续费很低**：Base L2 的手续费非常低，注册费用大约为 0.02 美元。1 美元的 ETH 就足够了。
- **在继续之前，请先核实钱包余额**：

```typescript
const balance = await publicClient.getBalance({ address: account.address });
console.log("Balance:", Number(balance) / 1e18, "ETH");

if (balance < 500000000000000n) {
  console.error("Need at least 0.0005 ETH for registration gas");
  process.exit(1);
}
```

## 4. 在线注册

在 ERC-8004 身份注册表中注册您的智能体。此操作会生成一个代表您永久在线身份的 NFT。

### 步骤 1：创建注册 JSON 文件

在 JSON 文件中包含 `services` 数组，以声明您的智能体具备的功能，以便其他智能体和服务能够识别您的服务类型：

```typescript
const registration = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: "Your Agent Name",
  description: "What your agent does",
  image: "https://example.com/your-agent-avatar.png",
  active: true,
  x402Support: false,
  services: [
    { name: "A2A", endpoint: "https://your-agent.example.com/a2a", version: "0.3.0" },
    { name: "MCP", endpoint: "https://your-agent.example.com/mcp", version: "0.1.0" },
  ],
};
```

- **`image`**：智能体头像或标志的 URL，会在浏览器和目录中显示。请使用 256x256 或更大尺寸的图片。如果没有，请将其设置为 `""`，之后可以通过 `setAgentURI` 方法添加。
- **`services`**：声明您的智能体在线上支持的功能。每个条目包含 `name`（服务标识）、`endpoint` 以及可选的 `version`。常见的服务类型包括 `A2A`（智能体之间的通信协议）和 `MCP`（模型上下文协议）。

### 步骤 2：将 JSON 数据编码为数据 URI

```typescript
const uri =
  "data:application/json;base64," + Buffer.from(JSON.stringify(registration)).toString("base64");
```

### 步骤 3：调用 Identity Registry 的 `register()` 方法

```typescript
import { encodeFunctionData } from "viem";

const IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const registerAbi = [
  {
    inputs: [{ name: "agentURI", type: "string" }],
    name: "register",
    outputs: [{ name: "agentId", type: "uint256" }],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const;

// Estimate gas first
const gas = await publicClient.estimateGas({
  account: account.address,
  to: IDENTITY_REGISTRY,
  data: encodeFunctionData({
    abi: registerAbi,
    functionName: "register",
    args: [uri],
  }),
});

console.log("Estimated gas:", gas.toString());

// Send the transaction
const hash = await walletClient.writeContract({
  address: IDENTITY_REGISTRY,
  abi: registerAbi,
  functionName: "register",
  args: [uri],
});

console.log("TX hash:", hash);
```

### 步骤 4：解析 Transfer 事件以获取您的代币 ID

```typescript
const receipt = await publicClient.waitForTransactionReceipt({ hash });

// ERC-721 Transfer event topic
const transferTopic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";
const transferLog = receipt.logs.find(
  (log) =>
    log.topics[0] === transferTopic && log.address.toLowerCase() === IDENTITY_REGISTRY.toLowerCase()
);

const erc8004AgentId = transferLog?.topics[3]
  ? BigInt(transferLog.topics[3]).toString()
  : undefined;

console.log("Your ERC-8004 Agent ID:", erc8004AgentId);
```

### 步骤 5：保存您的智能体 ID

保存 `erc8004AgentId`——这是您的永久在线身份。将其添加到您的 `.env` 文件中：

```
ERC8004_AGENT_ID=42
```

您可以在 BaseScan 上验证您的注册信息：
`https://basescan.org/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/{your_agent_id}`

## 5. 更新注册信息

初次注册后，您可以通过调用 Identity Registry 的 `setAgentURI` 方法来更新您的智能体信息（名称、描述、支持的功能）。这样无需重新注册即可添加新功能或修改元数据。

```typescript
const setAgentUriAbi = [
  {
    inputs: [
      { name: "agentId", type: "uint256" },
      { name: "agentURI", type: "string" },
    ],
    name: "setAgentURI",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const;

// Build updated registration JSON
const updatedRegistration = {
  type: "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  name: "Your Agent Name",
  description: "Updated description",
  image: "https://example.com/your-agent-avatar.png",
  active: true,
  x402Support: false,
  services: [
    { name: "A2A", endpoint: "https://your-agent.example.com/a2a", version: "0.3.0" },
    { name: "MCP", endpoint: "https://your-agent.example.com/mcp", version: "0.1.0" },
  ],
};

const newUri =
  "data:application/json;base64," +
  Buffer.from(JSON.stringify(updatedRegistration)).toString("base64");

const hash = await walletClient.writeContract({
  address: IDENTITY_REGISTRY,
  abi: setAgentUriAbi,
  functionName: "setAgentURI",
  args: [BigInt(process.env.ERC8004_AGENT_ID!), newUri],
});

console.log("URI updated, TX:", hash);
```

只有代币的所有者才能调用 `setAgentURI` 方法。

## 6. 合同地址及验证信息

| 合同            | 地址                                      | 链路        |
| ------------------- | -------------------------------------------- | ------------ |
| Identity Registry   | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | Base 主网 |
| Reputation Registry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | Base 主网 |

**在 BaseScan 上验证：**
- Identity Registry: [basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- Reputation Registry: [basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63)

**在线查询示例（仅限读取，无需支付手续费）：**

```typescript
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

const client = createPublicClient({ chain: base, transport: http() });

// Check who owns a token
const owner = await client.readContract({
  address: "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
  abi: [
    {
      inputs: [{ name: "agentId", type: "uint256" }],
      name: "ownerOf",
      outputs: [{ name: "", type: "address" }],
      stateMutability: "view",
      type: "function",
    },
  ],
  functionName: "ownerOf",
  args: [42n],
});

// Read an agent's metadata URI
const uri = await client.readContract({
  address: "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
  abi: [
    {
      inputs: [{ name: "tokenId", type: "uint256" }],
      name: "tokenURI",
      outputs: [{ name: "", type: "string" }],
      stateMutability: "view",
      type: "function",
    },
  ],
  functionName: "tokenURI",
  args: [42n],
});
```

## 7. 参考资源

- [8004.org](https://8004.org) — ERC-8004 协议官方文档
- [Base](https://base.org) — Base L2 链路
- [BaseScan](https://basescan.org) — Base 链路浏览器
- [viem](https://viem.sh) — 用于以太坊的 TypeScript 库

## 总结

1. **设置钱包**：生成私钥并安全存储。
2. **为钱包充值**：在 Base 上获取 ETH（通过 Coinbase、桥接服务或转账）。
3. **在线注册**：调用 Identity Registry 的 `register(agentURI)` 方法并传入您的服务信息。解析 Transfer 事件以获取您的代币 ID。
4. **更新注册信息**：调用 `setAgentURI` 方法来修改元数据或添加新服务。