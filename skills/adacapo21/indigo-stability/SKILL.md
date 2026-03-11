---
name: indigo-stability
description: "在 Indigo 协议中管理稳定性池（Stability Pool）的职位（Positions）。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# Indigo稳定性池（Stability Pools）

用于管理Indigo协议中的稳定性池（Stability Pools）相关操作。

## 先决条件

- `@indigoprotocol/indigo-mcp` 服务器正在运行。

## MCP工具（MCP Tools）

- `get_stability_pools` — 列出所有稳定性池
- `get_stability_pool_accounts` — 列出某个稳定性池中的账户
- `get_sp_account_by_owner` — 根据所有者获取稳定性池账户信息
- `create_sp_account` — 创建新的稳定性池账户
- `adjust_sp_account` — 调整稳定性池账户的存款金额
- `close_sp_account` — 关闭稳定性池账户
- `process_sp_request` — 处理待处理的稳定性池请求
- `annul_sp_request` — 取消待处理的稳定性池请求

## 子技能（Sub-skills）

- [池查询](sub-skills/sp-query.md) — 查询池的状态、账户信息及所有者信息
- [池管理](sub-skills/sp-manage.md) — 创建、调整或关闭账户
- [请求处理](sub-skills/sp-requests.md) — 处理和取消稳定性池请求

## 参考资料（References）

- [MCP工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型
- [稳定性池概念](references/concepts.md) — 稳定性池的运作机制、奖励规则及请求生命周期