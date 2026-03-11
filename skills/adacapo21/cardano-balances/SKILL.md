---
name: cardano-balances
description: "在Cardano区块链上查询钱包余额、地址以及未花费的交易输出（UTxOs）。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "💰"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---
# Cardano 钱包余额

用于查询 Cardano 区块链上的钱包余额、地址和未花费的交易输出（UTxOs）。

## 先决条件

- 必须运行 `@indigoprotocol/cardano-mcp` 服务器。

## MCP 工具

- `get_balances` — 获取连接钱包的所有余额和原生资产。
- `get_addresses` — 获取连接钱包的所有 Cardano 地址。
- `get_utxos` — 获取连接钱包的所有未花费的交易输出（UTxOs）。

## 使用场景

当用户询问以下内容时，可以使用此功能：

- 钱包余额或 ADA 数量
- 钱包中的原生代币或资产
- 钱包地址
- 未花费的交易输出（UTxOs）的详细信息

## 数据解释

- 平余额以 **lovelace** 为单位返回（1 ADA = 1,000,000 lovelace）。显示时请务必将其转换为 ADA。
- 原生资产通过 `policyId` 和 `nameHex` 进行标识。
- 如果存在，`name` 字段会提供可读的标签。