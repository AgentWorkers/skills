---
name: jb-v5-v51-contracts
description: |
  Juicebox V5 vs V5.1 contract version separation rules. Use when: (1) determining which
  contracts to use for a project, (2) versioned contracts show unexpected behavior,
  (3) transactions fail with "invalid terminal" or similar errors, (4) deploying new
  projects vs interacting with existing projects. CRITICAL: Versioned contracts must never mix.
---

# Juicebox V5 与 V5.1：合约版本分离

## 问题

Juicebox 有两个合约版本：V5（原始版本）和 V5.1（升级版本）。当一个合约同时存在这两个版本时，混合使用它们会导致交易失败。使用 `JBController5_1` 的项目必须使用 `JBMultiTerminal5_1`，而不能使用 V5 版本的终端。

## 背景/触发条件

- 部署新项目或终端时
- 交易因“无效终端”或权限错误而失败
- 查询规则集时返回意外数据
- 尽管地址正确，支付项目仍然失败
- 确定给定项目应使用哪个合约版本时遇到问题

## 解决方案

### 规则

**当一个合约同时具有 V5 和 V5.1 版本时，必须使用匹配的版本。**

仅具有一个版本（没有 `5_1` 变体的合约）可以与 V5 和 V5.1 版本的项目同时使用。

### 检测项目版本（至关重要）

**重要提示：** 一些非 revnet 项目也使用 V5.0 版本的合约。** 不能仅因为项目不是 revnet 就假设它使用的是 V5.1 版本。确定项目使用哪个合约的唯一可靠方法是查询 `JBDirectory.controllerOf()`。

**始终使用 `JBDirectory.controllerOf()` 来获取实际的控制器地址，然后与已知的 V5 和 V5.1 控制器地址进行比较。**

```typescript
const JB_DIRECTORY = '0x0061e516886a0540f63157f112c0588ee0651dcf'
const JB_CONTROLLER_V5 = '0x27da30646502e2f642be5281322ae8c394f7668a'
const JB_CONTROLLER_V5_1 = '0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1'

// Query JBDirectory for the project's controller
const controller = await publicClient.readContract({
  address: JB_DIRECTORY,
  abi: JB_DIRECTORY_ABI,
  functionName: 'controllerOf',
  args: [BigInt(projectId)],
})

// Determine version by comparing controller address
const isV5 = controller.toLowerCase() === JB_CONTROLLER_V5.toLowerCase()
const isV5_1 = controller.toLowerCase() === JB_CONTROLLER_V5_1.toLowerCase()

if (isV5) {
  // Use V5.0 contracts (JBMultiTerminal, JBRulesets, etc.)
} else if (isV5_1) {
  // Use V5.1 contracts (JBMultiTerminal5_1, JBRulesets5_1, etc.)
} else {
  // Unknown controller - handle edge case
}
```

**为什么不能仅通过所有者来判断？** 虽然 revnet 项目由 REVDeployer 拥有并且总是使用 V5.0 版本，但一些在 V5.1 之前部署的常规项目也使用 V5.0 版本。仅通过所有者来判断只能确定项目是否为 revnet，而不能确定它实际使用的是哪个合约版本。

### 合约地址参考

**通用合约（同时支持 V5 和 V5.1）**

| 合约 | 地址 |
|----------|---------|
| JBProjects | 0x885f707efa18d2cb12f05a3a8eba6b4b26c8c1d4 |
| JBTokens | 0x4d0edd347fb1fa21589c1e109b3474924be87636 |
| JBDirectory | 0x0061e516886a0540f63157f112c0588ee0651dcf |
| JBSplits | 0x7160a322fea44945a6ef9adfd65c322258df3c5e |
| JBFundAccessLimits | 0x3a46b21720c8b70184b0434a2293b2fdcc497ce7 |
| JBPermissions | 0xba948dab74e875b19cf0e2ca7a4546c0c2defc40 |
| JBPrices | 0x6e92e3b5ce1e7a4344c6d27c0c54efd00df92fb6 |
| JBFeelessAddresses | 0xf76f7124f73abc7c30b2f76121afd4c52be19442 |

**V5.1 合约（用于新项目）**

| 合约 | 地址 |
|----------|---------|
| JBController5_1 | 0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1 |
| JBMultiTerminal5_1 | 0x52869db3d61dde1e391967f2ce5039ad0ecd371c |
| JBRulesets5_1 | 0xd4257005ca8d27bbe11f356453b0e4692414b056 |
| JBTerminalStore5_1 | 0x82239c5a21f0e09573942caa41c580fa36e27071 |
| JBOmnichainDeployer5_1 | 0x587bf86677ec0d1b766d9ba0d7ac2a51c6c2fc71 |

**V5 合约（用于 revnet 项目）**

| 合约 | 地址 |
|----------|---------|
| JBController | 0x27da30646502e2f642be5281322ae8c394f7668a |
| JBMultiTerminal | 0x2db6d704058e552defe415753465df8df0361846 |
| JBRulesets | 0x6292281d69c3593fcf6ea074e5797341476ab428 |
| REVDeployer | 0x2ca27bde7e7d33e353b44c27acfcf6c78dde251d |

### 代码示例

```typescript
// Known controller addresses (same on all chains via CREATE2)
const CONTROLLERS = {
  V5: '0x27da30646502e2f642be5281322ae8c394f7668a',
  V5_1: '0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1',
}

// Versioned contracts by version
const VERSIONED_CONTRACTS = {
  V5: {
    controller: '0x27da30646502e2f642be5281322ae8c394f7668a',  // JBController
    terminal: '0x2db6d704058e552defe415753465df8df0361846',    // JBMultiTerminal
    rulesets: '0x6292281d69c3593fcf6ea074e5797341476ab428',    // JBRulesets
  },
  V5_1: {
    controller: '0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1',  // JBController5_1
    terminal: '0x52869db3d61dde1e391967f2ce5039ad0ecd371c',    // JBMultiTerminal5_1
    rulesets: '0xd4257005ca8d27bbe11f356453b0e4692414b056',    // JBRulesets5_1
  },
}

// Shared contracts work with any project
const SHARED = {
  directory: '0x0061e516886a0540f63157f112c0588ee0651dcf',
  splits: '0x7160a322fea44945a6ef9adfd65c322258df3c5e',
  fundAccessLimits: '0x3a46b21720c8b70184b0434a2293b2fdcc497ce7',
  projects: '0x885f707efa18d2cb12f05a3a8eba6b4b26c8c1d4',
  tokens: '0x4d0edd347fb1fa21589c1e109b3474924be87636',
}

// Helper to get correct contracts for a project
// ALWAYS queries JBDirectory.controllerOf() - the ONLY authoritative source
async function getContractsForProject(projectId: number): Promise<{
  controller: `0x${string}`,
  terminal: `0x${string}`,
  rulesets: `0x${string}`,
  version: 'V5' | 'V5_1',
}> {
  // Step 1: Query JBDirectory for the project's actual controller
  const controller = await publicClient.readContract({
    address: SHARED.directory,
    abi: JB_DIRECTORY_ABI,
    functionName: 'controllerOf',
    args: [BigInt(projectId)],
  })

  // Step 2: Determine version by comparing controller address
  const controllerLower = controller.toLowerCase()

  if (controllerLower === CONTROLLERS.V5.toLowerCase()) {
    return { ...VERSIONED_CONTRACTS.V5, version: 'V5' }
  }

  if (controllerLower === CONTROLLERS.V5_1.toLowerCase()) {
    return { ...VERSIONED_CONTRACTS.V5_1, version: 'V5_1' }
  }

  // Unknown controller - this shouldn't happen for valid Juicebox projects
  throw new Error(`Unknown controller ${controller} for project ${projectId}`)
}
```

### 使用 `Cast` 命令检查合约版本

```bash
# Get controller for a project - this is the authoritative source
cast call 0x0061e516886a0540f63157f112c0588ee0651dcf \
  "controllerOf(uint256)(address)" $PROJECT_ID --rpc-url $RPC_URL

# Compare result:
# 0x27da30646502e2f642be5281322ae8c394f7668a = V5.0
# 0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1 = V5.1
```

## 验证结果

- 支付交易成功，不会出现“无效终端”的错误
- 规则集查询返回预期数据
- 项目创建时使用正确的合约版本

## 示例

- 支付 NANA（项目 #1，一个 revnet）：
```bash
cast call 0x0061e516886a0540f63157f112c0588ee0651dcf "controllerOf(uint256)(address)" 1
# Returns: 0x27da30646502e2f642be5281322ae8c394f7668a (V5 controller)
# → Use V5 contracts: JBMultiTerminal 0x2db6d704058e552defe415753465df8df0361846
```

- 支付使用 V5.1 版本部署的项目：
```bash
cast call 0x0061e516886a0540f63157f112c0588ee0651dcf "controllerOf(uint256)(address)" 123
# Returns: 0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1 (V5.1 controller)
# → Use V5.1 contracts: JBMultiTerminal5_1 0x52869db3d61dde1e391967f2ce5039ad0ecd371c
```

## 注意事项

- **至关重要**：始终使用 `JBDirectory.controllerOf()` 来确定合约版本，切勿仅根据所有者来判断。
- 一些非 revnet 项目使用 V5.0 版本的合约（这些项目是在 V5.1 之前部署的）。
- 所有地址在所有链（Ethereum、Optimism、Base、Arbitrum）上都是统一的。
- JBOmnichainDeployer5_1 使用 V5.1 合约同时部署到所有链。
- 信息来源：[nana-core-v5/deployments](https://github.com/Bananapus/nana-core-v5/tree/main/deployments) 和 [docs.juicebox.money/dev/v5/addresses](https://docs.juicebox.money/dev/v5/addresses)

## 参考资料

- `JBDirectory`（用于查询控制器地址）：0x0061e516886a0540f63157f112c0588ee0651dcf
- V5 版本的 `JBController`：0x27da30646502e2f642be5281322ae8c394f7668a
- V5.1 版本的 `JBController`：0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1
- 官方文档：https://docs.juicebox.money/dev/v5/addresses