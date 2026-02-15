---
name: 8004-skill
description: 在Monad上注册和管理ERC-8004格式的身份NFT。当代理需要为CEO Protocol或其他集成ERC-8004标准的协议创建链上身份时，请使用该功能。
---

# ERC-8004 身份技能

当代理需要注册到 ERC-8004 身份注册表以获取链上身份 NFT 时，请使用此技能。该身份是注册为 CEO 协议（CEOVault）代理的**必需**条件。

参考：[EIP-8004 无信任代理](https://eips.ethereum.org/EIPS/eip-8004)

## 合约地址（Monad 主网）

| 合约 | 地址 |
|----------|---------|
| ERC-8004 身份 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

## 接口概述

身份注册表基于 ERC-721。注册会生成一个 NFT，其令牌 ID 即为代理 ID。

### 写入函数

| 函数 | 功能 |
|----------|---------|
| `register(string agentURI)` | 使用 URI 进行注册；生成 NFT，并返回 `agentId` |
| `register(string agentURI, MetadataEntry[] metadata)` | 使用 URI 和链上元数据进行注册 |
| `register()` | 无 URI 注册（之后可通过 `setAgentURI` 设置） |
| `setAgentURI(uint256 agentId, string newURI)` | 更新代理的 URI |
| `setMetadata(uint256 agentId, string metadataKey, bytes metadataValue)` | 设置链上元数据 |

### 读取函数（查看）

| 函数 | 返回值 | 用途 |
|----------|---------|-----|
| `ownerOf(uint256 tokenId)` | `address` | 查找拥有代理 NFT 的用户 |
| `tokenURI(uint256 tokenId)` | `string` | 获取代理的 URI（与 agentURI 相同） |
| `getAgentWallet(uint256 agentId)` | `address` | 获取与代理关联的钱包 |
| `getMetadata(uint256 agentId, string metadataKey)` | `bytes` | 获取链上元数据 |

### 事件

| 事件 | 用途 |
|-------|-----|
| `Registered(uint256 indexed agentId, string agentURI, address indexed owner)` | 注册时触发 |
| `URIUpdated(uint256 indexed agentId, string newURI, address indexed updatedBy)` | URI 更改时触发 |
| `MetadataSet(uint256 indexed agentId, string indexed metadataKey, string metadataKey, bytes metadataValue)` | 元数据设置时触发 |

## 注册数据模板

`agentURI` 必须指向符合 EIP-8004 注册规范的 JSON 文档。在托管之前，请使用此模板并替换占位符（IPFS 或数据 URI）：

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "AGENT_NAME",
  "description": "AGENT_DESCRIPTION",
  "image": "https://example.com/agent-image.png",
  "services": [
    {
      "name": "A2A",
      "endpoint": "https://YOUR_DOMAIN/.well-known/agent-card.json",
      "version": "0.3.0"
    },
    {
      "name": "MCP",
      "endpoint": "https://YOUR_DOMAIN/mcp",
      "version": "2025-06-18"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [],
  "supportedTrust": [
    "reputation"
  ]
}
```

| 字段 | 替换内容 |
|-------|--------------|
| `AGENT_NAME` | 代理显示名称 |
| `AGENT_DESCRIPTION` | 能力的简要描述 |
| `image` | 代理头像/图片的 URL |
| `YOUR_DOMAIN` | 用于 A2A/MCP 端点的域名（如不适用可省略） |
| `supportedTrust` | 信任模型（例如：`["reputation"]` 适用于 CEO 协议） |

对于仅用于 CEO 协议的简单注册，可以省略 `services` 或将其设置为空；`supportedTrust: ["reputation"]` 是常见的配置。

## 自动化脚本（推荐使用）

Docker 镜像中包含可立即使用的脚本，位于：

`/opt/erc8004-scripts`

脚本源代码位于：

`/root/.openclaw/workspace/skills/8004-skill/scripts`

### 脚本运行所需的环境变量

- `MONAD_RPC_URL`
- `MONADCHAIN_ID=143`（或通过 `--chainId` 传递）
- `AGENT_PRIVATE_KEY`
- `PINATA_JWT`
- `PINATA_GATEWAY`（建议用于验证）

### 脚本命令

```bash
# 1) Register on-chain with empty URI -> returns agentId
node /opt/erc8004-scripts/register.mjs --network monad-mainnet

# 2) Build card JSON with registrations[] embedded
node /opt/erc8004-scripts/build-card.mjs \
  --network monad-mainnet \
  --agentId 42 \
  --template /root/.openclaw/workspace/skills/8004-skill/assets/registration-template.json \
  --name "CEO-1" \
  --description "Autonomous strategist for The CEO Protocol" \
  --out /tmp/agent-42.json

# 3) Upload to Pinata -> returns ipfs://CID
node /opt/erc8004-scripts/upload-pinata.mjs --file /tmp/agent-42.json

# 4) Set token URI on-chain
node /opt/erc8004-scripts/set-agent-uri.mjs \
  --network monad-mainnet \
  --agentId 42 \
  --uri ipfs://CID

# 5) Verify owner, tokenURI, wallet, and registrations[] match
node /opt/erc8004-scripts/verify.mjs --network monad-mainnet --agentId 42
```

### 一次性命令

```bash
node /opt/erc8004-scripts/full-register.mjs \
  --network monad-mainnet \
  --name "CEO-1" \
  --description "Autonomous strategist for The CEO Protocol" \
  --template /root/.openclaw/workspace/skills/8004-skill/assets/registration-template.json \
  --outCard /tmp/agent-card.json \
  --identityFile /root/.openclaw/workspace/AGENT_IDENTITY.md
```

此命令会执行所有 4 个注册步骤（注册 -> 生成卡片 -> 上传 -> 设置 URI），并记录身份信息以供后续 CEO 协议使用。

## 注册流程

1. **先决条件**
   - 拥有包含 MON 的钱包（使用 `viem-local-signer address` 确认签名者）。
   - `agentURI`：指向您的注册 JSON 的 URI（使用上述模板）。可以使用 IPFS（`ipfs://...`）或数据 URI（`data:application/json;base64,...`）。

2. **调用 `register(agentURI)`**
   - 使用 `encodeFunctionData` 对调用数据（calldata）进行编码。
   - 通过 `viem-local-signer send-contract` 发送请求。
   - 解析 `Registered` 事件以获取 `agentId`。

3. **存储 `agentId`
   - 返回的 `agentId`（令牌 ID）是调用 CEO 协议 `registerAgentmetadataURI, ceoAmount, erc8004Id)` 所必需的。
   - 将其保存在身份文件中（见下文）。

## 身份文件模板

注册完成后，需将链上身份信息保存下来，以便代理在 CEO 协议及其他流程中使用。使用此模板：

```markdown
# Agent Identity
- **Address**: `<NOT SET>`
- **Agent ID**: `<NOT SET>`
- **Agent Registry**: `<NOT SET>`
- **Chain ID**: `<NOT SET>`
```

### 如何填写

| 字段 | 来源 | 示例 |
|-------|--------|---------|
| **Address** | `viem-local-signer address`（签名者钱包地址） | `0xB4AF3708DA37a485E84b4F09c146eD0A8B7Df5c4` |
| **Agent ID** | `register(agentURI)` 的返回值 | `42` |
| **Agent Registry** | ERC-8004 身份合约（Monad：`eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`） | `eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| **Chain ID** | Monad 主网 | `143` |

### 使用方法

1. **注册完成后**：将身份文件写入 `workspace/IDENTITY.md` 或 `workspace/AGENT_IDENTITY.md`，以便代理能够访问。
2. **在调用 CEO 协议的 `registerAgent` 之前**：从文件中读取 `Agent ID`（即 `erc8004Id`）。
3. **一致性检查**：确保 `Address` 与 `viem-local-signer address` 以及注册表中的 `ownerOf(agentId)` 一致。

示例填充后的身份文件：

```markdown
# Agent Identity
- **Address**: `0xB4AF3708DA37a485E84b4F09c146eD0A8B7Df5c4`
- **Agent ID**: `42`
- **Agent Registry**: `eip155:143:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Chain ID**: `143`
```

## ABI（最小化版本）

```json
[
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [{ "name": "agentURI", "type": "string" }],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentURI", "type": "string" },
      {
        "name": "metadata",
        "type": "tuple[]",
        "components": [
          { "name": "metadataKey", "type": "string" },
          { "name": "metadataValue", "type": "bytes" }
        ]
      }
    ],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "register",
    "stateMutability": "nonpayable",
    "inputs": [],
    "outputs": [{ "name": "agentId", "type": "uint256" }]
  },
  {
    "type": "function",
    "name": "setAgentURI",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "newURI", "type": "string" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "name": "setMetadata",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "metadataKey", "type": "string" },
      { "name": "metadataValue", "type": "bytes" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "name": "ownerOf",
    "stateMutability": "view",
    "inputs": [{ "name": "tokenId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "address" }]
  },
  {
    "type": "function",
    "name": "tokenURI",
    "stateMutability": "view",
    "inputs": [{ "name": "tokenId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "string" }]
  },
  {
    "type": "function",
    "name": "getAgentWallet",
    "stateMutability": "view",
    "inputs": [{ "name": "agentId", "type": "uint256" }],
    "outputs": [{ "name": "", "type": "address" }]
  },
  {
    "type": "function",
    "name": "getMetadata",
    "stateMutability": "view",
    "inputs": [
      { "name": "agentId", "type": "uint256" },
      { "name": "metadataKey", "type": "string" }
    ],
    "outputs": [{ "name": "", "type": "bytes" }]
  }
]
```

## 编码与发送

使用 `viem` 进行编码，然后通过 `viem-local-signer send-contract` 发送请求。示例（Node/脚本）：

```typescript
import { encodeFunctionData } from "viem";

const ERC8004_IDENTITY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";

const abi = [
  {
    type: "function",
    name: "register",
    stateMutability: "nonpayable",
    inputs: [{ name: "agentURI", type: "string" }],
    outputs: [{ name: "agentId", type: "uint256" }],
  },
] as const;

const agentURI = "ipfs://Qm..."; // or data:application/json;base64,...
const data = encodeFunctionData({
  abi,
  functionName: "register",
  args: [agentURI],
});

// Then run:
// viem-local-signer send-contract --to 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 --data <hex> --value-wei 0 --wait
```

## 代理操作手册

1. 确认签名者：`viem-local-signer address`
2. 确保钱包中有足够的 MON 作为交易费用。
3. 准备 `agentURI`（包含注册 JSON 的 IPFS 或数据 URI）。
4. 使用 `viem` 对 `register(agentURI)` 进行编码。
5. 显示交易摘要并请求用户确认。
6. 运行 `viem-local-signer send-contract --to 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 --data <calldata> --value-wei 0 --wait`
7. 从交易记录/日志中解析 `agentId`（或从 `Registered` 事件中获取）。
8. 使用上述模板填写 `workspace/AGENT_IDENTITY.md` 或 `workspace/IDENTITY.md` 文件，其中包含 `Address`、`Agent ID` 和 `Agent Registry`。

## CEO 协议集成

在调用 `registerAgent` 之前，CEOVault 要求使用 ERC-8004 身份：

```
CEOVault.registerAgent(metadataURI, ceoAmount, erc8004Id)
```

- `erc8004Id` = 从 `ERC8004Identity.register()` 返回的令牌 ID。
- 调用者必须拥有该 NFT（`ownerOf(erc8004Id) == msg.sender`）。

## 区块浏览器

- Monad：`https://monadscan.com/`
- 交易链接：`https://monadscan.com/tx/<hash>`
- 合约地址：`https://monadscan.com/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`