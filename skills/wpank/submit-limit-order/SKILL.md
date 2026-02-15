---
description: >-
  Submit a UniswapX Dutch auction limit order. Use when user wants to set a
  limit price, get MEV-protected execution, or submit an order that fills at
  the best available price. No gas cost until filled.
allowed-tools: >-
  Read, Glob, Grep,
  Task(subagent_type:trade-executor),
  mcp__uniswap__get_quote,
  mcp__uniswap__submit_uniswapx_order,
  mcp__uniswap__get_uniswapx_order_status,
  mcp__uniswap__check_safety_status
model: opus
---

# 提交限价单

提交一个无gas费用的UniswapX荷兰式拍卖限价单。

## 使用场景

当用户说出以下任何指令时，可以使用此功能：
- “设置限价单”
- “以价格Y购买X”
- “提交UniswapX订单”
- “限价买入/卖出”

## 输入参数提取

| 参数        | 是否必填 | 默认值 | 来源            |
|------------|---------|---------|-------------------|
| `tokenIn`     | 是       | —                | 要交易的代币名称/符号       |
| `tokenOut`     | 是       | —                | 目标代币名称/符号       |
| `amount`     | 是       | —                | 交易数量（数值）       |
| `chain`      | 否       | `ethereum`       | 目标区块链名称       |
| `limitPrice`   | 否       | 当前市场价格       | 限价单价格         |
| `expiry`     | 否       | 5分钟             | 限价单的有效期限       |

## 工作流程

1. **验证输入**：检查目标区块链上是否支持UniswapX交易，以及用户是否有足够的交易权限。
2. **获取当前市场价格**：调用`get_quote`函数获取参考价格。
3. **提交订单**：调用`submit_uniswapx_order`函数，传入以下参数：
   - `tokenIn`, `tokenOut`, `amount`, `chain`
   - `orderType`: “dutch”（默认）或“priority”
4. **监控订单状态**：定期调用`get_uniswapx_order_status`函数，直到订单成交、过期或被取消。

## 代码示例（请参考下方代码块）

```
Limit Order Submitted (UniswapX Dutch Auction)

  Input:   1,000 USDC
  Target:  0.310 WETH (limit: 1 WETH = $3,225)
  Decay:   $3,225 → $3,200 over 5 minutes
  Status:  PENDING
  Order:   0xORDER_HASH...

  Gas: $0.00 (gasless until filled)
  Monitoring: Will report when filled or expired.
```

## 错误处理

| 错误类型         | 用户提示信息 | 建议操作                |
|-----------------|-----------------|----------------------|
| `UNISWAPX_NOT_SUPPORTED` | “[chain]上不支持UniswapX交易。” | 更换支持该交易的区块链或使用其他交易方式 |
| `ORDER_EXPIRED`     | “订单已过期但未成交。” | 调整限价单价格或延长订单有效期 |
| `SAFETY_TOKEN_NOT_ALLOWED` | “该代币不在允许交易的列表中。” | 将该代币添加到交易配置中       |