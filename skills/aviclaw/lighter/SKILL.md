---
name: lighter
description: 与 Lighter 协议进行交互——这是一个基于 ZK（Zcash-Kernel）技术的汇总订单簿去中心化交易所（DEX）。当您需要在 Lighter 上进行交易、查看价格、管理持仓或查询账户数据时，可以使用该功能。
env:
  required:
    - LIGHTER_API_KEY
    - LIGHTER_ACCOUNT_INDEX
  optional:
    - LIGHTER_L1_ADDRESS
---
# Lighter 协议

Lighter 是一个基于零知识证明（Zero-Knowledge Proof, ZK）技术的去中心化交易所（DEX），支持订单簿交易，具有毫秒级的交易延迟和零交易费用。

## 快速入门（仅限读取）

```bash
# Markets are public - no credentials needed
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBooks"
```

## 什么是 Lighter？

- 零交易费用，适合零售交易者
- 毫秒级的交易延迟
- 所有交易操作都经过零知识证明的验证
- 由 Founders Fund、Robinhood 和 Coinbase Ventures 投资支持

**API 端点：** https://mainnet.zklighter.elliot.ai
**链 ID：** 300

## ⚠️ 安全注意事项

### 第三方依赖

- 该功能仅支持使用 **requests 库** 进行只读操作。
- 要签署交易订单，您有两种选择：

**选项 A：仅限读取**
```bash
pip install requests
```
仅适用于公开数据（市场、订单簿、价格信息）。

**选项 B：全功能交易**
需要使用官方的 Lighter SDK。在安装前请仔细检查并验证：
- SDK 仓库：https://github.com/elliottech/lighter-python
- 在进行任何设置之前，请核实仓库所有者、星标数量以及代码质量。

### 外部代码

**仅在满足以下条件时使用外部 SDK：**
1. 已经审查过 GitHub 仓库的代码。
2. 理解代码的用途。
3. 使用专用的交易钱包（而非您的主钱包）进行交易。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `LIGHTER_API_KEY` | 是 | 来自 SDK 设置的 API 密钥 |
| `LIGHTER_ACCOUNT_INDEX` | 是 | 您的 Lighter 账户索引 |
| `LIGHTER_L1_ADDRESS` | 可选 | 用于查询的 ETH 地址 |

## API 使用方法

### 公开接口（无需认证）

```bash
# List all markets
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBooks"

# Get order book
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBook?market_id=1"

# Get recent trades
curl "https://mainnet.zklighter.elliot.ai/api/v1/trades?market_id=1"
```

### 需要认证的接口

```bash
# Account balance (requires API key in header)
curl -H "x-api-key: $LIGHTER_API_KEY" \
  "https://mainnet.zklighter.elliot.ai/api/v1/account?by=index&value=$LIGHTER_ACCOUNT_INDEX"
```

## 获取您的账户索引

```bash
# Query by ETH address
curl "https://mainnet.zklighter.elliot.ai/api/v1/accountsByL1Address?l1_address=YOUR_ADDRESS"
```

响应中包含 `sub_accounts[].index`——请将其用作您的账户索引。

## 获取 API 密钥

1. 查看官方的 Lighter SDK 文档：https://github.com/elliottech/lighter-python
2. 克隆并审核 SDK 代码。
3. 使用专用钱包运行设置流程。
4. 安全地存储生成的 API 密钥。

## 常见问题

- **“受地域限制”**：Lighter 有地域使用限制，请确保遵守其服务条款。
- **SDK 签名问题**：为确保交易执行的可靠性，请使用 `create_market_order()` 而不是 `create_order()` 方法。

## 市场 ID

| ID | 符号 |
|----|--------|
| 1 | ETH-USD |
| 2 | BTC-USD |
| 3 | SOL-USD |

## 链接

- API：https://mainnet.zklighter.elliot.ai
- 仪表盘：https://dashboard.zklighter.io
- SDK：https://github.com/elliottech/lighter-python

---

**免责声明：** 在使用任何外部代码之前，请务必仔细审查。请使用专用的交易钱包进行交易操作。