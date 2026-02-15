---
name: jb-cash-out-hook
description: 根据自然语言规范生成自定义的 Juicebox V5 现金提取（cash out）功能。这些自定义功能会通过 Solidity 合同实现 `IJBCashOutHook` 和/或 `IJBRulesetDataHook` 接口，并配合 Foundry 测试工具进行验证。在生成自定义解决方案之前，系统会先评估现有的现成解决方案（如 721 Hook、Revnet）是否适用于当前的业务场景。
---

# Juicebox V5 提现钩子生成器

根据自然语言规范，为 Juicebox V5 项目生成自定义的提现钩子。

## 在编写自定义代码之前

**始终评估是否有现成的解决方案能满足用户需求：**

| 用户需求 | 推荐解决方案 |
|-----------|---------------------|
| 烧毁 NFT 以回收资金 | 直接部署 **nana-721-hook-v5** |
| 提现时提取费用 | 部署 **revnet**（提取 2.5% 的费用） |
| 具有提现规则的自主财库 | 使用 **revnet-core-v5** |

如果现有解决方案能够满足需求，请指导用户直接使用这些解决方案，而不是编写自定义代码。

## Juicebox V5 提现钩子的架构

V5 的提现钩子遵循两阶段模式：

### 第一阶段：数据钩子（beforeCashOutRecordedWith）
- 在记录提现信息之前接收相关数据
- 返回税率、数量、供应量以及钩子的相关配置
- 可以修改实际的提现计算方式
- 实现 `IJBRulesetDataHook` 接口

### 第二阶段：提现钩子（afterCashOutRecordedWith）
- 在提现记录完成后执行
- 接收转发的资金和相关上下文信息
- 实现 `IJBCashOutHook` 接口

## JBAfterCashOutRecordedContext 字段

```solidity
struct JBAfterCashOutRecordedContext {
    address holder;                 // Token holder cashing out
    uint256 projectId;              // Project ID
    uint256 rulesetId;              // Current ruleset ID
    uint256 cashOutCount;           // Tokens being cashed out
    JBTokenAmount reclaimedAmount;  // Amount reclaimed by holder
    JBTokenAmount forwardedAmount;  // Amount forwarded to hook
    uint256 cashOutTaxRate;         // Tax rate (0-10000)
    address payable beneficiary;    // Receives reclaimed funds
    bytes hookMetadata;             // Data from data hook
    bytes cashOutMetadata;          // Data from cash out initiator
}
```

## 设计模式

### 简单的提现钩子（仅使用 afterCashOutRecordedWith）
当您只需要在提现后执行逻辑而不需要修改计算结果时使用此模式。

```solidity
contract SimpleCashOutHook is IJBCashOutHook, ERC165 {
    function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context) external payable {
        // Validate caller is a project terminal
        // Execute custom logic with forwarded funds
    }

    function supportsInterface(bytes4 interfaceId) public view override returns (bool) {
        return interfaceId == type(IJBCashOutHook).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

### 数据钩子 + 提现钩子（完全控制）
当您需要修改税率、供应量计算或拦截资金时使用此模式。

```solidity
contract FullCashOutHook is IJBRulesetDataHook, IJBCashOutHook, ERC165 {
    function beforeCashOutRecordedWith(JBBeforeCashOutRecordedContext calldata context)
        external view returns (
            uint256 cashOutTaxRate,
            uint256 cashOutCount,
            uint256 totalSupply,
            JBCashOutHookSpecification[] memory hookSpecifications
        )
    {
        // Calculate custom tax rate or modify supply
        // Specify hooks and forwarded amounts
    }

    function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context) external payable {
        // Execute with forwarded funds
        // Handle fee extraction, burning, etc.
    }

    function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
        external view returns (uint256 weight, JBPayHookSpecification[] memory hookSpecifications)
    {
        // Pass through if not handling payments
        return (context.weight, new JBPayHookSpecification[](0));
    }

    function hasMintPermissionFor(uint256) external pure returns (bool) {
        return false;
    }
}
```

### 费用提取模式（来自 revnet-core-v5）
将部分提现金额路由到费用受益者。

```solidity
function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context) external payable {
    // Forward fee to beneficiary
    uint256 feeAmount = context.forwardedAmount.value;
    if (feeAmount > 0) {
        // Process fee payment
    }
}
```

### NFT 烧毁模式（来自 nana-721-hook-v5）
在提现时销毁 NFT 以回收相应的资金。

```solidity
function afterCashOutRecordedWith(JBAfterCashOutRecordedContext calldata context) external payable {
    // Decode token IDs from metadata
    uint256[] memory tokenIds = abi.decode(context.cashOutMetadata, (uint256[]));

    // Verify ownership and burn
    for (uint256 i; i < tokenIds.length; i++) {
        _burn(tokenIds[i]);
    }
}
```

## 生成指南

1. **就所需的提现行为提出明确的问题**
2. **首先评估现有的解决方案**
3. **选择最简单且符合需求的模式**
4. **在 afterCashOutRecordedWith 阶段加入终端验证**
5. **使用 Foundry 进行测试**
6. **使用正确的 V5 术语（如“提现”，而非“赎回”）**

## 示例提示

- “创建一个在提现时销毁 NFT 以释放全部回收价值的钩子”
- “我希望从所有提现中提取 5% 的费用并放入财库地址”
- “构建一个仅在满足持有期限后允许提现的钩子”
- “创建一个需要持有特定 NFT 才能提现的钩子”

## 参考实现

- **nana-721-hook-v5**: https://github.com/Bananapus/nana-721-hook-v5 （在提现时销毁 NFT）
- **revnet-core-v5**: https://github.com/rev-net/revnet-core-v5 （提取费用）

## 输出格式

生成以下文件：
1. 主合约（位于 `src/` 目录）
2. 如有需要，生成接口文件（位于 `src/interfaces/` 目录）
3. 测试文件（位于 `test/` 目录）
4. 如有请求，生成部署脚本（位于 `script/` 目录）

请使用基于 forge-std 的 Foundry 项目结构进行开发。