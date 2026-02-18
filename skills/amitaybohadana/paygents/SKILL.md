---
name: paygents
description: AI代理支付功能：生成MetaMask或Trust Wallet的钱包深度链接（deeplink），在链上验证交易，生成交易收据，查询账户余额。该功能不涉及资金托管，无需后端服务器，也不需要API密钥。所有交易均由用户本人通过自己的钱包进行确认。
---
# EVM支付深度链接功能

该功能用于生成用于EVM（以太坊虚拟机）支付的钱包深度链接。用户点击链接后，会在MetaMask中完成交易确认，随后代理会在链上验证交易是否成功。

## 功能流程

1. 代理收集支付信息（收款人地址、金额、链ID、代币类型）。
2. 代理运行链接生成脚本，获取MetaMask所需的深度链接。
3. 代理将链接发送给用户。
4. 用户点击链接后，MetaMask会自动弹出转账界面，用户需进行确认。
5. 用户确认转账后，代理会在链上验证交易是否完成。

## 钱包检测

在生成链接之前，代理需要知道用户使用的是哪种钱包。只需询问一次，即可永久记住用户的钱包类型。

**支持原生深度链接的钱包：**

| 钱包 | `--wallet` 参数 | 深度链接格式 |
|--------|----------------|-----------------|
| MetaMask | `metamask`（默认） | `https://link.metamask.io/send/...` |
| Trust Wallet | `trust` | `https://link.trustwallet.com/send?...` |

**不支持生成深度链接的钱包：**
- Rabby：仅支持应用内浏览器操作，无直接转账链接。
- Coinbase Wallet：仅提供DApp浏览器链接，无直接转账功能。
- Phantom：需要加密握手过程，无法通过简单URL进行转账。

如果用户使用的钱包不支持该功能，系统将默认使用MetaMask（最常用的钱包），或通知用户更换钱包。

**用户钱包偏好存储**：将用户的钱包偏好信息存储起来，避免重复询问。例如：可以将其添加到`TOOLS.md`文件或内存中。

## 必需输入参数

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| `--to` | 是 | 收款人地址（格式：`0x...`） |
| `--amount` | 是 | 人类可读的金额（例如：`1.5`） |
| `--chain-id` | 否 | 链ID（默认：`8453`） |
| `--asset` | 否 | 交易资产类型（默认：`ETH`或`ERC20`） |
| `--token` | 否 | 代币合约地址（对于USDC，系统会自动检测） |
| `--decimals` | 否 | 代币的小数位数（默认：USDC为`6`，ETH为`18`） |
| `--symbol` | 否 | 代币符号（用于显示，默认：`USDC`或`ETH`） |
| `--wallet` | 否 | 使用的钱包类型（默认：`metamask`） |

## 命令说明

### 生成支付链接

**ERC20（USDC）——使用MetaMask：**
```bash
skills/evm-usdc-wallet-poc/scripts/evm-payment-link.sh \
  --to 0x1234...5678 \
  --amount 10 \
  --chain-id 8453
```

**原生ETH——使用Trust Wallet：**
```bash
skills/evm-usdc-wallet-poc/scripts/evm-payment-link.sh \
  --to 0x1234...5678 \
  --amount 0.01 \
  --asset ETH \
  --chain-id 11155111 \
  --wallet trust
```

输出结果为JSON格式，包含以下内容：
- `intent`：结构化的支付信息
- `deeplink`：MetaMask所需的深度链接
- `messageTemplate`：用户可使用的转账提示信息

### 验证交易

用户确认转账后，代理会在链上验证交易是否完成：
```bash
skills/evm-usdc-wallet-poc/scripts/evm-verify-tx.sh \
  --chain-id 11155111 \
  --from 0xSENDER \
  --to 0xRECIPIENT \
  --asset ETH \
  --amount 0.001 \
  --blocks 50
```

如果验证成功，返回对应的交易哈希值；否则返回“未找到交易”。

## 支持的链

| 链ID | 默认USDC地址 |
|-------|-------------|
| Ethereum | 1 | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| Base | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bDa02913` |
| Sepolia | 11155111 | `0x1c7d4b196cb0c7b01d743fbc6116a902379c7238` |
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCf7e` |

## 用户提示信息

在发送链接时，务必包含以下内容：
1. 交易金额 + 代币类型 + 链ID
2. 收款人地址（部分隐藏）
3. “点击链接在MetaMask中确认转账”
4. “如果收款人或金额信息有误，请拒绝交易”

### 查询钱包余额

查询用户所有支持链上的原生货币及主要ERC20代币的余额：
```bash
# All chains at once
scripts/evm-balance.sh --address 0x1234...5678

# Single chain
scripts/evm-balance.sh --address 0x1234...5678 --chain-id 8453
```

输出结果为JSON格式，包含各链上的原生货币余额以及USDC、USDT、WETH、WBTC、DAI的余额。

**说明：** 无需API密钥，直接使用公开的RPC接口。

### 生成交易收据

交易验证成功后，生成结构化的交易收据：
```bash
skills/evm-usdc-wallet-poc/scripts/evm-receipt.sh \
  --tx-hash 0xabc123... \
  --chain-id 8453 \
  --memo "order-42" \
  --merchant "Cool Store"
```

**可选参数：**
- `--format json` | `markdown` | `both`（默认：`both`）
- `--out <目录>` | 将收据文件保存到指定目录（JSON格式或Markdown格式）
- `--memo` | 交易订单ID或备注信息
- `--merchant` | 商家/收款人名称

收据内容包括：交易状态、金额、代币类型、发送方/接收方地址、Gas费用、区块信息以及区块浏览器链接、时间戳。

收据可以发送给用户作为确认信息，用于账务记录，或转发给商家。

## 安全注意事项

- 用户的钱包安全至关重要——代理无法强制执行交易。
- 验证过程基于链上的实际交易记录，而非用户的自行声明。
- 本功能为测试性质，不涉及后端服务或政策执行。
- 严禁存储或处理用户的私钥。