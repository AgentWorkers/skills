---
name: jb-split-hook
description: 根据自然语言规范生成自定义的 Juicebox V5 分割钩（split hooks）。这些钩子基于 Solidity 编程语言实现，并通过 Foundry 工具进行测试。分割钩能够根据自定义逻辑（例如与 DeFi 系统的集成）来处理单个支付或预留代币的分割操作。
---

# Juicebox V5 分割钩生成器

根据自然语言规范，为 Juicebox V5 项目生成自定义的分割钩（split hooks）。

## 什么是分割钩（Split Hooks）？

分割钩允许在资金通过支付分配（payout splits）或预留代币分配（reserved token splits）时进行自定义处理。它们适用于以下场景：

- **去中心化金融（DeFi）集成**：将支付路由到流动性池、质押协议或收益协议
- **多接收者路由**：将单次分配进一步分配给多个地址
- **代币交换**：在转发之前转换接收到的代币
- **自定义会计处理**：跟踪或转换资金分配情况

**注意**：分割钩可以像其他 Juicebox 项目一样，被添加到 **Revnets** 中用于代币分配。

## V5 分割钩架构

分割钩实现了一个单一函数，该函数以乐观的方式接收资金并对其进行处理。

```solidity
interface IJBSplitHook is IERC165 {
    /// @notice Process a single split with custom logic.
    /// @dev Tokens and native currency are optimistically transferred to the hook.
    /// @param context The context passed by the terminal or controller.
    function processSplitWith(JBSplitHookContext calldata context) external payable;
}
```

## JBSplitHookContext 字段

```solidity
struct JBSplitHookContext {
    address token;          // Token being distributed (address(0) for native)
    uint256 amount;         // Amount sent to this split
    uint256 decimals;       // Token decimals
    uint256 projectId;      // Project distributing funds
    uint256 groupId;        // Split group ID
    JBSplit split;          // The split configuration
}
```

## JBSplit 配置

```solidity
struct JBSplit {
    bool preferAddToBalance;    // Add to project balance instead of paying
    uint256 percent;            // Percent of distribution (out of 1000000000)
    uint256 projectId;          // Project to pay (0 for wallet)
    address payable beneficiary; // Wallet if projectId is 0
    uint256 lockedUntil;        // Timestamp until split is locked
    IJBSplitHook hook;          // This split hook address
}
```

## 设计模式

### 基本分割钩（Basic Split Hook）

```solidity
contract BasicSplitHook is IJBSplitHook, ERC165 {
    function processSplitWith(JBSplitHookContext calldata context) external payable override {
        // Funds have been transferred to this contract
        // Process them according to custom logic

        if (context.token == address(0)) {
            // Handle native currency (ETH)
            uint256 amount = address(this).balance;
            // ... custom logic
        } else {
            // Handle ERC20 token
            uint256 amount = IERC20(context.token).balanceOf(address(this));
            // ... custom logic
        }
    }

    function supportsInterface(bytes4 interfaceId) public view override returns (bool) {
        return interfaceId == type(IJBSplitHook).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

### Uniswap V3 流动性池分割钩（Uniswap V3 LP Split Hook）

将支付路由到 Uniswap V3 流动性池。

```solidity
contract UniswapV3LPSplitHook is IJBSplitHook, ERC165 {
    INonfungiblePositionManager public immutable POSITION_MANAGER;
    uint256 public tokenId; // LP position NFT ID

    function processSplitWith(JBSplitHookContext calldata context) external payable override {
        if (context.token == address(0)) {
            // Wrap ETH to WETH
            WETH.deposit{value: msg.value}();
        }

        // Add liquidity to existing position or create new one
        // ...
    }
}
```

### 多接收者分割钩（Multi-Recipient Split Hook）

将资金进一步分配给多个接收者。

```solidity
contract MultiRecipientSplitHook is IJBSplitHook, ERC165 {
    struct Recipient {
        address payable addr;
        uint256 percent; // Out of 10000
    }

    Recipient[] public recipients;

    function processSplitWith(JBSplitHookContext calldata context) external payable override {
        uint256 total = context.amount;

        for (uint256 i; i < recipients.length; i++) {
            uint256 share = (total * recipients[i].percent) / 10000;

            if (context.token == address(0)) {
                recipients[i].addr.transfer(share);
            } else {
                IERC20(context.token).transfer(recipients[i].addr, share);
            }
        }
    }
}
```

### 代币交换分割钩（Token Swap Split Hook）

在转发之前交换接收到的代币。

```solidity
contract SwapSplitHook is IJBSplitHook, ERC165 {
    ISwapRouter public immutable ROUTER;
    address public immutable OUTPUT_TOKEN;
    address public immutable BENEFICIARY;

    function processSplitWith(JBSplitHookContext calldata context) external payable override {
        // Approve router
        IERC20(context.token).approve(address(ROUTER), context.amount);

        // Swap to output token
        uint256 amountOut = ROUTER.exactInputSingle(
            ISwapRouter.ExactInputSingleParams({
                tokenIn: context.token,
                tokenOut: OUTPUT_TOKEN,
                fee: 3000,
                recipient: BENEFICIARY,
                amountIn: context.amount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            })
        );
    }
}
```

## 配置分割钩

要使用分割钩，请在项目的 `split` 组中对其进行配置：

```solidity
JBSplit memory split = JBSplit({
    preferAddToBalance: false,
    percent: 100_000_000, // 10% (out of 1_000_000_000)
    projectId: 0,
    beneficiary: payable(address(0)),
    lockedUntil: 0,
    hook: IJBSplitHook(address(mySplitHook))
});
```

## 生成指南

1. **理解资金分配流程**：分割钩在支付或预留代币分配时接收资金
2. **支持 ETH 和 ERC20**：通过检查 `context.token` 来确定代币类型
3. **考虑 gas 成本**：复杂的去中心化金融操作可能会产生较高的费用
4. **包含适当的错误处理**：应优雅地处理外部调用失败的情况
5. **为去中心化金融集成生成 Foundry 测试**，并使用 fork 测试进行验证

## 示例提示：

- “创建一个分割钩，将 ETH 存入 Lido 并将 stETH 发送给受益人”
- “我希望将 50% 的支付路由到 Uniswap V3 流动性池”
- “构建一个分割钩，在将资金发送到金库之前将其转换为 USDC”
- “创建一个分割钩，将收到的资金分配给 5 个 DAO 多重签名账户”

## 参考实现

- **uniswapv3-lp-split-hook**：https://github.com/kyzooghost/uniswapv3-lp-split-hook

## 输出格式

生成以下文件：
1. 主合约（位于 `src/` 目录）
2. 如有需要，生成接口文件（位于 `src/interfaces/` 目录）
3. 测试文件（位于 `test/` 目录）
4. 如果需要，生成部署脚本（位于 `script/` 目录）

使用 Foundry 项目结构及 forge-std 工具进行开发。