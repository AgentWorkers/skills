---
name: claw-trader-lite
description: OpenClaw代理的多平台市场情报服务：实时监控Hyperliquid（去中心化金融，DeFi）和LNMarkets（比特币）平台上的价格、余额及持仓情况。支持使用公开地址进行安全的投资组合管理（仅提供读取权限）。
env:
  HYPERLIQUID_ACCOUNT_ADDRESS:
    description: "The public wallet address to pull balance and position data from on Hyperliquid (e.g. 0x...)"
    required: false
---

# Claw Trader LITE：多平台市场情报工具

专为 **Hyperliquid**（去中心化金融，DeFi）和 **LNMarkets**（比特币）生态系统设计的专业级钱包与市场监控工具。📈

### 🔍 主要功能：
* ✅ **实时情报**：统一扫描 BTC、ETH、SOL 及 100 多种山寨币的行情。
* ✅ **投资组合管理**：通过公开标识符实现跨平台余额和持仓监控。
* 🛡️ **零托管架构**：此“Lite”版本仅支持查询功能，不要求用户提供私钥或 API 密钥。

---

### 🛠️ 核心功能：
* `/status`：查看已连接账户的状态及公开余额。
* `/proof`：查看由该工具处理的、可验证的链上交易记录。
* `/help`：查阅完整的技术手册和集成指南。

---

## 🚀 使用方法

### 安装
```bash
pip install requests
```

### 基本使用
```python
from claw_lite import create_monitor

# Initialize secure monitor (Read-Only)
monitor = create_monitor()

# Fetch latest prices across chains
eth_price = monitor.get_price("ETH", "hyperliquid")
btc_price = monitor.get_price("BTC", "lnmarkets")

print(f"ETH: ${eth_price:,.2f} | BTC: ${btc_price:,.2f}")
```

---

### 📑 技术文档：
如需获取完整的技术手册、仓库链接以及关于高级连接功能或自定义集成的支持信息，请访问我们的文档频道：

👉 **[Claw 文档与支持](https://t.me/Opennnclawww_bot)** 🦞

---
**由 @Claw 开发 🦞 | 已在真实市场中经过验证**
* 专业用户可免费使用该监控工具。*