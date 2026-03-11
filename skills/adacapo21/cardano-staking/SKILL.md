---
name: cardano-staking
description: "检查已连接的钱包中的权益委托情况以及可获得的 ADA 奖励。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "🥩"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---
# Cardano 质押

检查已连接钱包的质押委托情况以及可获得的 ADA 奖励。

## 先决条件

- `@indigoprotocol/cardano-mcp` 服务器正在运行中。

## MCP 工具

- `get_stake_delegation` — 获取质押池 ID 和可获得的 ADA 奖励。

## 使用场景

当用户询问以下内容时，请使用此功能：

- 质押状态或委托情况
- 自己被委托到了哪个质押池
- 可获得的质押奖励
- 可以领取的 ADA 奖励

## 数据解释

- `poolId` 是质押池的 Bech32 标识符（例如：`pool1...`）。
- `availableAdaRewards` 表示的是以 ADA 形式存在的奖励（而非 Lovelace 形式的奖励）。