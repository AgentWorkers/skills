---
name: smart-accounts-kit
description: 使用 MetaMask 智能账户套件进行 Web3 开发。适用于用户需要使用 ERC-4337 智能账户构建去中心化应用程序（dApps）、发送用户操作、批量执行交易、配置签名者（如外部账户（EOA）、密码短语（passkey）、多重签名（multisig）、实现与支付服务提供商（paymasters）相关的气体费用管理（gas abstraction）、创建委托关系（delegations），或请求高级权限（ERC-7715）的场景。该套件支持与 Viem 的集成，支持多种签名者类型（Dynamic、Web3Auth、Wagmi），支持无气体费用的交易（gasless transactions），并具备委托框架（Delegation Framework）功能。
metadata: {"openclaw":{"emoji":"🦊","homepage":"https://docs.metamask.io/smart-accounts-kit"}}
---
## 快速参考

本技能文件提供了对 MetaMask 智能账户套件（MetaMask Smart Accounts Kit）v0.3.0 的快速访问方式。如需详细信息，请参阅相应的参考文件。

**📚 详细参考文件：**

- [智能账户参考](./references/smart-accounts.md) - 账户创建、实现方式、签名器
- [委托参考](./references/delegations.md) - 委托生命周期、权限范围、注意事项
- [高级权限参考](./references/advanced-permissions.md) - 通过 MetaMask 实现的 ERC-7715 权限

## 包安装

```bash
npm install @metamask/smart-accounts-kit@0.3.0
```

对于自定义的权限执行器（permission enforcers）：

```bash
forge install metamask/delegation-framework@v1.3.0
```

## 核心概念总结

### 1. 智能账户（ERC-4337）

**三种实现类型：**

| 实现类型 | 适用对象 | 主要特性 |
|---------------|----------|-------------|
| **Hybrid** (`Implementation.Hybrid`) | 标准 dApp 用户 | 支持 EOA（Externally Owned Account）和 passkey 签名器，灵活性最高 |
| **MultiSig** (`Implementation.MultiSig`) | 财务管理/DAO 操作 | 基于阈值的安全性，兼容 Safe 协议 |
| **Stateless7702** (`Implementation.Stateless7702`) | 已拥有 EOA 的高级用户 | 保持原有地址，通过 EIP-7702 添加智能账户功能 |

**决策指南：**
- 为普通用户开发？ → 选择 Hybrid
- 需要财务管理或多方控制？ → 选择 MultiSig
- 需要在不更改地址的情况下升级现有 EOA？ → 选择 Stateless7702

### 2. 委托框架（ERC-7710）

**委托者向受托者授予权限：**

- **权限范围** - 初始权限（支出限制、函数调用）
- **注意事项** - 由智能合约强制执行
- **类型** - Root、open root、redelegation、open redelegation
- **生命周期** - 创建 → 签名 → 存储 → 回赎

### 3. 高级权限（ERC-7715）

**通过 MetaMask 扩展请求权限：**

- 提供人类可读的 UI 确认
- 支持 ERC-20 和原生代币权限
- 需要 MetaMask Flask 13.5.0 或更高版本
- 用户必须拥有智能账户

## 快速代码示例

### 创建智能账户

```typescript
import { Implementation, toMetaMaskSmartAccount } from '@metamask/smart-accounts-kit'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount('0x...')

const smartAccount = await toMetaMaskSmartAccount({
  client: publicClient,
  implementation: Implementation.Hybrid,
  deployParams: [account.address, [], [], []],
  deploySalt: '0x',
  signer: { account },
})
```

### 创建委托

```typescript
import { createDelegation } from '@metamask/smart-accounts-kit'
import { parseUnits } from 'viem'

const delegation = createDelegation({
  to: delegateAddress,
  from: delegatorSmartAccount.address,
  environment: delegatorSmartAccount.environment,
  scope: {
    type: 'erc20TransferAmount',
    tokenAddress: '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238',
    maxAmount: parseUnits('10', 6),
  },
  caveats: [
    { type: 'timestamp', afterThreshold: now, beforeThreshold: expiry },
    { type: 'limitedCalls', limit: 5 },
  ],
})
```

### 签署委托

```typescript
const signature = await smartAccount.signDelegation({ delegation })
const signedDelegation = { ...delegation, signature }
```

### 回赎委托

```typescript
import { createExecution, ExecutionMode } from '@metamask/smart-accounts-kit'
import { DelegationManager } from '@metamask/smart-accounts-kit/contracts'
import { encodeFunctionData, erc20Abi } from 'viem'

const callData = encodeFunctionData({
  abi: erc20Abi,
  args: [recipient, parseUnits('1', 6)],
  functionName: 'transfer',
})

const execution = createExecution({ target: tokenAddress, callData })

const redeemCalldata = DelegationManager.encode.redeemDelegations({
  delegations: [[signedDelegation]],
  modes: [ExecutionMode.SingleDefault],
  executions: [[execution]],
})

// Via smart account
const userOpHash = await bundlerClient.sendUserOperation({
  account: delegateSmartAccount,
  calls: [{ to: delegateSmartAccount.address, data: redeemCalldata }],
})

// Via EOA
const txHash = await delegateWalletClient.sendTransaction({
  to: environment.DelegationManager,
  data: redeemCalldata,
})
```

### 请求高级权限

```typescript
import { erc7715ProviderActions } from '@metamask/smart-accounts-kit/actions'

const walletClient = createWalletClient({
  transport: custom(window.ethereum),
}).extend(erc7715ProviderActions())

const grantedPermissions = await walletClient.requestExecutionPermissions([
  {
    chainId: chain.id,
    expiry: now + 604800,
    signer: {
      type: 'account',
      data: { address: sessionAccount.address },
    },
    permission: {
      type: 'erc20-token-periodic',
      data: {
        tokenAddress,
        periodAmount: parseUnits('10', 6),
        periodDuration: 86400,
        justification: 'Transfer 10 USDC daily',
      },
    },
    isAdjustmentAllowed: true,
  },
])
```

### 回赎高级权限

```typescript
// Smart account
import { erc7710BundlerActions } from '@metamask/smart-accounts-kit/actions'

const bundlerClient = createBundlerClient({
  client: publicClient,
  transport: http(bundlerUrl),
}).extend(erc7710BundlerActions())

const permissionsContext = grantedPermissions[0].context
const delegationManager = grantedPermissions[0].signerMeta.delegationManager

const userOpHash = await bundlerClient.sendUserOperationWithDelegation({
  publicClient,
  account: sessionAccount,
  calls: [
    {
      to: tokenAddress,
      data: calldata,
      permissionsContext,
      delegationManager,
    },
  ],
})

// EOA
import { erc7710WalletActions } from '@metamask/smart-accounts-kit/actions'

const walletClient = createWalletClient({
  account: sessionAccount,
  chain,
  transport: http(),
}).extend(erc7710WalletActions())

const txHash = await walletClient.sendTransactionWithDelegation({
  to: tokenAddress,
  data: calldata,
  permissionsContext,
  delegationManager,
})
```

## 主要 API 方法

### 智能账户

- `toMetaMaskSmartAccount()` - 创建智能账户
- `aggregateSignature()` - 合并多签名
- `signDelegation()` - 签署委托
- `signUserOperation()` - 签署用户操作
- `signMessage()` / `signTypedData()` - 标准签名操作

### 委托

- `createDelegation()` - 创建委托
- `createOpenDelegation()` - 创建开放委托
- `createCaveatBuilder()` - 创建权限规则数组
- `createExecution()` - 创建执行结构
- `redeemDelegations()` - 编码回赎参数
- `signDelegation()` - 使用私钥签名
- `getSmartAccountsEnvironment()` - 获取账户环境信息
- `deploySmartAccountsEnvironment()` - 部署智能合约
- `overrideDeployedEnvironment()` - 覆盖已部署的环境设置

### 高级权限

- `erc7715ProviderActions()` - 钱包客户端扩展，用于请求权限
- `requestExecutionPermissions()` - 请求执行权限
- `erc7710BundlerActions()` - 批量处理工具扩展
- `sendUserOperationWithDelegation()` - 使用智能账户进行回赎
- `erc7710WalletActions()` - 钱包客户端扩展
- `sendTransactionWithDelegation()` - 使用 EOA 进行回赎

## 支持的 ERC-7715 权限类型

### ERC-20 代币权限

| 权限类型 | 描述 |
|----------------|-------------|
| `erc20-token-periodic` | 每个周期的限额，周期结束时重置 |
| `erc20-token-stream` | 每秒固定流量的线性传输 |

### 原生代币权限

| 权限类型 | 描述 |
|----------------|-------------|
| `native-token-periodic` | 每个周期的 ETH 限额，周期结束时重置 |
| `native-token-stream` | 每秒固定流量的线性传输 |

## 常见委托权限范围

### 支出限制

| 权限范围 | 描述 |
|---------------------------| -----------------------------|
| `erc20TransferAmount` | 固定的 ERC-20 代币限额 |
| `erc20PeriodTransfer` | 每个周期的 ERC-20 代币限额 |
| `erc20Streaming` | 线性传输的 ERC-20 代币 |
| `nativeTokenTransferAmount` | 固定的原生代币限额 |
| `nativeTokenPeriodTransfer` | 每个周期的原生代币限额 |
| `nativeTokenStreaming` | 线性传输的原生代币 |

### 常见函数调用权限

| 权限范围 | 描述 |
|------------------- | ---------------------------------- |
| `functionCall` | 允许调用的具体方法/地址 |
| `ownershipTransfer` | 仅允许所有权转移 |

## 常见权限执行器

### 目标地址与方法限制

- `allowedTargets` - 限制可调用的地址
- `allowedMethods` - 限制可调用的方法
- `allowedCalldata` - 验证特定的调用数据
- `exactCalldata` / `exactCalldataBatch` - 确保调用数据完全匹配
- `exactExecution` / `exactExecutionBatch` | 确保执行操作完全匹配

### 价值与代币限制

- `valueLte` - 限制原生代币的价值
- `erc20TransferAmount` - 限制 ERC-20 代币的转移金额
- `erc20BalanceChange` | 验证 ERC-20 代币的余额变化
- `erc721Transfer` / `erc721BalanceChange` | ERC-721 代币的转移限制
- `erc1155BalanceChange` | ERC-1155 代币的余额变化

## 时间与频率限制

- `timestamp` - 有效的时间范围（秒）
- `blockNumber` | 有效区块范围
- `limitedCalls` - 限制回赎次数
- `erc20PeriodTransfer` / `erc20Streaming` - 基于时间的 ERC-20 代币转移
- `nativeTokenPeriodTransfer` / `nativeTokenStreaming` | 基于时间的原生代币转移

## 安全性与状态限制

- `redeemer` - 限制回赎的接收地址
- `id` - 带有唯一标识符的委托
- `nonce` - 通过 nonce 进行批量撤销
- `deployed` - 自动部署合约
- `ownershipTransfer` | 仅允许所有权转移
- `nativeTokenPayment` | 要求支付
- `nativeBalanceChange` | 验证原生代币的余额
- `multiTokenPeriod` | 多种代币的周期限制

## 执行模式

| 模式 | 链路 | 处理方式 | 失败时处理方式 |
| --------------- | -------- | ----------- | ---------- |
| `SingleDefault` | 单次执行 | 顺序执行 | 回滚 |
| `SingleTry` | 单次执行 | 顺序执行 | 继续执行 |
| `BatchDefault` | 多次执行 | 交错执行 | 回滚 |
| `BatchTry` | 多次执行 | 交错执行 | 继续执行 |

## 合同地址（v1.3.0）

### 核心合约

| 合同名称 | 地址                                      |
| --------------------- | -------------------------------------------- |
| EntryPoint            | `0x0000000071727De22E5E9d8BAf0edAc6f37da032` |
| SimpleFactory         | `0x69Aa2f9fe1572F1B640E1bbc512f5c3a734fc77c` |
| DelegationManager     | `0xdb9B1e94B5b69Df7e401DDbedE43491141047dB3` |
| MultiSigDeleGatorImpl | `0x56a9EdB16a0105eb5a4C54f4C062e2868844f3A7` |
| HybridDeleGatorImpl   | `0x48dBe696A4D990079e039489bA2053B36E8FFEC4` |

## 重要规则

### 必须遵守的规则

1. **始终使用权限规则** - 绝不要创建无限制的委托
2. **先部署委托者合约** - 在回赎之前必须先部署委托者合约
3. **检查智能账户状态** - 使用 ERC-7715 需要用户拥有智能账户

### 行为规则

4. **权限规则是累积的** - 在委托链中，限制会逐层叠加
5. **函数调用默认设置** - v0.3.0 默认不允许使用原生代币（使用 `valueLte`）
6. **批量模式权限规则** - 当前没有兼容的权限执行器

### 系统要求

7. **ERC-7715 要求** - 需要 MetaMask Flask 13.5.0 或更高版本，以及智能账户
8. **多签名要求** - 需要至少指定数量的签名者
9. **7702 升级** - 使用 Stateless7702 需要先升级 EIP-7702

## 高级使用模式

### 并行用户操作（Nonce 钥匙）

智能账户使用 256 位的 nonce 结构：192 位用于标识键，64 位用于生成序列号。每个唯一键都有独立的序列号，从而支持并行执行。这对于后台服务同时处理多个委托非常重要。

#### 安装权限管理库

为了正确处理 nonce，需要与智能账户套件一起安装权限管理库（permissionless SDK）：

```bash
npm install permissionless
```

#### 并行 nonce 的工作原理

ERC-4337 使用一个 uint256 类型的 nonce：
- **192 位** 用于标识键
- **64 位** 用于生成序列号

每个键都有独立的序列号，因此使用不同键的用户操作可以并行执行，无需排序。

#### 使用权限管理库获取 nonce

```typescript
import { getAccountNonce } from 'permissionless'
import { entryPoint07Address } from 'viem/account-abstraction'

// Get nonce for a specific key
const parallelNonce = await getAccountNonce(publicClient, {
  address: smartAccount.address,
  entryPointAddress: entryPoint07Address,
  key: BigInt(Date.now()), // Unique key for parallel execution
})

const userOpHash = await bundlerClient.sendUserOperation({
  account: smartAccount,
  calls: [redeemCalldata],
  nonce: parallelNonce, // Properly encoded 256-bit nonce
})
```

#### 并行执行模式

```typescript
import { getAccountNonce } from 'permissionless'
import { entryPoint07Address } from 'viem/account-abstraction'

// Execute multiple redemption UserOps in parallel
const redeems = await Promise.all(
  delegations.map(async (delegation, index) => {
    // Generate unique key for this operation
    const nonceKey = BigInt(Date.now()) + BigInt(index * 1000)
    
    // Get properly encoded nonce for this key
    const nonce = await getAccountNonce(publicClient, {
      address: backendSmartAccount.address,
      entryPointAddress: entryPoint07Address,
      key: nonceKey,
    })
    
    const redeemCalldata = DelegationManager.encode.redeemDelegations({
      delegations: [[delegation]],
      modes: [ExecutionMode.SingleDefault],
      executions: [[execution]],
    })
    
    return bundlerClient.sendUserOperation({
      account: backendSmartAccount,
      calls: [{ to: backendSmartAccount.address, data: redeemCalldata }],
      nonce, // Parallel execution enabled via unique key
    })
  })
)
```

#### 不使用权限管理库（手动方式）

EntryPoint 合同将 nonce 编码为：`sequence | (key << 64)`

如果不使用权限管理库，请手动编码 nonce：

```typescript
// EntryPoint: nonceSequenceNumber[sender][key] | (uint256(key) << 64)
const key = BigInt(Date.now())
const sequence = 0n // New key starts at sequence 0
const nonce = sequence | (key << 64n)
// Or equivalently: (key << 64n) | sequence
```

**注意：** 建议使用 `getAccountNonce` 方法，因为它可以：
- 从 EntryPoint 获取当前 key 的序列号
- 正确编码 256 位的 nonce 值
- 处理边缘情况和验证问题

#### 关键点

- **不同键 = 并行执行** — 不同键的执行顺序不可预测
- **相同键 = 顺序执行** — 同一键的序列号会按顺序递增
- **应用场景**：后台回赎服务、定期投资（DCA）应用、高频交易、批量操作
- **nonce 生成**：`getAccountNonce` 会正确生成完整的 256 位 nonce

#### 常见错误

| 错误 | 结果 |
|---------|--------|
| 重复使用相同的 nonce | 导致顺序执行（违背并行执行的目的） |
| 不使用 `Date.now()` 生成 nonce | 如果多个操作同时执行，可能导致冲突 |
| 不使用 `getAccountNonce` | 可能无法获取当前序列号，导致操作失败 |
| 假设操作有固定顺序 | 会导致依赖操作出现竞争条件 |

#### 错误处理

```typescript
const results = await Promise.allSettled(redeems)

results.forEach((result, index) => {
  if (result.status === 'rejected') {
    // Check for specific errors
    if (result.reason.message?.includes('AA25')) {
      console.error(`Nonce collision for op ${index}`)
    }
    // Handle or retry
  }
})
```

### 后端委托回赎

**适用于服务器端自动化场景（如 DCA 机器人、托管服务、自动交易）：**

```typescript
// 1. Backend creates its own smart account as delegate
const backendAccount = await toMetaMaskSmartAccount({
  client: publicClient,
  implementation: Implementation.Hybrid,
  deployParams: [backendOwner.address, [], [], []],
  deploySalt: '0x',
  signer: { account: backendOwner },
})

// 2. Backend redeems by sending UserOp FROM its account
const userOpHash = await bundlerClient.sendUserOperation({
  account: backendAccount,
  calls: [{
    to: backendAccount.address,
    data: DelegationManager.encode.redeemDelegations({
      delegations: [[userDelegation]],
      modes: [ExecutionMode.SingleDefault],
      executions: [[swapExecution]],
    })
  }],
})
```

**应用场景：** 自动化美元成本平均（DCA）机器人根据市场信号或预定时间间隔回赎委托。

### 反事实账户部署

在回赎委托之前，必须先部署委托者账户。DelegationManager 会使用 `0xb9f0f171` 代码来处理反事实账户。

**解决方案：** 通过首次用户操作（UserOp）自动部署账户：

```typescript
// Build redemption calldata
const redeemCalldata = DelegationManager.encode.redeemDelegations({
  delegations: [[signedDelegation]],
  modes: [ExecutionMode.SingleDefault],
  executions: [[execution]],
})

// First redemption deploys the account automatically via initCode
const userOpHash = await bundlerClient.sendUserOperation({
  account: smartAccount, // Will deploy if counterfactual
  calls: [{
    to: smartAccount.address,
    data: redeemCalldata,
    value: 0n,
  }],
})
```

### 用于 AI 代理的会话账户

对于自动化服务，会话账户作为独立的签名器，只能在授权的委托范围内操作。私钥可以临时生成，存储在环境变量中，或通过 HSM/服务器钱包管理：

```typescript
// Session account created from various sources
const sessionAccount = privateKeyToAccount(
  process.env.SESSION_KEY || generatePrivateKey() || hsmWallet.key
)

// Request delegation from user to session account
const delegation = createDelegation({
  to: sessionAccount.address,
  from: userSmartAccount.address,
  environment,
  scope: { type: 'erc20TransferAmount', tokenAddress, maxAmount: parseUnits('100', 6) },
  caveats: [
    { type: 'timestamp', afterThreshold: now, beforeThreshold: expiry },
    { type: 'limitedCalls', limit: 10 },
  ],
})
// Session account can only act within delegation constraints
```

## 常见使用模式

### 模式 1：带时间限制的 ERC-20 代币

```typescript
const delegation = createDelegation({
  to: delegate,
  from: delegator,
  environment,
  scope: {
    type: 'erc20TransferAmount',
    tokenAddress,
    maxAmount: parseUnits('100', 6),
  },
  caveats: [
    { type: 'timestamp', afterThreshold: now, beforeThreshold: expiry },
    { type: 'limitedCalls', limit: 10 },
    { type: 'redeemer', redeemers: [delegate] },
  ],
})
```

### 模式 2：带金额限制的函数调用

```typescript
const delegation = createDelegation({
  to: delegate,
  from: delegator,
  environment,
  scope: {
    type: 'functionCall',
    targets: [contractAddress],
    selectors: ['transfer(address,uint256)'],
    valueLte: { maxValue: parseEther('0.1') },
  },
  caveats: [{ type: 'allowedMethods', selectors: ['transfer(address,uint256)'] }],
})
```

### 模式 3：定期转移原生代币

```typescript
const delegation = createDelegation({
  to: delegate,
  from: delegator,
  environment,
  scope: {
    type: 'nativeTokenPeriodTransfer',
    periodAmount: parseEther('0.01'),
    periodDuration: 86400,
    startDate: now,
  },
})
```

### 模式 4：委托链

```typescript
// Alice → Bob (100 USDC)
const aliceToBob = createDelegation({
  to: bob,
  from: alice,
  environment,
  scope: { type: 'erc20TransferAmount', tokenAddress, maxAmount: parseUnits('100', 6) },
})

// Bob → Carol (50 USDC, subset of authority)
const bobToCarol = createDelegation({
  to: carol,
  from: bob,
  environment,
  scope: { type: 'erc20TransferAmount', tokenAddress, maxAmount: parseUnits('50', 6) },
  parentDelegation: aliceToBob,
  caveats: [{ type: 'timestamp', afterThreshold: now, beforeThreshold: expiry }],
})
```

## 故障排查与快速修复

| 问题 | 解决方案 |
|------------------------| ------------------------------------------------------------|
| 账户未部署 | 使用 `bundlerClient.sendUserOperation()` 进行部署 |
| 签名无效 | 验证链 ID、委托管理器、签名器权限 |
| 权限规则被撤销 | 检查权限规则参数是否与执行操作匹配 |
| 回赎失败 | 检查委托者余额、调用数据有效性、目标合约 |
| ERC-7715 无法使用 | 升级到 MetaMask Flask 13.5.0 或更高版本，并确保用户拥有智能账户 |
| 权限被拒绝 | 优雅地处理错误，提供手动解决方案 |
| 达不到阈值 | 增加多签名者的数量 |
| 7702 无法使用 | 确保已通过 EIP-7702 升级 EOA |

## 错误代码参考

MetaMask 委托框架合约（v1.3.0）的错误代码。可以使用 [calldata.swiss-knife.xyz](https://calldata.swiss-knife.xyz/decoder) 等工具解码错误签名。

### DelegationManager 的错误代码（已验证）

| 错误代码 | 错误名称 | 含义 |
|------------|-----------|---------|
| `0xb5863604` | `InvalidDelegate()` | 调用者不是委托者 |
| `0xb9f0f171` | `InvalidDelegator()` | 调用者不是委托者 |
| `0x05baa052` | `CannotUseADisabledDelegation()` | 尝试回赎已被禁用的委托 |
| `0xded4370e` | `InvalidAuthority()` | 委托链权限验证失败 |
| `0x1bcaf69f` | `BatchDataLengthMismatch()` | 批量数据长度不匹配 |
| `0x005ecddb` | `AlreadyDisabled()` | 委托已被禁用 |
| `0xf2a5f75a` | `AlreadyEnabled()` | 委托已被启用 |
| `0xf645eedf` | `ECDSAInvalidSignature()` | ECDSA 签名格式无效 |
| `0xfce698f7` | `ECDSAInvalidSignatureLength(uint256)` | 签名长度不正确 |
| `0xd78bce0c` | `ECDSAInvalidSignatureS(bytes32)` | 签名 S 值无效 |
| `0xac241e11` | `EmptySignature()` | 签名为空 |
| `0xd93c0665` | `EnforcedPause()` | 合约处于暂停状态 |
| `0x3db6791c` | `InvalidEOASignature()` | EOA 签名验证失败 |
| `0x155ff427` | `InvalidERC1271Signature()` | ERC-1271 智能合约签名失败 |
| `0x118cdaa7` | `OwnableUnauthorizedAccount(address)` | 尝试操作未被授权的账户 |
| `0x1e4fbdf7` | `OwnableInvalidOwner(address)` | 所有权转移操作中的无效所有者地址 |
| `0xf6b6ef5b` | `InvalidShortString()` | 字符串参数太短 |
| `0xaa0ea2d8` | `StringTooLong(string)` | 字符串参数超过最大长度 |

### DeleGatorCore 的错误代码（已验证）

| 错误代码 | 错误名称 | 含义 |
|------------|-----------|---------|
| `0xd663742a` | `NotEntryPoint()` | 调用者不是 EntryPoint 合同 |
| `0x0796d945` | `NotEntryPointOrSelf()` | 调用者既不是 EntryPoint 也不是当前合约 |
| `0x1a4b3a04` | `NotDelegationManager()` | 调用者不是 DelegationManager |
| `0xb96fcfe4` | `UnsupportedCallType(bytes1)` | 不支持的调用类型 |
| `0x1187dc06` | `UnsupportedExecType(bytes1)` | 不支持的执行类型 |
| `0x29c3b7ee` | `NotSelf()` | 调用者不是当前合约 |

### 常见权限执行器错误（回滚信息）

| 错误信息 | 含义 |
|--------------|---------|
| `AllowedTargetsEnforcer:target-address-not-allowed` | 目标合约不在允许的列表中 |
| `AllowedTargetsEnforcer:invalid-terms-length` | 权限条款长度不是 20 字节 |
| `ERC20TransferAmountEnforcer:invalid-terms-length` | 权限条款长度必须为 52 字节 |
| `ERC20TransferAmountEnforcer:invalid-contract` | 目标合约与允许的代币类型不匹配 |
| `ERC20TransferAmountEnforcer:invalid-method` | 调用的方法不是 `transfer` |
| `ERC20TransferAmountEnforcer:allowance-exceeded` | 转移金额超过限制 |
| `CaveatEnforcer:invalid-call-type` | 必须使用单一的调用类型 |
| `CaveatEnforcer:invalid-execution-type` | 必须使用默认的执行类型 |

### 生产环境中常见的错误

**`0xb5863604` — InvalidDelegate()**
- **原因：** 调用者与委托中的地址不匹配
- **解决方法：** 确保 `msg.sender` 与委托中的 `to` 地址一致

**`0xb9f0f171` — InvalidDelegator()**
- **原因：** 试图从错误的地址启用/禁用委托，或尝试操作反事实账户
- **解决方法：** 只有委托者才能启用/禁用委托；对于反事实账户，需要先通过 UserOp 自动部署

**`0x05baa052` — CannotUseADisabledDelegation()**
- **原因：** 委托已被委托者禁用
- **解决方法：** 要求委托者重新启用委托，或使用其他委托方式

**`0xded4370e` — InvalidAuthority()**
- **原因：** 委托链结构错误（委托链顺序错误）
- **解决方法：** 确保委托链的顺序正确（从叶子节点到根节点）

**`0x1bcaf69f` — BatchDataLengthMismatch()**
- **原因：** `redeemDelegations` 调用中的数组长度不匹配 |
- **解决方法：** 确保 `permissionContexts`、`modes`、`executionCallDatas` 的长度一致

## 资源

- **NPM 包：`@metamask/smart-accounts-kit` |
- **相关合约：`metamask/delegation-framework@v1.3.0` |
- **ERC 标准：** ERC-4337、ERC-7710、ERC-7715、ERC-7579 |
- **MetaMask Flask：** https://metamask.io/flask

## 版本信息

- **工具包版本：** 0.3.0
- **委托框架版本：** 1.3.0
- **重要变更：** 函数调用默认不支持原生代币转移

---

**如需详细文档，请参阅 `/references` 目录下的参考文件。**