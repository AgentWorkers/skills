---
name: indigo-dex
description: "通过 Indigo 协议生态系统，可以与 Cardano 上的去中心化交易所进行交互。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# DEX集成

这是一项通过Indigo协议生态系统与Cardano上的去中心化交易所（DEX）进行交互的技能。该技能支持查询可用代币、通过SteelSwap获取交易估算、探索Iris的流动性池信息，以及通过Blockfrost查看钱包余额。

## MCP工具

- `get_steelswap_tokens` — 列出SteelSwap上所有可交易的代币
- `get_steelswap_estimate` — 获取SteelSwap上某对代币的交易估算（价格、滑点、交易路径）
- `get_iris_liquidity_pools` — 从Iris获取流动性池数据
- `get_blockfrost_balances` — 通过Blockfrost获取钱包中的代币余额

## 子技能

- [SteelSwap](sub-skills/steelswap.md) — 代币列表与交易估算
- [Iris Pools](sub-skills/iris-pools.md) — Iris的流动性池数据
- [Balances](sub-skills/balances.md) — 通过Blockfrost查看钱包余额

## 参考资料

- [MCP工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型
- [DEX概念](references/concepts.md) — SteelSwap、Iris、Blockfrost、价格影响、交易路径

## 示例用法

- “SteelSwap上有哪些代币可以交易？”
- “在SteelSwap上将100 ADA兑换成iUSD的交易估算是多少？”
- “显示当前的Iris流动性池信息”
- “这个钱包地址的代币余额是多少？”