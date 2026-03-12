---
name: tronscan-block-info
description: >
  查询 TRON 的最新区块信息，包括区块奖励、区块生成时间、区块生产者、已被烧毁的 TRX 数量以及资源使用情况，以及交易数量。  
  适用于用户询问“最新区块”、“区块高度”、“区块生产者”、“区块奖励”、“已被烧毁的 TRX 数量”或网络负载等情况。  
  **请勿用于实时交易处理或网络监控**（请使用 tronscan-realtime-network 工具）；如需按哈希值查询交易信息，请使用 tronscan-transaction-info 工具。
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: tronscan
---
# 块信息

## 概述

| 工具 | 功能 | 使用场景 |
|------|----------|----------|
| getLatestBlock | 获取最新块的信息 | 包括块编号、哈希值、大小、时间戳、见证者及交易数量 |
| getBlocks | 获取块列表 | 支持分页、排序，并可根据生产者或时间范围进行过滤 |
| getBlockStatistic | 获取块统计信息 | 包括24小时内的支付总额、块总数及被销毁的TRX数量 |

## 使用场景

1. **获取最新块信息**：使用 `getLatestBlock` 可获取当前块的编号、哈希值、大小、时间戳、见证者及交易数量。
2. **获取块奖励信息**：奖励信息可从块数据或链参数中获取；块列表可提供更详细的块级数据。
3. **查询块的时间戳及生产者**：可以使用 `getLatestBlock` 或 `getBlocks` 来获取时间戳和见证者（生产者）。
4. **查询被销毁的TRX数量**：使用 `getBlockStatistic` 可获取24小时内的被销毁TRX总数；每个块的销毁情况可能记录在块数据中。
5. **分析资源消耗**：块的大小和交易数量反映了资源使用情况；可使用 `getBlockStatistic` 进行汇总分析。
6. **统计交易数量**：使用 `getLatestBlock` 可获取最新块的交易数量；使用 `getBlocks` 可获取多个块的交易数量。
7. **实时监控网络负载**：结合使用 `getLatestBlock`、`getBlocks` 和 `getBlockStatistic` 可实时监控网络负载。

## MCP服务器

- **前提条件**：[TronScan MCP指南](https://mcpdoc.tronscan.org)

## 工具说明

### getLatestBlock

- **API**：`getLatestBlock` — 获取最新的确认块信息（包括编号、哈希值、大小、时间戳、见证者及交易数量）
- **使用场景**：当用户需要获取“最新块”、“当前块”或“块高度”时使用。
- **返回值**：块编号、哈希值、大小、时间戳、见证者、交易数量等。

### getBlocks

- **API**：`getBlocks` — 获取块列表，支持分页、排序，并可根据生产者或时间范围进行过滤
- **使用场景**：当用户需要获取“最近发布的块”、“按生产者分类的块”或“特定时间范围内的块”时使用。
- **输入参数**：`limit`（限制结果数量）、`sort`（排序方式，例如 `-number`）、可选的生产者地址、开始/结束时间。

### getBlockStatistic

- **API**：`getBlockStatistic` — 获取块统计信息（包括24小时内的支付总额、块总数及被销毁的TRX数量）
- **使用场景**：当用户需要获取“块统计信息”或“24小时内的块数据”时使用。
- **返回值**：24小时内的支付总额、块总数、被销毁的TRX数量及相关统计数据。

## 故障排除

关于MCP连接或速率限制问题，请参阅[README](../README.md#troubleshooting)。

## 注意事项

- 如需获取“块奖励”信息，需将块数据与 `getChainParameters`（Witness类别）的结果结合使用。
- 实时监控网络负载时，建议定期调用 `getLatestBlock` 和/或 `getBlockStatistic` 来获取网络负载和TRX销毁情况。