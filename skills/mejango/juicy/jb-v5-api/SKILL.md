---
name: jb-v5-api
description: Juicebox V5 协议 API 参考：包含所有合约的函数签名、参数及返回值。适用于查询“有哪些函数？”以及“函数的签名是什么？”等问题。如需了解内部实现机制和权衡因素，请参考 /jb-v5-impl。
---

# Juicebox V5 API 参考

本文档涵盖了 Juicebox V5 协议生态系统中所有函数的签名、参数及返回值。

> **注意**：如需深入了解实现细节、边缘情况或权衡因素，请参考 `/jb-v5-impl`。

## 协议架构概述

V5 协议由多个相互连接的仓库组成：

| 仓库 | 功能 |
|------------|---------|
| **nana-core-v5** | 核心基础设施：项目、规则集、代币、终端 |
| **nana-suckers-v5** | 通过 Merkle 证明实现跨链代币桥接 |
| **nana-buyback-hook-v5** | 集成 Uniswap V3 代币回购功能 |
| **nana-swap-terminal-v5** | 接受任何代币，并自动兑换为 ETH |
| **nana-721-hook-v5** | 支持基于支付的分层 NFT 发行 |
| **nana-permission-ids-v5** | 权限 ID 常量 |
| **nana-ownable-v5** | 支持 Juicebox 的所有权模型 |
| **nana-omnichain-deployers-v5** | 支持多链项目部署 |
| **revnet-core-v5** | 自主管理的代币化资金库网络 |
| **croptop-core-v5** | 公开 NFT 发布功能 |

---

## NANA-CORE-V5：核心协议

### 合同层

**核心合约**（状态管理）：
- `JBProjects` - ERC-721 项目所有权管理
- `JBRulesets` - 基于时间的配置队列管理
- `JBTokens` - 信用与 ERC-20 代币管理
- `JBDirectory` - 终端与控制器的映射管理
- `JBPermissions` - 访问控制权限管理
- `JBFundAccessLimits` - 提取限制管理
- `JBPrices` - 货币价格信息管理
- `JBSplits` - 支付分配列表管理

**用户入口合约**：
- `JBController` - 规则集与代币协调管理
- `JBMultiTerminal` - 支付、提现、分配管理
- `JBTerminalStore` - 交易记录管理

**辅助合约**：
- `JBDeadline` - 规则集提前审批功能
- `JBERC20` - 标准项目代币管理
- `JBFeelessAddresses` - 免费地址注册管理
- `JBChainlinkV3PriceFeed` - Chainlink 数据集成管理

---

### JBController 功能

#### 项目生命周期

```solidity
// Create a new project with initial rulesets
function launchProjectFor(
    address owner,                              // Receives project NFT
    string calldata projectUri,                 // IPFS metadata URI
    JBRulesetConfig[] calldata rulesetConfigurations,
    JBTerminalConfig[] calldata terminalConfigurations,
    string calldata memo
) external returns (uint256 projectId);

// Queue rulesets for existing project (first time setup)
function launchRulesetsFor(
    uint256 projectId,
    JBRulesetConfig[] calldata rulesetConfigurations,
    JBTerminalConfig[] calldata terminalConfigurations,
    string calldata memo
) external returns (uint256 rulesetId);

// Add rulesets to end of queue
function queueRulesetsOf(
    uint256 projectId,
    JBRulesetConfig[] calldata rulesetConfigurations,
    string calldata memo
) external returns (uint256 rulesetId);

// Migrate to a different controller
function migrate(uint256 projectId, IERC165 to) external;
```

#### 代币操作

```solidity
// Mint tokens to beneficiary
function mintTokensOf(
    uint256 projectId,
    uint256 tokenCount,
    address beneficiary,
    string calldata memo,
    bool useReservedPercent    // Apply reserved rate?
) external returns (uint256 beneficiaryTokenCount);

// Burn tokens from holder
function burnTokensOf(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    string calldata memo
) external;

// Deploy ERC-20 for project (enables token claiming)
function deployERC20For(
    uint256 projectId,
    string calldata name,
    string calldata symbol,
    bytes32 salt              // For deterministic address
) external returns (IJBToken token);

// Convert credits to ERC-20 tokens
function claimTokensFor(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    address beneficiary
) external;

// Transfer credits between addresses
function transferCreditsFrom(
    address holder,
    uint256 projectId,
    address recipient,
    uint256 creditCount
) external;

// Distribute pending reserved tokens
function sendReservedTokensToSplitsOf(uint256 projectId)
    external returns (uint256);
```

#### 配置管理

```solidity
// Update project metadata URI
function setUriOf(uint256 projectId, string calldata uri) external;

// Set project's ERC-20 token
function setTokenFor(uint256 projectId, IJBToken token) external;

// Update split groups
function setSplitGroupsOf(
    uint256 projectId,
    uint256 rulesetId,
    JBSplitGroup[] calldata splitGroups
) external;

// Add price feed for currency conversion
function addPriceFeed(
    uint256 projectId,
    uint256 pricingCurrency,
    uint256 unitCurrency,
    IJBPriceFeed feed
) external;
```

#### 查看功能

```solidity
function currentRulesetOf(uint256 projectId)
    external view returns (JBRuleset, JBRulesetMetadata);

function upcomingRulesetOf(uint256 projectId)
    external view returns (JBRuleset, JBRulesetMetadata);

function latestQueuedRulesetOf(uint256 projectId)
    external view returns (JBRuleset, JBRulesetMetadata, JBApprovalStatus);

function getRulesetOf(uint256 projectId, uint256 rulesetId)
    external view returns (JBRuleset, JBRulesetMetadata);

function allRulesetsOf(uint256 projectId, uint256 startingId, uint256 size)
    external view returns (JBRulesetWithMetadata[]);

function totalTokenSupplyWithReservedTokensOf(uint256 projectId)
    external view returns (uint256);

function setTerminalsAllowed(uint256 projectId) external view returns (bool);
function setControllerAllowed(uint256 projectId) external view returns (bool);
```

---

### JBTokens 功能

管理项目代币的账务，包括未领取的信用余额和 ERC-20 代币。

#### 代币部署

```solidity
// Deploy standard JBERC20 for a project
function deployERC20For(
    uint256 projectId,
    string calldata name,
    string calldata symbol,
    bytes32 salt              // For deterministic address (0 for non-deterministic)
) external returns (IJBToken token);

// Set a custom ERC20 as the project token
function setTokenFor(
    uint256 projectId,
    IJBToken token            // Must implement IJBToken interface
) external;
```

#### 代币操作

```solidity
// Mint tokens to a holder (called by controller)
function mintFor(
    address holder,
    uint256 projectId,
    uint256 count
) external;

// Burn tokens from a holder (called by controller)
function burnFrom(
    address holder,
    uint256 projectId,
    uint256 count
) external;

// Convert credits to ERC20 tokens
function claimTokensFor(
    address holder,
    uint256 projectId,
    uint256 count,
    address beneficiary
) external;

// Transfer credits between addresses
function transferCreditsFrom(
    address holder,
    uint256 projectId,
    address recipient,
    uint256 count
) external;
```

#### 查看功能

```solidity
// Get the ERC20 token for a project (address(0) if credits-only)
function tokenOf(uint256 projectId) external view returns (IJBToken);

// Get the project ID for a token
function projectIdOf(IJBToken token) external view returns (uint256);

// Get credit balance for a holder
function creditBalanceOf(address holder, uint256 projectId) external view returns (uint256);

// Get total credit supply for a project
function totalCreditSupplyOf(uint256 projectId) external view returns (uint256);

// Get total balance (credits + ERC20) for a holder
function totalBalanceOf(address holder, uint256 projectId) external view returns (uint256);

// Get total supply (credits + ERC20) for a project
function totalSupplyOf(uint256 projectId) external view returns (uint256);
```

#### IJBToken 接口（针对自定义代币）

自定义代币必须实现此接口：

```solidity
interface IJBToken is IERC20 {
    // Standard ERC20 functions (name, symbol, decimals, totalSupply, balanceOf, transfer, etc.)

    /// @notice Check if this token can be added to a project.
    /// @dev Must return true for setTokenFor() to succeed.
    function canBeAddedTo(uint256 projectId) external view returns (bool);

    /// @notice Mint tokens. Called by JBTokens on payments.
    function mint(address holder, uint256 amount) external;

    /// @notice Burn tokens. Called by JBTokens on cash outs.
    function burn(address holder, uint256 amount) external;
}
```

#### 自定义代币要求

| 要求 | 详情 |
|-------------|---------|
| **18 位小数** | `decimals()` 方法必须返回 18 位小数 |
| **canBeAddedTo** | 对于目标项目 ID，必须返回 true |
| **唯一分配** | 代币不能被分配给多个项目 |
| **控制器访问** | JBController 必须能够铸造/销毁代币 |

---

### JBMultiTerminal 功能

#### 支付管理

```solidity
// Pay a project
function pay(
    uint256 projectId,
    address token,              // address(0) for native
    uint256 amount,
    address beneficiary,        // Receives minted tokens
    uint256 minReturnedTokens,  // Slippage protection
    string calldata memo,
    bytes calldata metadata     // Hook data
) external payable returns (uint256 beneficiaryTokenCount);

// Add funds without minting tokens
function addToBalanceOf(
    uint256 projectId,
    address token,
    uint256 amount,
    bool shouldReturnHeldFees,
    string calldata memo,
    bytes calldata metadata
) external payable;
```

#### 提现（赎回）

```solidity
// Cash out tokens for funds
function cashOutTokensOf(
    address holder,
    uint256 projectId,
    uint256 cashOutCount,       // Tokens to burn
    address tokenToReclaim,     // Which token to receive
    uint256 minTokensReclaimed, // Slippage protection
    address payable beneficiary,
    bytes calldata metadata
) external returns (uint256 reclaimAmount);
```

#### 分配管理

```solidity
// Send payouts to splits (within payout limit)
function sendPayoutsOf(
    uint256 projectId,
    address token,
    uint256 amount,
    uint256 currency,
    uint256 minTokensPaidOut
) external returns (uint256 amountPaidOut);

// Use surplus allowance (discretionary withdrawal)
function useAllowanceOf(
    uint256 projectId,
    address token,
    uint256 amount,
    uint256 currency,
    uint256 minTokensPaidOut,
    address payable beneficiary,
    address payable feeBeneficiary,
    string calldata memo
) external returns (uint256 netAmountPaidOut);
```

#### 终端管理

```solidity
// Add token accounting contexts
function addAccountingContextsFor(
    uint256 projectId,
    JBAccountingContext[] calldata accountingContexts
) external;

// Migrate to new terminal
function migrateBalanceOf(
    uint256 projectId,
    address token,
    IJBTerminal to
) external returns (uint256 balance);

// Process held fees
function processHeldFeesOf(
    uint256 projectId,
    address token,
    uint256 count
) external;
```

#### 查看功能

```solidity
function currentSurplusOf(
    uint256 projectId,
    JBAccountingContext[] memory accountingContexts,
    uint256 decimals,
    uint256 currency
) external view returns (uint256);

function accountingContextsOf(uint256 projectId)
    external view returns (JBAccountingContext[]);

function accountingContextForTokenOf(uint256 projectId, address token)
    external view returns (JBAccountingContext);

function heldFeesOf(uint256 projectId, address token, uint256 count)
    external view returns (JBFee[]);
```

---

## NANA-SUCKERS-V5：跨链桥接

### 什么是 Suckers？

Suckers 允许在 Juicebox 项目之间进行跨链代币转移。当用户在一条链上销毁代币时，他们会在另一条链上收到等值的代币。Sucker 会在本地执行赎回操作，并将资金桥接到目标网络。

### 支持的桥接方式

- `JBOptimismSucker` - Ethereum ↔ Optimism
- `JBBaseSucker` - Ethereum ↔ Base
- `JBArbitrumSucker` - Ethereum ↔ Arbitrum

### 核心功能

```solidity
// Prepare tokens for bridging (burns locally)
function prepare(
    uint256 projectTokenAmount,
    address beneficiary,
    uint256 minTokensReclaimed,
    address tokenToReclaim
) external returns (uint256 terminalTokenAmount);

// Bridge outbox tree to remote chain
function toRemote(address token) external payable;

// Claim tokens on remote chain with merkle proof
function claim(JBClaim[] calldata claims) external;

// Get merkle root for verification
function outboxTreeRoot(address token) external view returns (bytes32);
```

### 项目要求

- 项目必须在两条链上都存在，并具有相同的 ID
- 必须支持 100% 的提现率
- 项目必须已在两条链上部署 ERC-20 代币

---

## NANA-BUYBACK-HOOK-V5：代币回购

### 功能

当通过 Uniswap V3 的交易获得的代币数量超过直接铸造的数量时，系统会自动执行回购操作。该合约同时充当数据钩子和支付钩子。

### 工作原理

1. `beforePayRecordedWith()` 方法比较铸造代币和交换代币的收益。
2. 如果交换更划算，系统会将此合约设置为支付钩子，并指定交换金额。
3. `afterPayRecordedWith()` 方法执行交换操作，销毁收到的代币，并以预设的比率重新铸造代币。

### 核心功能

```solidity
// Set Uniswap pool for a project
function setPoolFor(
    uint256 projectId,
    address token,
    uint24 fee,
    uint32 twapWindow,
    uint256 twapSlippageTolerance
) external;

// Get pool configuration
function poolOf(uint256 projectId, address token)
    external view returns (IUniswapV3Pool);

// Data hook: determine payment route
function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
    external view returns (uint256 weight, JBPayHookSpecification[]);

// Pay hook: execute swap if beneficial
function afterPayRecordedWith(JBAfterPayRecordedContext calldata context)
    external payable;
```

---

## NANA-SWAP-TERMINAL-V5：多代币接受

### 功能

接受任何 ERC-20 代币的支付，并通过 Uniswap V3 自动兑换为 ETH 或原生代币。

### 流程

1. 用户使用任意代币（例如 USDC）进行支付。
2. 终端通过配置的 Uniswap 池进行兑换。
3. ETH 被转发到目标终端。
4. 代币被铸造给受益者。

### 核心功能

```solidity
// Pay with any token (auto-swaps to ETH)
function pay(
    uint256 projectId,
    address token,              // Any ERC-20
    uint256 amount,
    address beneficiary,
    uint256 minReturnedTokens,
    string calldata memo,
    bytes calldata metadata     // Can include swap params
) external returns (uint256 beneficiaryTokenCount);

// Configure default Uniswap pool for token
function addDefaultPool(
    uint256 projectId,
    address token,
    IUniswapV3Pool pool
) external;
```

## NANA-721-HOOK-V5：分层 NFT

### 功能

在收到支付时，可以铸造分层 NFT（ERC-721）。每个层级都有可配置的价格、供应量、艺术作品和投票权。

### 层级属性

- **price**：铸造该层级的成本
- **initialSupply**：最大可铸造数量
- **votingUnits**：每个 NFT 的投票权
- **reserveFrequency**：每购买一个 NFT 会自动铸造一个额外代币
- **category**：项目分类
- **encodedIPFSUri**：艺术作品/元数据的存储位置
- **allowOwnerMint**：所有者可以直接铸造代币
- **transfersPausable**：可以限制代币的转移

### 核心功能

```solidity
// Data hook: specify NFT minting
function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
    external view returns (uint256 weight, JBPayHookSpecification[]);

// Pay hook: mint NFTs based on payment
function afterPayRecordedWith(JBAfterPayRecordedContext calldata context)
    external payable;

// Cash out hook: burn NFTs to reclaim funds
function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context)
    external payable;

// Get tiers for a hook
function tiersOf(
    address hook,
    uint256[] calldata categories,
    bool includeResolvedUri,
    uint256 startingId,
    uint256 size
) external view returns (JB721Tier[]);

// Adjust tiers (add/remove)
function adjustTiers(JB721TierConfig[] calldata tierConfigs) external;

// Owner mint from specific tiers
function mintFor(
    uint256[] calldata tierIds,
    address beneficiary
) external returns (uint256[] tokenIds);
```

## NANA-PERMISSION-IDS-V5：访问控制

### 所有权限 ID

| ID | 名称 | 权限 |
|----|------|--------|
| 1 | ROOT | 所有操作（超级用户） |
| 2 | QUEUE_RULESETS | 添加新规则集 |
| 3 | CASH_OUT_TOKENS | 代表持有人提取代币 |
| 4 | SEND_PAYOUTS | 触发支付分配 |
| 5 | MIGRATE_TERMINAL | 迁移终端余额 |
| 6 | SET_Project_URI | 更新项目元数据 URI |
| 7 | DEPLOY_ERC20 | 为项目部署 ERC-20 代币 |
| 8 | SET_TOKEN | 设置项目的代币 |
| 9 | MINT_TOKENS | 铸造项目代币 |
| 10 | BURN_TOKENS | 烧毁代币 |
| 11 | CLAIM_TOKENS | 将信用转换为 ERC-20 代币 |
| 12 | TRANSFER_CREDITS | 在地址之间转移信用 |
| 13 | SET_CONTROLLER | 更改项目控制器 |
| 14 | SET_TERMINALS | 修改项目终端 |
| 15 | SET_PRIMARY_TERMINAL | 设置项目的默认终端 |
| 16 | USE_ALLOWANCE | 使用剩余的信用额度 |
| 17 | SET_SPLIT_groups | 修改分配组 |
| 18 | ADD_PRICE_feed | 添加货币价格信息 |
| 19 | ADD_ACCOUNTING_CONTEXTS | 添加代币接受功能 |
| 20 | ADJUST_721_TIERS | 修改 NFT 层级 |
| 21 | SET_721_METADATA | 更新 NFT 元数据 |
| 22 | MINT_721 | 直接铸造 NFT |
| 23 | SET_721_DISCOUNT_PERCENT | 设置 NFT 折扣 |
| 24 | SET_BUYBACK_TWAP | 配置回购策略 |
| 25 | SET_BUYBACK_POOL | 设置回购 Uniswap 池 |
| 26 | ADD_SWAP_TERMINAL_POOL | 添加交换终端池 |
| 27 | ADD_SWAP_TERMINAL_TWAP_PARAMS | 设置交换终端的参数 |
| 28 | MAP_SUCKER_TOKEN | 映射跨链桥接代币 |
| 29 | DEPLOY_SUCKERS | 部署跨链桥接功能 |
| 30 | SUCKER_SAFETY | 管理跨链桥接的安全性 |

### 权限范围（按仓库划分）

| ID 范围 | 仓库 |
|----------|------------|
| 1 | ROOT（所有合约） |
| 2-19 | nana-core |
| 20-23 | nana-721-hook |
| 24-25 | nana-buyback-hook |
| 26-27 | nana-swap-terminal |
| 28-30 | nana-suckers |

### JBPermissions 功能

```solidity
// Grant permissions
function setPermissionsFor(
    address account,
    JBPermissionsData calldata permissionsData
) external;

// Check permission
function hasPermission(
    address operator,
    address account,
    uint256 projectId,
    uint256 permissionId,
    bool includeRoot,
    bool includeWildcardProjectId
) external view returns (bool);

// Get all permissions for operator
function permissionsOf(
    address operator,
    address account,
    uint256 projectId
) external view returns (uint256);
```

---

## NANA-OWNABLE-V5：基于项目的所有权

### 功能

扩展 OpenZeppelin 的 Ownable 模型，以支持 Juicebox 项目的所有权和权限委托。

### 主要特性

1. **项目所有权**：可以将所有权转移给 Juicebox 项目（任何项目所有者均可操作）。
2. **权限委托**：通过 JBPermissions 授予 `onlyOwner` 权限。
3. **元交易支持**：兼容 ERC-2771 标准。

### 相关合约

- `JBOwnable`：用于没有默认所有权的合约。
- `JBOwnableOverride`：用于继承 OpenZeppelin Ownable 功能的合约。

---

## NANA-OMNICHAIN-DEPLOYERS-V5：多链部署

### 功能

支持在一次交易中在多个链上部署 Juicebox 项目及跨链桥接功能。

### 支持的网络

- Ethereum 主网
- Sepolia 测试网
- Optimism 主网/测试网

### 使用方法

部署项目配置后，系统会自动完成以下操作：
- 在每个目标链上创建项目
- 部署跨链桥接功能
- 保持项目配置的一致性

---

## REVNET-CORE-V5：自主管理的资金库网络

### 什么是 Revnet？

Revnet 是一个 **自主运行的 Juicebox 项目**，部署完成后可以独立运作。部署者合约拥有该项目 NFT，并负责管理权限。

### 部署选项

| 部署者 | 功能 |
|----------|----------|
| `BasicRevnetDeployer` | 标准 Revnet |
| `PayHookRevnetDeployer` | 支持自定义支付钩子 |
| `Tiered721RevnetDeployer` | 支持分层 NFT |
| `CroptopRevnetDeployer` | 支持公开发布功能 |

### 关键概念

**阶段**：Revnet 会经历不同的发展阶段，每个阶段有不同的参数设置：
- 初始权重、价格上限、价格下限
- 为早期支持者提供的奖励机制（Boost）

**预铸造**：项目启动时为受益者铸造代币。

**奖励机制**：为指定接收者提供临时增加的代币分配。

### REVDeployer 功能

```solidity
// Deploy a new revnet
function deployFor(
    uint256 revnetId,
    REVConfig calldata configuration,
    JBTerminalConfig[] calldata terminalConfigurations,
    REVBuybackHookConfig calldata buybackHookConfiguration,
    REVSuckerDeploymentConfig calldata suckerDeploymentConfiguration
) external returns (uint256 projectId);

// Data hook: route payments through buyback
function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
    external view returns (uint256 weight, JBPayHookSpecification[]);

// Cash out hook: extract fees
function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context)
    external payable;
```

## CROPTOP-CORE-V5：公开 NFT 发布

### 功能

Croptop 允许项目公开发布 NFT。任何符合项目所有者设定条件的人都可以发布新的 NFT 层级。

### 发布流程

1. 所有者调用 `configurePostingCriteriaFor()` 方法设置价格/供应量要求。
2. 任何人都可以通过 `mintFrom()` 方法发布 NFT，同时提供层级配置和支付信息。
3. 系统会验证是否符合要求（价格 ≥ 最低价格、供应量在指定范围内）。
4. 创建 NFT 后，费用（费用的 1/20）会进入费用资金库。
5. 受益者会收到初始铸造的代币。

---

## 费用结构

### 标准费用（2.5%）

由 JBMultiTerminal 收取的费用包括：
- 向钱包的支付（项目间交易免费用）
- 超额提取时的费用
- 提现金额低于 100% 时的费用

### 费用处理

- 费用会流入项目资金库（Project #1）。
- 支持“Held Fees”模式，提供 28 天的退款期限。
- 可以注册免费地址以享受费用减免。

---

## 协议常量

```solidity
// Native token identifier
address constant NATIVE_TOKEN = 0x000000000000000000000000000000000000EEEe;

// Max values
uint256 constant MAX_RESERVED_RATE = 10000;      // 100%
uint256 constant MAX_CASH_OUT_TAX_RATE = 10000;  // 100%
uint256 constant MAX_FEE = 250;                   // 2.5%

// Split percent precision
uint256 constant SPLITS_TOTAL_PERCENT = 1_000_000_000;  // 100%
```

---

## 示例工作流程

### 创建带有回购功能的项目

1. 部署 `JBBuybackHook` 合约以管理代币。
2. 调用 `launchProjectFor()` 方法并传入规则集元数据：
   - `useDataHookForPay: true`
   - `dataHook: buybackHookAddress`
3. 当交易有利可图时，系统会自动通过 Uniswap 进行支付。

### 部署 Revnet

1. 选择合适的部署者（Basic、PayHook、Tiered721、Croptop）。
2. 配置项目阶段、预铸造参数和奖励机制。
3. 调用 `deployFor()` 方法进行部署。
4. Revnet 会自动运行。

### 启用跨链功能

1. 在两条链上使用相同的 ID 部署项目。
2. 通过 `JBSuckerRegistry` 部署跨链桥接功能。
3. 启用 100% 的提现率和所有者铸造功能。
4. 用户可以在一条链上准备支付，在另一条链上领取收益。

---

## 源代码仓库

- [nana-core-v5](https://github.com/Bananapus/nana-core-v5)
- [nana-suckers-v5](https://github.com/Bananapus/nana-suckers-v5)
- [nana-buyback-hook-v5](https://github.com/Bananapus/nana-buyback-hook-v5)
- [nana-swap-terminal-v5](https://github.com/Bananapus/nana-swap-terminal-v5)
- [nana-721-hook-v5](https://github.com/Bananapus/nana-721-hook-v5)
- [nana-permission-ids-v5](https://github.com/Bananapus/nana-permission-ids-v5)
- [nana-ownable-v5](https://github.com/Bananapus/nana-ownable-v5)
- [nana-omnichain-deployers-v5](https://github.com/Bananapus/nana-omnichain-deployers-v5)
- [revnet-core-v5](https://github.com/rev-net/revnet-core-v5)
- [croptop-core-v5](https://github.com/mejango/croptop-core-v5)