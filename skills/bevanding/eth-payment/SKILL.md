---
name: eth-payment
description: 生成适用于任何 EVM 链路的 EIP-681 Ethereum 支付链接和 QR 代码。无需任何配置，即可立即开始接收 ETH 和 ERC-20 类型的支付。适用于创建支付请求、发票、捐赠链接或任何链上支付请求的场景。支持 Base、Ethereum、Arbitrum、Optimism、Polygon 等区块链平台。
---
# ETH支付功能

> **零配置，即时可用。支持所有EVM区块链。**

## 功能介绍

该功能可生成符合EIP-681标准的支付链接，适用于MetaMask及其他以太坊钱包。非常适合以下场景：
- 支付请求与发票
- 捐赠链接
- 移动设备友好的支付流程
- 任何链上的支付收集

**无需API密钥、服务器或额外配置。**

## 安装

### 先决条件

- **Python 3.8及以上**：运行脚本的必备环境
- **Node.js（可选）**：仅用于生成二维码（使用`npx qrcode`命令）

### 快速安装

无需额外依赖项！该功能仅使用Python标准库以及`npx qrcode`工具（首次使用时会自动下载）。

### 运行该功能

```bash
python3 scripts/eth_payment.py create --to 0xYourAddress --amount 0.1
```

---

## 快速入门

```bash
# Basic ETH payment on Base
eth-payment create --to 0xYourAddress --amount 0.1

# USDC payment with QR code
eth-payment create --to 0xYourAddress --amount 100 --token USDC --qr payment.png

# Specify network
eth-payment create --to 0xYourAddress --amount 10 --token USDC --network ethereum --qr qr.png
```

## 命令说明

### `create` - 生成支付链接

```bash
eth-payment create --to <address> --amount <number> [options]

Required:
  --to <address>      Recipient address (0x...)
  --amount <number>   Amount to request

Options:
  --token <symbol>    Token symbol (default: ETH)
  --network <name>    Network: base, ethereum, arbitrum, optimism, polygon (default: base)
  --qr <path>         Generate QR code and save to path
  --json              Output as JSON for programmatic use
```

### `chains` - 列出支持的网络

```bash
eth-payment chains
eth-payment chains --json
```

### `tokens` - 显示指定网络的代币信息

```bash
eth-payment tokens --network base
eth-payment tokens --network ethereum --json
```

### `validate` - 验证地址

```bash
eth-payment validate 0x...
```

## 支持的网络

| 网络 | 链路ID | 原生代币 | ERC-20代币 |
|---------|----------|--------------|---------------|
| base | 8453 | ETH | USDC, USDT, WETH |
| ethereum | 1 | ETH | USDC, USDT, WETH, DAI |
| arbitrum | 42161 | ETH | USDC, USDT, ARB |
| optimism | 10 | ETH | USDC, OP |
| polygon | 137 | MATIC | USDC, USDT, WETH |

## 使用示例

### 通过二维码支付发票

```bash
eth-payment create \
  --to 0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e \
  --amount 100 \
  --token USDC \
  --network base \
  --qr invoice_qr.png
```

### 集成所需的JSON数据

```bash
eth-payment create --to 0x... --amount 10 --token USDC --json
```

**输出示例：**

```json
{
  "success": true,
  "network": "base",
  "chain_id": 8453,
  "token": "USDC",
  "recipient": "0x...",
  "amount": "10",
  "links": {
    "eip681": "ethereum:0x833...@8453/transfer?address=0x...&uint256=10000000",
    "metamask": "https://metamask.app.link/send/..."
  },
  "transaction": {
    "to": "0x833...",
    "value": "0x0",
    "data": "0xa9059cbb..."
  }
}
```

## 工作原理

1. **遵循EIP-681标准**：使用以太坊改进提案681格式生成支付链接。
2. **跨链兼容**：同一代码适用于所有EVM区块链，只需调整配置即可。
3. **二维码生成**：通过`npx qrcode`在本地生成二维码，无需依赖外部服务。

## 安全注意事项

- 该功能仅用于生成支付链接，无法执行交易。
- 无需使用私钥或敏感信息。
- 所有处理过程均在本地完成。
- 在分享支付链接前，请务必验证收款人地址。

## 添加新网络

如需添加新的EVM区块链，请编辑`config/chains.json`文件：

```json
{
  "chains": {
    "new-chain": {
      "name": "New Chain",
      "chain_id": 12345,
      "native_token": "NATIVE",
      "tokens": {
        "NATIVE": {
          "address": "0x0000000000000000000000000000000000000000",
          "decimals": 18,
          "is_native": true
        },
        "USDC": {
          "address": "0x...",
          "decimals": 6
        }
      }
    }
  }
}
```

---

**维护者**：Web3 Investor Team  
**许可证**：MIT许可证