---
name: solana-whale-alert
description: 监控 Solana 钱包和代币中的大额交易。当大额资金转移发生时，系统会自动发送警报。无需使用 API 密钥。
---

# Solana 财富持有者活动监控工具（Solana Whale Alert）

该工具可实时监控 Solana 钱包和代币的大额交易，帮助用户发现潜在的财富持有者（“whales”）的交易行为。

## 使用方法

- “监控这个钱包的大额交易：[钱包地址]”
- “当有人转移超过 1 万美元的 SOL 时提醒我”
- “监控 [代币名称] 的顶级持有者的交易行为（尤其是出售行为）”
- “查看最近的大额 SOL 转移记录”

## 命令

### 查看最近的大额转账记录
```bash
bash scripts/whale-check.sh [min_amount_sol]
```

### 监控特定钱包
```bash
bash scripts/watch-wallet.sh <wallet_address> [check_interval_seconds]
```

### 扫描顶级代币持有者的交易行为
```bash
bash scripts/scan-holders.sh <token_mint>
```

## 该工具能检测到的交易类型：

| 交易类型 | 描述 | 含义 |
|---------|---------|-------|
| 大额 SOL 转移 | 转移金额超过 1000 SOL | 可能是财富持有者的资产重新配置 |
| CEX（中心化交易所）存款 | 向知名交易所的大额转账 | 可能预示着出售压力 |
| CEX 提现 | 从交易所的大额转账 | 可能表明财富持有者正在积累资产 |
| 代币抛售 | 顶级持有者大量出售代币 | 存在风险（如价格暴跌） |
| 新出现的财富持有者 | 未知钱包的大量资金流入 | 可能是专业投资者的入场信号 |

## 使用的免费 API：

- Solana RPC（getSignaturesForAddress, getTransaction） |
- Helius Enhanced API（如果拥有相关密钥，可获取更丰富的数据） |
- DexScreener（用于获取代币交易背景信息）

## 注意事项：

- 公共 RPC 请求的速率有限（约 40 次/10 秒） |
- 为提高处理效率，请设置 SOLANA_RPC_URL 或 HELIUS_API_KEY |
- 由于缺乏索引数据，历史交易记录的查看范围有限 |