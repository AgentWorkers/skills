---
name: cardano-transactions
description: "在用户明确确认后，签署并提交 Cardano 交易。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "📤"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---
# Cardano交易

需要用户明确确认后，才能签名并提交Cardano交易。

## 先决条件

- `@indigoprotocol/cardano-mcp` 服务器正在运行。

## MCP工具

- `submit_transaction` — 用于签名并提交Cardano交易（以CBOR格式）。

## 使用场景

当用户请求以下操作时，请使用此功能：
- 提交或发送Cardano交易
- 使用用户的钱包对交易进行签名
- 广播预先构建好的交易

## 安全模型

**此工具具有风险。** 在调用 `submit_transaction` 之前，请执行以下步骤：
1. 用通俗易懂的语言向用户说明交易的详细内容。
2. 明确请求用户的确认。
3. 仅当用户表示同意后，才继续执行操作。
**切勿自动提交交易。**

## 数据解析：
- 输入数据为未签名的交易CBOR格式（十六进制字符串）。
- 成功提交后，输出将包含 `transactionHash` 和 `timestamp`。
- 交易将由用户连接的钱包的密钥进行签名。