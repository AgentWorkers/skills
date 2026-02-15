---
description: >-
  Execute a Uniswap token swap. Use when user wants to swap, trade, buy, or sell
  tokens. Handles quotes, safety checks, simulation, and execution autonomously.
  Supports V2, V3, V4, UniswapX, and cross-chain routing on all supported chains.
allowed-tools: >-
  Read, Glob, Grep,
  Task(subagent_type:trade-executor),
  mcp__uniswap__get_supported_chains,
  mcp__uniswap__search_tokens,
  mcp__uniswap__check_safety_status
model: opus
---

# 执行代币交换

在 Uniswap 上执行代币交换操作，并进行全面的安全性验证。

## 激活方式

当用户输入以下指令时，可以使用此功能：
- “将 X 交换为 Y”
- “用 Y 买入 X”
- “用 Y 卖出 X”
- “交易 X 和 Y”
- “将 X 转换为 Y”
- “交换 X 到 Y”

## 输入参数提取

从用户输入的消息中提取以下参数：

| 参数          | 是否必填 | 默认值       | 来源            |
|---------------|---------|------------|-------------------|
| `tokenIn`       | 是       | —           | 代币名称/符号/地址         |
| `tokenOut`      | 是       | —           | 代币名称/符号/地址         |
| `amount`       | 是       | —           | 数值金额           |
| `chain`        | 否       | `ethereum`     | 链路名称或上下文         |
| `slippage`      | 否       | 0.5%         | 明确指定的滑点百分比     |
| `routing`      | 否       | `auto`        | `via V3`, `use UniswapX` 等       |

## 工作流程

1. **验证输入**：使用 `search_tokens` 函数解析代币符号，并确认所选链路是否被支持。
2. **预先进行安全性检查**：调用 `check_safety_status` 函数，验证以下内容：
   - 当前交易额是否在可接受的范围内
   - 是否未超出交易速率限制
   - 是否未触发交易保护机制（如断路器）

3. **委托给交易执行器**：启动 `Task(subagent_type:trade-executor)`，传递以下参数：
   - `tokenIn`, `tokenOut`, `amount`, `chain`
   - `slippageTolerance`（以 bp 为单位）
   - `routingPreference`（auto/v2/v3/v4/uniswapx）

4. **以清晰的方式向用户报告结果**：

```
Swap Executed Successfully

  Input:  500.00 USDC
  Output: 0.1538 WETH ($499.55)
  Price:  1 WETH = $3,248.04
  Impact: 0.01%
  Gas:    $0.42

  Tx: https://basescan.org/tx/0xABC...

  Safety: All 7 checks passed
```

## 错误处理

| 错误类型        | 用户提示信息 | 建议操作                |
|----------------|-----------------|----------------------|
| `SAFETY_SPENDING_LIMIT_EXCEEDED` | “此次交易将超出您的每日限额。” | 减少交易金额或稍后再试         |
| `SAFETY_TOKEN_NOT_ALLOWED` | “该代币不在您的允许交易列表中。” | 将该代币添加到允许交易列表中         |
| `SAFETY_SIMULATION_FAILED` | “交换模拟失败：[原因]” | 检查相关地址，尝试减少交易金额       |
| `INSUFFICIENT_LIQUIDITY` | “在可接受的滑点范围内，流动性不足。” | 尝试减少交易金额           |

## 对 MCP 服务器的依赖

此功能依赖于 Uniswap MCP 工具来提供链路支持查询、代币搜索、安全性检查以及交易执行功能。
如果单独使用此功能（例如从技能目录中调用），请确保 Agentic Uniswap MCP 服务器正在运行：

- 仓库：[`Agentic-Uniswap` MCP 服务器](https://github.com/wpank/Agentic-Uniswap/tree/main/packages/mcp-server)
- 包：`@agentic-uniswap/mcp-server`