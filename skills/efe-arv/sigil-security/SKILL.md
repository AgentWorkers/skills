---
name: sigil-security
description: Secure AI agent wallets via Sigil Protocol. Use when you need to deploy a smart wallet, send transactions through the Guardian, manage spending policies, create session keys, freeze/unfreeze accounts, manage recovery, or check wallet status. Covers all chains: Avalanche, Base, Arbitrum, Polygon, 0G.
homepage: https://sigil.codes
source: https://github.com/Arven-Digital/sigil-public
metadata:
  openclaw:
    primaryEnv: SIGIL_API_KEY
    emoji: "🛡️"
    requires:
      env:
        - SIGIL_API_KEY
        - SIGIL_ACCOUNT_ADDRESS
---

# Sigil协议 — 代理钱包技能

为AI代理提供安全的智能钱包，支持5个EVM区块链。三层安全机制（Guardian）会在交易被共同签署前对其进行评估。

**API基础地址：** `https://api.sigil_codes/v1`
**控制面板：** `https://sigil_codes`
**支持的区块链：** Avalanche（43114）、Base（8453）、Arbitrum（42161）、Polygon（137）、0G Mainnet（16661）

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SIGIL_API_KEY` | ✅ 是 | 来自Sigil控制面板的代理API密钥（以`sgil_`开头）。可在[https://sigil_codes/dashboard/agent-access]生成 |
| `SIGIL_ACCOUNT_ADDRESS` | ✅ 是 | 你部署的Sigil智能账户地址。可在[https://sigil_codes/onboarding]进行部署 |
| `SIGIL_API_URL` | 否 | API基础URL（默认：`https://api.sigil_codes`） |
| `SIGILCHAIN_ID` | 否 | 区块链ID：43114=Avalanche, 8453=Base, 42161=Arbitrum, 137=Polygon, 16661=0G（默认：`43114`） |

## ⚠️ 工作原理（请先阅读此部分）

Sigil有三个地址，请勿混淆：
- **所有者钱包**：你的MetaMask/EOA，用于控制设置（仅限人类操作）
- **Sigil智能账户**：链上的资金保管库，负责执行交易
- **代理密钥**：用于API认证的凭证，**不是钱包**

> **💰 请将资金存入Sigil账户，而非代理密钥。**
> 代理通过API密钥进行认证 → 调用 `/v1/execute` → 服务器构建、签署并提交交易。Sigil账户使用自己的资金执行交易。

[完整设置指南 →](references/agent-setup-guide.md)

## 安装（OpenClaw / ClawdBot）

将此技能添加到代理配置中。`env`字段必须是一个扁平的键值对象，**不能是数组**。

✅ **正确格式**（在`openclaw.json`的`skills`部分）：
```json
{
  "name": "sigil-security",
  "env": {
    "SIGIL_API_KEY": "sgil_your_key_here",
    "SIGIL_ACCOUNT_ADDRESS": "0xYourSigilAccount"
  }
}
```

❌ **错误格式**（会导致网关崩溃）：
```json
{
  "name": "sigil-security",
  "env": [
    { "name": "SIGIL_API_KEY", "value": "sgil_..." }
  ]
}
```

### 步骤：
1. 在[https://sigil_codes/onboarding]部署Sigil账户
2. 在[https://sigil_codes/dashboard/agent-access]生成API密钥
3. 将上述技能配置添加到`openclaw.json`中的代理配置
4. 重启网关

## 安全性与密钥权限

**`SIGIL_API_KEY`不是所有者密钥**。它是用于代理向Guardian API进行认证的密钥。权限模型如下：

| 操作 | 代理密钥 | 所有者（SIWE） | 会话密钥 |
|--------|-----------|--------------|-------------|
| 执行交易（签名 + 提交） | ✅ | ✅ | ❌ |
| 评估交易 | ✅ | ✅ | ✅ |
| 检查钱包状态 | ✅ | ✅ | ✅ |
| 查看审计日志 | ✅ | ✅ | ❌ |
| 更新策略 | ❌ | ✅ | ❌ |
| 冻结账户 | ❌ | ✅ | ❌ |
| 旋转密钥 | ❌ | ✅ | ❌ |
| 紧急提款 | ❌ | ✅（仅限链上操作） | ❌ |
| 添加/删除恢复监护人 | ❌ | ✅ | ❌ |

**密钥原则：**
- 代理密钥**不能**冻结、提款、旋转密钥或更改策略——这些操作仅由所有者执行（需要所有者钱包的签名）
- 代理密钥**可以**提交交易以供Guardian评估并获得共同签署
- **会话密钥**（推荐使用）具有更严格的限制：限时、消费限额、目标白名单和自动过期
- Guardian**仅负责验证，不执行任何操作**——不能移动资金或单独行动
- 紧急提款是**仅限所有者的链上功能**——任何API密钥都无法触发

**最佳实践：**日常代理操作使用会话密钥。`SIGIL_API_KEY仅用于认证——无论使用哪种密钥，Guardian都会执行所有限制。

## 认证

有两种方法：

### API密钥（更简单）
所有者通过控制面板的代理访问页面生成密钥。

```bash
curl -X POST https://api.sigil.codes/v1/agent/auth/api-key \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "sgil_your_key_here"}'
# Returns: { "token": "eyJ..." }
```

### 委托签名（更安全）
所有者签署EIP-712消息，将权限委托给代理。

```bash
# Get signing info
GET /v1/agent/delegation-info

# Authenticate
POST /v1/agent/auth/delegation
{
  "ownerAddress": "0x...",
  "agentIdentifier": "my-agent",
  "signature": "0x...",
  "expiresAt": 1739404800,
  "nonce": "unique-string"
}
```

所有请求：`Authorization: Bearer <token>`（有效期4小时，需使用相同凭据重新认证）

## 首次设置

### 1. 运行设置向导
```
GET /v1/agent/setup/wizard
```
向导会提供指导性问题、用例配置文件和安全提示。**部署前务必咨询所有者**。

### 2. 通过控制面板进行部署
指导所有者访问[https://sigil.codes/onboarding]：
1. 连接钱包并使用SIWE登录
2. 选择策略模板（保守型/中等型/激进型/DeFi代理/NFT代理）
3. 选择区块链
4. 生成代理密钥对
5. 部署智能账户

### 3. （如果通过编程方式部署）进行注册
```bash
POST /v1/agent/wallets/register
{
  "address": "0xNewWallet",
  "chainId": 43114,
  "agentKey": "0xKey",
  "factoryTx": "0xHash"
}
```

## 日常操作

### 检查状态
```
GET /v1/agent/wallets/0xYourWallet
```
返回：余额、策略、会话密钥、每日消费额、监护人状态、冻结状态。

### 执行交易（推荐）
非托管模式：代理在本地签名，服务器共同签署并提交。

```bash
# 1. Build UserOp and sign with your agent private key (locally)
# 2. Submit pre-signed UserOp
POST /v1/execute
{
  "userOp": {
    "sender": "0xYourSigilAccount",
    "nonce": "0x0",
    "callData": "0x...",
    "callGasLimit": "500000",
    "verificationGasLimit": "200000",
    "preVerificationGas": "50000",
    "maxFeePerGas": "25000000000",
    "maxPriorityFeePerGas": "1500000000",
    "signature": "0xYourAgentSignature..."
  },
  "chainId": 137
}
```

返回：`{"txHash": "0x...", "verdict": "APPROVED", "riskScore": 12, "evaluationMs": 1450}`

**Sigil从不存储你的私钥**。代理在本地签名 → Guardian进行评估并共同签署 → 然后提交到链上。即使我们的服务器被攻击，攻击者也无法获取任何私钥。

如果交易被拒绝：`{"verdict": "REJECTED", "rejectionReason": "...", "guidance": "..."}`

### 评估交易（高级功能）
适用于自行管理密钥并希望自行处理提交的代理。每笔交易都会经过Guardian的三层审核流程：
1. **第1层：确定性检查** — 遵守策略限制、白名单检查、速度检查
2. **第2层：模拟测试** — 进行模拟测试，检查是否会出现回滚或意外状态变化
3. **第3层：AI风险评估** — 人工智能对交易进行评分（0-100分，阈值70分）

```bash
POST /v1/evaluate
{
  "userOp": {
    "sender": "0xYourAccount",
    "nonce": "0x0",
    "callData": "0x...",
    "callGasLimit": "200000",
    "verificationGasLimit": "200000",
    "preVerificationGas": "50000",
    "maxFeePerGas": "25000000000",
    "maxPriorityFeePerGas": "1500000000",
    "signature": "0x"
  }
}
```

结果：`APPROVE`（带有Guardian的签名）、`REJECT`（附带解释原因及修复建议）、`ESCALATE`（需要所有者介入）

### 策略管理
```bash
# Update limits
PUT /v1/agent/wallets/:addr/policy
{ "maxTxValue": "200000000000000000", "dailyLimit": "2000000000000000000" }

# Whitelist targets
POST /v1/agent/wallets/:addr/targets
{ "targets": ["0xContract"], "allowed": true }

# Whitelist functions
POST /v1/agent/wallets/:addr/functions
{ "selectors": ["0xa9059cbb"], "allowed": true }

# Token policies (cap approvals!)
POST /v1/agent/wallets/:addr/token-policies
{ "token": "0xUSDC", "maxApproval": "1000000000", "dailyTransferLimit": "5000000000" }
```

### 会话密钥
限时且权限受限的密钥，会自动过期。建议优先使用会话密钥而非完整的代理密钥。

### 紧急控制
```bash
# Freeze everything
POST /v1/accounts/:addr/freeze
{ "reason": "Suspicious activity detected" }

# Unfreeze
POST /v1/accounts/:addr/unfreeze

# Rotate agent key
POST /v1/accounts/:addr/rotate-key
{ "newAgentKey": "0xNewKey" }

# Emergency withdraw (owner-only, direct contract call)
# Use the SigilAccount ABI: emergencyWithdraw(address to)
```

### 社交恢复机制
```bash
# Get recovery config
GET /v1/accounts/:addr/recovery

# Add guardian
POST /v1/accounts/:addr/recovery/guardians
{ "guardian": "0xTrustedAddress" }

# Set threshold (N-of-M)
PUT /v1/accounts/:addr/recovery/threshold
{ "threshold": 2 }
```

### 审计日志
```
GET /v1/audit?account=0xYourWallet&limit=50
```

## 合同地址

| 区块链 | 区块链ID | 工厂地址 |
|-------|----------|---------|
| Avalanche C-Chain | 43114 | `0x2f4dd6db7affcf1f34c4d70998983528d834b8f6` |
| Base | 8453 | `0x45b20a5F37b9740401a29BD70D636a77B18a510D` |
| Arbitrum One | 42161 | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| Polygon | 137 | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| 0G Mainnet | 16661 | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| Avalanche Fuji（测试网） | 43113 | `0x86E85dE25473b432dabf1B9E8e8CE5145059b85b` |
| Guardian：`0xD06fBe90c06703C4b705571113740AfB104e3C67` |
**入口点（v0.7）：`0x0000000071727De22E5E9d8BAf0edAc6f37da032`

## MCP服务器

对于兼容MCP的代理，设置说明请参考[references/mcp-setup.md]。MCP设置需要**人工操作**——请勿自行执行设置命令。

## 策略模板（针对不同区块链）

模板会根据原生代币的价值调整限制：

| 模板 | AVAX限制 | ETH限制 | POL限制 | A0GI限制 |
|----------|-------------|------------|------------|-------------|
| **保守型** | 0.1/0.5/0.05 | 0.0003/0.0015/0.00015 | 1/5/0.5 | 1/5/0.5 |
| **中等型** | 0.5/2/0.2 | 0.0015/0.006/0.0006 | 5/20/2 | 5/20/2 |
| **激进型** | 2/10/1 | 0.006/0.03/0.003 | 20/100/10 | 20/100/10 |
| **DeFi代理** | 0.3/5/0.1 | 0.0009/0.015/0.0003 | 3/50/1 | 3/50/1 |
| **NFT代理** | 1/3/0.5 | 0.003/0.009/0.0015 | 10/30/5 | 10/30/5 |

（单位：最大交易次数/每日/监护人阈值）

## 最佳实践：
1. **从保守型开始** — 先设置较低的限制，根据实际情况逐步增加
2. **明确设置白名单** — 使用目标白名单和功能白名单
3. **使用会话密钥** — 会话密钥会自动过期，比完整的代理密钥更安全
4. **设置代币审批限额** — 为代币策略设置`maxApproval`。无限审批权限是DeFi攻击的主要途径
5. **如果交易被拒绝，请查看`guidance`** — Guardian会解释拒绝原因及修复方法
6. **操作前请检查状态** — 使用`GET /v1/agent/wallets/:addr`查询
7. **监控保护机制** — 如果保护机制被触发，所有共同签署操作将停止，直到所有者重置

## 高级功能

有关详细的API参考、共同签署层级、恢复系统和DeFi白名单配置，请参阅[references/api-reference.md]。