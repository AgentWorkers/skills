---
description: >-
  Execute multiple token swaps in sequence. Use when user wants to rebalance,
  swap into multiple tokens, or execute a multi-step trading plan. Each swap
  goes through full safety validation independently.
allowed-tools: >-
  Read, Glob, Grep,
  Task(subagent_type:trade-executor),
  mcp__uniswap__check_safety_status,
  mcp__uniswap__get_agent_balance
model: opus
---

# 批量交换

依次执行多个代币交换操作，每次交换都进行独立的安全性验证。

## 激活方式

当用户输入以下指令时，使用此功能：
- “将 X 交换为 Y 和 Z”
- “将资产重新平衡为 50% ETH 和 50% USDC”
- “购买 3 种不同的代币”
- “执行以下交换操作：...”

## 输入参数提取

| 参数          | 是否必填 | 默认值    | 来源            |
|---------------|---------|---------|-------------------|
| `swaps`       | 是       | —         | {tokenIn, tokenOut, amount} 的列表 |
| `chain`       | 否       | ethereum   | 所有交换操作的默认链 |
| `stopOnFailure` | 否       | true       | 是否在首次失败时停止所有操作 |

## 工作流程

1. **解析用户输入的交换指令**，确保所有代币符号都能被正确识别。
2. **预检查**：使用 `check_safety_status` 和 `get_agent_balance` 函数验证总花费是否在每日限额范围内，以及所有交换操作所需的余额是否充足。
3. **依次执行交换操作**：
   - 对于每个交换操作，启动 `Task(subagent_type:trade-executor)` 并传递相应的参数。
   - 在开始下一个交换操作之前，等待前一个操作的确认结果。
   - 更新每次交换后的剩余余额。
   - 如果 `stopOnFailure` 为 `true` 且某个交换操作失败，则停止剩余的所有操作。

4. **生成操作总结报告**：

```
Batch Swap Complete (3/3 succeeded)

  #  Swap              Amount In    Amount Out   Tx
  1  USDC → WETH      1,000 USDC   0.307 WETH   0xABC...
  2  USDC → WBTC      1,000 USDC   0.015 WBTC   0xDEF...
  3  USDC → UNI       1,000 USDC   142.3 UNI    0xGHI...

  Total gas: $1.26
```

## 错误处理

| 错误类型         | 用户提示信息 | 建议操作                |
|-----------------|-----------------|----------------------|
| `BATCH_PARTIAL_FAILURE` | “交换操作 #N 失败。剩余操作将停止。” | 查看失败的交换操作并重新运行剩余的操作 |
| `INSUFFICIENT_BALANCE` | “余额不足，无法完成全部操作。” | 减少每次交换的金额 |
| `SAFETY_AGGREGATE_LIMIT` | “总交换金额超过每日限额。” | 减少交换操作的总量 |