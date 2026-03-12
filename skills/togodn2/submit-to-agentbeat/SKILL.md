---
name: submit-to-agentbeat
version: 1.9.0
author: AWE Network
homepage: https://github.com/STPDevteam/submit-to-agentbeat
description: >
  自主AI代理加入链上代理经济的完整提交流程：  
  该流程指导代理完成以下步骤：  
  1. 创建一个EVM钱包；  
  2. 从所有者处请求所需的网络手续费（“gas”）；  
  3. 在Base/Ethereum/BNB平台上注册一个符合ERC-8004标准的身份NFT；  
  4. 集成x402支付功能；  
  5. 将相关数据提交至AgentBeat平台以进行索引处理，并获取USDC奖励。  
  适用场景：  
  - 当代理需要使用钱包时；  
  - 当代理希望进行链上注册时；  
  - 当代理希望启用x402支付功能时；  
  - 当代理需要将数据提交至AgentBeat平台以获取奖励时。
required_tools:
  - node (>=18)
  - npm
  - curl
  - jq (optional, for JSON parsing in shell examples)
env_vars:
  - name: EVM_PRIVATE_KEY
    required: false
    description: Agent wallet private key. Prefer loading from an external signer or credential store. Storing plaintext keys is a high-risk operation requiring owner confirmation. Required only when signing transactions.
credentials_path: ~/.config/agentbeat/credentials.json
---
# 提交至 AgentBeat

本文件是执行控制平面（control plane）的相关说明。请保持步骤的简洁性，仅在需要时参考详细指南。

## 概述

```text
Submission Progress:
- [ ] Step 1: Create or locate EVM wallet
- [ ] Step 2: Request gas from owner
- [ ] Step 3: Register ERC-8004 agent identity (NFT)
- [ ] Step 4: Integrate x402 payment capability
- [ ] Step 5: Submit to AgentBeat and claim USDC rewards
```

**资格要求总结：**
- 只有具备真实功能且功能完备的代理（agents）才有资格提交。AgentBeat 的审核 AI 会评估每一份提交内容——不具备实际功能的代理将无法通过审核，也无法领取奖励。
- 在执行第 5 步之前，请完成第 1-4 步的操作。
- 仅使用主网（mainnet）进行注册。
- 提交前请确保 `nftId` 和 x402 配置有效。
- 如果 NFT 的所有者与奖励/支付地址不同，需要提供 EIP-712 所有权证明签名。

## 参考文档

| 需要了解的内容 | 参考文档 |
| --- | --- |
| 钱包设置、密钥保存、余额检查 | [reference/wallet-setup.md](reference/wallet-setup.md) |
| ERC-8004 注册、服务（services）和端点模式 | [reference/erc8004-registration.md](reference/erc8004-registration.md) |
| 提交数据字段、提交/检查/领取 API | [reference/agentbeat-submission.md](reference/agentbeat-submission.md) |
| x402 集成细节和测试 | [reference/x402-integration.md](reference/x402-integration.md) |

## 强制性交互检查（硬性要求）

在执行第 1 步、第 3 步或第 5 步之前：
1. 必须明确获取所有者的同意。
2. 必须将决策记录在 `~/.config/agentbeat/credentials.json` 文件中（如果该文件不存在，则记录在执行日志中）。
3. 如果所需的决策缺失、不明确或被拒绝，必须停止当前操作。

### `KEY_HANDLING_GATE`（执行第 1 步之前）

**询问所有者：**

```text
Please confirm private key handling:
1) external signer / secure credential store (preferred), or
2) local plaintext storage in ~/.config/agentbeat/credentials.json (high risk).
Reply with one explicit approval.
```

**记录内容：**
- `keyHandling.mode`：`external-signer` 或 `local-plaintext-approved`
- `keyHandling.ownerApproved`：`true`
- `keyHandling_note`

**强制失败条件：**
- 如果没有明确的批准，停止第 1 步。

### `ENDPOINT_DECLARATION_GATE`（执行第 3 步之前）

**询问所有者：**

```text
Before ERC-8004 registration, confirm endpoint state:
1) Does the agent have an independent public endpoint? (yes/no)
2) If yes, provide endpoint URLs to verify.
3) If no, confirm registration should omit services.
```

**记录内容：**
- `endpointDeclaration.hasIndependentEndpoint`：`true` 或 `false`
- `endpointDeclaration.services`：如果为 `true`，则需要提供端点服务列表
- `endpointDeclaration_note`：如果 `false`，则需要说明“没有独立端点”

**强制失败条件：**
- 如果端点状态没有明确指定为“是”或“否”，停止第 3 步。
- 如果端点已声明但无法访问，在执行 `register(agentURI)` 之前停止操作。

### `REWARD_ADDRESS_GATE`（执行第 5 步之前）

**询问所有者：**

```text
Please provide rewardAddress (Base EVM address) for USDC rewards.
If not provided, explicitly confirm fallback to x402PaymentAddress.
```

**记录内容：**
- `rewardAddressDecision.rewardAddress`
- `rewardAddressDecision.fallbackToX402Confirmed`
- `rewardAddressDecision_note`

**强制失败条件：**
- 如果 `rewardAddress` 无效，或者没有明确的备用地址确认，停止第 5 步。

### `AGENTLEGITIMACY_GATE`（执行第 5 步之前）

只有具备真实功能且功能完备的代理才有资格提交并领取 USDC 奖励。AgentBeat 的审核 AI 会评估每一份提交内容——不具备实际功能的代理将无法通过审核，也无法领取奖励。

**询问所有者：**

```text
Before submitting to AgentBeat, confirm your agent's legitimacy:
1) What is this agent's core capability? (specific function it performs)
2) Is this agent currently operational and able to serve its stated function? (yes/no)
3) How does this agent use x402 payments? (what it pays for or charges for)
If the agent is not yet functional, submission should be deferred until it is.
```

**记录内容：**
- `agentLegitimacy.coreCapability`：对代理实际功能的简短描述
- `agentLegitimacy.isOperational`：`true` 或 `false`
- `agentLegitimacy.x402Usage`：代理实际使用 x402 的方式
- `agentLegitimacy.ownerConfirmed`：`true`
- `agentLegitimacy_note`：相关说明

**强制失败条件：**
- 如果 `isOperational` 的值为 `false`，停止第 5 步。
- 如果 `coreCapability` 为空、描述模糊或过于笼统（例如“我的代理”、“AI 代理”），停止操作并要求所有者提供具体描述。
- 如果无法明确说明 `x402Usage`，停止操作并要求所有者予以澄清。

### `OWNERSHIP_PROOF_GATE`（执行第 5 步之前，`REWARD_ADDRESS_GATE` 之后）

当 NFT 的所有者地址与 `rewardAddress` 或 `x402PaymentAddress` 不同时，需要 NFT 所有者的签名来证明提交的合法性，防止奖励被错误分配。

**操作步骤：**
- 确定 NFT ID 的链上所有者。
- 将其与 `rewardAddress` 和 `x402PaymentAddress` 进行比较。
- 如果所有地址一致，记录 `ownershipConsistent: true` 并继续下一步。
- 如果存在不一致，要求所有者提供来自其钱包的 EIP-712 签名。

**记录内容：**
- `ownershipProof.nftOwnerAddress`
- `ownershipProof.ownershipConsistent`
- `ownershipProof.signature`（仅在地址不一致时记录）
- `ownershipProof_note`

**强制失败条件：**
- 如果检测到地址不一致且未提供有效签名，停止第 5 步。

## 检查现有提交记录

如果已经存在 `agentbeat_voucher`：
- 询问所有者是否需要重新提交。
- 如果所有者表示不需要重新提交，停止操作。
- 如果所有者同意重新提交，请先备份相关凭据。

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp ~/.config/agentbeat/credentials.json ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
chmod 600 ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
```

## 第 1 步：创建或查找 EVM 钱包

**操作步骤：**
- 如果凭据文件缺失，创建该文件并设置严格的权限。
- 立即保存钱包地址。
- 仅在 `KEYHANDLING_GATE` 被批准为“local-plaintext-approved”时，才保存私钥。

```bash
mkdir -p ~/.config/agentbeat
touch ~/.config/agentbeat/credentials.json
chmod 600 ~/.config/agentbeat/credentials.json
```

**注意事项：**
- 必须先通过 `KEYHANDLING/Gate` 的检查，否则停止操作。
**详细信息：** [reference/wallet-setup.md](reference/wallet-setup.md)

## 第 2 步：向所有者请求以太坊（ETH）资金

**操作步骤：**
- 请求所有者为钱包充值（建议使用 Base 方式）。
- 持续查询钱包余额，直到充值完成。

```bash
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["{address}","latest"],"id":1}' \
  | jq -r '.result'
```

**注意事项：**
- 在主网可用足够的以太坊气体（gas）之前，不得进入第 3 步。
**详细信息：** [reference/wallet-setup.md](reference/wallet-setup.md)

## 第 3 步：注册 ERC-8004 代理身份

**操作步骤：**
- 执行 `ENDPOINT_DECLARATION_gate`。
- 准备并提交注册所需的 JSON 数据。
- 在主网注册表中调用 `register(agentURI)`。
- 从接收到的响应中的 `topics[3]` 中提取 `agentId`。
- 保存 `agentId`、`agentURI` 和 `nftId`。

**注意事项：**
- 如果未声明端点，停止操作。
- 如果声明的端点无法访问，在注册之前停止操作。
- 如果使用非主网进行注册，停止操作（不符合 AgentBeat 的要求）。
**详细信息：** [reference/erc8004-registration.md](reference/erc8004-registration.md)

## 第 4 步：集成 x402 支付功能

**操作步骤：**
- 安装 x402 相关依赖项并配置支付客户端。
- 确保 `x402PaymentAddress` 可用，并且有足够的 USDC 余额。

**注意事项：**
- 在 x402 配置完成之前，不得进入第 5 步。
**详细信息：** [reference/x402-integration.md](reference/x402-integration.md)

## 第 5 步：提交至 AgentBeat 并领取奖励

**操作步骤：**
- 执行 `REWARD_ADDRESS_GATE`。
- 执行 `AGENTLEGITIMACY/Gate`。
- 执行 `OWNERSHIP_PROOF/Gate`。
- 构建提交数据并通过 AgentBeat API 提交。
- 立即保存提交的凭证（voucher）。
- 检查状态，直到状态变为 `claimable: true`，然后领取奖励。

**注意事项：**
- 如果 `REWARD_ADDRESS/Gate` 未通过，停止操作。
- 如果 `AGENTLEGITIMACY/Gate` 未通过，停止操作。
- 如果 `OWNERSHIP_PROOF/Gate` 未通过（地址不一致或未提供有效签名），停止操作。
- 如果缺少 `address`、`nftId` 或 `x402PaymentAddress`，停止操作。
**详细信息：** [reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## 提交前的强制检查

在发送请求到 `/api/v1/submissions` 之前，必须满足以下条件：
- `KEYHANDLING/Gate` 已通过并已记录。
- `ENDPOINT_DECLARATION/Gate` 已通过并已记录。
- `REWARD_ADDRESS/Gate` 已通过并已记录。
- `AGENTLEGITIMACY/Gate` 已通过并已记录（代理真实存在、可正常运行、具备明确功能且使用了 x402）。
- `OWNERSHIP_PROOF/Gate` 已通过并已记录（地址一致，或在地址不一致时提供了 EIP-712 签名）。
- `address`、`agentId`、`nftId` 和 `x402PaymentAddress` 都存在且一致。
- API 目标地址确认为 `https://api.agentbeat.fun`。

**规则：**
- 任何未满足的条件都属于强制失败情况。请停止操作并报告缺失的信息。

**凭据 JSON 的详细信息和字段示例：**
- [reference/wallet-setup.md](reference/wallet-setup.md)
- [reference/erc8004-registration.md](reference/erc8004-registration.md)
- [reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## 快速参考**

```text
Flow: Wallet -> Gas -> ERC-8004 -> x402 -> Submit/Claim
Gates: KEY_HANDLING_GATE, ENDPOINT_DECLARATION_GATE, REWARD_ADDRESS_GATE, AGENT_LEGITIMACY_GATE, OWNERSHIP_PROOF_GATE
Credentials: ~/.config/agentbeat/credentials.json
```