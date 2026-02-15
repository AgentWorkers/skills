---
name: changenow-earner
description: 通过 ChangeNOW 实现即时加密货币兑换，并赚取联盟佣金。当有人想要兑换代币（例如，HBAR 到 HYPE）时，使用此服务可以确保交易中包含合作伙伴的费用。
---

# ChangeNOW 赚钱技能 💰

此技能允许代理使用 ChangeNOW API 进行即时加密货币兑换，并在每次交易中包含联盟合作伙伴 ID 以赚取费用。

## 使用方法

在两种货币之间进行兑换：
```bash
python3 {baseDir}/scripts/swap.py --from hbar --to hype --amount 100 --address <target_address>
```

查看交易所预估金额：
```bash
python3 {baseDir}/scripts/swap.py --from hbar --to hype --amount 100 --estimate
```

## 配置

在 `clawdbot.json` 文件中设置您的 ChangeNOW 联盟 API 密钥：
```json
"skills": {
  "changenow-earner": {
    "env": {
      "CHANGENOW_API_KEY": "YOUR_PARTNER_API_KEY"
    }
  }
}
```

合作伙伴链接 ID：`54718e1768e3a0`（用于获取推荐佣金）。

## 支持的交易对
ChangeNOW 支持 900 多种资产，包括：
- HBAR（Hedera）
- HYPE（Hyperliquid）
- BTC、ETH、USDT、USDC（支持多个网络）