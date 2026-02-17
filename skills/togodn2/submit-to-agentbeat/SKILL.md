---
name: submit-to-agentbeat
version: 1.8.0
author: awe network
homepage: https://github.com/STPDevteam/submit-to-agentbeat
description: >
  自主AI代理加入链上代理经济的完整提交流程：  
  该流程指导代理创建EVM钱包、从所有者处获取Gas费用、在Base/Ethereum/BNB平台上注册ERC-8004格式的身份NFT、集成x402支付功能，并将相关信息提交至AgentBeat平台以完成索引处理并获得USDC奖励。  
  适用场景包括：代理需要使用钱包、希望在链上注册、启用x402支付功能，或需要将数据提交至AgentBeat平台进行处理。
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

本文件是执行控制的中心。请在此处保持步骤的简洁性，仅在需要时才从参考文档中加载详细的指导信息。

## 概述

```text
Submission Progress:
- [ ] Step 1: Create or locate EVM wallet
- [ ] Step 2: Request gas from owner
- [ ] Step 3: Register ERC-8004 agent identity (NFT)
- [ ] Step 4: Integrate x402 payment capability
- [ ] Step 5: Submit to AgentBeat and claim USDC rewards
```

资格要求总结：

- 在执行步骤 5 之前，请完成步骤 1-4。
- 仅使用主网进行注册。
- 在提交之前，请确保 `nftId` 和 x402 设置有效。

## 需要查阅的文档

| 需要的内容 | 参考文档 |
| --- | --- |
| 钱包设置、密钥持久化、余额检查 | [reference/wallet-setup.md](reference/wallet-setup.md) |
| ERC-8004 注册、服务配置、端点模式 | [reference/erc8004-registration.md](reference/erc8004-registration.md) |
| 提交数据字段、提交/检查/领取 API | [reference/agentbeat-submission.md](reference/agentbeat-submission.md) |
| x402 集成细节和测试 | [reference/x402-integration.md](reference/x402-integration.md) |

## 必须执行的交互步骤（硬性要求）

在步骤 1 / 步骤 3 / 步骤 5 之前：

1. 必须明确获得所有者的同意。
2. 必须将决策记录在 `~/.config/agentbeat/credentials.json` 文件中（如果该文件不存在，则记录在执行日志中）。
3. 如果所需的决策缺失、不明确或被拒绝，则必须停止执行。

### `KEYHANDLING/Gate`（步骤 1 之前）

询问所有者：

```text
Please confirm private key handling:
1) external signer / secure credential store (preferred), or
2) local plaintext storage in ~/.config/agentbeat/credentials.json (high risk).
Reply with one explicit approval.
```

记录以下信息：

- `keyHandling.mode`：`external-signer` 或 `local-plaintext-approved`
- `keyHandling.ownerApproved`：`true`
- `keyHandling_note`

如果未获得明确批准，则强制停止步骤 1。

### `ENDPOINT_DECLARATION/Gate`（步骤 3 之前）

询问所有者：

```text
Before ERC-8004 registration, confirm endpoint state:
1) Does the agent have an independent public endpoint? (yes/no)
2) If yes, provide endpoint URLs to verify.
3) If no, confirm registration should omit services.
```

记录以下信息：

- `endpointDeclaration.hasIndependentEndpoint`：`true` 或 `false`
- `endpointDeclaration.services`：如果为 `true`，则记录一个数组
- `endpointDeclaration_note`：如果为 `false`，则需要记录 “无独立端点”

如果端点的状态没有明确指定为 “是” 或 “否”，则强制停止步骤 3。
- 如果端点已声明但无法访问，则在调用 `register(agentURI)` 之前停止执行。

### `REWARD_ADDRESS/Gate`（步骤 5 之前）

询问所有者：

```text
Please provide rewardAddress (Base EVM address) for USDC rewards.
If not provided, explicitly confirm fallback to x402PaymentAddress.
```

记录以下信息：

- `rewardAddressDecision.rewardAddress`
- `rewardAddressDecision.fallbackToX402Confirmed`
- `rewardAddressDecision_note`

如果 `rewardAddress` 无效或没有明确的回退确认，则强制停止步骤 5。

## 预检现有提交记录

如果 `agentbeat_voucher` 已经存在：

- 询问所有者是否需要重新提交。
- 如果所有者回答 “否”，则停止执行。
- 如果所有者回答 “是”，则先备份相关凭据。

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp ~/.config/agentbeat/credentials.json ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
chmod 600 ~/.config/agentbeat/credentials.backup.${TIMESTAMP}.json
```

## 步骤 1：创建或查找 EVM 钱包

操作：

- 如果凭据文件缺失，请创建该文件并设置严格的权限。
- 立即保存钱包地址。
- 仅当 `KEYHANDLING/Gate` 被批准为 “local-plaintext-approved” 时，才保存私钥。

```bash
mkdir -p ~/.config/agentbeat
touch ~/.config/agentbeat/credentials.json
chmod 600 ~/.config/agentbeat/credentials.json
```

**注意**：
- 必须先通过 `KEYHANDLING/Gate`，否则停止执行。
详情：[reference/wallet-setup.md](reference/wallet-setup.md)

## 步骤 2：向所有者请求以太坊Gas

操作：

- 请所有者为钱包充值（建议使用基础金额）。
- 持续查询以太坊余额，直到充值完成。

```bash
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["{address}","latest"],"id":1}' \
  | jq -r '.result'
```

**注意**：
- 在主网Gas可用之前，不得进入步骤 3。
详情：[reference/wallet-setup.md](reference/wallet-setup.md)

## 步骤 3：注册 ERC-8004 代理身份

操作：

- 执行 `ENDPOINT_DECLARATION/Gate`。
- 准备并提交注册所需的 JSON 数据。
- 在主网注册表上调用 `register(agentURI)`。
- 从接收到的响应中的 `topics[3]` 字段解析 `agentId`。
- 保存 `agentId`、`agentURI` 和 `nftId`。

**注意**：
- 如果未声明端点，则停止执行。
- 如果声明的端点无法访问，则在注册之前停止执行。
- 如果使用非主网进行注册，则无法参与 AgentBeat 活动。
详情：[reference/erc8004-registration.md](reference/erc8004-registration.md)

## 步骤 4：集成 x402 支付功能

操作：

- 安装 x402 相关依赖项并配置支付客户端。
- 确保 `x402PaymentAddress` 可用且 USDC 账户中有足够的余额。

```bash
npm install @x402/axios @x402/evm @x402/core
```

**注意**：
- 在 x402 设置完成之前，不得进入步骤 5。
详情：[reference/x402-integration.md](reference/x402-integration.md)

## 步骤 5：提交至 AgentBeat 并领取奖励

操作：

- 执行 `REWARD_ADDRESS/Gate`。
- 构建提交数据并通过 AgentBeat API 提交。
- 立即保存生成的凭证。
- 检查状态，直到状态变为 “claimable: true”，然后领取奖励。

**注意**：
- 如果 `REWARD_ADDRESS/Gate` 未通过，则停止执行。
- 如果缺少 `address`、`nftId` 或 `x402PaymentAddress`，则停止执行。
详情：[reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## 提交前的硬性检查

在发送请求到 `/api/v1/submissions` 之前，必须满足以下条件：

- `KEYHANDLING/Gate` 已通过并记录在日志中。
- `ENDPOINT_DECLARATION/Gate` 已通过并记录在日志中。
- `REWARD_ADDRESS/Gate` 已通过并记录在日志中。
- `address`、`agentId`、`nftId` 和 `x402PaymentAddress` 均存在且信息一致。
- API 目标地址确认为 `https://api.agentbeat.fun`。

**规则**：
- 任何未满足的条件都视为硬性失败。请停止执行并报告缺失的信息。

**凭据 JSON 的详细信息和字段示例**：
- [reference/wallet-setup.md](reference/wallet-setup.md)
- [reference/erc8004-registration.md](reference/erc8004-registration.md)
- [reference/agentbeat-submission.md](reference/agentbeat-submission.md)

## 快速参考

```text
Flow: Wallet -> Gas -> ERC-8004 -> x402 -> Submit/Claim
Gates: KEY_HANDLING_GATE, ENDPOINT_DECLARATION_GATE, REWARD_ADDRESS_GATE
Credentials: ~/.config/agentbeat/credentials.json
```