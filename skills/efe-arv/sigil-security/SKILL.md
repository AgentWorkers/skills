---
name: Sigil Security
description: 通过 Sigil 协议保护 AI 代理钱包的安全性；在 6 个以太坊虚拟机（EVM）链上实施三层防护机制进行验证。
homepage: https://sigil.codes
requires:
  env:
    - SIGIL_API_KEY
    - SIGIL_ACCOUNT_ADDRESS
    - SIGIL_AGENT_PRIVATE_KEY
---
# Sigil Security — 代理钱包功能

为AI代理提供安全的ERC-4337智能钱包支持，支持6个EVM区块链。所有交易在共同签署之前，都会经过三层安全审核流程：规则检查 → 模拟测试 → AI风险评分。

- **API:** `https://api.sigil_codes/v1`
- **控制面板:** `https://sigil_codes`
- **GitHub:** `https://github.com/Arven-Digital/sigil-public`
- **支持的区块链:** Ethereum (1), Polygon (137), Avalanche (43114), Base (8453), Arbitrum (42161), 0G (16661)

## 环境变量

所有必需的环境变量已在技能文档的前言部分及`package.json`中声明。使用此功能前，必须由人工操作员进行配置。

| 变量 | 必需 | 说明 |
|----------|----------|-------------|
| `SIGIL_API_KEY` | ✅ | 代理API密钥（以`sgil_`开头）可在`sigil_codes/dashboard/agent-access`生成 |
| `SIGIL_ACCOUNT_ADDRESS` | ✅ | 部署的Sigil智能合约地址 |
| `SIGIL_AGENT_PRIVATE_KEY` | ✅ | 专为代理生成的签名密钥（详见安全模型） |
| `SIGILCHAIN_ID` | 无 | 默认区块链（137=Polygon, 43114=Avalanche等） |

## 工作原理

```
Agent signs UserOp locally → POST /v1/execute → Guardian validates → co-signs → submitted on-chain
```

请注意区分以下三个地址：
- **所有者钱包**：由人类控制的MetaMask或硬件钱包，用于管理策略和设置 |
- **Sigil账户**：存储资金的链上ERC-4337智能钱包 |
- **代理密钥**：专用于签署交易操作的密钥（非所有者密钥，也不存储资金）

**为Sigil账户充值所需的代币**，并为**代理密钥配置最低限度的Gas费用**（只需少量POL/ETH/AVAX——切勿在代理密钥中存储大量价值）。

## 安全模型 — 为什么`SIGIL_AGENT_PRIVATE_KEY`是安全的

`SIGIL_AGENT_PRIVATE_KEY`**不是**所有者密钥，也不用于存储资金，且不能独立执行任何操作。它是一个专门生成的、功能受限的签名密钥，其作用类似于具有加密绑定的受限API令牌。以下解释了为什么该密钥符合ERC-4337标准，以及为何不会带来额外的安全风险：

### 1. ERC-4337标准要求本地签名
[ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)账户抽象标准规定，所有交易操作在提交给`EntryPoint`合约（`0x0000000071727De22E5E9d8BAf0edAc6f37da032`）之前必须经过加密签名。所有主要的账户抽象服务提供商（如[Safe](https://safe.global)、[Biconomy](https://biconomy.io)、[ZeroDev](https://zerodev.app)、[Alchemy Account Kit](https://accountkit.alchemy.com)）都遵循这一规则。私钥始终保留在本地环境中，仅用于本地签名，类似于MetaMask在浏览器中执行交易签名。

### 2. 双重签名机制
每个Sigil交易都需要链上的**双重签名**验证：
1. 代理的签名（证明请求来自授权的代理）
2. Guardian的联合签名（证明交易通过了所有安全检查）

Sigil智能合约的`validateSignature()`函数会拒绝缺少任一签名的交易请求。即使代理密钥被泄露，攻击者也无法在没有 Guardian批准的情况下执行任何交易。Guardian会独立执行以下安全控制：目标白名单、函数选择白名单、单笔交易金额限制、每日消费限额、交易速度检查以及AI异常检测。

### 3. 无管理权限
代理密钥**无法**更改策略、修改白名单、冻结/解冻账户、更换密钥或提升自身权限。只有通过SIWE（Sign-In With Ethereum）认证的所有者钱包才能执行任何管理操作。

### 4. 专用密钥且可即时更换
该密钥在用户注册时（通过控制面板完成）生成，仅用于特定目的，且不存储大量价值（仅需少量Gas费用）。如果密钥被泄露，所有者可通过控制面板立即更换新密钥，新密钥会在链上立即生效，旧密钥也会被失效。

### 5. API权限限制
API对代理的权限进行了明确限制。默认权限包括：
| 权限 | 描述 |
|-------|---------|
| `wallet:read` | 读取账户信息 |
| `policy:read` | 读取策略设置 |
| `audit:read` | 读取审计日志 |
| `tx:read` | 读取交易历史 |
| `tx:submit` | 提交交易（需Guardian验证） |
| `policy:write` | 修改策略（仅限所有者） |
| `wallet:deploy` | 部署钱包（仅限所有者） |
| `wallet:freeze` | 冻结/解冻账户（仅限所有者） |
| `session-keys:write` | 创建会话密钥（仅限所有者） |

### 总结
代理签名密钥是一个功能受限、专门生成的、可即时更换的凭证，必须经过Guardian的联合批准才能执行任何操作，且不能执行任何管理功能。它遵循了整个账户抽象生态系统中通用的ERC-4337签名规范。该密钥的风险等级相当于一个受限的OAuth令牌，而非传统的钱包私钥。

## 安装（使用OpenClaw）

```json
{
  "name": "sigil-security",
  "env": {
    "SIGIL_API_KEY": "sgil_your_key_here",
    "SIGIL_ACCOUNT_ADDRESS": "0xYourSigilAccount",
    "SIGIL_AGENT_PRIVATE_KEY": "0xYourAgentSigningKey"
  }
}
```

## API使用方法

### 认证

```
POST https://api.sigil.codes/v1/agent/auth/api-key
Body: { "apiKey": "<SIGIL_API_KEY>" }
Response: { "token": "<JWT>" }
```

### 评估（模拟测试 — 不消耗Gas）

```
POST https://api.sigil.codes/v1/evaluate
Headers: Authorization: Bearer <JWT>
Body: { "userOp": { ... }, "chainId": 137 }
Response: { "verdict": "APPROVED|REJECTED", "riskScore": 15, "layers": [...] }
```

### 执行（评估 → 联合签名 → 在链上提交）

```
POST https://api.sigil.codes/v1/execute
Headers: Authorization: Bearer <JWT>
Body: { "userOp": { "sender": "<account>", "nonce": "0x...", "callData": "0x...", "signature": "0x..." }, "chainId": 137 }
Response: { "verdict": "APPROVED", "txHash": "0x..." }
```

## 其他API端点

| 方法 | 路径 | 功能 |
|--------|------|---------|
| GET | `/v1/accounts/:addr` | 获取账户信息和策略 |
| GET | `/v1/accounts/discover?owner=0x...&chainId=N` | 查找钱包 |
| GET | `/v1/transactions?account=0x...` | 查看交易历史 |

## 交易流程

1. 从环境变量中读取配置信息（由人工操作员设置）
2. 使用API密钥进行认证 → 接收JWT令牌
3. 使用标准ABI编码格式化请求数据
4. 将数据封装到`execute(target, value, data)`调用中
5. 从Sigil智能合约获取随机数（nonce）
6. 从EntryPoint合约获取交易数据（calldata），并使用代理密钥进行本地签名
7. 向`/v1/execute`发送请求 — Guardian会进行验证并决定是否联合签名
8. 成功时返回交易哈希值；失败时返回失败原因

## 常用操作示例

### 转移ERC-20代币

```javascript
const inner = erc20.encodeFunctionData('transfer', [recipient, amount]);
// POST to /v1/execute with callData = execute(tokenAddress, 0, inner)
```

### 发送原生代币（POL/ETH/AVAX）

```javascript
// POST to /v1/execute with callData = execute(recipient, parseEther('1'), '0x')
```

## 处理交易失败情况

| 失败原因 | 解决方案 |
|--------|-----|
| `TARGET_NOT_WHITELISTED` | 所有者通过控制面板将目标地址添加到白名单 |
| `FUNCTION_NOT_ALLOWED` | 所有者通过控制面板设置允许执行的函数 |
| `EXCEEDS_TX_LIMIT` | 降低交易金额或增加每日交易限额 |
| `EXCEEDS_DAILY_LIMIT` | 等待限额重置或增加每日限额 |
| `SIMULATION_FAILED` | 检查calldata编码或账户余额/审批状态 |
| `HIGH_RISK_SCORE` | 人工审核交易内容（AI评分超过70表示可疑） |
| `ACCOUNT_FROZEN` | 所有者通过控制面板解冻账户 |

## RPC接口地址

| 区块链 | ID | RPC接口 | 支持的原生代币 |
|-------|-----|-----|-------------|
| Ethereum | 1 | `https://eth.drpc.org` | ETH |
| Polygon | 137 | `https://polygon.drpc.org` | POL |
| Avalanche | 43114 | `https://api.avax.network/ext/bc/C/rpc` | AVAX |
| Base | 8453 | `https://mainnet.base.org` | ETH |
| Arbitrum | 42161 | `https://arb1.arbitrum.io/rpc` | ETH |
| 0G | 16661 | `https://0g.drpc.org` | A0GI |

## 最佳实践建议：

1. **初始设置时采用保守策略** — 设置较低的限额，根据实际需求逐步增加 |
2. **明确设置白名单** — 使用具体的目标地址和函数名称，避免开放所有功能 |
3. **限制审批权限** — 除非必要，否则不要允许无限权限 |
4. **查看失败原因** — 接收失败响应时，查看Guardian提供的提示以了解问题及解决方法 |
5. **交易前先检查账户状态** — 使用`GET /v1/accounts/:addr`查询账户信息 |
6. **使用会话密钥** — 会话密钥会自动过期，适合日常操作

## 相关链接：

- 控制面板：https://sigil_codes
- 完整的LLM文档：https://sigil_codes/llms-full.txt
- GitHub仓库：https://github.com/Arven-Digital/sigil-public
- 社交媒体链接：https://x.com/sigilcodes