---
name: planetexpress-marketplace
description: 基于Monad区块链的去中心化文件市场——您可以在这里购买、出售和浏览经过加密的文件（文件采用x402格式）。
homepage: https://planetexpress.dropclaw.cloud
user-invocable: true
---
# Planet Express Marketplace — 去中心化的文件交易平台

这是一个基于Monad区块链的去中心化文件交易平台，支持加密文件的买卖。所有交易均通过x402协议进行托管，并支持多链支付。

## 快速参考

- **API基础地址**：`https://dropclaw.cloud/marketplace`
- **协议**：x402（HTTP 402支付流程）
- **区块链**：Monad（chainId：143）
- **智能合约**：`0xeFc5D4f6ee82849492b1F297134872dA2Abb260d`
- **支付方式**：MON、SOL或Base USDC
- **前端**：`https://planetexpress.dropclaw.cloud`

## 端点

### 浏览列表（免费）
```
GET /marketplace/listings
```
返回所有活跃的市场列表。

### 获取列表详情（免费）
```
GET /marketplace/listing/{id}
```
返回包含价格信息的列表详情（单位：MON/SOL/USDC）。

### 购买文件（使用x402支付）
```
POST /marketplace/purchase
Content-Type: application/json

{
  "listingId": 123,
  "buyerAddress": "0x..."  // optional
}
```
触发x402支付流程：接收402响应 → 在首选区块链上进行支付 → 使用`X-PAYMENT`头部重新尝试支付。

### 上架文件出售（需支付30美元的列表费）
```
POST /marketplace/list
Content-Type: application/json

{
  "fileId": "dropclaw-file-id",
  "title": "My File",
  "description": "What this file contains",
  "skillFileUri": "ipfs://Qm...",
  "keyHash": "0x...",
  "price": "0.5"
}
```
需支付30美元的列表费。

## 购买流程

1. 使用`GET /marketplace/listings`浏览可用文件。
2. 使用`GET /marketplace/listing/{id}`获取详细信息和价格。
3. 使用`POST /marketplace/purchase`并传入`listingId`，接收支付选项。
4. 在您选择的支持的区块链（MON、SOL或Base USDC）上进行支付。
5. 使用`X-PAYMENT: base64(JSON({ network, txHash })`重新尝试POST请求。
6. 收到加密文件及解密所需的技能文件。

## 上架流程

1. 首先通过DropClaw存储您的文件（使用`POST /vault/store`），系统会生成一个`fileId`。
2. 使用`POST /marketplace/list`上传文件详情和价格，系统会通过x402协议收取30美元的列表费。
3. 在任何支持的区块链上支付列表费。
4. 您的文件将出现在市场上供他人购买。

## 费用

| 费用 | 金额 | 说明 |
|-----|--------|-------|
| 列表费 | 30美元 | 上架文件时支付 |
| 买家费用 | 约1美元 | 加入购买价格 |
| 交付费用 | 2.5% | 从列表价格中扣除 |
| FARNS回购费用 | 50% | 所有协议费用的50%用于回购FARNS |

## 支付区块链

- **Monad**（eip155:143）：原生MON区块链，支持直接合约交互。
- **Solana**（solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp）：支持SOL支付。
- **Base**（eip155:8453）：支持USDC支付。

## 前端

该市场拥有完全去中心化的前端，托管在IPFS上：
- **Web**：`https://planetexpress.dropclaw.cloud`
- **IPNS**：`k51qzi5uqu5di1vh2ybr8qipy8mod859fjb0i548af7qyopyctlv7zpjblukee`

安装SDK：`npm i dropclaw` 或 `pip install dropclaw`