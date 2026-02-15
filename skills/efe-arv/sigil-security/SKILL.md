---
name: sigil-security
description: 通过 Sigil 协议保护 AI 代理钱包的安全。当您需要部署智能钱包、通过 Guardian 发送交易、管理支出策略、生成会话密钥、冻结/解冻账户、管理账户恢复流程或检查钱包状态时，请使用该方案。该方案支持所有区块链网络：Avalanche、Base、Arbitrum 和 0G。
homepage: https://sigil.codes
source: https://github.com/Arven-Digital/sigil-public
env:
  - name: SIGIL_API_KEY
    description: "Agent API key from Sigil dashboard (starts with sgil_). Generate at https://sigil.codes/dashboard/agent-access"
    required: true
    primary: true
  - name: SIGIL_ACCOUNT_ADDRESS
    description: "Your deployed Sigil smart account address (deploy at https://sigil.codes/onboarding)"
    required: true
  - name: SIGIL_API_URL
    description: "Sigil API base URL"
    required: false
    default: "https://api.sigil.codes"
  - name: SIGIL_CHAIN_ID
    description: "Chain ID (43114=Avalanche, 8453=Base, 42161=Arbitrum, 16661=0G)"
    required: false
    default: "43114"
metadata:
  clawdbot:
    emoji: "🛡️"
    requires:
      env:
        - SIGIL_API_KEY
        - SIGIL_ACCOUNT_ADDRESS
---

# Sigil协议 — 代理钱包技能

为AI代理提供安全的智能钱包，支持4个EVM区块链。三层防护机制会在所有交易被共同签署之前进行审核。

**API基础地址：** `https://api.sigil_codes/v1`  
**控制面板：** `https://sigil_codes`  
**支持的区块链：** Avalanche (43114), Base (8453), Arbitrum (42161), 0G Mainnet (16661)

## 安全性与密钥管理

**`SIGIL_API_KEY` 并非所有者密钥。** 它是一个用于代理身份验证的密钥，用于向防护机制（Guardian）API发起请求。权限模型如下：

| 操作 | 代理密钥 | 所有者密钥（SIWE） | 会话密钥 |
|--------|-----------|--------------|-------------|
| 评估交易 | ✅ | ✅ | ✅ |
| 查看钱包状态 | ✅ | ✅ | ✅ |
| 查看审计日志 | ✅ | ✅ | ❌ |
| 更新策略 | ❌ | ✅ | ❌ |
| 冻结账户 | ❌ | ✅ | ❌ |
| 旋转密钥 | ❌ | ✅ | ❌ |
| 紧急提款 | ❌ | ✅（仅限链上操作） | ❌ |
| 添加/移除恢复监护人 | ❌ | ✅ | ❌ |

**密钥使用原则：**
- 代理密钥 **无法** 冻结、提款、旋转密钥或更改策略——这些操作仅由所有者密钥（SIWE）执行。
- 代理密钥 **可以** 提交交易以供防护机制审核，并接收共同签署。
- **会话密钥**（推荐使用）具有更严格的限制：限时使用、消费额度限制、目标白名单以及自动过期。
- 防护机制 **仅负责验证交易，不具执行权限**——它不能转移资金或单独操作。
- 紧急提款 **仅由所有者通过链上操作触发**——任何API密钥都无法执行此操作。

**最佳实践：** 日常操作使用会话密钥。`SIGIL_API_KEY` 仅用于身份验证——无论使用哪种密钥，防护机制都会执行所有限制。

## 身份验证

有两种身份验证方式：

### API密钥（更简单）
所有者可以在控制面板的代理访问页面生成API密钥。

```bash
curl -X POST https://api.sigil.codes/v1/agent/auth/api-key \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "sgil_your_key_here"}'
# Returns: { "token": "eyJ..." }
```

### 委托签名（更安全）
所有者通过EIP-712消息委托代理进行操作。

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

所有请求都需要包含 `Authorization: Bearer <token>`（有效期4小时，需使用相同凭据重新认证）。

## 首次设置

### 1. 运行设置向导
```
GET /v1/agent/setup/wizard
```
向导会提供指导性问题、用例配置以及安全提示。**在部署前务必咨询所有者。**

### 2. 通过控制面板进行部署
指导所有者访问 `https://sigil_codes/onboarding`，完成以下步骤：
1. 连接钱包并使用SIWE登录。
2. 选择策略模板（保守型/中等型/激进型/DeFi代理/NFT代理）。
3. 选择目标区块链。
4. 生成代理密钥对。
5. 部署智能合约。

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

### 查看状态
```
GET /v1/agent/wallets/0xYourWallet
```
返回信息包括：余额、策略设置、会话密钥、每日消费额、监护人状态以及账户是否被冻结。

### 交易审核
每笔交易都会经过防护机制的三层审核流程：
1. **第一层（L1）：** 检查策略限制和白名单。
2. **第二层（L2）：** 进行模拟测试，检查是否存在回滚或意外状态变化。
3. **第三层（L3）：** 由AI对交易进行风险评估（评分范围0-100，阈值70）。

**审核结果：** `APPROVE`（带有监护人签名），`REJECT`（附带解释原因及修复建议），`ESCALATE`（需要所有者介入）。

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
会话密钥具有时间限制和用途限制，会自动过期。建议优先使用会话密钥而非完整的代理密钥。

### 紧急控制措施
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

## 合约地址

| 区块链 | 区块链ID | 工厂地址（Factory） |
|-------|----------|---------|
| Avalanche C-Chain | 43114 | `0x2f4dd6db7affcf1f34c4d70998983528d834b8f6` |
| Base | 8453 | `0x45b20a5F37b9740401a29BD70D636a77B18a510D` |
| Arbitrum One | 42161 | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| 0G Mainnet | 16661 | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| Avalanche Fuji（测试网） | 43113 | `0x86E85dE25473b432dabf1B9E8e8CE5145059b85b` |
**防护机制地址：** `0xD06fBe90c06703C4b705571113740AfB104e3C67`  
**入口点（v0.7）：** `0x0000000071727De22E5E9d8BAf0edAc6f37da032`

## MCP服务器

对于支持MCP协议的代理，MCP服务器的源代码可在此处获取：
https://github.com/Arven-Digital/sigil-public/tree/main/packages/mcp

可以克隆、审计并在本地运行相关工具：
```bash
git clone https://github.com/Arven-Digital/sigil-public.git
cd sigil-public/packages/mcp
pnpm install && pnpm build
SIGIL_API_KEY=sgil_... SIGIL_ACCOUNT_ADDRESS=0x... node dist/index.js
```

可用工具包括：`get_account_info`, `evaluate_transaction`, `create_session_key`, `freeze_account`, `unfreeze_account`, `update_policy`, `get_transaction_history`, `rotate_agent_key`, `get_protection_status`。

## 策略模板（针对不同区块链定制）

模板会根据原生代币的价值调整交易限制：

| 模板 | AVAX限制 | ETH限制 | A0GI限制 |
|----------|-------------|------------|-------------|
| **保守型** | 0.1/0.5/0.05 | 0.0003/0.0015/0.00015 | 1/5/0.5 |
| **中等型** | 0.5/2/0.2 | 0.0015/0.006/0.0006 | 5/20/2 |
| **激进型** | 2/10/1 | 0.006/0.03/0.003 | 20/100/10 |
| **DeFi代理** | 0.3/5/0.1 | 0.0009/0.015/0.0003 | 3/50/1 |
| **NFT代理** | 1/3/0.5 | 0.003/0.009/0.0015 | 10/30/5 |

*（限制包括：最大交易次数/每日交易次数/监护人审核阈值）*

## 最佳实践建议：
1. **从保守策略开始**——先设置较低的限额，根据实际情况逐步提高。
2. **明确设置白名单**——使用目标白名单和功能白名单。
3. **优先使用会话密钥**——它们会自动过期，比完整的代理密钥更安全。
4. **设置代币审批上限**——在策略中设置`maxApproval`限制。无限制的审批权限是DeFi攻击的主要途径。
5. **收到拒绝响应时，请阅读提示**——防护机制会说明拒绝原因及修复方法。
6. **操作前请先查看状态**——使用 `GET /v1/agent/wallets/:addr` 命令查询账户信息。
7. **监控系统保护机制**——如果保护机制被触发，所有交易将暂停，直到所有者手动重置。

## 高级内容

有关详细的API参考、共同签署机制、恢复系统以及DeFi白名单配置，请参阅 [references/api-reference.md](references/api-reference.md)。