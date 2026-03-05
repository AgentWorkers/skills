---
name: polymarket-arbitrage-pro
description: Polymarket预测市场交易工具。自动检测套利机会并执行交易。
metadata:
  author: BOB-Z-PRO
  version: 7.0.5
  env:
    - POLYMARKET_PRIVATE_KEY
---

# 💰 Polymarket Arbitrage Pro

**预测市场交易 | 套利检测 | 自动交易**

---

## 功能

✅ 市场扫描与套利检测  
✅ 真实交易下单  
✅ 7×24持续监控  

---

## 环境变量

```bash
# Polygon钱包私钥（用于签署交易）
export POLYMARKET_PRIVATE_KEY="your_polygon_private_key"
```

---

## 使用

```bash
arbitrage scan     # 扫描机会并执行交易
arbitrage start    # 启动持续监控
arbitrage balance  # 查看钱包余额
```

---

## 交易说明

1. **获取Polygon私钥** - 从MetaMask或OKX钱包导出
2. **钱包准备** - 需要USDC.e（交易）+ POL（Gas）
3. **设置环境变量** - `export POLYMARKET_PRIVATE_KEY="你的私钥"`

---

## 风险提示

- 加密货币交易有风险
- 请先用测试钱包小额测试
- 盈亏自负
