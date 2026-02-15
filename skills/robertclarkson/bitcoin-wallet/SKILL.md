---
slug: breezclaw
name: BreezClaw
description: "适用于AI代理的自托管比特币及Lightning网络钱包。支持通过Lightning Network、Spark或链上比特币进行资金发送与接收。功能包括：查询比特币余额、支付操作、生成Lightning网络发票以及管理钱包相关事务。使用该钱包需要安装BreezClaw插件并拥有Breez API密钥。"
version: 1.0.0
author: onesandzeros-nz
keywords: bitcoin, lightning, wallet, breez, spark, sats, payments, self-custodial, breezclaw
homepage: https://github.com/onesandzeros-nz/BreezClaw
---

# BreezClaw

这是一个专为AI代理设计的、支持自我管理的比特币和Lightning网络钱包。该钱包由Breez SDK Spark提供技术支持。

## 安装

```bash
# Clone plugin
cd ~/.openclaw/extensions
git clone https://github.com/onesandzeros-nz/BreezClaw.git breezclaw

# Install dependencies and build
cd breezclaw
npm install
npm run build
```

## 配置

### 1. 获取Breez API密钥

请访问 https://breez.technology/sdk/ 进行注册。

### 2. 添加到OpenClaw配置文件中

编辑 `~/.openclaw/openclaw.json` 文件：

```json
{
  "plugins": {
    "entries": {
      "breezclaw": {
        "enabled": true,
        "config": {
          "breezApiKey": "YOUR_BREEZ_API_KEY",
          "network": "mainnet"
        }
      }
    }
  }
}
```

### 3. 重启OpenClaw

```bash
openclaw gateway restart
```

## 工具

| 工具 | 描述 |
|------|-------------|
| `wallet_status` | 检查钱包是否存在及其连接状态 |
| `wallet_connect` | 通过助记词连接或创建钱包 |
| `wallet_balance` | 查看余额（单位：sats或BTC） |
| `wallet.receive` | 生成支付请求 |
| `wallet_prepare_send` | 准备支付请求并估算费用 |
| `wallet_send` | 执行已确认的支付 |
| `wallet_transactions` | 查看交易历史记录 |
| `wallet_info` | 查看钱包详细信息 |
| `wallet_backup` | 备份钱包数据（注意：此操作涉及敏感信息！） |
| `walletdisconnect` | 断开钱包连接 |

## 支付方式

- `spark` — 可重用的Spark地址（默认方式） |
- `sparkinvoice` — 包含金额的Spark发票 |
- `lightning` — BOLT11发票 |
- `bitcoin` — 在链上的比特币地址 |

## 支付流程

**始终需要两步：**

1. 使用 `wallet_prepare_send` 准备支付请求并查看费用；
2. 用户确认后，使用 `wallet_send(confirmed=true)` 执行支付。

## 安全性注意事项：

- 除非用户明确要求，否则切勿泄露助记词；
- 在发送任何交易之前，务必向用户显示费用信息；
- 所有支付操作均需用户明确确认；
- 钱包数据存储在 `~/.openclaw/breezclaw/` 目录下。

## 示例

```
"What's my balance?" → wallet_balance

"Invoice for 1000 sats" → wallet_receive(method="lightning", amount_sats=1000)

"Send 500 sats to user@wallet.com" → resolve LNURL → wallet_prepare_send → confirm → wallet_send
```