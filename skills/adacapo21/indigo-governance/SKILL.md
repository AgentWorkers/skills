---
name: indigo-governance
description: "查询 Indigo 协议的治理数据，包括协议参数、轮询信息等。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# 治理与参数

查询 Indigo 协议的治理数据，包括协议参数、温度检查结果以及投票信息。

## MCP 工具

| 工具 | 描述 |
|------|-------------|
| `get_protocol_params` | 获取当前的 Indigo 协议参数 |
| `get_temperature_checks` | 获取正在进行的治理温度检查结果 |
| `get_polls` | 获取治理相关的投票数据 |

## 子技能

- [协议参数](sub-skills/protocol-params.md) — 查询协议参数 |
- [投票](sub-skills/polls.md) — 温度检查结果及治理投票信息 |

## 参考资料

- [MCP 工具参考](references/mcp-tools.md) — 工具的详细参数及返回类型 |
- [治理概念](references/concepts.md) — 投票流程、协议参数等