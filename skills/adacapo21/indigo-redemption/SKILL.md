---
name: indigo-redemption
description: "在 Indigo 协议中，管理赎回操作以及赎回订单簿（Redemption Order Book, ROB）中的持仓情况。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# Indigo Redemption & ROB

这是一项用于管理Indigo协议中赎回操作以及Redemption Order Book（ROB）中头寸的技能。

## 先决条件

- Node.js 20+版本
- `@indigoprotocol/indigo-mcp`服务器正在运行

## MCP服务器

```bash
npx @indigoprotocol/indigo-mcp
```

## 工具

| 工具 | 描述 |
|------|-------------|
| `get_order_book` | 从订单簿中获取未成交的ROB头寸，可按资产或所有者进行筛选 |
| `get_redemption_orders` | 获取赎回订单，可按时间戳或价格范围进行筛选 |
| `get_redemption_queue` | 获取特定iAsset的汇总赎回队列，按最高价格升序排序 |
| `open_rob` | 使用ADA开设新的ROB头寸，并设置最高价格限制 |
| `cancel_rob` | 取消现有的ROB头寸 |
| `adjust_rob` | 调整ROB头寸中的ADA数量；可选地更新最高价格 |
| `claim_rob` | 从ROB头寸中领取收到的iAssets |
| `redeem_rob` | 使用一个或多个ROB头寸来赎回iAssets |

## 子技能

- [订单簿](sub-skills/order-book.md) — 查询ROB订单簿和赎回订单 |
- [赎回队列](sub-skills/redemption-queue.md) — 按iAsset分类的汇总赎回队列 |
- [ROB管理](sub-skills/rob-manage.md) — 开设、取消、调整、领取和赎回ROB头寸 |

## 参考资料

- [MCP工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型 |
- [赎回概念](references/concepts.md) — ROB的运作机制、订单簿和赎回队列