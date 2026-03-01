---
name: lighter
description: 与 Lighter 协议进行交互——这是一个基于 ZK（Zcash-Kernel）技术的订单簿去中心化交易所（DEX）。当您需要在 Lighter 上进行交易、查看价格、管理持仓或查询账户数据时，可以使用该功能。
env:
  required:
    - LIGHTER_API_KEY
    - LIGHTER_ACCOUNT_INDEX
  optional:
    - LIGHTER_L1_ADDRESS
---
# Lighter 协议

Lighter 是一个基于零知识证明（ZK）技术的订单簿去中心化交易所（DEX），支持零费用交易，并具有毫秒级的交易延迟。

## 快速入门（仅限读取操作）

```bash
# Markets are public - no credentials needed
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBooks"
```

## 什么是 Lighter？

- 零费用：对散户交易者完全免费
- 毫秒级延迟：确保交易指令能够快速执行
- 所有操作均经过零知识证明（ZK）验证
- 获得 Founders Fund、Robinhood 和 Coinbase Ventures 的支持

**API 端点：** https://mainnet.zklighter.elliot.ai
**链 ID：** 300

## ⚠️ 安全注意事项

### 第三方依赖

对于仅限读取的操作，Lighter 可以使用 **just requests 库**。若需执行订单签署操作，有以下两种选择：

**选项 A（仅限读取操作）：**
```bash
pip install requests
```
仅适用于获取公开数据（市场信息、订单簿、价格等）。

**选项 B（全功能交易）：**
需要使用官方的 Lighter SDK。在安装前请务必仔细检查并验证：
- SDK 仓库：https://github.com/elliottech/lighter-python
- 在运行任何设置之前，请核实仓库所有者、星标数量以及代码质量。

### 外部代码

**仅在满足以下条件时使用外部 SDK：**
1. 已经仔细查阅了 GitHub 仓库的代码。
2. 理解代码的功能和用途。
3. 使用专门的交易钱包（而非你的主要钱包）进行交易。

## 环境变量

| 变量        | 是否必填 | 说明                                      | 来源                          |
|------------|---------|-----------------------------------------|-----------------------------|
| `LIGHTER_API_KEY` | 是      | 来自 Lighter SDK 设置的 API 密钥                | 详见“获取 API 密钥”部分            |
| `LIGHTER_ACCOUNT_INDEX` | 是      | 你的 Lighter 子账户索引（0-252）                   | 详见“获取账户索引”部分            |
| `LIGHTER_L1_ADDRESS` | 可选      | 你在 Lighter 上使用的 ETH 地址（格式：0x...）            | 你的 MetaMask/钱包地址                |

### 设置你的凭证

**步骤 1：获取你的 L1 地址**
- 这是你的以太坊地址（例如：`0x1234...abcd`）。
- 使用连接到 Lighter 仪表板的同一钱包。

**步骤 2：获取你的账户索引**
```bash
curl "https://mainnet.zklighter.elliot.ai/api/v1/accountsByL1Address?l1_address=YOUR_ETH_ADDRESS"
```
响应结果中包含 `sub_accounts[]`.index`——这就是你的账户索引（主账户通常为 0）。

**步骤 3：获取你的 API 密钥**
1. 安装 Lighter Python SDK：`pip install lighter-python`
2. 按照官方文档中的设置指南进行操作：https://github.com/elliottech/lighter-python/blob/main/examples/system_setup.py
3. SDK 会为你生成与账户关联的 API 密钥。
4. 请妥善保管私钥，切勿将其提交到 Git 中。

**快速测试（仅限读取操作，无需输入凭证）：**
```bash
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBooks"
```

## API 使用方法

### 公开端点（无需认证）

```bash
# List all markets
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBooks"

# Get order book
curl "https://mainnet.zklighter.elliot.ai/api/v1/orderBook?market_id=1"

# Get recent trades
curl "https://mainnet.zklighter.elliot.ai/api/v1/trades?market_id=1"
```

### 需要认证的端点

```bash
# Account balance (requires API key in header)
curl -H "x-api-key: $LIGHTER_API_KEY" \
  "https://mainnet.zklighter.elliot.ai/api/v1/account?by=index&value=$LIGHTER_ACCOUNT_INDEX"
```

## 获取你的账户索引

请参考上述“设置你的凭证”部分的说明，了解如何使用 curl 命令获取账户索引。

## 获取 API 密钥

请参考上述“设置你的凭证”部分的步骤指南，了解如何获取 API 密钥。

## 常见问题

**“受地域限制”：**
- Lighter 有地域使用限制，请确保你的操作符合其使用条款。

**SDK 签署问题：**
- 为确保交易执行的可靠性，请使用 `create_market_order()` 而非 `create_order()` 函数。

## 市场 ID

| ID       | 符号        |
|---------|-----------|
| 1        | ETH-USD      |
| 2        | BTC-USD      |
| 3        | SOL-USD      |

## 链接

- API：https://mainnet.zklighter.elliot.ai
- 仪表板：https://dashboard.zklighter.io
- SDK：https://github.com/elliottech/lighter-python

---

## 其他示例

请参阅该技能文件夹中的 `USAGE.md` 文件，其中包含：
- 所有端点的详细 curl 命令示例
- 订单簿和交易查询方法
- 账户及持仓信息的查询方式
- 签署交易流程（从生成随机数（nonce）到交易签名再到广播）

**免责声明：** 在使用任何外部代码之前，请务必仔细检查。请使用专用交易钱包进行交易。