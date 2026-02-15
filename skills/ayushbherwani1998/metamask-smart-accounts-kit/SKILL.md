---
name: smart-accounts-kit
description: 使用 MetaMask 智能账户套件进行 Web3 开发。适用于用户需要使用 ERC-4337 智能账户构建去中心化应用（dApps）、执行用户操作、批量发送交易、配置签名者（如外部托管账户（EOA）、多签名（MultiSig）、通过支付管理器实现气体费用抽象（Gas Abstraction）、创建委托关系（Delegations），或请求高级权限（如 ERC-7715）的场景。该套件支持与 Viem 的集成，支持多种签名者类型（动态签名者、Web3Auth、Wagmi），支持无气体费用的交易（Gasless Transactions），并具备委托框架（Delegation Framework）功能。
metadata: {"openclaw":{"emoji":"🦊","homepage":"https://docs.metamask.io/smart-accounts-kit"}}
---
## 快速参考

本技能文件提供了对 MetaMask 智能账户套件（MetaMask Smart Accounts Kit）v0.3.0 的快速访问。如需详细信息，请参阅相应的参考文件。

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

- **实现类型**：
  - **混合型** (`Implementation.Hybrid`) - 持有者操作权限（EOA, EOA）+ 密码签名器
  - **多签名** (`Implementation.MultiSig`) - 需要达到一定签名人数的多签名机制
  - **Stateless7702** (`Implementation.Stateless7702`) - 基于 EIP-7702 升级的 EOA（无状态智能账户）

### 2. 委托框架（ERC-7710）

- 委托人向受托人授予权限：
  - **权限范围** - 初始授权（如交易限额、函数调用）
  - **注意事项** - 由智能合约执行的限制条件
  - **类型**：根委托（Root Delegation）、开放委托（Open Delegation）、重新委托（Redelegation）
  - **生命周期**：创建 → 签名 → 存储 → 提现

### 3. 高级权限（ERC-7715）

- 通过 MetaMask 扩展程序请求权限：
  - 提供人类可读的 UI 确认流程
  - 支持 ERC-20 标准和原生代币的权限管理
  - 需要 MetaMask Flask 13.5.0 或更高版本
  - 用户必须拥有智能账户

## 快速代码示例

- **创建智能账户**：```typescript
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
- **创建委托**：```typescript
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
- **签署委托**：```typescript
const signature = await smartAccount.signDelegation({ delegation })
const signedDelegation = { ...delegation, signature }
```
- **赎回委托**：```typescript
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
- **请求高级权限**：```typescript
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
- **赎回高级权限**：```typescript
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

### 智能账户相关：
- `toMetaMaskSmartAccount()` - 创建智能账户
- `aggregateSignature()` - 合并多签名者的签名
- `signDelegation()` - 签署委托
- `signUserOperation()` - 签署用户操作
- `signMessage()` / `signTypedData()` - 标准签名操作

### 委托相关：
- `createDelegation()` - 创建委托关系
- `createOpenDelegation()` - 创建开放委托
- `createCaveatBuilder()` - 构建权限限制数组
- `createExecution()` - 创建执行结构
- `redeemDelegations()` - 编码赎回所需的数据
- `signDelegation()` - 使用私钥签署委托
- `getSmartAccountsEnvironment()` - 获取智能账户环境信息
- `deploySmartAccountsEnvironment()` - 部署智能合约
- `overrideDeployedEnvironment()` - 覆盖已部署的环境设置

### 高级权限相关：
- `erc7715ProviderActions()` - 用于请求权限的钱包客户端扩展
- `requestExecutionPermissions()` - 请求执行权限
- `erc7710BundlerActions()` - 用于打包委托的扩展
- `sendUserOperationWithDelegation()` - 使用智能账户进行交易
- `erc7710WalletActions()` - 与钱包客户端相关的功能
- `sendTransactionWithDelegation()` - 使用 EOA 进行交易

## 支持的 ERC-7715 权限类型

### ERC-20 标准代币权限：
- `erc20-token-periodic` - 每个周期内的使用限额，限额会重置
- `erc20-token-streaming` - 每秒固定流量的使用限制

### 原生代币权限：
- `native-token-periodic` - 每个周期内的使用限额，限额会重置
- `native-token-streaming` - 每秒固定流量的使用限制

## 常见的委托权限范围

### 交易限额：
- `erc20TransferAmount` - 固定的 ERC-20 交易限额
- `erc20PeriodTransfer` - 每个周期内的 ERC-20 交易限额
- `erc20Streaming` - 每秒固定流量的 ERC-20 交易
- `nativeTokenTransferAmount` - 固定的原生代币交易限额
- `nativeTokenPeriodTransfer` - 每个周期内的原生代币交易限额
- `nativeTokenStreaming` - 每秒固定流量的原生代币交易

### 常见的权限限制类型

- **交易限额**：指定类型的交易金额限制
- **函数调用**：允许调用的具体函数或地址
- **权限范围**：定义可执行的操作类型

## 常见的权限执行器（Permission Enforcers）：

- **目标地址与方法限制**：限制可调用的目标地址和函数
- **数据验证**：验证传递的参数是否符合要求
- **执行细节**：确保执行操作符合预设条件
- **价值与代币限制**：限制交易金额或代币数量
- **时间与频率限制**：指定时间范围或交易频率
- **安全与状态检查**：限制交易行为或账户状态

### 合同地址（v1.3.0）：
- `EntryPoint`：合约入口地址（`0x0000000071727De22E5E9d8BAf0edAc6f37da032`）
- `SimpleFactory`：基础委托管理合约
- `DelegationManager`：委托管理合约
- `MultiSigDeleGatorImpl`：多签名委托实现
- `HybridDeleGatorImpl`：混合型委托实现

## 重要规则：

- **务必使用权限限制**：切勿创建无限制的委托关系
- **先部署委托者合约**：在赎回前必须先部署委托者合约
- **检查智能账户状态**：使用 ERC-7715 需要用户拥有智能账户

- **权限限制是累积的**：在多个委托链中，限制条件会叠加
- **函数调用默认设置**：v0.3.0 默认不允许使用原生代币
- **批量委托功能**：当前版本不支持兼容的批量委托执行器

### 其他要求：
- **系统要求**：MetaMask Flask 13.5.0 或更高版本，用户需拥有智能账户
- **多签名机制**：至少需要达到指定的签名人数
- **升级要求**：使用 Stateless7702 需要先完成 EIP-7702 的升级

## 常见使用场景：

- **示例 1：带有时间限制的 ERC-20 交易**：```typescript
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
- **示例 2：带有金额限制的函数调用**：```typescript
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
- **示例 3：周期性使用的原生代币**：```typescript
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
- **示例 4：委托链的交互流程**：```typescript
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

## 常见问题及解决方法：

- **账户未部署**：使用 `bundlerClient.sendUserOperation()` 进行部署
- **签名无效**：检查链 ID、委托管理合约和签名者的权限
- **权限执行失败**：核实权限参数和执行顺序
- **赎回失败**：检查委托人的余额、参数有效性及目标合约
- **ERC-7715 功能不可用**：升级 MetaMask 到 13.5.0 或更高版本，并确保用户拥有智能账户
- **权限被拒绝**：提供友好的错误处理机制或手动解决方案
- **签名人数不足**：为多签名委托增加更多签名者
- **EIP-7702 未升级**：确保已完成 EIP-7702 的升级

## 相关资源：
- **NPM 包**：`@metamask/smart-accounts-kit`
- **相关合约**：`metamask/delegation-framework@v1.3.0`
- **标准规范**：ERC-4337, ERC-7710, ERC-7715, ERC-7579
- **MetaMask Flask**：https://metamask.io/flask

## 版本信息：
- **技能工具包版本**：0.3.0
- **委托框架版本**：1.3.0
- **重要变更**：函数调用默认不允许使用原生代币

**如需详细文档，请查阅 `/references` 目录下的参考文件。**