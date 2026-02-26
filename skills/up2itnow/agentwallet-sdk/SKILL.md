# Agent Wallet SDK 技能

这是一个专为自主 AI 代理设计的非托管钱包 SDK。它支持 x402 支付、CCTP V2 跨链桥接转账、ERC-8004 代理身份验证以及 Uniswap V3 代币交换功能——所有这些操作均无需代理持有用户的私钥。

## 使用场景

当 AI 代理需要执行以下操作时，可以使用此 SDK：
- 创建或管理非托管钱包（ERC-4337 智能合约）
- 向 API 发送 x402 HTTP 请求进行支付
- 通过 CCTP V2 实现跨链代币桥接
- 通过 Uniswap V3 进行代币交换
- 通过 ERC-8004 注册或验证代理身份
- 自主签署交易，无需承担托管风险

## 安装

```bash
npm install agentwallet-sdk
```

当前版本：**v2.4.1**（在 npm 上发布，通过 158 项测试，无编译错误）

## 核心模块

### WalletModule — 账户抽象（ERC-4337）
```typescript
import { AgentWallet } from 'agentwallet-sdk';

const wallet = await AgentWallet.create({
  chain: 'base',
  signer: privateKey, // Agent's own key — never custodied
});

// Send ETH
await wallet.transfer({ to: recipient, value: '0.01' });

// Get balance
const balance = await wallet.getBalance();
```

### PaymentModule — x402 HTTP 支付
```typescript
// Pay for API access automatically
const response = await wallet.x402Pay({
  url: 'https://api.example.com/data',
  maxPayment: '0.001', // ETH
});
```

### BridgeModule — CCTP V2 跨链桥接
```typescript
// Bridge USDC from Base to Ethereum
await wallet.bridge({
  token: 'USDC',
  amount: '100',
  fromChain: 'base',
  toChain: 'ethereum',
});
```

### SwapModule — Uniswap V3 代币交换
```typescript
// Swap ETH for USDC
await wallet.swap({
  tokenIn: 'ETH',
  tokenOut: 'USDC',
  amount: '0.5',
  slippage: 0.5, // 0.5%
});
```

### IdentityModule — ERC-8004 身份验证
```typescript
// Register agent identity on-chain
await wallet.registerIdentity({
  name: 'MyTradingAgent',
  capabilities: ['x402-payment', 'swap', 'bridge'],
});

// Verify another agent
const verified = await wallet.verifyAgent(agentAddress);
```

## 安全模型

- **非托管模式**：代理自行保管私钥，服务器不会存储任何密钥。
- **ERC-4337 智能合约**：支持批量交易和会话密钥管理。
- **无需依赖外部数据源**：不依赖任何外部价格信息源，从而防止被操纵。
- **经过审计**：智能合约的伪造测试通过率为 129/129。

## 与其他组件的集成

### 与 Mastra（AI 框架）集成
```bash
npm install @agent-wallet/mastra-plugin
```
提供 10 个 Mastra 工具：`getBalance`、`transfer`、`swap`、`bridge`、`x402Pay`、`registerIdentity`、`verifyAgent`、`getTransactionHistory`、`estimateGas`、`getChainInfo`。

### 与 ClawPay MCP 集成
```bash
npm install clawpay-mcp
```
将钱包功能作为 MCP（Mastra 的扩展框架）工具提供给任何兼容 MCP 的代理。

## 链接

- npm：[agentwallet-sdk](https://www.npmjs.com/package/agentwallet-sdk)
- Mastra 插件：[@agent-wallet/mastra-plugin](https://www.npmjs.com/package/@agent-wallet/mastra-plugin)
- ClawPay MCP：[clawpay-mcp](https://www.npmjs.com/package/clawpay-mcp)