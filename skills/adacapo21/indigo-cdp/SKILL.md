---
name: indigo-cdp
description: "在 Indigo 协议上管理抵押债务头寸（Collateralized Debt Positions，简称 CDPs）。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# Indigo CDP（Collateralized Debt Position）与贷款管理

在 Indigo 协议上管理抵押债务头寸（CDPs）。

## 先决条件

- `@indigoprotocol/indigo-mcp` 服务器正在运行。

## MCP 工具

- `open_cdp` — 创建一个新的 CDP
- `deposit_cdp` — 向 CDP 存入抵押品
- `withdraw_cdp` — 从 CDP 中提取抵押品
- `close_cdp` — 关闭 CDP 并收回抵押品
- `mint_cdp` — 使用 CDP 生成 iAssets
- `burn_cdp` — 烧毁 iAssets 以减少 CDP 的债务
- `analyze_cdp_health` — 检查 CDP 的健康状况和清算风险
- `liquidate_cdp` — 清算不健康的 CDP
- `redeem_cdp` — 用 iAssets 赎回 CDP 中的债务
- `freeze_cdp` — 冻结 CDP
- `merge_cdps` — 将多个 CDP 合并为一个
- `leverage_cdp` — 通过 ROB（Robotic Order Book）开设杠杆 CDP 交易
- `get_all_cdps` — 列出所有 CDP
- `get_cdps_by_owner` — 按所有者列出 CDP
- `get_cdps_by_address` — 按地址列出 CDP

## 子技能

- [CDP 基础](sub-skills/cdp-basics.md) — 创建、存入、提取、关闭 CDP
- [生成与销毁 iAssets](sub-skills/cdp-mint-burn.md) — 生成和销毁 iAssets
- [CDP 健康状况](sub-skills/cdp-health.md) — 分析 CDP 的健康状况和清算风险
- [清算](sub-skills/cdp-liquidation.md) — 清算、赎回、冻结、合并 CDP
- [杠杆操作](sub-skills/cdp-leverage.md) — 通过 ROB 开设杠杆 CDP 交易

## 参考资料

- [MCP 工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型
- [CDP 概念](references/concepts.md) — 抵押比率、清算、iAssets 等相关概念