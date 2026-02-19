---
name: goldenclaw
description: 在 Solana 上管理 GoldenClaw (GCLAW)：创建钱包、从 faucet（资金池）领取代币、查看余额、发送代币以及查看交易历史记录。适用于 OpenClaw AI 代理程序。
license: MIT
metadata:
  version: 1.1.0
  commands: gclaw
  author: AgentCrypto
---
# GoldenClaw (GCLAW) 技能

这是一个用于 [OpenClaw](https://openclaw.ai) 的 Solana SPL（Solana Protocol Language）技能，支持以下功能：管理 GCLAW 代币、从 faucet 提取代币、以及在不同代理之间进行代币转账。

## 安装

1. 将该技能文件解压到您的 `skills/` 文件夹中。
2. 在技能目录中运行 `npm run build` 命令（如果缺少依赖项，系统会自动安装它们）。

## 命令

- `gclaw setup` – 创建加密钱包。
- `gclaw claim` – 从 faucet (goldenclaw.org) 提取 GCLAW 代币。
- `gclaw balance` – 查看 GCLAW 代币和 SOL 代币的余额。
- `gclaw address` – 查看您的钱包地址。
- `gclaw send <amount> <address>` – 将 GCLAW 代币发送给其他代理。
- `gclaw donate <SOL>` – 向主钱包（treasury）捐赠 SOL 代币。
- `gclaw history` – 查看交易历史记录。
- `gclaw limits` – 查看消费限额。
- `gclaw tokenomics` – 查看代币分配统计信息。

## 链接

- Faucet: https://goldenclaw.org
- 官网: https://goldenclaw.org
- X 社交媒体账号: https://x.com/GClaw68175
- 代币信息: [Solscan](https://solscan.io/token/8fUqKCgQ2PHcYRnce9EPCeMKSaxd14t7323qbXnSJr4z)