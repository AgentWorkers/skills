---
name: cardano-identity
description: "解决并列出已连接的 Cardano 钱包的 ADAHandles。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
  openclaw:
    emoji: "🪪"
    requires:
      env: [SEED_PHRASE]
    install:
      - kind: node
        package: "@indigoprotocol/cardano-mcp"
---
# Cardano 身份验证 — ADAHandles

用于解析并列出已连接的 Cardano 钱包所拥有的 ADAHandles（ADA 交易处理标识符）。

## 先决条件

- `@indigoprotocol/cardano-mcp` 服务器正在运行。

## MCP 工具

- `get_adahandles` — 获取已连接钱包拥有的所有 ADAHandles。

## 使用场景

当用户询问以下内容时，请使用此功能：

- 他们的 ADAHandle 或 `$handle`；
- 人类可读的钱包标识符；
- 通过 ADAHandle 查找对应的钱包地址。

## 数据解释

- ADAHandles 是基于特定策略 ID 的 Cardano 原生代币；
- 每个 ADAHandle 对应一个钱包地址（例如，`$alice` 对应 `addr1...`）；
- 返回的 ADAHandles 为纯字符串形式，不包含 `$` 前缀。