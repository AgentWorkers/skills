---
name: indigo-staking
description: "查询和管理 Indigo 协议上的 INDY 代币质押情况。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# INDY质押

在Indigo协议上查询和管理INDY代币的质押状态。可以查看质押信息、浏览当前的所有质押位置，并打开、调整或关闭这些质押位置。

## MCP工具

| 工具 | 描述 |
|------|-------------|
| `get_staking_info` | 获取INDY质押的通用信息和参数 |
| `get_staking_positions` | 获取所有活跃的质押位置 |
| `get_staking_positions_by_owner` | 获取特定所有者的质押位置 |
| `get_staking_position_by_address` | 根据地址获取特定的质押位置 |
| `open_staking_position` | 开启一个新的INDY质押位置 |
| `adjust_staking_position` | 调整现有的质押位置 |
| `close_staking_position` | 关闭现有的质押位置 |
| `distribute_staking_rewards` | 分发待发放的质押奖励 |

## 子技能

- [质押查询](sub-skills/staking-query.md) — 查询质押信息和状态 |
- [质押管理](sub-skills/staking-manage.md) — 打开、调整和关闭质押位置 |
- [质押奖励](sub-skills/staking-rewards.md) — 分发质押奖励 |

## 参考资料

- [MCP工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型 |
- [质押概念](references/concepts.md) — INDY的质押机制、奖励和治理规则