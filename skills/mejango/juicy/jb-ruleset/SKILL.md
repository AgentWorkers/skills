---
name: jb-ruleset
description: 配置并安排 Juicebox V5 规则集的运行顺序。设计规则集参数，包括发放频率、预留频率、提现税率、分成比例、支付限额以及审批流程。生成用于排队新规则集的脚本。
---

# Juicebox V5 规则集配置

用于设计和排队 Juicebox V5 项目的规则集。

## 什么是规则集？

规则集是具有时间限制的配置包，用于定义项目的行为：
- **代币经济**：发行速率（minting rate）、预留速率（reserved rate）
- **提现行为**：提现税率（cash out tax rate）
- **资金分配**：支付限额（payout limits）、分配比例（splits）
- **治理**：用于变更控制的审批机制（approval hooks）

当一个规则集结束后，下一个排队的规则集将生效。如果没有规则集排队，则当前规则集将重新启用（可选择减少发行量）。

## 规则集参数

### JBRuleset（只读状态）

```solidity
struct JBRuleset {
    uint256 cycleNumber;        // Increments each cycle
    uint256 id;                 // Unique ruleset ID
    uint256 basedOnId;          // Previous ruleset ID
    uint256 start;              // Start timestamp
    uint256 duration;           // Duration (0 = indefinite)
    uint256 weight;             // Token minting weight (18 decimals)
    uint256 weightCutPercent;   // Weight cut per cycle (0-1000000000, where 1e9 = 100%)
    IJBRulesetApprovalHook approvalHook;
    JBRulesetMetadata metadata;
}
```

### JBRulesetMetadata

```solidity
struct JBRulesetMetadata {
    uint256 reservedRate;       // Reserved tokens (0-10000, where 10000 = 100%)
    uint256 cashOutTaxRate;     // Tax on cash outs (0-10000)
    uint256 baseCurrency;       // Base currency for accounting
    bool pausePay;              // Pause payments
    bool pauseCashOut;          // Pause cash outs
    bool pauseTransfers;        // Pause token transfers
    bool allowOwnerMinting;     // Owner can mint tokens
    bool allowTerminalMigration;
    bool allowSetTerminals;
    bool allowSetController;
    bool allowAddAccountingContexts;
    bool allowAddPriceFeed;
    bool ownerMustSendPayouts;
    bool holdFees;              // Hold fees for potential refund
    bool useTotalSurplusForCashOuts;
    bool useDataHookForPay;     // Enable pay data hook
    bool useDataHookForCashOut; // Enable cash out data hook
    address dataHook;           // Data hook address
    uint256 metadata;           // Custom metadata bits
}
```

## 排队规则集

使用 `JBController.queueRulesetsOf()` 来排队未来的规则集：

```solidity
function queueRulesetsOf(
    uint256 projectId,
    JBRulesetConfig[] calldata rulesetConfigurations,
    string calldata memo
) external returns (uint256 rulesetId);
```

## 配置示例

### 基本规则集（无限期）

```solidity
JBRulesetMetadata memory metadata = JBRulesetMetadata({
    reservedRate: 1000,         // 10% reserved
    cashOutTaxRate: 0,          // No cash out tax
    baseCurrency: uint32(uint160(JBConstants.NATIVE_TOKEN)),
    pausePay: false,
    pauseCashOut: false,
    pauseTransfers: false,
    allowOwnerMinting: false,
    allowTerminalMigration: false,
    allowSetTerminals: false,
    allowSetController: false,
    allowAddAccountingContexts: false,
    allowAddPriceFeed: false,
    ownerMustSendPayouts: false,
    holdFees: false,
    useTotalSurplusForCashOuts: false,
    useDataHookForPay: false,
    useDataHookForCashOut: false,
    dataHook: address(0),
    metadata: 0
});

JBRulesetConfig memory config = JBRulesetConfig({
    mustStartAtOrAfter: 0,
    duration: 0,                // Indefinite
    weight: 1e18,               // 1 token per unit
    weightCutPercent: 0,
    approvalHook: IJBRulesetApprovalHook(address(0)),
    metadata: metadata,
    splitGroups: new JBSplitGroup[](0),
    fundAccessLimitGroups: new JBFundAccessLimitGroup[](0)
});
```

### 带有发行量削减的每周周期

```solidity
JBRulesetConfig memory config = JBRulesetConfig({
    mustStartAtOrAfter: 0,
    duration: 7 days,           // 1 week cycles
    weight: 1000e18,            // Start at 1000 tokens/ETH
    weightCutPercent: 50000000, // 5% weight cut per cycle (50000000 / 1e9)
    approvalHook: IJBRulesetApprovalHook(address(0)),
    metadata: metadata,
    splitGroups: splitGroups,
    fundAccessLimitGroups: fundAccessLimits
});
```

### 带有审批机制的规则集（3 天延迟）

```solidity
// JBDeadline requires 3 days notice for ruleset changes
IJBRulesetApprovalHook approvalHook = IJBRulesetApprovalHook(JB_DEADLINE);

JBRulesetConfig memory config = JBRulesetConfig({
    mustStartAtOrAfter: 0,
    duration: 30 days,
    weight: 1e18,
    weightCutPercent: 0,
    approvalHook: approvalHook,  // Requires advance notice
    metadata: metadata,
    splitGroups: splitGroups,
    fundAccessLimitGroups: fundAccessLimits
});
```

### 带有数据通知机制的规则集

```solidity
JBRulesetMetadata memory metadata = JBRulesetMetadata({
    // ... other fields
    useDataHookForPay: true,
    useDataHookForCashOut: false,
    dataHook: address(myBuybackHook),
    // ...
});
```

## 分配配置

### 支付分配

在触发支付时分配资金：

```solidity
JBSplit[] memory payoutSplits = new JBSplit[](2);

// 50% to treasury
payoutSplits[0] = JBSplit({
    preferAddToBalance: false,
    percent: 500_000_000,       // 50% (out of 1e9)
    projectId: 0,               // Not a project
    beneficiary: payable(treasuryAddress),
    lockedUntil: 0,
    hook: IJBSplitHook(address(0))
});

// 50% to another project
payoutSplits[1] = JBSplit({
    preferAddToBalance: true,   // Add to balance, not pay
    percent: 500_000_000,
    projectId: otherProjectId,
    beneficiary: payable(address(0)),
    lockedUntil: 0,
    hook: IJBSplitHook(address(0))
});

JBSplitGroup[] memory splitGroups = new JBSplitGroup[](1);
splitGroups[0] = JBSplitGroup({
    groupId: 1,                 // Payout splits group
    splits: payoutSplits
});
```

### 预留代币分配

分配预留代币：

```solidity
JBSplit[] memory reservedSplits = new JBSplit[](1);

reservedSplits[0] = JBSplit({
    preferAddToBalance: false,
    percent: 1_000_000_000,     // 100%
    projectId: 0,
    beneficiary: payable(teamMultisig),
    lockedUntil: block.timestamp + 365 days,  // Locked for 1 year
    hook: IJBSplitHook(address(0))
});

splitGroups[1] = JBSplitGroup({
    groupId: 2,                 // Reserved tokens group
    splits: reservedSplits
});
```

## 资金访问限制

设置支付限额和剩余资金分配：

```solidity
JBCurrencyAmount[] memory payoutLimits = new JBCurrencyAmount[](1);
payoutLimits[0] = JBCurrencyAmount({
    amount: 10 ether,
    currency: uint32(uint160(JBConstants.NATIVE_TOKEN))
});

JBCurrencyAmount[] memory surplusAllowances = new JBCurrencyAmount[](1);
surplusAllowances[0] = JBCurrencyAmount({
    amount: 0,                  // No discretionary access
    currency: uint32(uint160(JBConstants.NATIVE_TOKEN))
});

JBFundAccessLimitGroup[] memory fundAccessLimits = new JBFundAccessLimitGroup[](1);
fundAccessLimits[0] = JBFundAccessLimitGroup({
    terminal: address(TERMINAL),
    token: JBConstants.NATIVE_TOKEN,
    payoutLimits: payoutLimits,
    surplusAllowances: surplusAllowances
});
```

## 排队脚本示例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Script} from "forge-std/Script.sol";
import {IJBController} from "@bananapus/core/src/interfaces/IJBController.sol";
// ... other imports

contract QueueRuleset is Script {
    IJBController constant CONTROLLER = IJBController(0x...);
    uint256 constant PROJECT_ID = 1;

    function run() external {
        vm.startBroadcast();

        // Build ruleset config...
        JBRulesetConfig[] memory configs = new JBRulesetConfig[](1);
        configs[0] = /* config */;

        CONTROLLER.queueRulesetsOf(PROJECT_ID, configs, "Update ruleset");

        vm.stopBroadcast();
    }
}
```

## 生成指南

1. **了解当前规则集**——在修改之前检查现有参数。
2. **考虑时机**——当前规则集结束后，新的规则集才会生效。
3. **为需要治理控制的项目使用审批机制**。
4. **配置适当的限额**——支付限额可防止资金突然被提取（rug pull）。
5. **使用 `lockedUntil` 时间戳锁定关键分配比例。

## 示例提示

- “排队一个将预留速率提高到 20% 的规则集。”
- “设置每月最高 5 ETH 的支付周期。”
- “为规则集的更改添加 3 天的审批延迟。”
- “配置分配比例，将 30% 的资金发送到 DAO 储备金。”

## 参考资料

- **nana-core-v5**：https://github.com/Bananapus/nana-core-v5