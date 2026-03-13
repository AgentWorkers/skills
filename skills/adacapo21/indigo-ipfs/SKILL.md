---
name: indigo-ipfs
description: "在 IPFS 上存储和检索数据，并查询 Indigo 协议的收集器（collector）未花费的交易输出（UTXOs）。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# Indigo IPFS & Collector

用于在 IPFS 上存储和检索数据，以及查询 Cardano 平台上 Indigo 协议的收集器 UTXO（未花费的交易输出）。

## MCP 工具

### store_on_ipfs

将文本内容存储到 IPFS 上。

**参数：**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|----------|-------------|
| `text` | 字符串 | 是 | 要存储到 IPFS 上的文本内容 |

**返回值：** 存储内容的 IPFS 内容标识符（CID）。

---

### retrieve_from_ipfs

通过 CID 从 IPFS 中检索内容。

**参数：**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|----------|-------------|
| `cid` | 字符串 | 是 | IPFS 内容标识符（CID） |

**返回值：** 位于指定 CID 处的文本内容。

---

### get_collector_utxos

获取用于费用分配的收集器 UTXO。

**参数：**

| 名称 | 类型 | 是否必需 | 描述 |
|------|------|----------|-------------|
| `length` | 数字 | 否 | 需要返回的 UTXO 最大数量 |

**返回值：** 一个包含收集器 UTXO 及其对应价值的列表。

## 子技能

- [IPFS 存储](sub-skills/ipfs-storage.md) — 在 IPFS 上存储和检索数据
- [收集器](sub-skills/collector.md) — 查询用于费用分配的收集器 UTXO

## 参考资料

- [MCP 工具参考](references/mcp-tools.md) — 工具参数和返回值的详细信息
- [概念](references/concepts.md) — IPFS 内容寻址和收集器费用分配机制