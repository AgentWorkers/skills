---
name: build-hook
description: >-
  Build a Uniswap V4 hook. Use when user wants to create a custom V4 hook
  contract. Generates Solidity code, Foundry tests, mines CREATE2 address
  for hook flags, and produces deployment scripts. Handles the full hook
  development lifecycle.
allowed-tools: >-
  Read, Write, Edit, Glob, Grep,
  Bash(forge:*), Bash(npm:*), Bash(git:*),
  Task(subagent_type:hook-builder),
  mcp__uniswap__get_supported_chains
model: opus
---

# 构建挂钩（Build Hook）

## 概述

该功能通过调用 `hook-builder` 代理来构建一个完整的 Uniswap V4 挂钩。它涵盖了整个开发生命周期，包括理解用户需求、确定挂钩类型、生成 Solidity 合同、编写测试用例、生成用于部署的 CREATE2 地址以及生成部署脚本。最终生成的代码可以直接应用于项目中。

## 使用场景

当用户提出以下请求时，可激活此功能：
- “构建 V4 挂钩”
- “创建限价单挂钩”
- “创建动态费用挂钩”
- “创建 TWAMM 挂钩”
- “自定义 V4 挂钩”
- “在价格波动期间收取更高费用的挂钩”
- “将 LP 费用分配给质押者的挂钩”
- “集成预言机的挂钩”

## 参数

| 参数 | 是否必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| behavior | 是 | -- | 挂钩的具体类型（例如：限价单、动态费用、TWAMM、基于预言机的定价） |
| callbacks | 否 | 自动检测 | 如果用户指定了特定的 V4 回调函数（例如：`beforeSwap`、`afterSwap`），则需要提供这些回调函数 |
| constraints | 否 | -- | 气体预算、安全要求或特定的设计约束 |
| chain | 否 | `ethereum` | 部署的目标链（影响 PoolManager 地址的选择） |

## 工作流程

1. **从用户请求中提取参数**：确定挂钩的类型、所需的回调函数以及任何特定的约束条件。
2. **委托给 `hook-builder` 代理**：调用 `Task(subagent_type:hook-builder)` 并传递所有相关信息。`hook-builder` 代理将：
   - 理解用户需求并确定需要哪些回调函数
   - 将回调函数与挂钩参数关联并验证参数组合是否有效
   - 生成基于 `BaseHook` 的 Solidity 合同，并确保其符合规范（使用 `NatSpec`）
   - 编写全面的测试用例（单元测试、集成测试、边界测试等）
   - 生成一个 CREATE2 地址，该地址包含正确的参数组合
   - 生成包含部署步骤的脚本

3. **向用户展示结果**：提供以下内容的总结：
   - 生成的文件路径（合同文件、测试文件、部署脚本文件）
   - 挂钩的实现原理及状态流转方式
   - 实现的回调函数及其对应的参数组合
   - 每个回调函数所需的气体消耗量（来自测试结果）
   - 开发者的下一步操作（运行测试、部署到测试网或主网）

## 输出格式

以总结的形式展示所有生成的文件：

```text
V4 Hook Built: LimitOrderHook

  Contract:   src/hooks/LimitOrderHook.sol (187 lines)
  Tests:      test/hooks/LimitOrderHook.t.sol (12 tests)
  Deployment: script/DeployLimitOrderHook.s.sol

  Callbacks: beforeSwap, afterSwap
  Flags:     0x00C0
  CREATE2:   Salt mined, address verified

  Gas Estimates:
    beforeSwap: ~45,000 gas
    afterSwap:  ~32,000 gas
    Total overhead per swap: ~77,000 gas

  Architecture:
    Orders are placed at specific ticks and stored in an on-chain order book.
    During beforeSwap, the hook checks for matching orders at the target tick.
    Matched orders are filled atomically within the same transaction.

  Next Steps:
    1. Run tests: forge test --match-contract LimitOrderHookTest
    2. Deploy to testnet: forge script script/DeployLimitOrderHook.s.sol --rpc-url sepolia
    3. Verify on Etherscan: forge verify-contract <address> LimitOrderHook
```

## 重要说明

- 该功能完全依赖于 `hook-builder` 代理来完成任务，不会直接调用 MCP 工具。
- `hook-builder` 生成的 Solidity 代码具有重入保护机制和访问控制功能。
- 通过生成正确的 CREATE2 地址，确保部署后的挂钩能够正确地传递参数到 PoolManager。
- 需要安装 Foundry 工具才能生成和编译测试用例；如果未安装，系统会提供安装指南。
- 生成的代码基于 Solidity 0.8.26 版本，并引用了 `@uniswap/v4-core` 和 `@uniswap/v4-periphery` 库。

## 错误处理

| 错误类型 | 向用户显示的提示信息 | 建议的操作 |
| --- | --- | --- |
| `INVALID_CALLBACK_COMBINATION` | “请求的挂钩类型需要相互冲突的回调函数。” | 请简化挂钩功能或将其拆分为多个挂钩 |
| `CREATE2_MINING_TIMEOUT` | “未能在指定时间内生成有效的 CREATE2 地址。” | 增加生成时间或减少所需的参数数量 |
| `FORGE_NOT_INSTALLED` | “需要安装 Foundry 工具。” | 安装方法：`curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| `VAGUE_REQUIREMENTS` | “关于所需挂钩功能的描述不够详细。” | 请提供更具体的需求（例如：“在价格波动时执行限价单”） |
| `COMPILATION_ERROR` | “生成的合同存在编译错误。” | 请检查错误信息并调整需求。