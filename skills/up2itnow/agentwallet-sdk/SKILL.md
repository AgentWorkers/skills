# 代理钱包（Agent Wallet）

该钱包为自主运行的AI代理设置了链上交易限额。为每个代币设定预算，代理可在预算范围内自由进行交易；超出限额的交易将进入等待人工审核的队列。

## 功能概述

代理钱包（Agent Wallet）是一个基于ERC-6551标准的智能合约钱包，专为Base平台上的AI代理设计。与传统的私钥管理方式不同，该钱包采用了以下强制性的限制机制：

- **单笔交易限额**：每笔交易的最高支出金额由合约在链上严格控制。
- **每日预算上限**：为每个代币设定滚动周期内的预算限制。
- **操作员权限管理**：允许代理在无需共享私钥的情况下执行特定操作。
- **审核队列**：超出预算的交易会进入等待所有者审核的队列（兼容ERC-4337标准）。
- **操作员权限失效机制**：在NFT转移时，所有操作员权限会自动失效，以防止权限过期后仍能继续访问资源。
- **防重入保护**：所有可能修改合约状态的函数都配备了防重入保护机制。

## 部署地址

| 网络 | 合约地址 | 公共地址 |
|---------|----------|---------|
| **Base主网** | `0x700e9Af71731d707F919fa2B4455F27806D248A1` |
| **Base Sepolia** | `0x337099749c516B7Db19991625ed12a6c420453Be` |

## SDK使用方式

```bash
npm install @agentwallet/sdk
```

```typescript
import { createWallet, agentTransferToken } from '@agentwallet/sdk';

// Connect to an agent's wallet
const wallet = createWallet({
  accountAddress: '0x...',
  chain: 'base',
  walletClient
});

// Agent spends within limits — no approval needed
await agentTransferToken(wallet, {
  token: USDC_ADDRESS,
  to: recipientAddress,
  amount: parseUnits('50', 6)
});

// Set spend limits (owner only)
await wallet.setSpendLimit({
  token: USDC_ADDRESS,
  maxPerTx: parseUnits('100', 6),
  periodLimit: parseUnits('500', 6),
  periodDuration: 86400 // 24 hours
});
```

## 安全模型

### 链上安全机制
- 合约中内置了交易限额检查机制，代理代码无法绕过这些限制。
- 在NFT转移时，所有操作员权限会自动失效。
- 所有可能修改合约状态的函数都配备了防重入保护机制（包括基于ERC-4337标准的函数）。
- 通过固定时间窗口机制防止边界条件下的双重支付攻击。
- 提供NFT销毁保护功能：销毁的NFT对应的资金可被恢复。

### 安全审查情况
项目内部进行了两轮安全审查（包括AI辅助的对抗性测试），尚未接受第三方审计：
- **第一轮审查**：发现并修复了潜在的安全漏洞（如重入攻击路径和访问控制问题）。
- **第二轮审查**：通过对抗性测试，发现并修复了NFT被恶意借用的风险、操作员权限持续存在的问题、基于ERC-4337标准的攻击机制以及边界条件下的双重支付问题。

**完整审计报告：**
- [`AUDIT_REPORT.md`](./AUDIT_REPORT.md) — 第一轮审查报告
- [`AUDIT_REPORT_V2.md`](./AUDIT_REPORT_V2.md) — 第二轮（对抗性测试）报告

### 测试结果
- **129项Solidity测试全部通过**（涵盖单元测试、漏洞利用测试、不变量测试、工厂功能测试、路由功能测试、ERC-4337标准相关测试等）。
- **34项SDK测试全部通过**（包括钱包创建、交易限额控制、操作员权限管理、交易处理等功能的测试）。
- 特别设计的漏洞利用测试验证了所有已发现的攻击路径均被有效拦截。

## 架构设计

```
NFT (ERC-721)
  └── Token Bound Account (ERC-6551)
       ├── Owner: NFT holder (full control)
       ├── Operators: Scoped access (set by owner)
       ├── Spend Limits: Per-token, per-period (on-chain)
       ├── Approval Queue: Over-limit txs (ERC-4337)
       └── Factory: CREATE2 deterministic deploys
```

## 已知问题

有关项目的限制和正在监控的问题，请参阅[KNOWN_ISSUES.md](./KNOWN_ISSUES.md)。

## 许可证

MIT许可证