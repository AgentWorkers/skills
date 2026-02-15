---
name: jb-terminal-wrapper
description: |
  Terminal wrapper pattern for extending JBMultiTerminal functionality. Use when: (1) need dynamic
  splits at pay time, (2) revnet can't modify ruleset data hooks, (3) want atomic pay + distribute
  operations, (4) need to intercept/redirect tokens before delivery, (5) implementing pay-time
  configuration, (6) cash out + bridge/swap in one tx, (7) cash out + stake redeemed funds.
  Covers IJBTerminal implementation, _acceptFunds pattern from JBSwapTerminalRegistry, beneficiary
  manipulation for both pay and cash out flows, and the critical mental model that wrappers are
  additive (not restrictive).
---

# 终端封装模式（Terminal Wrapper Pattern）

## 问题

Revnets 及其他项目通常需要扩展的支付功能，而这些功能仅通过规则集数据钩子（ruleset data hooks）是无法实现的。常见的需求包括：
- 在支付时动态分配金额
- 拦截并重定向代币
- 原子化的多步骤操作（支付 + 分发）
- 提供特定于客户端的特性，同时不破坏无权限访问（permissionless access）的原则

## 使用场景 / 触发条件

在以下情况下使用此模式：
- 构建需要动态配置的支付流程
- 在无法编辑规则集钩子的 revnets 环境中工作
- 需要将多个操作原子化地组合在一起
- 需要拦截代币以进行进一步处理
- 实现“支付后执行某操作”的流程

## 解决方案

### 核心架构

创建一个自定义的 `IJBTerminal`，它封装了 `JBMultiTerminal`。使用来自 `JBSwapTerminalRegistry` 的共享 `_acceptFunds` 辅助函数来统一处理 ETH/ERC20 交易：

```solidity
contract PayWithSplitsTerminal is IJBTerminal {
    using SafeERC20 for IERC20;

    IJBMultiTerminal public immutable MULTI_TERMINAL;
    IJBController public immutable CONTROLLER;

    constructor(IJBMultiTerminal _multiTerminal, IJBController _controller) {
        MULTI_TERMINAL = _multiTerminal;
        CONTROLLER = _controller;
    }

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

        // 3. Accept funds (handles ETH/ERC20 uniformly)
        uint256 valueToSend = _acceptFunds(token, amount, address(MULTI_TERMINAL));

        // 4. Forward to underlying terminal
        beneficiaryTokenCount = MULTI_TERMINAL.pay{value: valueToSend}(
            projectId,
            token,
            amount,
            beneficiary,
            minReturnedTokens,
            memo,
            innerMetadata
        );

        // 5. Distribute reserved tokens
        CONTROLLER.sendReservedTokensToSplitsOf(projectId);

        return beneficiaryTokenCount;
    }

    /// @notice Accept funds from caller and prepare for forwarding.
    /// @dev Pattern from JBSwapTerminalRegistry - consolidates token handling.
    function _acceptFunds(
        address token,
        uint256 amount,
        address spender
    ) internal returns (uint256 valueToSend) {
        if (token == JBConstants.NATIVE_TOKEN) {
            return msg.value; // Forward ETH
        }

        // ERC20: pull from sender, approve spender
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        IERC20(token).forceApprove(spender, amount);
        return 0; // No ETH to forward
    }
}
```

### 受益人操作模式（Beneficiary Manipulation Pattern）

通过将受益人设置为封装器本身来拦截代币：

```solidity
function payAndStake(
    uint256 projectId,
    address token,
    uint256 amount,
    uint256 minReturnedTokens,
    bytes calldata metadata
) external payable returns (uint256 tokenCount) {
    // Parse user's desired destination from metadata
    (address finalDestination, bytes memory stakingParams) = abi.decode(
        metadata,
        (address, bytes)
    );

    // Receive tokens to this contract
    tokenCount = MULTI_TERMINAL.pay{value: msg.value}(
        projectId,
        token,
        amount,
        address(this),  // <-- Wrapper receives tokens
        minReturnedTokens,
        "",
        ""
    );

    // Do something with the tokens
    IERC20 projectToken = IERC20(CONTROLLER.TOKENS().tokenOf(projectId));

    // Example: stake them somewhere on behalf of user
    _stakeTokens(projectToken, tokenCount, finalDestination, stakingParams);

    return tokenCount;
}
```

### 元数据编码（客户端侧）（Metadata Encoding, Client Side）

```typescript
import { encodeAbiParameters, parseAbiParameters } from 'viem';

// For dynamic splits
const metadata = encodeAbiParameters(
  parseAbiParameters('(address preferredBeneficiary, uint256 percent, uint256 lockedUntil)[], bytes'),
  [
    [
      { preferredBeneficiary: '0x...', percent: 500000000n, lockedUntil: 0n }, // 50%
      { preferredBeneficiary: '0x...', percent: 500000000n, lockedUntil: 0n }, // 50%
    ],
    '0x' // Inner metadata for MultiTerminal
  ]
);

// For beneficiary redirection
const metadata = encodeAbiParameters(
  parseAbiParameters('address finalDestination, bytes stakingParams'),
  [userAddress, stakingCalldata]
);
```

### 关键思维模式（Critical Mental Model）

**错误的想法**：“我会使用封装器来阻止不符合条件 X 的支付”
**实际情况**：用户始终可以直接调用 `JBMultiTerminal.pay()`。

**正确的想法**：“我会使用封装器为选择使用该功能的客户提供增强功能”

## 使用案例

| 使用场景 | 封装器如何提供帮助 |
|----------|-------------------|
| **支付封装器** | |
| 支付时动态分配金额 | 从元数据中解析分配比例，并在支付前进行配置 |
| 支付 + 分配预留资金 | 原子化操作，无需单独的交易 |
| 拦截代币 | 将代币接收至封装器自身，然后进行质押、锁定或转发 |
| 推荐人跟踪 | 从元数据中解析推荐人信息，并在链上记录 |
| 条件逻辑 | 在转发到 `JBMultiTerminal` 之前检查条件 |
| 多跳支付 | 接收代币，然后兑换成其他项目所需的货币 |
| **提现封装器** | |
| 提现 + 桥接 | 拦截已赎回的资金，并将其桥接到另一个区块链 |
| 提现 + 兑换 | 在支付前将赎回的 ETH 兑换为稳定币 |
| 提现 + 质押 | 将赎回的资金质押到其他协议中 |
| 提现 + 加入流动性池 | 将赎回的资金加入流动性池 |

### 提现封装器模式（Cash Out Wrapper Pattern）

对于提现操作，同样可以使用将受益人设置为封装器自身的方法：

```solidity
/// @notice Cash out with automatic swap to different token.
function cashOutAndSwap(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    address tokenToReclaim,
    uint256 minTokensReclaimed,
    address tokenOut,       // Custom param: swap to this
    uint256 minAmountOut,   // Custom param: slippage
    address beneficiary,
    bytes calldata metadata
) external returns (uint256 amountOut) {
    // 1. Cash out to THIS contract (intercept funds)
    uint256 reclaimAmount = MULTI_TERMINAL.cashOutTokensOf(
        holder,
        projectId,
        tokenCount,
        tokenToReclaim,
        minTokensReclaimed,
        address(this),  // <-- Wrapper receives redeemed funds
        metadata
    );

    // 2. Swap redeemed tokens to desired output
    amountOut = _swap(tokenToReclaim, tokenOut, reclaimAmount, minAmountOut);

    // 3. Send swapped tokens to beneficiary
    _sendFunds(tokenOut, amountOut, beneficiary);

    return amountOut;
}

/// @notice Cash out with automatic bridging.
function cashOutAndBridge(
    address holder,
    uint256 projectId,
    uint256 tokenCount,
    address tokenToReclaim,
    uint256 minTokensReclaimed,
    address beneficiary,
    uint256 destChainId,
    bytes calldata metadata
) external returns (uint256 reclaimAmount) {
    // 1. Cash out to this contract
    reclaimAmount = MULTI_TERMINAL.cashOutTokensOf(
        holder,
        projectId,
        tokenCount,
        tokenToReclaim,
        minTokensReclaimed,
        address(this),
        metadata
    );

    // 2. Bridge funds to destination chain
    _bridgeFunds(tokenToReclaim, reclaimAmount, beneficiary, destChainId);

    return reclaimAmount;
}
```

### 与交换终端的比较（Comparison with Swap Terminal）

交换终端（Swap Terminal）是这种模式的典型示例：

```
User pays with USDC ──► SwapTerminal ──► Swaps to ETH ──► JBMultiTerminal
                        (wraps + transforms)
```

你的封装器遵循相同的架构，但具有不同的处理逻辑。

## 验证步骤

1. 部署指向现有 `JBMultiTerminal` 的封装器
2. 测试直接使用 `JBMultiTerminal` 进行的支付是否仍然可以正常工作（无需权限）
3. 测试使用封装器进行的支付是否具有增强功能
4. 验证原子化操作是否能够完整执行或一起回滚
5. 测试元数据解析的边缘情况（如数据为空或格式错误）

## 示例

**支付时动态分配金额的完整实现示例：**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {IJBTerminal} from "@bananapus/core/src/interfaces/IJBTerminal.sol";
import {IJBMultiTerminal} from "@bananapus/core/src/interfaces/IJBMultiTerminal.sol";
import {IJBController} from "@bananapus/core/src/interfaces/IJBController.sol";
import {IJBSplits} from "@bananapus/core/src/interfaces/IJBSplits.sol";
import {JBSplit} from "@bananapus/core/src/structs/JBSplit.sol";
import {JBSplitGroup} from "@bananapus/core/src/structs/JBSplitGroup.sol";

contract DynamicSplitsTerminal is IJBTerminal {
    IJBMultiTerminal public immutable MULTI_TERMINAL;
    IJBController public immutable CONTROLLER;

    // Split group ID for reserved tokens
    uint256 constant RESERVED_TOKEN_GROUP = 1;

    error InvalidSplitTotal();

    constructor(IJBMultiTerminal _multiTerminal, IJBController _controller) {
        MULTI_TERMINAL = _multiTerminal;
        CONTROLLER = _controller;
    }

    /// @notice Pay a project with dynamic splits specified in metadata
    /// @param projectId The project to pay
    /// @param token The token to pay with (use JBConstants.NATIVE_TOKEN for ETH)
    /// @param amount The amount to pay
    /// @param beneficiary Who receives the project tokens
    /// @param minReturnedTokens Minimum tokens to receive (slippage protection)
    /// @param memo Payment memo
    /// @param metadata ABI-encoded (JBSplit[], bytes innerMetadata)
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

        // Forward payment to MultiTerminal
        beneficiaryTokenCount = MULTI_TERMINAL.pay{value: msg.value}(
            projectId,
            token,
            amount,
            beneficiary,
            minReturnedTokens,
            memo,
            innerMetadata
        );

        // Distribute reserved tokens to the new splits
        CONTROLLER.sendReservedTokensToSplitsOf(projectId);

        return beneficiaryTokenCount;
    }

    function _validateAndSetSplits(uint256 projectId, JBSplit[] memory splits) internal {
        // Validate splits sum to 100% (1e9 = JBConstants.SPLITS_TOTAL_PERCENT)
        uint256 total;
        for (uint256 i; i < splits.length; i++) {
            total += splits[i].percent;
        }
        if (total != 1e9) revert InvalidSplitTotal();

        // Get current ruleset
        uint256 rulesetId = CONTROLLER.currentRulesetOf(projectId).id;

        // Set splits for reserved token group
        JBSplitGroup[] memory groups = new JBSplitGroup[](1);
        groups[0] = JBSplitGroup({
            groupId: RESERVED_TOKEN_GROUP,
            splits: splits
        });

        CONTROLLER.setSplitGroupsOf(projectId, rulesetId, groups);
    }

    // Implement other IJBTerminal functions as pass-through...
    function addToBalanceOf(
        uint256 projectId,
        address token,
        uint256 amount,
        bool shouldReturnHeldFees,
        string calldata memo,
        bytes calldata metadata
    ) external payable {
        MULTI_TERMINAL.addToBalanceOf{value: msg.value}(
            projectId, token, amount, shouldReturnHeldFees, memo, metadata
        );
    }
}
```

## 注意事项

- 如果需要设置分配比例，封装器必须被授予相应的权限（需添加到项目的权限系统中）
- 需要考虑额外操作所产生的 gas 成本
- 元数据解析会增加攻击面——请仔细验证
- 对于 revnets 来说，这通常是部署后添加功能的唯一方法
- 可以存在多个用于不同目的的封装器——它们之间不会产生冲突
- 封装器可以链式使用：WrapperA → WrapperB → MultiTerminal

## 相关技能

- `/jb-patterns` – 所有 JB V5 设计模式（包含此模式的简化版本）
- `/jb-pay-hook` – 用于支付时逻辑的数据钩子（当规则集允许时）
- `/jb-split-hook` – 自定义的分配逻辑
- `/jb-v5-api` – 核心终端和控制器接口