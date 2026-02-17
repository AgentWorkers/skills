# 代理钱包（Agent Wallet）

这是一个为自主AI代理设计的链上支出限制系统。作为Base L2平台的加密钱包组件，它支持在人类审核的支出控制下进行自主支付。您可以为每个代币设置预算，让代理在预算范围内自由交易；超出预算的交易将进入等待人类审核的队列。该钱包负责管理Gas费用和链上交易，使代理能够专注于其核心任务。

## 适用场景

- 当代理需要自主进行支付时
- 当代理需要一个具有支出限制的加密钱包时
- 当用户询问代理的财务自主性时
- 当代理需要在Base平台上发送ETH或ERC-20代币时
- 当代理需要人类审核的支出限制时
- 在构建代理之间的支付流程时
- 当代理需要一个具有支出控制功能的财务管理系统时
- 当需要集成基于ERC-6551标准的代币绑定账户以实现代理支出时

## 安全性概况

| 指标        | 详情                                      |
|------------|-------------------------------------------|
| **测试数量**     | 129个Solidity测试 · 34个SDK测试 · 104个后端测试 — 共267项测试             |
| **安全审查**     | 两轮内部对抗性安全审查（非第三方机构进行）                     |
| **验证过程**     | 8轮验证过程 — 无可修复的安全问题                   |
| **透明度**     | 详细记录了所有已知的安全限制（参见KNOWN_ISSUES.md文件）           |
| **许可证**     | MIT许可证 — 完全开源软件                         |

## 功能介绍

Agent Wallet是一个专为Base平台上的AI代理设计的智能合约钱包（基于ERC-6551标准的代币绑定账户）。与传统的私钥管理方式不同，该钱包采用了以下强制性的安全措施：

- **单次交易限额**：每笔交易的最高支出金额在链上得到严格限制。
- **每日预算限制**：为每个代币设置滚动预算。
- **操作权限管理**：仅向代理授予必要的操作权限，无需共享私钥。
- **审核队列**：超出预算的交易会进入等待所有者审核的队列（兼容ERC-4337标准）。
- **操作权限自动失效**：在NFT转移时，所有操作权限自动失效，防止权限滥用。
- **防重入保护**：所有可能改变状态的函数都受到保护，防止恶意代码的重复执行。

## 部署地址

| 网络        | 合同地址                                      |          |
|------------|-----------------------------------------|------------|
| **Base主网**     | `0x700e9Af71731d707F919fa2B4455F27806D248A1`             |         |
| **Base Sepolia**     | `0x337099749c516B7Db19991625ed12a6c420453Be`             |         |

## SDK使用说明

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

- **支出限制**：在合约中直接进行验证，代理代码无法绕过这些限制。
- **操作权限自动失效**：在NFT转移时，所有操作权限自动失效。
- **防重入保护**：所有可能修改状态的函数都受到保护，防止恶意代码的重复执行。
- **固定时间窗口**：防止在时间边界处发生双重支付攻击。
- **NFT销毁保护**：如果NFT被销毁，相关资金可被恢复，系统会进行干净的重置。

### 安全审查过程

安全性审查由内部团队完成（两轮AI辅助的对抗性测试）。未接受第三方审计。

- **第一轮审查**：发现并修复了多个安全漏洞，包括重入攻击和访问控制问题。
- **第二轮审查**：发现并修复了NFT被恶意占用的问题、操作权限的持久性问题、基于ERC-4337标准的攻击机制以及边界双重支付问题。

**审计报告**：
- [`AUDIT_REPORT.md`](./AUDIT_REPORT.md) — 第一轮审查报告
- [`AUDIT_REPORT_V2.md`](./AUDIT_REPORT_V2.md) — 第二轮（对抗性测试）报告

### 测试结果

- **129个Solidity测试全部通过**（包括单元测试、漏洞测试、不变量测试、工厂功能测试、路由测试、ERC-4337标准测试等）。
- **34个SDK测试全部通过**（涵盖钱包创建、支出限制、操作权限管理、交易处理等关键功能）。
- 特殊的漏洞测试确认所有已发现的攻击途径均被有效阻止。

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

有关系统的限制和正在监控的问题，请参阅[KNOWN_ISSUES.md](./KNOWN_ISSUES.md)文件。

## 许可证

MIT许可证