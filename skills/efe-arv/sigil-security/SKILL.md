---
name: Sigil Protocol
title: Sigil Protocol
slug: sigil-security
description: 通过 Sigil 协议保护 AI 代理钱包的安全。在 6 个 EVM 链上，通过三层防护机制（规则检查、模拟测试、AI 风险评估）来验证和提交 ERC-4337 交易。代理在本地签署 UserOps 操作——Sigil 从不接触私钥。
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
        - SIGIL_AGENT_PRIVATE_KEY
---
# Sigil协议 — 代理钱包技能

为AI代理提供安全的ERC-4337智能钱包，支持6个EVM区块链。每笔交易在共同签署之前，都会经过三层安全审核（规则检查 → 模拟测试 → AI风险评分）。

**API:** `https://api.sigil_codes/v1`  
**控制面板:** `https://sigil_codes`  
**支持的区块链:** Ethereum (1), Polygon (137), Avalanche (43114), Base (8453), Arbitrum (42161), 0G (16661)

## 环境变量

| 变量 | 必填 | 说明 |
|----------|----------|-------------|
| `SIGIL_API_KEY` | ✅ | 代理API密钥（以`sgil_`开头）. 在sigil_codes/dashboard/agent-access生成 |
| `SIGIL_ACCOUNT_ADDRESS` | ✅ | 部署的Sigil智能合约地址 |
| `SIGIL_AGENT_PRIVATE_KEY` | ✅ | 代理签名密钥（用于UserOp操作） |
| `SIGILCHAIN_ID` | 不必填写 | 默认链（137=Polygon, 43114=Avalanche等） |

## 工作原理

```
Agent signs UserOp → POST /v1/execute → Guardian validates → co-signs → submitted on-chain
```

请注意以下三个地址的区别：
- **所有者钱包**：由人类控制的MetaMask钱包，用于管理策略和设置 |
- **Sigil账户**：链上的智能钱包，用于存储资金 |
- **代理密钥**：专为代理生成的专用签名密钥（不同于所有者密钥），用于执行UserOp操作 |

**为Sigil账户充值所需的代币**。**为代理密钥仅充值少量Gas（POL/ETH/AVAX），用于向EntryPoint提交UserOp操作** — **切勿在代理密钥中存储大量价值**。

## 安全模型及为什么需要`SIGIL_AGENT_PRIVATE_KEY`

`SIGIL_AGENT_PRIVATE_KEY`既不是所有者密钥，也不是用于存储资金的钱包密钥。它是专门为代理在注册过程中生成的签名密钥。其安全性体现在以下几点：
1. **ERC-4337协议要求使用加密签名**。代理必须先在本地签名UserOp操作，才能通过安全审核。这确保了交易来自授权的代理，而非被窃取的API密钥。
2. **代理密钥无法单独执行交易**。每笔交易都需要代理的签名和Guardian的联合签名。即使代理密钥被泄露，攻击者仍需获得Guardian的批准。此外，系统还实施了白名单、价值限制、交易速度检查及AI风险评分机制。
3. **代理密钥无法修改自身权限**. 仅所有者钱包（通过SIWE）才能更改策略、冻结账户、更换密钥或添加白名单目标。代理密钥只能提交交易请求供Guardian审核。
4. **`tx:submit`操作是安全的**，因为所有交易都会经过三层安全验证。如果超出限制、调用未列出的合约或触发风险警报，交易将被自动拒绝。安全保障由Guardian负责，而非API密钥。

**最佳实践：**
- 使用新的密钥对（仅在注册时生成）。为代理账户充值少量Gas。在Sigil控制面板设置保守的策略限制。无论代理尝试什么操作，Guardian都会严格执行安全规则。

## 安装（使用OpenClaw）

```json
{
  "name": "sigil-security",
  "env": {
    "SIGIL_API_KEY": "sgil_your_key_here",
    "SIGIL_ACCOUNT_ADDRESS": "0xYourSigilAccount",
    "SIGIL_AGENT_PRIVATE_KEY": "0xYourAgentPK"
  }
}
```

⚠️ `env`必须是一个扁平的键值对象（数组形式不可用）。

## 完整操作示例（可直接复制粘贴）

以下是从授权到交易确认的完整流程，使用ethers.js v6实现。

```javascript
const { ethers } = require('ethers');

// ─── Config (from your env vars) ───
const API_KEY = process.env.SIGIL_API_KEY;           // sgil_...
const ACCOUNT = process.env.SIGIL_ACCOUNT_ADDRESS;   // 0x...
const AGENT_PK = process.env.SIGIL_AGENT_PRIVATE_KEY; // 0x...
const CHAIN_ID = parseInt(process.env.SIGIL_CHAIN_ID || '137');
const API = 'https://api.sigil.codes/v1';
const ENTRYPOINT = '0x0000000071727De22E5E9d8BAf0edAc6f37da032';

// ─── RPC URLs ───
const RPCS = {
  1: 'https://eth.drpc.org',
  137: 'https://polygon.drpc.org',
  43114: 'https://api.avax.network/ext/bc/C/rpc',
  8453: 'https://mainnet.base.org',
  42161: 'https://arb1.arbitrum.io/rpc',
  16661: 'https://0g.drpc.org',
};

const provider = new ethers.JsonRpcProvider(RPCS[CHAIN_ID]);
const agentWallet = new ethers.Wallet(AGENT_PK, provider);

// ─── Step 1: Authenticate ───
async function auth() {
  const res = await fetch(`${API}/agent/auth/api-key`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ apiKey: API_KEY }),
  });
  const { token, error } = await res.json();
  if (error) throw new Error(`Auth failed: ${error}`);
  return token; // Use as: Authorization: Bearer <token>
}

// ─── Step 2: Build, sign, and submit a transaction ───
async function sendTransaction(token, target, value, innerData, description) {
  // 2a. Encode execute(target, value, innerData)
  const executeIface = new ethers.Interface([
    'function execute(address target, uint256 value, bytes data)',
  ]);
  const callData = executeIface.encodeFunctionData('execute', [target, value, innerData]);

  // 2b. Get nonce from the Sigil account
  const account = new ethers.Contract(ACCOUNT, [
    'function getNonce() view returns (uint256)',
  ], provider);
  const nonce = await account.getNonce();

  // 2c. Pack gas fields (v0.7 format)
  // Safe defaults: 300k verification, 500k call gas, 50gwei fees
  const vgl = 300000n, cgl = 500000n, preVerGas = 60000n;
  const feeData = await provider.getFeeData();
  const maxPriority = feeData.maxPriorityFeePerGas ?? 30000000000n;
  const maxFee = feeData.maxFeePerGas ?? 50000000000n;

  const accountGasLimits = '0x' +
    vgl.toString(16).padStart(32, '0') +
    cgl.toString(16).padStart(32, '0');
  const gasFees = '0x' +
    maxPriority.toString(16).padStart(32, '0') +
    maxFee.toString(16).padStart(32, '0');

  // 2d. Get UserOp hash from EntryPoint and sign it
  const ep = new ethers.Contract(ENTRYPOINT, [
    'function getUserOpHash((address,uint256,bytes,bytes,bytes32,uint256,bytes32,bytes,bytes)) view returns (bytes32)',
  ], provider);
  const userOpHash = await ep.getUserOpHash([
    ACCOUNT, ethers.toBeHex(nonce), '0x', callData,
    accountGasLimits, ethers.toBeHex(preVerGas), gasFees, '0x', '0x',
  ]);
  const signature = await agentWallet.signMessage(ethers.getBytes(userOpHash));

  // 2e. Submit to Sigil — Guardian evaluates and co-signs
  const res = await fetch(`${API}/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      userOp: {
        sender: ACCOUNT,
        nonce: ethers.toBeHex(nonce),
        callData,
        accountGasLimits,
        preVerificationGas: preVerGas.toString(),
        gasFees,
        signature,
      },
      chainId: CHAIN_ID,
    }),
  });
  const result = await res.json();

  if (result.verdict === 'APPROVED') {
    console.log(`✅ ${description}: ${result.txHash}`);
  } else {
    console.log(`❌ ${description}: ${result.rejectionReason}`);
    console.log('   Guidance:', result.guidance?.message);
  }
  return result;
}

// ─── Example: Approve 100 USDC to a DEX on Polygon ───
async function main() {
  const token = await auth();

  const usdc = new ethers.Interface(['function approve(address,uint256)']);
  const innerData = usdc.encodeFunctionData('approve', [
    '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45', // Uniswap SwapRouter02
    ethers.parseUnits('100', 6), // 100 USDC
  ]);

  await sendTransaction(
    token,
    '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', // USDC on Polygon
    0n,
    innerData,
    'Approve 100 USDC to SwapRouter02',
  );
}

main().catch(console.error);
```

上述`sendTransaction()`函数可处理所有操作，只需更改`target`、`value`和`innerData`参数即可。

## 快速操作指南

### 转移代币
```javascript
const inner = erc20.encodeFunctionData('transfer', [recipient, amount]);
await sendTransaction(token, tokenAddress, 0n, inner, 'Transfer');
```

### 发送原生代币（POL/ETH/AVAX）
```javascript
await sendTransaction(token, recipient, ethers.parseEther('1'), '0x', 'Send 1 POL');
```

### 将原生代币转换为WMATIC/WETH/WAVAX
```javascript
await sendTransaction(token, WMATIC, ethers.parseEther('1'), '0xd0e30db0', 'Wrap 1 POL');
```

### 使用Uniswap V3进行交易
```javascript
const router = new ethers.Interface([
  'function exactInputSingle(tuple(address,address,uint24,address,uint256,uint256,uint160))',
]);
const inner = router.encodeFunctionData('exactInputSingle', [
  [tokenIn, tokenOut, 3000, ACCOUNT, amountIn, 0, 0],
]);
await sendTransaction(token, ROUTER_ADDRESS, 0n, inner, 'Swap');
```

## 仅进行评估（不执行交易）

操作方式与上述相同，但需向`/v1/evaluate`发送请求，而非`/v1/execute`。评估结果会包含风险评分及详细信息，无需消耗Gas。

## 处理交易拒绝

当交易被拒绝时，响应中会包含`guidance`（建议的操作指南）：

```json
{
  "verdict": "REJECTED",
  "rejectionReason": "TARGET_NOT_WHITELISTED",
  "guidance": {
    "message": "Contract 0xABC... is not in your whitelist. Add it in Dashboard → Policies.",
    "action": "add_target"
  }
}
```

**处理流程：**
1. 如果`TARGET_NOT_WHITELISTED`或`FUNCTION_NOT_ALLOWED`，提示用户/所有者通过控制面板将目标添加到白名单。此问题无法自行解决。
2. 如果`EXCEEDS_TX_LIMIT`或`EXCEEDS_DAILY_LIMIT`，请减少交易金额或请求所有者增加限额。
3. 如果`SIMULATION_FAILED`，检查数据格式是否正确（目标地址、ABI编码、代币余额及审批状态）。
4. 如果`HIGH_RISK_SCORE`，说明交易被AI标记为高风险，请重新检查操作内容。
5. 如果`ACCOUNT_FROZEN`或`CIRCUIT_BREAKER`，所有者需通过控制面板进行干预。

## RPC接口地址

| 区块链 | ID | RPC接口 | 支持的代币 |
|-------|-----|-----|-------------|
| Ethereum | 1 | `https://eth.drpc.org` | ETH |
| Polygon | 137 | `https://polygon.drpc.org` | POL |
| Avalanche | 43114 | `https://api.avax.network/ext/bc/C/rpc` | AVAX |
| Base | 8453 | `https://mainnet.base.org` | ETH |
| Arbitrum | 42161 | `https://arb1.arbitrum.io/rpc` | ETH |
| 0G | 16661 | `https://0g.drpc.org` | A0GI |

## 主要代币的地址

### Polygon (137)
| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | 6 |
| USDC.e | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | 6 |
| WMATIC | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270` | 18 |
| WETH | `0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619` | 18 |

### Avalanche (43114)
| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` | 6 |
| WAVAX | `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` | 18 |

### Base (8453)
| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 |
| WETH | `0x4200000000000000000000000000000000000006` | 18 |

### Arbitrum (42161)
| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` | 6 |
| WETH | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | 18 |

## API接口

| 方法 | 路径 | 功能 |
|--------|------|---------|
| POST | `/v1/agent/auth/api-key` | 用户认证（JWT签名） |
| POST | `/v1/evaluate` | 仅进行评估 |
| POST | `/v1/execute` | 评估并提交交易 |
| GET | `/v1accounts/:addr` | 账户信息及策略 |
| GET | `/v1/accounts/discover?owner=0x...&chainId=N` | 查找钱包信息 |
| GET | `/v1/transactions?account=0x...` | 查看交易历史 |

## 处理交易拒绝的原因及解决方法

| 原因 | 解决方法 |
|--------|-----|
| `TARGET_NOT_WHITELISTED` | 所有者需通过控制面板将目标添加到白名单 |
| `FUNCTION_NOT_ALLOWED` | 所有者需在控制面板中启用相应功能 |
| `EXCEEDS_TX_LIMIT` | 减少交易金额或请求所有者增加限额 |
| `EXCEEDS_DAILY_LIMIT` | 等待限额重置或请求所有者增加每日限额 |
| `SIMULATION_FAILED` | 检查数据格式或余额/审批状态 |
| `HIGH_RISK_SCORE` | 交易被AI标记为高风险 |
| `ACCOUNT_FROZEN` | 所有者需通过控制面板解冻账户 |

## 代理权限

| 权限 | 默认值 | 说明 |
|-------|---------|-------------|
| `wallet:read` | ✅ | 读取账户信息 |
| `policy:read` | ✅ | 读取策略设置 |
| `audit:read` | ✅ | 读取审计日志 |
| `tx:read` | ✅ | 读取交易历史 |
| `tx:submit` | ✅ | 提交交易 |
| `policy:write` | ❌ | 修改策略（仅限所有者） |
| `wallet:deploy` | ❌ | 部署钱包（危险操作） |
| `wallet:freeze` | ❌ | 冻结/解冻钱包 |
| `session-keys:write` | ❌ | 创建会话密钥 |

## V12工厂地址

| 区块链 | 工厂地址 |
|-------|---------|
| Ethereum (1) | `0x20f926bd5f416c875a7ec538f499d21d62850f35` |
| Polygon (137) | `0x483D6e4e203771485aC75f183b56D5F5cDcbe679` |
| Avalanche (43114) | `0x86e85de25473b432dabf1b9e8e8ce5145059b85b` |
| Base (8453) | `0x5729291ed4c69936f5b5ace04dee454c6838fd50` |
| Arbitrum (42161) | `0x2f4dd6db7affcf1f34c4d70998983528d834b8f6` |
| 0G (16661) | `0x8bAD12A489338B533BCA3B19138Cd61caA17405F` |

**EntryPoint v0.7**的通用地址：`0x0000000071727De22E5E9d8BAf0edAc6f37da032`（适用于所有区块链）

## 常用操作函数及选择器

| 功能 | 使用的选择器 |
|----------|----------|
| `approve(address,uint256)` | `0x095ea7b3` |
| `transfer(address,uint256)` | `0xa9059cbb` |
| `deposit()`（转换代币） | `0xd0e30db0` |
| `exactInputSingle(...)` | `0x414bf389` |
| `multicall(uint256,bytes[])` | `0x5ae401dc` |
| `multicall(bytes[])` | `0xac9650d8` |

## 最佳实践：
- **初始设置时采用保守的权限限制**，根据实际需求逐步调整。
- **明确设置白名单**：使用具体的目标地址和功能名称进行白名单管理。
- **限制审批权限**：除非必要，否则不要设置无限制的权限（例如`type(uint256).max`）。
- **收到拒绝响应时查看`guidance`以获取原因及解决方案**。
- **交易前先查询账户状态**：使用`GET /v1/accounts/:addr`。
- **日常操作使用会话密钥**：会话密钥会自动过期。

## 相关链接：
- 控制面板：https://sigil_codes
- 完整的LLM文档：https://sigil_codes/llms-full.txt
- GitHub仓库：https://github.com/Arven-Digital/sigil-public
- ClawdHub安装指南：`clawdhub install sigil-security`
- 社交媒体平台：https://x.com/sigilcodes

## 正在进行的漏洞赏金计划（诱饵挑战）

**状态：** 正在进行中 | **目标区块链：** Polygon (137)  
**公告链接：** https://x.com/sigilcodes/status/2026667797070156097  
示例钱包地址：`0x3cf7CBea6B03de76fE610B5ed9F04a1E351B083C`  
代理私钥（公开）：`0x177fbce08840d4b9a32d8e4f33b93ed817262ac2e208f96449e5ea4570006c5b`  
这个已启用的Sigil钱包正在Uniswap V3上进行交易。代理密钥是公开的。尝试尝试超出白名单范围的交易操作。如果成功入侵，请通过X平台联系@sigilcodes。