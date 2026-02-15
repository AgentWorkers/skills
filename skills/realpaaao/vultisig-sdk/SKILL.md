---
name: vultisig
description: 当代理需要创建加密钱包、发送交易、交换代币、查询余额或使用阈值签名（Threshold Signatures, TSS）在36种以上的区块链上执行任何链上操作时，请使用此技能。Vultisig SDK提供了自主管理的MPC（Multi-Party Computation）安全存储解决方案——无需使用助记词，也没有任何单点故障风险。Fast Vaults（基于VultiServer的2-of-2验证机制）允许代理在无需人工批准的情况下完全自主地执行操作。
user-invocable: true
---

# Vultisig SDK 技能（以代理为中心）

## 该技能的功能

- 创建和管理自托管的加密保险库（Fast Vault 适用于代理，Secure Vault 适用于多设备）
- 在 36 个以上的区块链（包括 Bitcoin、Ethereum、Solana、Cosmos 等）之间发送交易
- 通过 THORChain、MayaChain、1inch、LiFi、KyberSwap 等平台进行跨链代币交换
- 查询所有支持链路的余额和 gas 费用
- 导入/导出保险库备份文件（.vult 文件）
- 通过 BIP39 种子短语导入现有钱包
- 构建自动化策略：定期投资（DCA）、重新平衡、条件交换、代理间支付等

## 默认配置决策

1) **所有代理使用场景均采用 Fast Vault（2-of-2）**
   - 代理持有其中一个密钥份额，VultiServer 持有另一个份额
   - VultiServer 根据策略规则自动进行联合签名——无需人工干预
   - 仅在需要多设备人工批准时使用 Secure Vault

2) **使用 TypeScript SDK (`@vultisig/sdk)` 作为主要接口**
   - `npm install @vultisig/sdk`
   - 代码来源：[github.com/vultisig/vultisig-sdk](https://github.com/vultisig/vultisig-sdk)
   - SDK 用户指南：[`docs/SDK-USERS-GUIDE.md`](https://github.com/vultisig/vultisig-sdk/blob/main/docs/SDK-USERS-GUIDE.md)

3) **对于临时使用的代理，使用 `MemoryStorage`；对于持久性代理，实现 `Storage` 接口**
   - `MemoryStorage` 是 SDK 提供的唯一存储方式
   - 对于持久性保险库，使用您选择的存储方式实现 `Storage` 接口

4) **三步交易流程：准备 → 签名 → 广播**
   - 严禁跳过任何步骤。必须先准备密钥签名数据，然后签名，最后广播。
   - Fast Vault 的签名是自动完成的（由 VultiServer 联合签名）。Secure Vault 需要设备的协调。

5) **发送金额使用 `bigint` 类型（最小单位）；交换金额使用 `number` 类型（便于人类阅读）**
   - `prepareSendTx` 方法接受 `amount: bigint` 类型的参数（例如，`BigInt('100000000000000000')` 表示 0.1 ETH）
   - `getSwapQuote` 方法接受 `amount: number` 类型的参数（例如，`0.1` 表示 0.1 ETH）

## 操作流程

### 1. 初始化 SDK

```typescript
import { Vultisig, MemoryStorage } from '@vultisig/sdk';

const sdk = new Vultisig({ storage: new MemoryStorage() });
await sdk.initialize();
```

> 代码来源：[`Vultisig.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/Vultisig.ts)

### 2. 创建 Fast Vault

分为两步：创建（触发电子邮件验证）然后验证。

```typescript
const vaultId = await sdk.createFastVault({
  name: 'my-agent-vault',
  email: 'agent@example.com',
  password: 'secure-password',
});

// Verify with the code sent to the email
const vault = await sdk.verifyVault(vaultId, '123456');
// Returns: FastVault instance — ready for operations
```

**风险提示：**
- 密码用于加密保险库份额。如果密码丢失，保险库将无法恢复。
- 必须提供电子邮件验证码——代理需要拥有电子邮件访问权限或使用电子邮件中继服务。

### 2b. 创建 Secure Vault（需要人工联合签名）

当代理在执行交易前需要人工批准时（例如高价值转账、资金操作、合规流程），请使用 Secure Vault。代理持有其中一个份额，人工持有另一个份额。人工通过 Vultisig 移动应用扫描二维码进行联合签名——只有双方同意后交易才会执行。

```typescript
const { vault, vaultId, sessionId } = await sdk.createSecureVault({
  name: 'agent-with-human-approval',
  onQRCodeReady: (qrPayload) => {
    // Display QR for the human co-signer to scan with Vultisig app
    displayQRCode(qrPayload);
  },
  onDeviceJoined: (deviceId, total, required) => {
    console.log(`Device joined: ${total}/${required}`);
  },
});
```

签名过程需要人工参与：

```typescript
const signature = await vault.sign(payload, {
  onQRCodeReady: (qr) => {
    // Human must scan this QR with Vultisig app to co-sign
    displayQRCode(qr);
  },
  onDeviceJoined: (id, total, required) => {
    console.log(`Signing: ${total}/${required} devices ready`);
  },
});
// Completes only when the human co-signer participates
```

> 代码来源：[`SecureVault.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/vault/SecureVault.ts)

**何时使用 Secure Vault 而不是 Fast Vault：**
- 交易金额超过风险阈值，需要人工批准
- 需要人工批准的财务或 DAO 操作
- 需要代理不能单方面行动的合规流程

### 3. 获取地址

```typescript
const ethAddress = await vault.address('Ethereum');
const btcAddress = await vault.address('Bitcoin');
const solAddress = await vault.address('Solana');

// All addresses at once
const allAddresses = await vault.addresses();
// Returns: Record<string, string>
```

> 代码来源：[`VaultBase.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/vault/VaultBase.ts)

链标识符使用 PascalCase 格式的字符串，与 `Chain` 枚举相匹配：`'Bitcoin'`、`'Ethereum'`、`'Solana'`、`'THORChain'`、`'Cosmos'`、`'Polygon'`、`'Arbitrum'`、`'Base'`、`'Avalanche'`、`'BSC'` 等。

> 完整的链列表：[`Chain.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/core/chain/Chain.ts)

### 4. 检查余额

```typescript
// Native chain balance
const ethBalance = await vault.balance('Ethereum');
// Returns Balance: {
//   amount: string,      // Raw amount in smallest unit
//   decimals: number,    // Chain decimals (18 for ETH)
//   symbol: string,      // "ETH"
//   chainId: string,
//   fiatValue?: number,  // USD value if available
// }

// Multiple chains
const allBalances = await vault.balances();
// Returns: Record<string, Balance>

// Force refresh (clears cache)
const fresh = await vault.updateBalance('Ethereum');
```

#### 代币余额（ERC-20、SPL 等）

```typescript
// Get a specific token balance by contract address
const usdcBalance = await vault.balance('Ethereum', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48');
// Returns Balance: { amount: "1000000", decimals: 6, symbol: "USDC", ... }

// Get all token balances on a chain
const ethTokens = await vault.tokenBalances('Ethereum');
// Returns: Token[] — all tokens with non-zero balances

// Include tokens when fetching multi-chain balances
const everything = await vault.balances(undefined, true); // includeTokens = true
```

**风险提示：**
- 原生余额和代币余额是分开查询的。`vault.balance('Ethereum')` 只返回 ETH 的余额，不包含 ERC-20 代币。
- 查询代币余额时需要提供合约地址作为 `tokenId` 参数。

### 5. 估算 gas 费用

```typescript
// Returns chain-specific gas info
const evmGas = await vault.gas('Ethereum');
// EvmGasInfo: { gasPrice, gasPriceGwei, maxFeePerGas, maxPriorityFeePerGas, gasLimit, estimatedCostUSD }

const utxoGas = await vault.gas('Bitcoin');
// UtxoGasInfo: { gasPrice, byteFee, estimatedCostUSD }

const cosmosGas = await vault.gas('Cosmos');
// CosmosGasInfo: { gasPrice, gas, estimatedCostUSD }
```

> 代码来源：[`VaultBase.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/vault/VaultBase.ts) — `gas<C extends Chain>(chain: C): Promise<GasInfoForChain<C>>`

### 6. 发送交易

三步流程：`prepareSendTx` → `sign` → `broadcastTx`

```typescript
// Step 1: Prepare keysign payload
const payload = await vault.prepareSendTx({
  coin: {
    chain: 'Ethereum',
    address: ethAddress,     // Sender address (from vault.address())
    decimals: 18,
    ticker: 'ETH',
  },
  receiver: '0xRecipientAddress...',
  amount: BigInt('100000000000000000'), // 0.1 ETH in wei
  memo: '',                             // Optional
});
// Returns: KeysignPayload

// Step 2: Sign (Fast Vault — VultiServer co-signs automatically)
const signature = await vault.sign(payload);
// Returns: Signature { signature: string, recovery?: number, format: 'DER' | 'ECDSA' | 'EdDSA' }

// Step 3: Broadcast
const txHash = await vault.broadcastTx({
  chain: 'Ethereum',
  keysignPayload: payload,
  signature: signature,
});
// Returns: string (transaction hash)

// Explorer URL
const url = Vultisig.getTxExplorerUrl('Ethereum', txHash);
```

> 代码来源：[`VaultBase.prepareSendTx()`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/vault/VaultBase.ts)，[`FastVault.sign()`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/vault/FastVault.ts)

**风险提示：**
- `amount` 应使用链的最小单位（ETH 为 wei，BTC 为 satoshi）。计算小数点位置错误会导致发送错误的金额。
- 必须始终验证接收者地址。交易是不可撤销的。
- 在发送前请检查 gas 费用估算，以避免交易失败。

#### 发送 ERC-20 / 代币

如果要发送代币而不是原生货币，请在 `coin` 对象中添加 `id` 字段（合约地址）：

```typescript
// Send 10 USDC on Ethereum
const tokenPayload = await vault.prepareSendTx({
  coin: {
    chain: 'Ethereum',
    address: ethAddress,
    decimals: 6,            // USDC has 6 decimals
    ticker: 'USDC',
    id: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // Token contract address
  },
  receiver: '0xRecipientAddress...',
  amount: BigInt('10000000'), // 10 USDC (6 decimals)
});

const sig = await vault.sign(tokenPayload);
const txHash = await vault.broadcastTx({
  chain: 'Ethereum',
  keysignPayload: tokenPayload,
  signature: sig,
});
```

**风险提示：**
- `id` 字段是代币的合约地址。如果没有这个字段，SDK 会将其视为原生货币转账。
- 使用代币的小数位数，而不是链的小数位数。例如，USDC 的小数位数为 6，WETH 为 18，WBTC 为 8。
- 发送者仍需要使用原生 ETH 或代币来支付交易费用。

### 7. 交换代币

四步流程：`getSwapQuote` → `prepareSwapTx` → `sign` → `broadcastTx`

```typescript
// Step 1: Get quote
const quote = await vault.getSwapQuote({
  fromCoin: {
    chain: 'Ethereum',
    address: ethAddress,
    decimals: 18,
    ticker: 'ETH',
  },
  toCoin: {
    chain: 'Ethereum',
    address: usdcAddress,
    decimals: 6,
    ticker: 'USDC',
    id: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // Token contract
  },
  amount: 0.1, // Human-readable (NOT bigint)
});
// Returns: SwapQuoteResult {
//   provider: string,
//   estimatedOutput: bigint,
//   estimatedOutputFiat?: number,
//   requiresApproval: boolean,
//   fees: SwapFees,
//   warnings: string[],
// }

// Step 2: Prepare swap transaction
const swapResult = await vault.prepareSwapTx({
  fromCoin: quote.fromCoin,
  toCoin: quote.toCoin,
  amount: 0.1,
  swapQuote: quote,
});
// Returns: SwapPrepareResult {
//   keysignPayload: KeysignPayload,
//   approvalPayload?: KeysignPayload,  // If token approval needed
//   quote: SwapQuoteResult,
// }

// Step 2.5: If approval required, sign and broadcast approval first
if (swapResult.approvalPayload) {
  const approvalSig = await vault.sign(swapResult.approvalPayload);
  await vault.broadcastTx({
    chain: 'Ethereum',
    keysignPayload: swapResult.approvalPayload,
    signature: approvalSig,
  });
}

// Step 3: Sign swap
const swapSig = await vault.sign(swapResult.keysignPayload);

// Step 4: Broadcast swap
const swapTxHash = await vault.broadcastTx({
  chain: 'Ethereum',
  keysignPayload: swapResult.keysignPayload,
  signature: swapSig,
});
```

**交换提供商**（自动选择最佳费率）：
- **THORChain** — 原生跨链交换（BTC <> ETH 等）
- **MayaChain** — 提供额外的跨链对
- **1inch** — EVM DEX 聚合服务
- **LiFi** — 跨链 + 跨 DEX 交换
- **KyberSwap** — EVM DEX 聚合服务

**风险提示：**
- 交换金额应使用人类可读的数字（例如 `0.1`），而不是 `bigint`。SDK 会处理小数转换。
- 在执行前请检查 `quote.warnings`，其中可能包含滑点或流动性警告。
- ERC-20 代币交换可能需要额外的批准交易（`approvalPayload`）。
- 跨链交换耗时较长（几分钟，而非几秒），且失败模式不同。

### 8. 导出 / 导入保险库

```typescript
// Export to encrypted .vult file
const { filename, data } = await vault.export('backup-password');
// filename: string, data: Base64-encoded vault backup

// Import from .vult file
const importedVault = await sdk.importVault(data, 'backup-password');
```

### 9. 通过种子短语创建保险库

```typescript
// Validate BIP39 seedphrase
const validation = await sdk.validateSeedphrase('word1 word2 ...');
// Returns: { valid: boolean, wordCount: number, error?: string }

// Discover which chains have existing balances
const discovery = await sdk.discoverChainsFromSeedphrase('word1 word2 ...');
// Returns: ChainDiscoveryAggregate

// Create Fast Vault from seedphrase (still needs email verification)
const vaultId = await sdk.createFastVaultFromSeedphrase({
  name: 'imported-vault',
  email: 'agent@example.com',
  password: 'secure-password',
  mnemonic: 'word1 word2 ...',
});
const vault = await sdk.verifyVault(vaultId, 'email-code');
```

**风险提示：**
- 使用种子短语会从种子生成一个新的 TSS 保险库——原有的基于种子的钱包仍然独立存在。
- 非常谨慎地处理种子短语。切勿记录、以明文形式存储或传输未加密的种子短语。

### 10. 保险库生命周期管理

```typescript
// List all vaults
const vaults = await sdk.listVaults();

// Set active vault
await sdk.setActiveVault(vault);

// Get active vault
const active = await sdk.getActiveVault();

// Check vault type
if (Vultisig.isFastVault(vault)) { /* FastVault methods */ }
if (Vultisig.isSecureVault(vault)) { /* SecureVault methods */ }

// Delete vault
await sdk.deleteVault(vault);
```

### 11. 检查交易状态

交易广播后，可以使用浏览器地址或特定链的方法来确认交易状态：

```typescript
// Get explorer URL for any chain
const explorerUrl = Vultisig.getTxExplorerUrl('Ethereum', txHash);
// e.g., "https://etherscan.io/tx/0x..."

const addressUrl = Vultisig.getAddressExplorerUrl('Bitcoin', btcAddress);
// e.g., "https://mempool.space/address/bc1..."
```

对于需要在下一步操作前确认完成情况的自动化策略，可以轮询余额或使用外部 RPC/indexer 来检查交易是否最终完成。SDK 不提供内置的交易状态查询功能——请使用 `vault.updateBalance()` 在广播后强制刷新数据，并在广播前后进行比较。

```typescript
// Pattern: confirm send completed
const balanceBefore = await vault.balance('Ethereum');
// ... broadcast transaction ...
await new Promise(r => setTimeout(r, 15000)); // Wait for block confirmation
const balanceAfter = await vault.updateBalance('Ethereum');
// Compare balanceBefore.amount vs balanceAfter.amount
```

### 12. 地址簿

用于管理自动转账的重复接收者：

```typescript
// Get saved addresses (optionally filter by chain)
const allContacts = await sdk.getAddressBook();
const ethContacts = await sdk.getAddressBook('Ethereum');

// Add entries
await sdk.addAddressBookEntry([
  { chain: 'Ethereum', address: '0x...', name: 'Treasury' },
  { chain: 'Bitcoin', address: 'bc1...', name: 'Cold Storage' },
]);

// Update a name
await sdk.updateAddressBookEntry('Ethereum', '0x...', 'Main Treasury');

// Remove entries
await sdk.removeAddressBookEntry([
  { chain: 'Ethereum', address: '0x...' },
]);
```

> 代码来源：[`Vultisig.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/sdk/src/Vultisig.ts)

### 13. $VULT 折扣等级

持有 $VULT 代币可以降低交换费用（最高可达 50%）。SDK 可以检查并更新代理的折扣等级：

```typescript
// Check current discount tier
const tier = await vault.getDiscountTier();
// Returns: string | null — e.g., "gold", "silver", or null if no discount

// Update tier (after acquiring more $VULT)
const newTier = await vault.updateDiscountTier();
```

> 代币合约：[`0xb788144DF611029C60b859DF47e79B7726C4DEBa`](https://etherscan.io/token/0xb788144DF611029C60b859DF47e79B7726C4DEBa)（Ethereum）

### 14. 监听事件

```typescript
// SDK-level events
sdk.on('vaultCreationProgress', (data) => { /* keygen progress */ });
sdk.on('vaultCreationComplete', (data) => { /* vault ready */ });
sdk.on('vaultChanged', (data) => { /* active vault switched */ });

// Vault-level events
vault.on('balanceUpdated', (data) => { /* balance changed */ });
vault.on('transactionSigned', (data) => { /* signature complete */ });
vault.on('transactionBroadcast', (data) => { /* tx submitted */ });
vault.on('signingProgress', (data) => { /* signing steps */ });
vault.on('swapQuoteReceived', (data) => { /* quote ready */ });

// SecureVault only (multi-device coordination)
vault.on('qrCodeReady', (data) => { /* show QR for device pairing */ });
vault.on('deviceJoined', (data) => { /* co-signer connected */ });
vault.on('allDevicesReady', (data) => { /* threshold met, signing can proceed */ });

// Error handling
vault.on('error', (error) => { /* handle errors */ });
sdk.on('error', (error) => { /* handle SDK-level errors */ });
```

> 代码来源：[`packages/sdk/src/events/`](https://github.com/vultisig/vultisig-sdk/tree/main/packages/sdk/src/events)

## 支持的区块链

> 代码来源：[`Chain.ts`](https://github.com/vultisig/vultisig-sdk/blob/main/packages/core/chain/Chain.ts)

| 类别 | 区块链 | 签名方式 |
|----------|--------|-----------|
| **UTXO** | Bitcoin、Litecoin、Dogecoin、Bitcoin Cash、Dash、Zcash | ECDSA |
| **EVM** | Ethereum、BSC、Polygon、Avalanche、Arbitrum、Optimism、Base、Blast、Cronos、zkSync、Hyperliquid、Mantle、Sei | ECDSA |
| **Cosmos/IBC** | THORChain、MayaChain、Cosmos Hub、Osmosis、Dydx、Kujira、Noble、Terra、Terra Classic、Akash | ECDSA |
| **其他** | Solana、Sui、Polkadot、TON、Ripple、Tron、Cardano | EdDSA / 混合签名方式 |

## 安全模型

- **不使用种子短语** — 保险库份额替代了传统的 12/24 个单词的种子短语
- **无单点故障** — 没有任何设备持有完整的私钥
- **不进行链上密钥注册** — 与多签名钱包不同
- **DKLS23 协议** — 采用三轮 TSS 签名机制，与 Silence Laboratories 共同开发
- **开源且经过审计**  
- 详情请参阅：[安全与技术文档](https://docs.vultisig.com/security-and-technology/security-technology)

## 命令行界面（CLI）选项

```bash
npm install -g @vultisig/sdk

vsig vault create --name agent-vault --type fast
vsig balance --chain Ethereum
vsig send --chain Ethereum --to 0x... --amount 0.1
vsig swap --from ETH --to USDC --amount 0.1
```

> 代码来源：[`clients/cli/`](https://github.com/vultisig/vultisig-sdk/tree/main/clients/cli)

## 逐步披露信息

- [SDK 用户指南](https://github.com/vultisig/vultisig-sdk/blob/main/docs/SDK-USERS-GUIDE.md) — 完整的 API 使用说明
- [架构文档](https://github.com/vultisig/vultisig-sdk/blob/main/docs/architecture/ARCHITECTURE.md) — SDK 内部结构、数据流、设计模式
- [代理集成指南](https://github.com/vultisig/vultisig-sdk/blob/main/docs/agent.md) — 代理特定的模式和最佳实践
- [Fast Vault 文档](https://docs.vultisig.com/infrastructure/what-is-vultisigner/how-does-vultisigner-work) — VultiServer 的联合签名机制
- [市场插件指南](https://docs.vultisig.com/developer-docs/marketplace/basics-quick-start) — 如何构建自动化插件
- [llms.txt](https://vultisig.com/llms.txt) — 适用于 Web 浏览器的简洁链接索引
- [llms-full.txt](https://vultisig.com/llms-full.txt) — 包含示例的详细文档