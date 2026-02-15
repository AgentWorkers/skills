---
name: jb-patterns
description: |
  Common Juicebox V5 design patterns for vesting, NFT treasuries, terminal wrappers, yield integration, and
  governance-minimal configurations. Use when: (1) need treasury vesting without custom contracts, (2) building
  NFT-gated redemptions, (3) extending revnet functionality via pay wrappers, (4) implementing custom ERC20
  tokens, (5) integrating yield protocols like Aave, (6) deciding between native mechanics vs custom code.
  Covers 11 patterns including terminal wrapper for dynamic pay-time splits, yield-generating hooks for
  Aave/DeFi integration, and token interception. Golden rule: prefer configuration over custom contracts.
---

# Juicebox V5 设计模式

这些模式经过验证，适用于使用 Juicebox 原生机制的常见用例。**始终优先选择配置方式，而非自定义合约。**

## 金科玉律

> 在编写自定义代码之前，请先问自己：“这个问题是否可以通过设置支付限额、剩余资金分配规则、分配比例以及循环规则集来解决？”

---

## 模式 1：通过原生机制进行权益分配

**用例**：逐步将资金释放给受益人（例如，团队权益分配、基于里程碑的资金释放）

**解决方案**：使用带有支付限额的循环规则集

### 工作原理

| 机制        | 行为                                      | 适用场景                |
|-------------|-----------------------------------------|-------------------------|
| **支付限额**     | 每个周期都会重置                               | 定期分配（权益分配）             |
| **剩余资金分配** | 每个规则集仅分配一次                            | 可自由使用的资金池              |
| **循环周期长度** | 决定分配频率                                | 通常为 30 天                |

### 配置

```solidity
JBRulesetConfig({
    duration: 30 days,                    // Monthly cycles
    // ... other config
    fundAccessLimitGroups: [
        JBFundAccessLimitGroup({
            terminal: address(TERMINAL),
            token: JBConstants.NATIVE_TOKEN,
            payoutLimits: [
                JBCurrencyAmount({
                    amount: 6.67 ether,   // Monthly vesting amount
                    currency: nativeCurrency
                })
            ],
            surplusAllowances: [
                JBCurrencyAmount({
                    amount: 20 ether,     // One-time treasury (doesn't reset)
                    currency: nativeCurrency
                })
            ]
        })
    ]
});
```

### 资本流动

```
Month 0: Balance = 100 ETH
         Surplus = Balance - Payout Limit = 93.33 ETH (redeemable)

Month 1: Team calls sendPayoutsOf() → receives 6.67 ETH
         Balance = 93.33 ETH
         Surplus = 86.67 ETH

Month 12: All vested, Balance = 20 ETH (treasury allowance)
```

### 关键要点

- **支付限额** 可防止权益资金被提前赎回             |
- **剩余资金** 可供代币持有者随时提取                   |
- **无需使用自定义合约             |

---

## 模式 2：基于 NFT 的资金池

**用例**：出售 NFT，允许持有者用 NFT 从资金池中提取资金

**解决方案**：使用 nana-721-hook-v5 并结合原生资金提取功能

### 配置

1. 使用 `JB721TiersHookProjectDeployer` 部署项目
2. 将 721 触发器配置为支付和资金提取的数据接口
3. 将 `cashOutTaxRate` 设置为 0 以实现全额提取

```solidity
JBRulesetMetadata({
    cashOutTaxRate: 0,              // Full redemption
    useDataHookForPay: true,        // 721 hook mints NFTs
    useDataHookForCashOut: true,    // 721 hook handles burns
    dataHook: address(0),           // Set by deployer
    // ...
});
```

### 资金提取方式

1. 用户在终端调用 `cashOutTokensOf()`
2. 721 触发器计算提取金额：`(NFT 价格 / 总价格) × 剩余资金`
3. NFT 被销毁，ETH 被发送给用户

**无需自定义资金提取逻辑**——721 触发器可处理所有流程

---

## 模式 3：最小化治理需求的资金池

**用例**：无需管理员管理的不可篡改资金池

**解决方案**：设置完成后将资金池的所有权转移至指定地址

### 配置

```solidity
// 1. Deploy project with restrictive metadata
JBRulesetMetadata({
    allowOwnerMinting: false,
    allowTerminalMigration: false,
    allowSetTerminals: false,
    allowSetController: false,
    allowAddAccountingContext: false,
    allowAddPriceFeed: false,
    // ...
});

// 2. After deployment, burn ownership
PROJECTS.transferFrom(deployer, 0x000000000000000000000000000000000000dEaD, projectId);
```

### 实现效果

- 任何人无法更改规则集
- 任何人无法添加或删除终端
- 任何人无法随意铸造代币
- 支付和提取功能将按照配置永久执行

---

## 模式 4：无需自定义钩子即可分配资金给多个接收者

**用例**：将资金分配给多个接收地址

**解决方案**：使用原生的资金分配功能直接分配给指定接收者

### 配置

```solidity
JBSplit[] memory splits = new JBSplit[](3);

splits[0] = JBSplit({
    percent: 500_000_000,           // 50%
    beneficiary: payable(team1),
    projectId: 0,
    hook: IJBSplitHook(address(0)), // No hook needed!
    // ...
});

splits[1] = JBSplit({
    percent: 300_000_000,           // 30%
    beneficiary: payable(team2),
    // ...
});

splits[2] = JBSplit({
    percent: 200_000_000,           // 20%
    beneficiary: payable(treasury),
    // ...
});
```

**仅在需要自定义逻辑时使用自定义钩子**（例如，交换代币、加入流动性池）

---

## 模式 5：结合 NFT 和权益分配

**用例**：出售 NFT，同时将部分资金逐步分配给团队成员；持有者可通过销毁 NFT 退出

**解决方案**：结合模式 1 和 2 的功能

### 架构

```
┌─────────────────────────────────────────────────┐
│  JB Project with 721 Hook                       │
│                                                 │
│  • NFT tier: 100 supply, 1 ETH each            │
│  • Payout limit: 6.67 ETH/month (vesting)      │
│  • Surplus allowance: 20 ETH (treasury)        │
│  • Cash out tax: 0%                            │
│  • Owner: burn address                         │
│                                                 │
│  Treasury Flow:                                │
│  ├── Month 0: 80 ETH surplus (all unvested)   │
│  ├── Month 6: 40 ETH surplus                  │
│  └── Month 12: 0 ETH surplus (fully vested)   │
│                                                 │
│  NFT Holder: Can burn anytime for pro-rata    │
│              share of current surplus          │
└─────────────────────────────────────────────────┘
```

### 完整示例**

请参考 Drip x Juicebox 部署脚本以获取完整实现示例：
- 100 个 NFT，每个价值 1 ETH
- 立即可用的 20 ETH（作为剩余资金）
- 80 ETH 在 12 个月内逐步分配（通过支付限额）
- NFT 持有者可随时销毁 NFT 以退出
- 完全不需要自定义合约

---

## 模式 6：通过自定义解析器处理 NFT 内容

**用例**：NFT 项目包含自定义艺术作品、可组合资产或动态元数据，并使用现成的 721 触发器

**解决方案**：实现 `IJB721TokenUriResolver` 来处理自定义内容，同时使用标准的 721 触发器处理资金池逻辑

### 为什么选择这种模式？

721 触发器负责处理所有复杂任务：
- 支付处理和层级选择
- 代币铸造和供应跟踪
- 提取金额计算
- 代币分配机制的实现

您只需编写自定义代码来处理 **内容生成**（如艺术作品、元数据等）。

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Standard 721-Hook (off-the-shelf)                          │
│  ├── Handles payments, minting, cash outs                   │
│  ├── Manages tier supply and pricing                        │
│  └── Calls tokenUriResolver.tokenUriOf() for metadata       │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Custom TokenUriResolver (your code)                │   │
│  │  ├── Implements IJB721TokenUriResolver              │   │
│  │  ├── tokenUriOf() → dynamic SVG/metadata            │   │
│  │  └── Custom behaviors (composability, decoration)   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 接口

```solidity
interface IJB721TokenUriResolver {
    /// @notice Get the token URI for a given token.
    /// @param hook The 721 hook address.
    /// @param tokenId The token ID.
    /// @return The token URI (typically base64-encoded JSON with SVG).
    function tokenUriOf(address hook, uint256 tokenId)
        external view returns (string memory);
}
```

### 基本解析器实现

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {IJB721TokenUriResolver} from "@bananapus/721-hook/src/interfaces/IJB721TokenUriResolver.sol";
import {IJB721TiersHook} from "@bananapus/721-hook/src/interfaces/IJB721TiersHook.sol";

contract CustomTokenUriResolver is IJB721TokenUriResolver {
    /// @notice Generate token URI with custom artwork/metadata.
    function tokenUriOf(address hook, uint256 tokenId)
        external view override returns (string memory)
    {
        // Get tier info from the hook
        IJB721TiersHook tiersHook = IJB721TiersHook(hook);
        uint256 tierId = tiersHook.tierIdOfToken(tokenId);

        // Generate your custom metadata/artwork
        string memory name = _getNameForTier(tierId);
        string memory svg = _generateSvgForToken(tokenId, tierId);

        // Return base64-encoded JSON
        return string(abi.encodePacked(
            "data:application/json;base64,",
            Base64.encode(bytes(abi.encodePacked(
                '{"name":"', name, '",',
                '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
            )))
        ));
    }

    function _getNameForTier(uint256 tierId) internal view returns (string memory) {
        // Your tier naming logic
    }

    function _generateSvgForToken(uint256 tokenId, uint256 tierId) internal view returns (string memory) {
        // Your SVG generation logic
    }
}
```

### 高级实现：可组合的 NFT（Banny 模式）

对于可组合的 NFT，可以将其与基础代币结合使用：

```solidity
contract ComposableTokenUriResolver is IJB721TokenUriResolver {
    // Track which items are attached to which base tokens
    mapping(address hook => mapping(uint256 baseTokenId => uint256[])) public attachedItems;

    // Prevent changes for a duration (e.g., 7 days)
    mapping(address hook => mapping(uint256 tokenId => uint256)) public lockedUntil;

    /// @notice Attach items to a base token.
    function decorateWith(
        address hook,
        uint256 baseTokenId,
        uint256[] calldata itemIds
    ) external {
        // Verify caller owns both base token and items
        require(IJB721TiersHook(hook).ownerOf(baseTokenId) == msg.sender);
        require(lockedUntil[hook][baseTokenId] < block.timestamp, "LOCKED");

        for (uint256 i; i < itemIds.length; i++) {
            require(IJB721TiersHook(hook).ownerOf(itemIds[i]) == msg.sender);
            // Transfer item to this contract (escrow while attached)
            IJB721TiersHook(hook).transferFrom(msg.sender, address(this), itemIds[i]);
        }

        attachedItems[hook][baseTokenId] = itemIds;
    }

    /// @notice Lock outfit changes for 7 days.
    function lockChangesFor(address hook, uint256 baseTokenId) external {
        require(IJB721TiersHook(hook).ownerOf(baseTokenId) == msg.sender);
        lockedUntil[hook][baseTokenId] = block.timestamp + 7 days;
    }

    /// @notice Generate composite SVG from base + attached items.
    function tokenUriOf(address hook, uint256 tokenId) external view override returns (string memory) {
        uint256[] memory items = attachedItems[hook][tokenId];

        // Generate layered SVG combining base + all attached items
        string memory svg = _generateCompositeSvg(hook, tokenId, items);

        return _encodeAsDataUri(svg);
    }
}
```

### 部署集成

```solidity
// 1. Deploy your custom resolver
CustomTokenUriResolver resolver = new CustomTokenUriResolver();

// 2. Configure 721 hook with resolver
REVDeploy721TiersHookConfig memory hookConfig = REVDeploy721TiersHookConfig({
    baseline721HookConfiguration: JBDeploy721TiersHookConfig({
        // ... tier configs
        tokenUriResolver: IJB721TokenUriResolver(address(resolver)),
        // ...
    }),
    // ...
});

// 3. Deploy project/revnet with hook config
deployer.deployWith721sFor(projectId, hookConfig, ...);
```

## 何时使用这种模式

| 需求                | 是否需要使用解析器？                |
|------------------|-------------------------|
| 静态层级图像（IPFS）        | 不需要 - 在层级配置中使用 `encodedIPFSUri`       |
| 动态/生成型艺术作品        | 需要                     |
| 可组合/分层 NFT          | 需要                     |
| 在链上存储 SVG            | 需要                     |
| 代币特定元数据          | 需要                     |
| 标准 ERC-721 元数据        | 不需要 - 使用默认设置           |

### 参考实现

**banny-retail-v5**: https://github.com/mejango/banny-retail-v5
- `Banny721TokenUriResolver.sol`：支持可组合 SVG NFT 和装饰性外观
- `Deploy.s.sol`：用于部署项目的自定义解析器
- `Drop1.s.sol`：用于添加自定义层级的脚本

**主要特性**：
- 在链上存储 SVG 并进行哈希验证
- 可组合的外观设计
- 外观设计可附加到基础 NFT 上
- 外观设计有 7 天的锁定期

---

## 模式 7：具有动态提取金额的预测游戏

**用例**：游戏结果决定了提取金额的分配（预测市场、梦幻体育、竞赛等）

**解决方案**：扩展 721 触发器，添加自定义逻辑；使用链上治理机制来处理结果

### 为什么需要扩展 721 触发器？

与模式 6 不同，预测游戏需要修改 **核心资金池机制**：

| 需求                | 为什么仅使用解析器不够？                |
|------------------|---------------------------|
| 动态提取金额计算        | 提取金额的计算需要在触发器中完成，而非解析器中       |
| 原始铸造者的奖励分配      | 奖励应给予原始铸造者，而非当前持有者         |
| 游戏阶段的规则调整        | 不同游戏阶段有不同的规则             |

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Game Lifecycle (via Juicebox Rulesets)                     │
│                                                             │
│  COUNTDOWN → MINT → REFUND → SCORING → COMPLETE             │
│      │         │       │        │          │                │
│      │    Players   Early    Holders    Winners             │
│      │    mint      exit     vote on    cash out            │
│      │    NFTs      OK       scorecard  winnings            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Custom Delegate (extends JB721Hook)                        │
│  ├── Tracks first owners (for fair reward distribution)     │
│  ├── Phase-aware cash out logic                             │
│  ├── Dynamic tier weights (set by governor)                 │
│  └── Enforces phase restrictions                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Governor Contract                                          │
│  ├── NFT holders propose scorecards                         │
│  ├── Tier-weighted voting (own 25% of tier = 25% of votes)  │
│  ├── 50% quorum required for ratification                   │
│  └── Ratification sets tier cash out weights                │
└─────────────────────────────────────────────────────────────┘
```

### 游戏阶段

```solidity
enum DefifaGamePhase {
    COUNTDOWN,           // Game announced, no minting yet
    MINT,                // Players can mint NFTs (pick teams)
    REFUND,              // Early exit window (get mint cost back)
    SCORING,             // Game over, holders vote on scorecard
    COMPLETE,            // Scorecard ratified, winners cash out
    NO_CONTEST_INEVITABLE, // Not enough participation
    NO_CONTEST           // Game cancelled, full refunds
}
```

### 动态提取金额计算

标准 721 触发器：`cashOutWeight = 层级价格`（固定）

**Defifa 模式**：`cashOutWeight = scorecardWeight[tierId]`（动态）

```solidity
// Total weight is 1e18 (100%), distributed among tiers by scorecard
uint256 constant TOTAL_CASH_OUT_WEIGHT = 1e18;

struct DefifaTierCashOutWeight {
    uint256 id;           // Tier ID
    uint256 cashOutWeight; // Share of total (e.g., 0.5e18 = 50%)
}

// Example: 4-team tournament, Team A wins
// Team A: 1e18 (100% of pot)
// Team B: 0
// Team C: 0
// Team D: 0

// Example: Fantasy league with scoring
// Team A (1st): 0.5e18 (50%)
// Team B (2nd): 0.3e18 (30%)
// Team C (3rd): 0.15e18 (15%)
// Team D (4th): 0.05e18 (5%)
```

### 原始铸造者的奖励分配

**关键点**：
- 保证公平性——奖励应给予原始铸造者，而非当前持有者

### 模式 8：使用自定义解析器

**用例**：需要自定义 NFT 内容的项目

**解决方案**：实现 `IJB721TokenUriResolver` 来处理自定义内容，同时使用标准的 721 触发器处理资金池逻辑

### 为什么使用这种模式？

721 触发器负责处理所有复杂任务：
- 支付处理和层级选择
- 代币铸造和供应跟踪
- 提取金额计算
- 保留代币分配机制

您只需编写自定义代码来处理 **内容生成**（如艺术作品、元数据等）。

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Standard 721-Hook (off-the-shelf)                          │
│  ├── Handles payments, minting, cash outs                   │
│  ├── Manages tier supply and pricing                        │
│  └── Calls tokenUriResolver.tokenUriOf() for metadata       │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Custom TokenUriResolver (your code)                │   │
│  │  ├── Implements IJB721TokenUriResolver              │   │
│  │  ├── tokenUriOf() → dynamic SVG/metadata            │   │
│  │  └── Custom behaviors (composability, decoration)   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 接口

```solidity
interface IJB721TokenUriResolver {
    /// @notice Get the token URI for a given token.
    /// @param hook The 721 hook address.
    /// @param tokenId The token ID.
    /// @return The token URI (typically base64-encoded JSON with SVG).
    function tokenUriOf(address hook, uint256 tokenId)
        external view returns (string memory);
}
```

### 基本解析器实现

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {IJB721TokenUriResolver} from "@bananapus/721-hook/src/interfaces/IJB721TokenUriResolver.sol";
import {IJB721TiersHook} from "@bananapus/721-hook/src/interfaces/IJB721TiersHook.sol";

contract CustomTokenUriResolver is IJB721TokenUriResolver {
    /// @notice Generate token URI with custom artwork/metadata.
    function tokenUriOf(address hook, uint256 tokenId)
        external view override returns (string memory)
    {
        // Get tier info from the hook
        IJB721TiersHook tiersHook = IJB721TiersHook(hook);
        uint256 tierId = tiersHook.tierIdOfToken(tokenId);

        // Generate your custom metadata/artwork
        string memory name = _getNameForTier(tierId);
        string memory svg = _generateSvgForToken(tokenId, tierId);

        // Return base64-encoded JSON
        return string(abi.encodePacked(
            "data:application/json;base64,",
            Base64.encode(bytes(abi.encodePacked(
                '{"name":"', name, '",',
                '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
            )))
        ));
    }

    function _getNameForTier(uint256 tierId) internal view returns (string memory) {
        // Your tier naming logic
    }

    function _generateSvgForToken(uint256 tokenId, uint256 tierId) internal view returns (string memory) {
        // Your SVG generation logic
    }
}
```

### 高级实现：可组合的 NFT（Banny 模式）

对于可组合的 NFT，可以将其与基础代币结合使用：

```solidity
contract ComposableTokenUriResolver is IJB721TokenUriResolver {
    // Track which items are attached to which base tokens
    mapping(address hook => mapping(uint256 baseTokenId => uint256[])) public attachedItems;

    // Prevent changes for a duration (e.g., 7 days)
    mapping(address hook => mapping(uint256 tokenId => uint256)) public lockedUntil;

    /// @notice Attach items to a base token.
    function decorateWith(
        address hook,
        uint256 baseTokenId,
        uint256[] calldata itemIds
    ) external {
        // Verify caller owns both base token and items
        require(IJB721TiersHook(hook).ownerOf(baseTokenId) == msg.sender);
        require(lockedUntil[hook][baseTokenId] < block.timestamp, "LOCKED");

        for (uint256 i; i < itemIds.length; i++) {
            require(IJB721TiersHook(hook).ownerOf(itemIds[i]) == msg.sender);
            // Transfer item to this contract (escrow while attached)
            IJB721TiersHook(hook).transferFrom(msg.sender, address(this), itemIds[i]);
        }

        attachedItems[hook][baseTokenId] = itemIds;
    }

    /// @notice Lock outfit changes for 7 days.
    function lockChangesFor(address hook, uint256 baseTokenId) external {
        require(IJB721TiersHook(hook).ownerOf(baseTokenId) == msg.sender);
        lockedUntil[hook][baseTokenId] = block.timestamp + 7 days;
    }

    /// @notice Generate composite SVG from base + attached items.
    function tokenUriOf(address hook, uint256 tokenId) external view override returns (string memory) {
        uint256[] memory items = attachedItems[hook][tokenId];

        // Generate layered SVG combining base + all attached items
        string memory svg = _generateCompositeSvg(hook, tokenId, items);

        return _encodeAsDataUri(svg);
    }
}
```

### 部署集成

```solidity
// 1. Deploy your custom resolver
CustomTokenUriResolver resolver = new CustomTokenUriResolver();

// 2. Configure 721 hook with resolver
REVDeploy721TiersHookConfig memory hookConfig = REVDeploy721TiersHookConfig({
    baseline721HookConfiguration: JBDeploy721TiersHookConfig({
        // ... tier configs
        tokenUriResolver: IJB721TokenUriResolver(address(resolver)),
        // ...
    }),
    // ...
});

// 3. Deploy project/revnet with hook config
deployer.deployWith721sFor(projectId, hookConfig, ...);
```

## 何时使用这种模式

| 需求                | 是否需要使用解析器？                |
|------------------|-------------------------|
| 静态层级图像（IPFS）        | 不需要 - 在层级配置中使用 `encodedIPFSUri`       |
| 动态/生成型艺术作品        | 需要                     |
| 可组合/分层 NFT          | 需要                     |
| 在链上存储 SVG            | 需要                     |
| 代币特定元数据          | 需要                     |
| 标准 ERC-721 元数据        | 不需要 - 使用默认设置           |

### 参考实现

**banny-retail-v5**: https://github.com/mejango/banny-retail-v5
- `Banny721TokenUriResolver.sol`：支持可组合 SVG NFT 和装饰性外观
- `Deploy.s.sol`：用于部署项目的自定义解析器
- `Drop1.s.sol`：用于添加自定义层级的脚本

**主要特性**：
- 在链上存储 SVG 并进行哈希验证
- 可组合的外观设计
- 外观设计可附加到基础 NFT 上
- 外观设计有 7 天的锁定期

---

## 模式 9：具有动态提取金额的预测游戏

**用例**：游戏结果决定了提取金额的分配（预测市场、梦幻体育、竞赛等）

**解决方案**：扩展 721 触发器，添加自定义逻辑；使用链上治理机制来处理结果

### 为什么需要扩展 721 触发器？

与模式 6 不同，预测游戏需要修改 **核心资金池机制**：

| 需求                | 为什么仅使用解析器不够？                |
|------------------|---------------------------|
| 动态提取金额计算        | 提取金额的计算需要在触发器中完成，而非解析器中       |
| 原始铸造者的奖励分配      | 奖励应给予原始铸造者，而非当前持有者         |
| 游戏阶段的规则调整        | 不同游戏阶段有不同的规则             |

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Game Lifecycle (via Juicebox Rulesets)                     │
│                                                             │
│  COUNTDOWN → MINT → REFUND → SCORING → COMPLETE             │
│      │         │       │        │          │                │
│      │    Players   Early    Holders    Winners             │
│      │    mint      exit     vote on    cash out            │
│      │    NFTs      OK       scorecard  winnings            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Custom Delegate (extends JB721Hook)                        │
│  ├── Tracks first owners (for fair reward distribution)     │
│  ├── Phase-aware cash out logic                             │
│  ├── Dynamic tier weights (set by governor)                 │
│  └── Enforces phase restrictions                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Governor Contract                                          │
│  ├── NFT holders propose scorecards                         │
│  ├── Tier-weighted voting (own 25% of tier = 25% of votes)  │
│  ├── 50% quorum required for ratification                   │
│  └── Ratification sets tier cash out weights                │
└─────────────────────────────────────────────────────────────┘
```

### 游戏阶段

```solidity
enum DefifaGamePhase {
    COUNTDOWN,           // Game announced, no minting yet
    MINT,                // Players can mint NFTs (pick teams)
    REFUND,              // Early exit window (get mint cost back)
    SCORING,             // Game over, holders vote on scorecard
    COMPLETE,            // Scorecard ratified, winners cash out
    NO_CONTEST_INEVITABLE, // Not enough participation
    NO_CONTEST           // Game cancelled, full refunds
}
```

### 动态提取金额计算

标准 721 触发器：`cashOutWeight = 层级价格`（固定）

**Defifa 模式**：`cashOutWeight = scorecardWeight[tierId]`（动态）

```solidity
// Total weight is 1e18 (100%), distributed among tiers by scorecard
uint256 constant TOTAL_CASH_OUT_WEIGHT = 1e18;

struct DefifaTierCashOutWeight {
    uint256 id;           // Tier ID
    uint256 cashOutWeight; // Share of total (e.g., 0.5e18 = 50%)
}

// Example: 4-team tournament, Team A wins
// Team A: 1e18 (100% of pot)
// Team B: 0
// Team C: 0
// Team D: 0

// Example: Fantasy league with scoring
// Team A (1st): 0.5e18 (50%)
// Team B (2nd): 0.3e18 (30%)
// Team C (3rd): 0.15e18 (15%)
// Team D (4th): 0.05e18 (5%)
```

### 原始铸造者的奖励分配

**关键点**：
- 保证公平性——奖励应给予原始铸造者，而非当前持有者

### 模式 10：使用自定义 ERC20 项目代币

**用例**：项目需要超出标准铸造/销毁机制的定制代币逻辑

**解决方案**：实现 `IJBToken` 接口，并使用 `setTokenFor()` 而不是 `deployERC20For()`

### 为什么使用这种模式？

虽然 Juicebox 的默认代币（credits 或 JBERC20）适用于大多数项目，但某些用例需要更复杂的代币逻辑：

| 默认代币的限制        | 自定义代币的解决方案            |
|--------------------------|----------------------|
| 无转账费用          | 实现转账税                          |
| 固定供应机制          | 使用重新基数/弹性供应机制                |
| 无治理功能          | 扩展 ERC20Votes 接口                |
| 不可更改的代币名称/符号      | 添加 setName/setSymbol 函数                |

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Juicebox Protocol (unchanged)                              │
│  ├── JBController calls mint/burn on token                  │
│  ├── JBTokens tracks credits + token supply                 │
│  └── JBMultiTerminal handles payments/cash outs             │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Custom ERC20 Token (your code)                     │   │
│  │  ├── Implements IJBToken interface                  │   │
│  │  ├── Authorizes JBController for mint/burn          │   │
│  │  ├── Uses 18 decimals (REQUIRED)                    │   │
│  │  └── Custom logic: taxes, rebasing, governance, etc │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 接口要求

```solidity
interface IJBToken is IERC20 {
    /// @notice Must return true for the target project ID
    function canBeAddedTo(uint256 projectId) external view returns (bool);

    /// @notice Called by JBController when payments are received
    function mint(address holder, uint256 amount) external;

    /// @notice Called by JBController when tokens are cashed out
    function burn(address holder, uint256 amount) external;
}
```

### 示例：收取转账税的代币

这种代币在每次转账时都会收取费用：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TaxedProjectToken is ERC20 {
    uint256 public constant TAX_BPS = 100; // 1%
    address public immutable controller;
    address public immutable treasury;
    uint256 public immutable projectId;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId,
        address _treasury
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        treasury = _treasury;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    function _update(address from, address to, uint256 amount) internal override {
        // No tax on mints, burns, or controller operations
        if (from == address(0) || to == address(0) || msg.sender == controller) {
            super._update(from, to, amount);
            return;
        }

        // Apply transfer tax
        uint256 tax = (amount * TAX_BPS) / 10000;
        super._update(from, treasury, tax);
        super._update(from, to, amount - tax);
    }
}
```

**部署示例**：
```solidity
// 1. Deploy custom token (before or after project creation)
TaxedProjectToken token = new TaxedProjectToken(
    "Taxed Token",
    "TAX",
    address(CONTROLLER),
    projectId,
    treasuryAddress
);

// 2. Set as project token (requires SET_TOKEN permission)
CONTROLLER.setTokenFor(projectId, IJBToken(address(token)));
```

### 示例：具有投票功能的治理代币

在保持资金池机制的同时，实现链上治理功能：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20Votes, ERC20} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {Nonces} from "@openzeppelin/contracts/utils/Nonces.sol";

contract GovernanceProjectToken is ERC20Votes {
    address public immutable controller;
    uint256 public immutable projectId;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId
    ) ERC20(name, symbol) EIP712(name, "1") {
        controller = _controller;
        projectId = _projectId;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    // Inherits: delegate(), delegateBySig(), getVotes(), getPastVotes(), etc.
}
```

**与治理系统的结合使用**：
```solidity
// Deploy governor that uses token's voting power
GovernorBravo governor = new GovernorBravo(
    GovernanceProjectToken(token),
    timelockAddress,
    votingDelay,
    votingPeriod,
    proposalThreshold
);

// Token holders delegate and vote
token.delegate(voterAddress);  // Self-delegate to activate voting
governor.propose(...);
governor.castVote(proposalId, support);
```

### 示例：可编辑名称/符号的代币

允许项目所有者在不部署新代币的情况下更改项目名称：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IJBProjects} from "@bananapus/core/src/interfaces/IJBProjects.sol";

contract EditableProjectToken is ERC20 {
    IJBProjects public immutable PROJECTS;
    address public immutable controller;
    uint256 public immutable projectId;

    string private _tokenName;
    string private _tokenSymbol;

    event NameUpdated(string oldName, string newName);
    event SymbolUpdated(string oldSymbol, string newSymbol);

    constructor(
        string memory initialName,
        string memory initialSymbol,
        address _controller,
        uint256 _projectId,
        IJBProjects projects
    ) ERC20(initialName, initialSymbol) {
        _tokenName = initialName;
        _tokenSymbol = initialSymbol;
        controller = _controller;
        projectId = _projectId;
        PROJECTS = projects;
    }

    modifier onlyProjectOwner() {
        require(msg.sender == PROJECTS.ownerOf(projectId), "NOT_OWNER");
        _;
    }

    function name() public view override returns (string memory) {
        return _tokenName;
    }

    function symbol() public view override returns (string memory) {
        return _tokenSymbol;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    /// @notice Update token name. Only callable by project owner.
    function setName(string calldata newName) external onlyProjectOwner {
        emit NameUpdated(_tokenName, newName);
        _tokenName = newName;
    }

    /// @notice Update token symbol. Only callable by project owner.
    function setSymbol(string calldata newSymbol) external onlyProjectOwner {
        emit SymbolUpdated(_tokenSymbol, newSymbol);
        _tokenSymbol = newSymbol;
    }
}
```

**使用场景**：
- 项目重新品牌化时无需迁移现有流动性
- 根据季节或事件更改项目名称
- 发现发布后的拼写错误时进行更正
- 通过社区投票更新项目名称

**注意事项**：
- 一些去中心化交易所（DEX）和聚合器可能会缓存代币元数据，导致更改不会立即生效

### 示例：具有权益分配功能的代币

在代币层面实现基于时间的权益分配——适用于团队分配、投资者锁定或需要逐步分配代币的情况：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IJBProjects} from "@bananapus/core/src/interfaces/IJBProjects.sol";

/// @notice Project token with per-address vesting schedules.
/// @dev Vesting restricts transfers, not minting/burning. Combined with treasury
/// vesting (payout limits), this creates layered protection.
contract VestingProjectToken is ERC20 {
    struct VestingSchedule {
        uint256 totalAmount;     // Total tokens in this schedule
        uint256 released;        // Already released/transferred
        uint40 start;            // Vesting start timestamp
        uint40 cliff;            // Cliff end timestamp (0 = no cliff)
        uint40 duration;         // Total vesting duration from start
    }

    IJBProjects public immutable PROJECTS;
    address public immutable controller;
    uint256 public immutable projectId;

    mapping(address => VestingSchedule) public vestingOf;

    event VestingScheduleSet(
        address indexed beneficiary,
        uint256 totalAmount,
        uint40 start,
        uint40 cliff,
        uint40 duration
    );

    error CliffNotReached();
    error InsufficientVestedBalance();
    error VestingAlreadyExists();

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId,
        IJBProjects projects
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        PROJECTS = projects;
    }

    modifier onlyProjectOwner() {
        require(msg.sender == PROJECTS.ownerOf(projectId), "NOT_OWNER");
        _;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    /// @notice Set a vesting schedule for an address.
    /// @dev Call this AFTER minting tokens to the beneficiary.
    /// @param beneficiary Address whose tokens will vest.
    /// @param totalAmount Total tokens subject to vesting (should match balance).
    /// @param start When vesting begins (can be in the past).
    /// @param cliffDuration Seconds until cliff ends (0 for no cliff).
    /// @param vestingDuration Total seconds for full vesting from start.
    function setVestingSchedule(
        address beneficiary,
        uint256 totalAmount,
        uint40 start,
        uint40 cliffDuration,
        uint40 vestingDuration
    ) external onlyProjectOwner {
        if (vestingOf[beneficiary].totalAmount > 0) revert VestingAlreadyExists();

        vestingOf[beneficiary] = VestingSchedule({
            totalAmount: totalAmount,
            released: 0,
            start: start,
            cliff: start + cliffDuration,
            duration: vestingDuration
        });

        emit VestingScheduleSet(
            beneficiary,
            totalAmount,
            start,
            start + cliffDuration,
            vestingDuration
        );
    }

    /// @notice Calculate how many tokens have vested for an address.
    function vestedAmountOf(address account) public view returns (uint256) {
        VestingSchedule memory schedule = vestingOf[account];

        // No vesting schedule = all tokens are vested (freely transferable)
        if (schedule.totalAmount == 0) return balanceOf(account);

        // Before cliff = nothing vested
        if (block.timestamp < schedule.cliff) return 0;

        // After full duration = everything vested
        if (block.timestamp >= schedule.start + schedule.duration) {
            return schedule.totalAmount;
        }

        // Linear vesting between cliff and end
        uint256 elapsed = block.timestamp - schedule.start;
        return (schedule.totalAmount * elapsed) / schedule.duration;
    }

    /// @notice Calculate transferable (vested and unreleased) tokens.
    function transferableOf(address account) public view returns (uint256) {
        VestingSchedule memory schedule = vestingOf[account];

        // No vesting = full balance transferable
        if (schedule.totalAmount == 0) return balanceOf(account);

        uint256 vested = vestedAmountOf(account);
        uint256 locked = schedule.totalAmount > vested
            ? schedule.totalAmount - vested
            : 0;

        uint256 balance = balanceOf(account);
        return balance > locked ? balance - locked : 0;
    }

    function _update(address from, address to, uint256 amount) internal override {
        // Skip vesting checks for mints, burns, and controller operations
        if (from == address(0) || to == address(0) || msg.sender == controller) {
            super._update(from, to, amount);
            return;
        }

        VestingSchedule storage schedule = vestingOf[from];

        // No vesting schedule = normal transfer
        if (schedule.totalAmount == 0) {
            super._update(from, to, amount);
            return;
        }

        // Before cliff = no transfers allowed
        if (block.timestamp < schedule.cliff) revert CliffNotReached();

        // Check transferable amount
        uint256 transferable = transferableOf(from);
        if (amount > transferable) revert InsufficientVestedBalance();

        // Track released amount for accounting
        schedule.released += amount;

        super._update(from, to, amount);
    }
}
```

**关键设计决策**：
- 权益分配按地址进行，由项目所有者设置
- 设置权益分配计划后，代币可自由转让（符合 ERC20 的常规行为）
- 在达到权益分配截止日期之前，代币不可转让
- 权益分配结束后，代币可自由转让

**使用场景**：
- 团队分配          | ✅
- 投资者锁定          | ✅
- 定期工资/补助金        | ✅
- 基于里程碑的分配      | ✅
- 全体持有者保护        | ✅

**注意事项**：
- 使用这种模式会增加复杂性
- 权益分配计划一旦设置就无法更改
- 不会阻止提取操作（控制器操作不受影响）

### 示例：限制代币集中度的机制

防止任何单一持有者积累过多代币：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ConcentrationLimitedToken is ERC20 {
    uint256 public maxHolderBps = 200;  // 2% max per holder
    address public immutable controller;
    uint256 public immutable projectId;
    mapping(address => bool) public isExempt;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        isExempt[_controller] = true;  // Controller always exempt
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    function _update(address from, address to, uint256 amount) internal override {
        // Skip checks for mints, burns, and exempt addresses
        if (from == address(0) || to == address(0) || isExempt[to]) {
            super._update(from, to, amount);
            return;
        }

        // Check concentration limit
        uint256 maxBalance = (totalSupply() * maxHolderBps) / 10000;
        require(balanceOf(to) + amount <= maxBalance, "EXCEEDS_MAX_HOLDING");

        super._update(from, to, amount);
    }

    function setExempt(address account, bool exempt) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        isExempt[account] = exempt;
    }
}
```

**使用场景**：
- 促进代币的广泛分配
- 防止治理权力集中
- 降低市场操纵风险

**注意事项**：
- 流动性池和控制器必须被标记为特殊处理对象
- 在早期高供应阶段，新持有者可能会遇到分配限制

**何时使用这种模式**：
- 当需要限制代币集中度时                | ✅
- 在简单筹款场景中        | ✅
- 需要转账费用或税收时        | ✅
- 需要重新基数机制时        | ✅
- 需要治理投票时        | ✅

### 关键实现考虑因素**

1. **阶段转换**：通过规则集来控制转换时机
2. **退款窗口**：在结果确定前允许提前退出
3. **法定人数要求**：法定人数过低可能导致僵局，过高可能导致操纵
4. **奖励分配给原始铸造者还是当前持有者**：需要明确奖励对象
5. **处理无参与者情况**：如何处理无人参与的情况

### 参考实现

**defifa-collection-deployer-v5**: https://github.com/BallKidz/defifa-collection-deployer-v5

**关键合约**：
- `DefifaDelegate.sol`：扩展了 JB721Hook，实现了阶段逻辑和动态权重
- `DefifaGovernor.sol`：用于链上投票以确认分配结果
- `DefifaDeployer.sol`：用于启动游戏
- `DefifaTokenUriResolver.sol`：用于显示分配比例

**主要特性**：
- 基于阶段的游戏生命周期
- 按层级分配的治理投票
- 动态提取金额的重新分配
- 保证原始铸造者的奖励分配
- 处理无参与者情况

---

## 模式 11：自定义 ERC20 项目代币

**用例**：项目需要超出标准铸造/销毁机制的定制代币逻辑

**解决方案**：实现 `IJBToken` 接口，并使用 `setTokenFor()` 而不是 `deployERC20For()`

### 为什么使用这种模式？

虽然 Juicebox 的默认代币（credits 或 JBERC20）适用于大多数项目，但某些用例需要更复杂的代币逻辑：

| 默认代币的限制        | 自定义代币的解决方案            |
|--------------------------|----------------------|
| 无转账费用          | 实现转账税                          |
| 固定供应机制          | 使用重新基数/弹性供应机制                |
| 无治理功能          | 扩展 ERC20Votes 接口                |
| 不可更改的代币名称/符号      | 添加 setName/setSymbol 函数                |

### 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Juicebox Protocol (unchanged)                              │
│  ├── JBController calls mint/burn on token                  │
│  ├── JBTokens tracks credits + token supply                 │
│  └── JBMultiTerminal handles payments/cash outs             │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Custom ERC20 Token (your code)                     │   │
│  │  ├── Implements IJBToken interface                  │   │
│  │  ├── Authorizes JBController for mint/burn          │   │
│  │  ├── Uses 18 decimals (REQUIRED)                    │   │
│  │  └── Custom logic: taxes, rebasing, governance, etc │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 接口要求

```solidity
interface IJBToken is IERC20 {
    /// @notice Must return true for the target project ID
    function canBeAddedTo(uint256 projectId) external view returns (bool);

    /// @notice Called by JBController when payments are received
    function mint(address holder, uint256 amount) external;

    /// @notice Called by JBController when tokens are cashed out
    function burn(address holder, uint256 amount) external;
}
```

### 示例：收取转账税的代币

这种代币在每次转账时都会收取费用：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TaxedProjectToken is ERC20 {
    uint256 public constant TAX_BPS = 100; // 1%
    address public immutable controller;
    address public immutable treasury;
    uint256 public immutable projectId;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId,
        address _treasury
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        treasury = _treasury;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    function _update(address from, address to, uint256 amount) internal override {
        // No tax on mints, burns, or controller operations
        if (from == address(0) || to == address(0) || msg.sender == controller) {
            super._update(from, to, amount);
            return;
        }

        // Apply transfer tax
        uint256 tax = (amount * TAX_BPS) / 10000;
        super._update(from, treasury, tax);
        super._update(from, to, amount - tax);
    }
}
```

**部署示例**：
```solidity
// 1. Deploy custom token (before or after project creation)
TaxedProjectToken token = new TaxedProjectToken(
    "Taxed Token",
    "TAX",
    address(CONTROLLER),
    projectId,
    treasuryAddress
);

// 2. Set as project token (requires SET_TOKEN permission)
CONTROLLER.setTokenFor(projectId, IJBToken(address(token)));
```

### 示例：具有投票功能的治理代币

在保持资金池机制的同时，实现链上治理功能：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20Votes, ERC20} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {Nonces} from "@openzeppelin/contracts/utils/Nonces.sol";

contract GovernanceProjectToken is ERC20Votes {
    address public immutable controller;
    uint256 public immutable projectId;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId
    ) ERC20(name, symbol) EIP712(name, "1") {
        controller = _controller;
        projectId = _projectId;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    // Inherits: delegate(), delegateBySig(), getVotes(), getPastVotes(), etc.
}
```

**与治理系统的结合使用**：
```solidity
// Deploy governor that uses token's voting power
GovernorBravo governor = new GovernorBravo(
    GovernanceProjectToken(token),
    timelockAddress,
    votingDelay,
    votingPeriod,
    proposalThreshold
);

// Token holders delegate and vote
token.delegate(voterAddress);  // Self-delegate to activate voting
governor.propose(...);
governor.castVote(proposalId, support);
```

### 示例：可编辑名称/符号的代币

允许项目所有者在不部署新代币的情况下更改项目名称：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IJBProjects} from "@bananapus/core/src/interfaces/IJBProjects.sol";

contract EditableProjectToken is ERC20 {
    IJBProjects public immutable PROJECTS;
    address public immutable controller;
    uint256 public immutable projectId;

    string private _tokenName;
    string private _tokenSymbol;

    event NameUpdated(string oldName, string newName);
    event SymbolUpdated(string oldSymbol, string newSymbol);

    constructor(
        string memory initialName,
        string memory initialSymbol,
        address _controller,
        uint256 _projectId,
        IJBProjects projects
    ) ERC20(initialName, initialSymbol) {
        _tokenName = initialName;
        _tokenSymbol = initialSymbol;
        controller = _controller;
        projectId = _projectId;
        PROJECTS = projects;
    }

    modifier onlyProjectOwner() {
        require(msg.sender == PROJECTS.ownerOf(projectId), "NOT_OWNER");
        _;
    }

    function name() public view override returns (string memory) {
        return _tokenName;
    }

    function symbol() public view override returns (string memory) {
        return _tokenSymbol;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    /// @notice Update token name. Only callable by project owner.
    function setName(string calldata newName) external onlyProjectOwner {
        emit NameUpdated(_tokenName, newName);
        _tokenName = newName;
    }

    /// @notice Update token symbol. Only callable by project owner.
    function setSymbol(string calldata newSymbol) external onlyProjectOwner {
        emit SymbolUpdated(_tokenSymbol, newSymbol);
        _tokenSymbol = newSymbol;
    }
}
```

**使用场景**：
- 项目重新品牌化时无需迁移现有流动性
- 根据季节或事件更改项目名称
- 发现发布后的拼写错误时进行更正
- 通过社区投票更新项目名称

**注意事项**：
- 一些去中心化交易所（DEX）和聚合器可能会缓存代币元数据，导致更改不会立即生效

### 示例：具有权益分配功能的代币

在代币层面实现基于时间的权益分配——适用于团队分配、投资者锁定或需要逐步分配代币的情况：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IJBProjects} from "@bananapus/core/src/interfaces/IJBProjects.sol";

/// @notice Project token with per-address vesting schedules.
/// @dev Vesting restricts transfers, not minting/burning. Combined with treasury
/// vesting (payout limits), this creates layered protection.
contract VestingProjectToken is ERC20 {
    struct VestingSchedule {
        uint256 totalAmount;     // Total tokens in this schedule
        uint256 released;        // Already released/transferred
        uint40 start;            // Vesting start timestamp
        uint40 cliff;            // Cliff end timestamp (0 = no cliff)
        uint40 duration;         // Total vesting duration from start
    }

    IJBProjects public immutable PROJECTS;
    address public immutable controller;
    uint256 public immutable projectId;

    mapping(address => VestingSchedule) public vestingOf;

    event VestingScheduleSet(
        address indexed beneficiary,
        uint256 totalAmount,
        uint40 start,
        uint40 cliff,
        uint40 duration
    );

    error CliffNotReached();
    error InsufficientVestedBalance();
    error VestingAlreadyExists();

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId,
        IJBProjects projects
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        PROJECTS = projects;
    }

    modifier onlyProjectOwner() {
        require(msg.sender == PROJECTS.ownerOf(projectId), "NOT_OWNER");
        _;
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    /// @notice Set a vesting schedule for an address.
    /// @dev Call this AFTER minting tokens to the beneficiary.
    /// @param beneficiary Address whose tokens will vest.
    /// @param totalAmount Total tokens subject to vesting (should match balance).
    /// @param start When vesting begins (can be in the past).
    /// @param cliffDuration Seconds until cliff ends (0 for no cliff).
    /// @param vestingDuration Total seconds for full vesting from start.
    function setVestingSchedule(
        address beneficiary,
        uint256 totalAmount,
        uint40 start,
        uint40 cliffDuration,
        uint40 vestingDuration
    ) external onlyProjectOwner {
        if (vestingOf[beneficiary].totalAmount > 0) revert VestingAlreadyExists();

        vestingOf[beneficiary] = VestingSchedule({
            totalAmount: totalAmount,
            released: 0,
            start: start,
            cliff: start + cliffDuration,
            duration: vestingDuration
        });

        emit VestingScheduleSet(
            beneficiary,
            totalAmount,
            start,
            start + cliffDuration,
            vestingDuration
        );
    }

    /// @notice Calculate how many tokens have vested for an address.
    function vestedAmountOf(address account) public view returns (uint256) {
        VestingSchedule memory schedule = vestingOf[account];

        // No vesting schedule = all tokens are vested (freely transferable)
        if (schedule.totalAmount == 0) return balanceOf(account);

        // Before cliff = nothing vested
        if (block.timestamp < schedule.cliff) return 0;

        // After full duration = everything vested
        if (block.timestamp >= schedule.start + schedule.duration) {
            return schedule.totalAmount;
        }

        // Linear vesting between cliff and end
        uint256 elapsed = block.timestamp - schedule.start;
        return (schedule.totalAmount * elapsed) / schedule.duration;
    }

    /// @notice Calculate transferable (vested and unreleased) tokens.
    function transferableOf(address account) public view returns (uint256) {
        VestingSchedule memory schedule = vestingOf[account];

        // No vesting = full balance transferable
        if (schedule.totalAmount == 0) return balanceOf(account);

        uint256 vested = vestedAmountOf(account);
        uint256 locked = schedule.totalAmount > vested
            ? schedule.totalAmount - vested
            : 0;

        uint256 balance = balanceOf(account);
        return balance > locked ? balance - locked : 0;
    }

    function _update(address from, address to, uint256 amount) internal override {
        // Skip vesting checks for mints, burns, and controller operations
        if (from == address(0) || to == address(0) || msg.sender == controller) {
            super._update(from, to, amount);
            return;
        }

        VestingSchedule storage schedule = vestingOf[from];

        // No vesting schedule = normal transfer
        if (schedule.totalAmount == 0) {
            super._update(from, to, amount);
            return;
        }

        // Before cliff = no transfers allowed
        if (block.timestamp < schedule.cliff) revert CliffNotReached();

        // Check transferable amount
        uint256 transferable = transferableOf(from);
        if (amount > transferable) revert InsufficientVestedBalance();

        // Track released amount for accounting
        schedule.released += amount;

        super._update(from, to, amount);
    }
}
```

**关键设计决策**：
- 权益分配按地址进行，由项目所有者设置
- 设置权益分配计划后，代币可自由转让（符合 ERC20 的常规行为）
- 在达到权益分配截止日期之前，代币不可转让
- 权益分配结束后，代币可自由转让

**使用场景**：
- 团队分配          | ✅
- 投资者锁定          | ✅
- 定期工资/补助金        | ✅
- 基于里程碑的分配      | ✅
- 全体持有者保护        | ✅

**注意事项**：
- 使用这种模式会增加复杂性
- 权益分配计划一旦设置就无法更改
- 不会阻止提取操作（控制器操作不受影响）
- 必须在铸造后设置权益分配计划

### 示例：限制代币集中度的机制

防止任何单一持有者积累过多代币：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ConcentrationLimitedToken is ERC20 {
    uint256 public maxHolderBps = 200;  // 2% max per holder
    address public immutable controller;
    uint256 public immutable projectId;
    mapping(address => bool) public isExempt;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId
    ) ERC20(name, symbol) {
        controller = _controller;
        projectId = _projectId;
        isExempt[_controller] = true;  // Controller always exempt
    }

    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    function _update(address from, address to, uint256 amount) internal override {
        // Skip checks for mints, burns, and exempt addresses
        if (from == address(0) || to == address(0) || isExempt[to]) {
            super._update(from, to, amount);
            return;
        }

        // Check concentration limit
        uint256 maxBalance = (totalSupply() * maxHolderBps) / 10000;
        require(balanceOf(to) + amount <= maxBalance, "EXCEEDS_MAX_HOLDING");

        super._update(from, to, amount);
    }

    function setExempt(address account, bool exempt) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        isExempt[account] = exempt;
    }
}
```

**使用场景**：
- 促进代币的广泛分配
- 防止治理权力集中
- 降低市场操纵风险

**注意事项**：
- 流动性池和控制器必须被标记为特殊处理对象
- 在早期高供应阶段，新持有者可能会遇到分配限制

**何时使用这种模式**：
- 当需要限制代币集中度时                | ✅
- 在简单筹款场景中        | ✅
- 需要转账费用或税收时        | ✅
- 需要重新基数机制时        | ✅
- 需要治理投票时        | ✅
- 需要自定义代币逻辑时        | ✅

### 关键权衡**

| 方面            | 标准代币                | 自定义代币                |
|------------------|----------------------|
| 复杂性            | 低                    | 高                    |
| 审计负担          | 由 Juicebox 处理             | 由开发者自行处理             |
| 开销            | 最优化                 | 可能较高                 |
| 集成            | 无缝集成                 | 需要额外测试             |
| 灵活性            | 有限                   | 完全可控                 |

### 关键限制

1. **必须使用 18 位小数**：所有 Juicebox 相关的计算都假设使用 18 位小数
2. **控制器必须获得授权**：铸造/销毁操作必须经过授权
3. **每个项目只能使用一个代币**：设置后无法更改代币
4. `totalSupply()` 的准确性**：提取金额取决于实际供应量
5. **铸造期间不得收取转账费用**：铸造的代币数量必须与请求的数量一致

### 部署检查清单

- [ ] 代币实现了 `canBeAddedTo(projectId)` 方法，并返回 `true`
- [ ] 代币使用 18 位小数
- [ ] 控制器地址获得了铸造权限
- [ ] 控制器地址获得了销毁权限
- [ ] 自定义逻辑（如税收、限制）不会影响控制器操作
- [ ] 经过 Juicebox 的支付流程测试
- [ ] 经过 Juicebox 的提取流程测试
- [ ] 在代币设置后，测试了信用提取功能
- [ ] 安全审计已完成（建议进行）

---

## 决策树：何时编写自定义代码

```
Need custom payment logic?
├── Can 721 hook handle it? → Use 721 hook
├── Can buyback hook handle it? → Use buyback hook
└── Neither works? → Write custom pay hook

Need custom redemption logic?
├── Does 721 hook's burn-to-redeem work? → Use 721 hook
├── Is redemption just against surplus? → Use native cash out
└── Need external data source? → Write custom cash out hook

Need custom payout routing?
├── Can direct beneficiary addresses work? → Use native splits
├── Need token swapping? → Write split hook
├── Need LP deposits? → Write split hook
└── Just multi-recipient? → Use native splits

Need vesting/time-locks?
├── Treasury funds over time? → Use cycling rulesets + payout limits
├── Milestone-based releases? → Queue multiple rulesets
├── Per-holder token locks? → Custom ERC20 with vesting schedules
├── Investor/team cliffs? → Custom ERC20 with vesting schedules
└── Complex conditions? → Consider Revnet or custom

Need time-limited campaign?
├── Fundraise then close forever? → Two rulesets (active + paused)
├── Want immutability? → Burn ownership after deploy
└── May run another campaign? → Keep ownership

Need custom NFT content?
├── Static images per tier? → Use encodedIPFSUri in tier config
├── Dynamic/generative art? → Write IJB721TokenUriResolver
├── Composable/layered NFTs? → Write IJB721TokenUriResolver
└── On-chain SVG? → Write IJB721TokenUriResolver

Need prediction/game mechanics?
├── Fixed redemption values? → Use standard 721-hook
├── Outcome-based payouts? → Extend 721-hook (Defifa pattern)
├── On-chain outcome voting? → Add Governor contract
└── First-owner rewards? → Track in custom delegate

Need custom token mechanics?
├── Standard ERC20 sufficient? → Use deployERC20For()
├── Transfer taxes/fees? → Custom ERC20 with _update override
├── Governance voting? → Custom ERC20Votes
├── Rebasing/elastic supply? → Custom ERC20 (careful with totalSupply)
├── Editable name/symbol? → Custom ERC20 with setName/setSymbol
├── Concentration limits? → Custom ERC20 with max holder checks
├── Per-holder vesting/cliffs? → Custom ERC20 with vesting schedules
└── Pre-existing token? → Wrap with IJBToken interface

Need extended pay functionality on locked project/revnet?
├── Dynamic splits at pay time? → Terminal wrapper
├── Atomic pay + distribute? → Terminal wrapper
├── Token interception/staking? → Terminal wrapper (beneficiary-to-self)
├── Multi-hop payments? → Terminal wrapper
├── Block certain payments? → CAN'T DO (permissionless is a feature)
└── Standard payments work fine? → Use MultiTerminal directly
```

---

## 应避免的错误做法

### 1. 将 721 触发器封装起来

**错误做法**：创建一个封装或代理 721 触发器的数据钩子
**正确做法**：直接使用 721 触发器，并通过规则集配置来实现权益分配

### 2. 为资金池编写自定义权益分配合约

**错误做法**：编写自定义的 VestingSplitHook 来管理资金的持有和释放
**正确做法**：使用支付限额（每个周期都会重置）来实现定期分配

**例外情况**：针对特定场景（如团队分配、投资者锁定），可以使用自定义 ERC20 合约（例如模式 8：具有权益分配功能的代币）

### 3. 为简单循环设置多个规则集

**错误做法**：为 12 个月的权益分配设置 12 个规则集
**正确做法**：使用一个持续 30 天的规则集，并自动循环执行

### 4. 为直接转账设置分割钩子

**错误做法**：创建一个仅用于转发资金的分割钩子
**正确做法**：将目标地址直接设置为分割的接收者

### 5. 为标准提取操作编写自定义提取钩子

**错误做法**：编写自定义钩子来计算提取金额
**正确做法**：将 `cashOutTaxRate` 设置为 0，并让终端负责处理提取操作

---

## 模式 9：限时活动

**用例**：为特定时期筹集资金，之后永久停止支付

**解决方案**：部署两个规则集：一个用于活动期间，另一个用于活动结束后

### 为什么使用这种模式？

许多项目不需要持续性的支付。限时活动更简洁：
- 设定截止日期的众筹
- 在指定时间内铸造 NFT
- 设定截止日期的奖励轮次
- 一次设置即可的简单资金管理方式

### 配置

```solidity
// Ruleset 1: Active Campaign
JBRulesetConfig({
    duration: 30 days,              // Campaign length
    weight: 1e18,                   // Token issuance rate
    decayPercent: 0,
    approvalHook: IJBRulesetApprovalHook(address(0)),
    metadata: JBRulesetMetadata({
        // ... normal settings
        pausePay: false,            // Payments ENABLED
    }),
    // ... splits, fund access, etc.
});

// Ruleset 2: Campaign End (queued immediately)
JBRulesetConfig({
    duration: 0,                    // Lasts forever
    weight: 0,                      // No more tokens issued
    decayPercent: 0,
    approvalHook: IJBRulesetApprovalHook(address(0)),
    metadata: JBRulesetMetadata({
        pausePay: true,             // Payments DISABLED
        // Keep cash outs enabled if desired
    }),
    // No payout limits needed - campaign is over
});
```

### 活动结束后所有权处理

**部署完成后，项目所有者可以选择以下选项**：

**选项 A：保留所有权**
- 可以后续添加新的规则集（启动新的活动）
- 可以调整分配比例或资金访问权限
- 保持灵活性

**选项 B：永久锁定所有权**
```solidity
// Transfer ownership to burn address
PROJECTS.transferFrom(
    deployer,
    0x000000000000000000000000000000000000dEaD,
    projectId
);
```
- 任何人都无法更改规则
- 完全去中心化且不可篡改
- 无法撤销

### 完整流程

```
Deploy with 2 rulesets
         │
         ▼
┌─────────────────────────────────────┐
│  Ruleset 1: Active Campaign         │
│  ├── Duration: 30 days              │
│  ├── Payments: enabled              │
│  └── Tokens issued to payers        │
└─────────────────────────────────────┘
         │
         │ (30 days pass automatically)
         ▼
┌─────────────────────────────────────┐
│  Ruleset 2: Campaign Over           │
│  ├── Duration: forever              │
│  ├── Payments: paused               │
│  └── Cash outs still work           │
└─────────────────────────────────────┘
         │
         ▼
   Owner decides:
   ├── Keep ownership → can modify later
   └── Burn ownership → locked forever
```

### 适用场景**

| 场景                | 适合使用此模式吗？                |
|------------------|-------------------------|
| 一次性众筹        | ✅                |
| 带有截止日期的 NFT 铸造     | ✅                |
| 奖励轮次            | ✅                |
| 持续性的会员/订阅      | ✅（建议使用循环规则集）         |
| 使用 Revnet 的自动发行     | ✅（建议使用 Revnet 部署器）         |

### 主要优势**

1. **简单**：只需两个规则集，无需自定义合约
2. **规则明确**：所有人都知道活动何时结束
3. **可选的不可篡改性**：可以选择锁定所有权或保持灵活性
4. **无需持续管理**：设置一次即可

---

## 模式 10：终端封装器（支付封装器）

**用例**：在不修改规则集的情况下扩展支付功能——特别是对于无法编辑规则集的 Revnet 系统

**解决方案**：创建一个 `IJBTerminal`，它封装了 `JBMultiTerminal` 的功能

### 为什么使用这种模式？

Revnet 和锁定权限的项目无法修改规则集数据钩子。但可以通过封装终端来添加新功能：

| 需求                | 封装器如何解决？                |
|------------------|----------------------|
| 支付时的动态分配比例     | 从元数据中解析信息，然后在转发前进行配置       |
| 同时完成支付和分配       | 将多个操作合并到一个交易中           |
| 代币拦截           | 将接收者设置为封装器的接收者，然后进行质押/转发     |
| 推荐人跟踪         | 从元数据中解析推荐人信息，并记录在链上       |
| 多跳支付           | 接收代币，进行交换，然后支付给另一个项目     |

### 核心架构

```solidity
contract PayWithSplitsTerminal is IJBTerminal {
    IJBMultiTerminal public immutable MULTI_TERMINAL;
    IJBController public immutable CONTROLLER;

    function pay(
        uint256 projectId,
        address token,
        uint256 amount,
        address beneficiary,
        uint256 minReturnedTokens,
        string calldata memo,
        bytes calldata metadata
    ) external payable returns (uint256 beneficiaryTokenCount) {
        // 1. Parse custom metadata
        (JBSplit[] memory splits, bytes memory innerMetadata) = _parseMetadata(metadata);

        // 2. Configure splits if provided
        if (splits.length > 0) {
            _configureSplits(projectId, splits);
        }

        // 3. Forward to underlying terminal
        beneficiaryTokenCount = MULTI_TERMINAL.pay{value: msg.value}(
            projectId, token, amount, beneficiary,
            minReturnedTokens, memo, innerMetadata
        );

        // 4. Distribute reserved tokens
        CONTROLLER.sendReservedTokensToSplitsOf(projectId);

        return beneficiaryTokenCount;
    }
}
```

### 将接收者设置为封装器的模式

通过将接收者设置为封装器的所有者，可以实现特定功能：

```solidity
function payAndStake(uint256 projectId, ..., bytes calldata metadata) external payable {
    (address finalDestination, bytes memory stakingParams) = abi.decode(metadata, (address, bytes));

    // Wrapper receives tokens
    uint256 tokenCount = MULTI_TERMINAL.pay{value: msg.value}(
        projectId, token, amount,
        address(this),  // <-- Beneficiary is wrapper
        minReturnedTokens, "", ""
    );

    // Do something with them
    _stakeTokens(projectToken, tokenCount, finalDestination, stakingParams);
}
```

### 关键思维方式

**错误思维**：“我会使用封装器来阻止不符合条件的支付”

**正确思维**：“我为选择此功能的客户提供增强型服务”

### 与 Swap Terminal 的比较

Swap Terminal 是一个典型的例子：

```
User pays USDC ──► SwapTerminal ──► Swaps to ETH ──► JBMultiTerminal
```

您的封装器遵循相同的架构，但实现逻辑不同

### 提取封装器

这种模式也适用于提取操作。通过封装 `cashOutTokensOf` 来拦截提取的代币：

```solidity
/// @notice Cash out with automatic bridging of redeemed funds.
function cashOutAndBridge(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    address tokenToReclaim,
    uint256 minTokensReclaimed,
    address beneficiary,
    uint256 destChainId,    // Custom: where to bridge
    bytes calldata metadata
) external returns (uint256 reclaimAmount) {
    // 1. Cash out to THIS contract (intercept funds)
    reclaimAmount = MULTI_TERMINAL.cashOutTokensOf(
        holder,
        projectId,
        tokenCount,
        tokenToReclaim,
        minTokensReclaimed,
        address(this),  // <-- Wrapper receives funds
        metadata
    );

    // 2. Bridge the redeemed funds to destination chain
    _bridgeFunds(tokenToReclaim, reclaimAmount, beneficiary, destChainId);

    return reclaimAmount;
}

/// @notice Cash out with automatic swap to different token.
function cashOutAndSwap(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    address tokenToReclaim,
    uint256 minTokensReclaimed,
    address tokenOut,       // Custom: swap to this token
    uint256 minAmountOut,   // Custom: slippage protection
    address beneficiary,
    bytes calldata metadata
) external returns (uint256 amountOut) {
    // 1. Cash out to this contract
    uint256 reclaimAmount = MULTI_TERMINAL.cashOutTokensOf(
        holder,
        projectId,
        tokenCount,
        tokenToReclaim,
        minTokensReclaimed,
        address(this),
        metadata
    );

    // 2. Swap redeemed tokens
    amountOut = _swap(tokenToReclaim, tokenOut, reclaimAmount, minAmountOut);

    // 3. Send swapped tokens to beneficiary
    _sendFunds(tokenOut, amountOut, beneficiary);

    return amountOut;
}
```

### 适用场景**

| 场景                | 是否需要使用终端封装器？                | 是否需要其他替代方案？                |
|------------------|-------------------|-------------------------|
| 需要在支付时进行动态分配比例   | ✅                    | ✅                     |
| Revnet 需要新的支付功能     | ✅                    | （无法修改规则集）               |
| 支付时需要动态分配比例   | ✅                    | ✅                     |
| 原生分配比例         | ✅                    | ✅                     |
| 提取后需要质押         | ✅                    | ✅                     |
| 提取后需要桥接至其他项目     | ✅                    | ✅                     |
| 提取后需要转换为其他代币     | ✅                    | ✅                     |
| 提取后需要同时进行提取和质押   | ✅                    | ✅                     |
| 需要进行提取和质押的操作   | ✅                    | ✅                     |

### 完整示例：支付时的分配比例封装器

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {IJBTerminal} from "@bananapus/core/src/interfaces/IJBTerminal.sol";
import {IJBMultiTerminal} from "@bananapus/core/src/interfaces/IJBMultiTerminal.sol";
import {IJBController} from "@bananapus/core/src/interfaces/IJBController.sol";
import {JBSplit} from "@bananapus/core/src/structs/JBSplit.sol";
import {JBSplitGroup} from "@bananapus/core/src/structs/JBSplitGroup.sol";
import {JBConstants} from "@bananapus/core/src/libraries/JBConstants.sol";
import {JBPermissionIds} from "@bananapus/permission-ids/src/JBPermissionIds.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @notice Terminal wrapper that allows payers to specify reserved token splits at pay time.
/// @dev Useful for revnets where ruleset hooks can't be modified post-deploy.
/// @dev Follows JBSwapTerminalRegistry pattern with shared _acceptFunds helper.
contract PayWithSplitsTerminal is IJBTerminal {
    using SafeERC20 for IERC20;

    // ═══════════════════════════════════════════════════════════════════════
    // ERRORS
    // ═══════════════════════════════════════════════════════════════════════

    error InvalidSplitTotal();

    // ═══════════════════════════════════════════════════════════════════════
    // CONSTANTS
    // ═══════════════════════════════════════════════════════════════════════

    /// @notice Split group ID for reserved tokens.
    uint256 public constant RESERVED_TOKEN_GROUP = 1;

    /// @notice The underlying terminal this wrapper forwards to.
    IJBMultiTerminal public immutable MULTI_TERMINAL;

    /// @notice The controller for setting splits and distributing reserved tokens.
    IJBController public immutable CONTROLLER;

    // ═══════════════════════════════════════════════════════════════════════
    // CONSTRUCTOR
    // ═══════════════════════════════════════════════════════════════════════

    /// @param _multiTerminal The JBMultiTerminal to wrap.
    /// @param _controller The JBController for this deployment.
    constructor(IJBMultiTerminal _multiTerminal, IJBController _controller) {
        MULTI_TERMINAL = _multiTerminal;
        CONTROLLER = _controller;
    }

    // ═══════════════════════════════════════════════════════════════════════
    // EXTERNAL FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════

    /// @notice Pay a project with optional dynamic splits specified in metadata.
    /// @dev If metadata contains splits, they're applied before payment. Reserved tokens
    ///      are distributed after payment completes.
    /// @param projectId The project to pay.
    /// @param token The token to pay with (JBConstants.NATIVE_TOKEN for ETH).
    /// @param amount The amount to pay (ignored for ETH, uses msg.value).
    /// @param beneficiary Who receives the project tokens.
    /// @param minReturnedTokens Minimum tokens to receive (slippage protection).
    /// @param memo Payment memo.
    /// @param metadata ABI-encoded (JBSplit[] splits, bytes innerMetadata).
    ///        - splits: Reserved token split configuration (empty array to skip)
    ///        - innerMetadata: Passed through to MultiTerminal (for hooks, etc.)
    /// @return beneficiaryTokenCount The number of tokens minted to beneficiary.
    function pay(
        uint256 projectId,
        address token,
        uint256 amount,
        address beneficiary,
        uint256 minReturnedTokens,
        string calldata memo,
        bytes calldata metadata
    ) external payable returns (uint256 beneficiaryTokenCount) {
        bytes memory innerMetadata;

        // Parse and apply splits if metadata provided
        if (metadata.length > 0) {
            JBSplit[] memory splits;
            (splits, innerMetadata) = abi.decode(metadata, (JBSplit[], bytes));

            if (splits.length > 0) {
                _validateAndSetSplits(projectId, splits);
            }
        }

        // Accept funds and get value to forward
        uint256 valueToSend = _acceptFunds(token, amount, address(MULTI_TERMINAL));

        // Forward payment to MultiTerminal
        beneficiaryTokenCount = MULTI_TERMINAL.pay{value: valueToSend}(
            projectId,
            token,
            amount,
            beneficiary,
            minReturnedTokens,
            memo,
            innerMetadata
        );

        // Distribute reserved tokens to the configured splits
        CONTROLLER.sendReservedTokensToSplitsOf(projectId);

        return beneficiaryTokenCount;
    }

    /// @notice Add to a project's balance without receiving tokens.
    /// @dev Pass-through to MultiTerminal.
    function addToBalanceOf(
        uint256 projectId,
        address token,
        uint256 amount,
        bool shouldReturnHeldFees,
        string calldata memo,
        bytes calldata metadata
    ) external payable {
        // Accept funds and get value to forward
        uint256 valueToSend = _acceptFunds(token, amount, address(MULTI_TERMINAL));

        MULTI_TERMINAL.addToBalanceOf{value: valueToSend}(
            projectId,
            token,
            amount,
            shouldReturnHeldFees,
            memo,
            metadata
        );
    }

    /// @notice Check accounting contexts accepted by underlying terminal.
    function accountingContextForTokenOf(
        uint256 projectId,
        address token
    ) external view returns (JBAccountingContext memory) {
        return MULTI_TERMINAL.accountingContextForTokenOf(projectId, token);
    }

    /// @notice Get all accounting contexts for a project.
    function accountingContextsOf(
        uint256 projectId
    ) external view returns (JBAccountingContext[] memory) {
        return MULTI_TERMINAL.accountingContextsOf(projectId);
    }

    /// @notice Get current surplus in a project's terminal.
    function currentSurplusOf(
        uint256 projectId,
        JBAccountingContext[] calldata accountingContexts,
        uint256 decimals,
        uint256 currency
    ) external view returns (uint256) {
        return MULTI_TERMINAL.currentSurplusOf(
            projectId,
            accountingContexts,
            decimals,
            currency
        );
    }

    // ═══════════════════════════════════════════════════════════════════════
    // INTERNAL FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════════

    /// @notice Accept funds from the caller and prepare them for forwarding.
    /// @dev For ERC20s: transfers from sender, approves spender.
    /// @dev For ETH: returns msg.value to forward.
    /// @dev Pattern from JBSwapTerminalRegistry - consolidates token handling.
    /// @param token The token being paid (NATIVE_TOKEN for ETH).
    /// @param amount The amount being paid.
    /// @param spender The address that will spend the tokens (the terminal).
    /// @return valueToSend The ETH value to forward (0 for ERC20s).
    function _acceptFunds(
        address token,
        uint256 amount,
        address spender
    ) internal returns (uint256 valueToSend) {
        if (token == JBConstants.NATIVE_TOKEN) {
            // For ETH, just return msg.value to forward
            return msg.value;
        }

        // For ERC20s: pull tokens from sender
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);

        // Approve the spender (terminal) to pull tokens
        IERC20(token).forceApprove(spender, amount);

        // No ETH to forward for ERC20 payments
        return 0;
    }

    /// @notice Validate splits sum to 100% and set them on the controller.
    /// @dev This wrapper must have SET_SPLIT_GROUPS permission on the project.
    function _validateAndSetSplits(uint256 projectId, JBSplit[] memory splits) internal {
        // Validate splits sum to 100%
        uint256 total;
        for (uint256 i; i < splits.length; i++) {
            total += splits[i].percent;
        }
        if (total != JBConstants.SPLITS_TOTAL_PERCENT) revert InvalidSplitTotal();

        // Get current ruleset ID
        (JBRuleset memory ruleset,) = CONTROLLER.currentRulesetOf(projectId);

        // Build split group
        JBSplitGroup[] memory groups = new JBSplitGroup[](1);
        groups[0] = JBSplitGroup({
            groupId: RESERVED_TOKEN_GROUP,
            splits: splits
        });

        // Set splits (requires SET_SPLIT_GROUPS permission)
        CONTROLLER.setSplitGroupsOf(projectId, ruleset.id, groups);
    }

    /// @notice Required for receiving ETH refunds from terminal.
    receive() external payable {}
}
```

### 客户端使用示例（TypeScript）

```typescript
import {
  encodeFunctionData,
  encodeAbiParameters,
  parseAbiParameters,
  parseUnits,
  Address
} from 'viem';

const SPLITS_TOTAL_PERCENT = 1_000_000_000n; // 1e9

// Build split configuration
function encodeSplits(recipients: { address: Address; percent: number }[]) {
  // Convert percentages (0-100) to JB format (0-1e9)
  const splits = recipients.map(r => ({
    preferredProjectId: 0n,
    preferredBeneficiary: r.address,
    percent: BigInt(Math.floor(r.percent * 10_000_000)), // 1% = 10_000_000
    lockedUntil: 0n,
    hook: '0x0000000000000000000000000000000000000000' as Address,
  }));

  return splits;
}

// Encode metadata for pay call
function encodePayMetadata(
  splits: ReturnType<typeof encodeSplits>,
  innerMetadata: `0x${string}` = '0x'
) {
  return encodeAbiParameters(
    parseAbiParameters([
      '(uint256 preferredProjectId, address preferredBeneficiary, uint256 percent, uint256 lockedUntil, address hook)[]',
      'bytes'
    ]),
    [splits, innerMetadata]
  );
}

// Example: Pay with dynamic splits
async function payWithSplits(
  walletClient: WalletClient,
  wrapperAddress: Address,
  projectId: bigint,
  paymentAmount: bigint,
  recipients: { address: Address; percent: number }[]
) {
  const splits = encodeSplits(recipients);
  const metadata = encodePayMetadata(splits);

  const NATIVE_TOKEN = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE';

  const hash = await walletClient.writeContract({
    address: wrapperAddress,
    abi: PAY_WITH_SPLITS_ABI,
    functionName: 'pay',
    args: [
      projectId,
      NATIVE_TOKEN,
      paymentAmount,
      walletClient.account.address, // beneficiary
      0n, // minReturnedTokens
      'Payment with custom splits',
      metadata
    ],
    value: paymentAmount
  });

  return hash;
}

// Usage
await payWithSplits(
  walletClient,
  '0x...wrapper',
  3n, // projectId
  parseUnits('1', 18), // 1 ETH
  [
    { address: '0xaaa...', percent: 50 }, // 50% to address A
    { address: '0xbbb...', percent: 30 }, // 30% to address B
    { address: '0xccc...', percent: 20 }, // 20% to address C
  ]
);
```

### 部署与权限设置

```solidity
// Deploy the wrapper
PayWithSplitsTerminal wrapper = new PayWithSplitsTerminal(
    IJBMultiTerminal(MULTI_TERMINAL_ADDRESS),
    IJBController(CONTROLLER_ADDRESS)
);

// Grant SET_SPLIT_GROUPS permission to wrapper
// (Must be called by project owner or someone with SET_PERMISSIONS)
JBPermissionsData[] memory permissions = new JBPermissionsData[](1);
permissions[0] = JBPermissionsData({
    operator: address(wrapper),
    projectId: PROJECT_ID,
    permissionIds: _asSingletonArray(JBPermissionIds.SET_SPLIT_GROUPS)
});

PERMISSIONS.setPermissionsFor(projectOwner, permissions);
```

### 关键注意事项**

- 如果需要设置分配比例，必须授予封装器相应的权限
- 可以存在多个封装器，用于不同的目的，它们之间不会冲突
- 封装器可以链式使用：WrapperA → WrapperB → MultiTerminal
- 对于 Revnet 系统，封装器通常是部署后添加功能的唯一方式
- 仔细验证元数据——解析元数据可能会带来安全风险

---

## 模式 11：生成收益的钩子（与 Aave 的集成）

**用例**：将贡献资金存入收益协议（如 Aave、Compound 等），并将收益路由到项目余额，同时允许提取本金

**解决方案**：结合支付/提取钩子，将资金存入 Aave，并将收益与本金分开处理

### 为什么使用这种模式？

这种模式允许投资者通过 DeFi 协议获得收益；投资者可以随时提取本金；收益会流入项目余额；同时保护本金和收益

### 架构

```
┌─────────────────────────────────────────────────────────────────┐
│  Payment Flow                                                    │
│  User pays → Hook deposits to Aave → Principal tracked           │
│                                                                  │
│  Yield Flow                                                      │
│  Aave earns yield → Hook withdraws → addToBalanceOf()           │
│                     → Appears in project balance                 │
│                     → Team uses sendPayoutsOf()                  │
│                                                                  │
│  Cash Out Flow                                                   │
│  User cashes out → Hook withdraws from Aave → Direct to user    │
│                    (bypasses terminal, separate from yield)      │
└─────────────────────────────────────────────────────────────────┘
```

### 核心钩子结构

```solidity
contract YieldHook is IJBPayHook, IJBCashOutHook, IJBRulesetDataHook {
    IPool public immutable AAVE_POOL;
    IJBTerminal public immutable TERMINAL;

    mapping(uint256 projectId => uint256) public principalDeposited;
    mapping(uint256 projectId => uint256) public principalWithdrawn;
    mapping(uint256 projectId => uint256) public yieldWithdrawn;

    struct ProjectConfig {
        address principalToken;    // USDC, ETH, etc.
        address aToken;           // Corresponding aToken
        uint256 yieldThreshold;   // Min yield before transfer
        bool active;
    }
}
```

### 数据钩子：将资金路由到 Aave

```solidity
function beforePayRecordedWith(
    JBBeforePayRecordedContext calldata context
) external view override returns (
    uint256 weight,
    JBPayHookSpecification[] memory hookSpecifications
) {
    weight = context.weight;

    // Forward ALL payment funds to this hook for Aave deposit
    hookSpecifications = new JBPayHookSpecification[](1);
    hookSpecifications[0] = JBPayHookSpecification({
        hook: IJBPayHook(address(this)),
        amount: context.amount.value,  // Must be explicit, not 0
        metadata: ""
    });
}
```

### 支付钩子：将资金存入 Aave

```solidity
function afterPayRecordedWith(
    JBAfterPayRecordedContext calldata context
) external payable override {
    ProjectConfig storage config = projectConfigs[context.projectId];
    uint256 amount = context.forwardedAmount.value;

    // Deposit to Aave
    IERC20(config.principalToken).forceApprove(address(AAVE_POOL), amount);
    AAVE_POOL.supply(config.principalToken, amount, address(this), 0);

    // Track principal
    principalDeposited[context.projectId] += amount;

    // Check if yield should be transferred
    _maybeTransferYield(context.projectId);
}
```

### 提取钩子：提取本金

```solidity
function beforeCashOutRecordedWith(
    JBBeforeCashOutRecordedContext calldata context
) external view override returns (
    uint256 cashOutTaxRate,
    uint256 cashOutCount,
    uint256 totalSupply,
    JBCashOutHookSpecification[] memory hookSpecifications
) {
    // Calculate user's share of principal
    uint256 availablePrincipal = principalDeposited[context.projectId]
                                - principalWithdrawn[context.projectId];
    uint256 userShare = (availablePrincipal * context.cashOutCount) / context.totalSupply;

    cashOutTaxRate = 0;  // No tax on principal
    cashOutCount = context.cashOutCount;
    totalSupply = context.totalSupply;

    // Route to this hook for Aave withdrawal
    hookSpecifications = new JBCashOutHookSpecification[](1);
    hookSpecifications[0] = JBCashOutHookSpecification({
        hook: IJBCashOutHook(address(this)),
        amount: userShare,
        metadata: ""
    });
}

function afterCashOutRecordedWith(
    JBAfterCashOutRecordedContext calldata context
) external payable override {
    ProjectConfig storage config = projectConfigs[context.projectId];
    uint256 amount = context.forwardedAmount.value;

    // Withdraw principal from Aave directly to user
    AAVE_POOL.withdraw(config.principalToken, amount, context.beneficiary);
    principalWithdrawn[context.projectId] += amount;
}
```

### 收益管理：将收益路由到项目余额

```solidity
function _maybeTransferYield(uint256 projectId) internal {
    ProjectConfig storage config = projectConfigs[projectId];
    uint256 availableYield = _calculateAvailableYield(projectId);

    if (availableYield >= config.yieldThreshold) {
        // Withdraw yield from Aave to this contract
        uint256 withdrawn = AAVE_POOL.withdraw(
            config.principalToken,
            availableYield,
            address(this)
        );

        // Approve terminal
        IERC20(config.principalToken).forceApprove(address(TERMINAL), withdrawn);

        // Add to project balance (team can then use sendPayoutsOf)
        TERMINAL.addToBalanceOf(
            projectId,
            config.principalToken,
            withdrawn,
            false,  // shouldReturnHeldFees
            "",     // memo
            ""      // metadata
        );

        yieldWithdrawn[projectId] += withdrawn;
    }
}

function _calculateAvailableYield(uint256 projectId) internal view returns (uint256) {
    ProjectConfig storage config = projectConfigs[projectId];
    uint256 totalBalance = IERC20(config.aToken).balanceOf(address(this));
    uint256 principalRemaining = principalDeposited[projectId] - principalWithdrawn[projectId];

    if (totalBalance > principalRemaining + yieldWithdrawn[projectId]) {
        return totalBalance - principalRemaining - yieldWithdrawn[projectId];
    }
    return 0;
}
```

### 项目配置

```solidity
// Ruleset must enable data hooks
JBRulesetMetadata({
    useDataHookForPay: true,      // Enable beforePay/afterPay
    useDataHookForCashOut: true,  // Enable beforeCashOut/afterCashOut
    dataHook: address(yieldHook), // Your hook address
    // ...
});
```

### 适用场景**

| 场景                | 适合使用此模式吗？                | -------------------------|
| 需要收益支持的融资       | ✅                    |
| 与 Aave/Compound 的集成     | ✅                    |
| 保护本金的投资         | ✅                    |
| 需要整合质押奖励的融资     | ✅                    | （需根据质押协议进行调整）         |
| 标准众筹           | ✅                    | （建议使用原生终端）           |
| 基于 NFT 的融资       | ✅                    | （建议使用 721 触发器）           |

### 关键实现注意事项**

1. `JBPayHookSpecification` 中的 `amount` 必须设置为 `context.amount.value`，以便正确转发资金
2. 使用 `addToBalanceOf()` 将收益添加到项目余额
3. 分离本金和收益的跟踪
4. 提供紧急情况下的直接提取功能
5. 使用收益阈值进行批量转账

### 参考实现

- **YeeHaw 模式**：基于收益的众筹模式
- 使用了 jb-yield-to-balance-pattern 中的实现方式

---

## 参考实现示例

- **Vesting + NFT**：Drip x Juicebox（参见 `/jb-project` 了解部署脚本）
- **自动资金池**：Revnet（`revnet-core-v5`）
- **NFT 奖励**：任何使用 `JB721TiersHookProjectDeployer` 的项目
- **自定义 NFT 内容**：[banny-retail-v5](https://github.com/mejango/banny-retail-v5)——支持可组合的 SVG NFT 和装饰性外观
- **预测游戏**：[defifa-collection-deployer-v5](https://github.com/BallKidz/defifa-collection-deployer-v5)——具有动态提取金额和链上治理功能的游戏

## 相关技能

- `/jb-simplify`：用于减少自定义代码的 checklist
- `/jb-project`：项目部署和配置工具
- `/jb-ruleset`：规则集配置细节
- `/jb-v5-impl`：深度实现细节
- `/jb-terminal-wrapper`：完整的终端封装器实现细节