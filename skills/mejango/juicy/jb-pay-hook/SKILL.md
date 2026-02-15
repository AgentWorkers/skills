---
name: jb-pay-hook
description: 根据自然语言规范生成自定义的 Juicebox V5 支付钩子（pay hooks）。使用 Foundry 工具创建实现 `IJBPayHook` 和/或 `IJBRulesetDataHook` 接口的 Solidity 合同，并进行相应的测试。首先会评估现有的现成解决方案（如回购钩子、721 钩子、Revnet）是否适用于当前的业务场景。
---

# Juicebox V5 支付钩生成器

根据自然语言规范，为 Juicebox V5 项目生成自定义的支付钩（pay hooks）。

## 在编写自定义代码之前

**始终评估是否有现成的解决方案能满足用户需求：**

| 用户需求 | 推荐解决方案 |
|-----------|---------------------|
| 通过 Uniswap 进行代币回购 | 直接部署 **nana-buyback-hook-v5** |
| 根据支付金额提供分层 NFT 奖励 | 直接部署 **nana-721-hook-v5** |
| 自主化的代币化资金管理 | 部署 **revnet-core-v5** |
| 带有 NFT 分层的 Revnet | 使用 **Tiered721RevnetDeployer** |
| 带有自定义支付钩的 Revnet | 使用 **PayHookRevnetDeployer** |

如果现有解决方案能够满足需求，请指导用户直接使用这些解决方案，而非编写自定义代码。

## Juicebox V5 的支付钩架构

V5 的支付钩遵循两阶段模式：

### 第一阶段：数据钩（beforePayRecordedWith）
- 在记录支付信息之前接收支付数据
- 返回调整后的权重和钩子配置
- 实现 `IJBRulesetDataHook` 接口

### 第二阶段：支付钩（afterPayRecordedWith）
- 在支付信息被记录后执行
- 接收转发的资金和相关上下文数据
- 实现 `IJBPayHook` 接口

一个合约可以同时实现这两个接口（例如回购钩），也可以仅实现支付钩。

## JBAfterPayRecordedContext 字段

```solidity
struct JBAfterPayRecordedContext {
    address payer;                  // Payment originator
    uint256 projectId;              // Project being paid
    uint256 rulesetId;              // Current ruleset ID
    JBTokenAmount amount;           // Payment amount
    JBTokenAmount forwardedAmount;  // Amount forwarded to hook
    uint256 weight;                 // Token minting weight
    uint256 newlyIssuedTokenCount;  // Tokens minted
    address beneficiary;            // Token recipient
    bytes hookMetadata;             // Data from data hook
    bytes payerMetadata;            // Data from payer
}
```

## 设计模式

### 简单支付钩（仅使用 afterPayRecordedWith）
当您只需要在支付后执行逻辑而不需要修改代币铸造行为时使用。

```solidity
contract SimplePayHook is IJBPayHook, ERC165 {
    function afterPayRecordedWith(JBAfterPayRecordedContext calldata context) external payable {
        // Validate caller is a project terminal
        // Execute custom logic
    }

    function supportsInterface(bytes4 interfaceId) public view override returns (bool) {
        return interfaceId == type(IJBPayHook).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

### 数据钩 + 支付钩（完全控制）
当您需要修改权重、拦截资金或控制钩子的路由时使用。

```solidity
contract FullPayHook is IJBRulesetDataHook, IJBPayHook, ERC165 {
    function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
        external view returns (uint256 weight, JBPayHookSpecification[] memory hookSpecifications)
    {
        // Analyze payment, determine routing
        // Return weight and hook specs
    }

    function afterPayRecordedWith(JBAfterPayRecordedContext calldata context) external payable {
        // Execute with forwarded funds
    }

    function beforeCashOutRecordedWith(JBBeforeCashOutRecordedContext calldata context)
        external view returns (uint256, uint256, uint256, JBCashOutHookSpecification[] memory)
    {
        // Pass through if not handling cash outs
        return (context.ruleset.cashOutTaxRate, context.cashOutCount, context.totalSupply, new JBCashOutHookSpecification[](0));
    }

    function hasMintPermissionFor(uint256) external pure returns (bool) {
        return false; // Only true if hook needs to mint
    }
}
```

### “合约即所有者”模式
当项目需要具备自主性、结构化的规则和委托权限时使用。

参考实现：**revnet-core-v5**（REVDeployer）
- 合约拥有 Juicebox 项目的 NFT
- 实现钩子功能并控制项目配置
- 通过 JBPermissions 授权机制进行权限委托

## 生成指南

1. **询问关于所需行为的详细信息**
2. **首先评估是否有现成的解决方案**
3. **选择最简单且符合需求的方案**
4. **在 afterPayRecordedWith 中加入终端验证逻辑**
5. **使用 Foundry 工具生成测试用例，并针对已部署的合约进行测试**
6. **使用正确的 V5 术语（如 ruleset、cash out、weight、reserved rate）**

## 示例提示

- “创建一个根据支付金额生成自定义 ERC20 代币的支付钩”
- “我想根据支付金额向付款者提供积分奖励”
- “构建一个将 10% 的支付金额转发到慈善机构的支付钩”
- “创建一个能够限制单笔支付金额的自主项目”

## 参考实现

- **nana-buyback-hook-v5**: https://github.com/Bananapus/nana-buyback-hook-v5
- **nana-721-hook-v5**: https://github.com/Bananapus/nana-721-hook-v5
- **revnet-core-v5**: https://github.com/rev-net/revnet-core-v5

## 输出格式

生成以下文件：
1. 主合约文件（位于 `src/` 目录）
2. 如有需要，生成接口文件（位于 `src/interfaces/` 目录）
3. 测试文件（位于 `test/` 目录）
4. 如果需要，生成部署脚本（位于 `script/` 目录）

请使用 Foundry 项目结构及 forge-std 工具进行开发。