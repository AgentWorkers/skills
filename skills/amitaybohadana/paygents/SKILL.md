---
name: paygents
description: AI代理支付功能：生成钱包的深度链接（MetaMask、Trust Wallet），在链上验证交易，生成交易收据，查询账户余额。无需托管服务，无需后端支持，也无需API密钥。所有交易均由用户本人通过自己的钱包进行审批。
metadata:
  openclaw:
    requires:
      bins:
        - node
        - bash
---
# EVM支付深度链接功能

该功能用于生成用于EVM（以太坊虚拟机）支付的钱包深度链接。用户点击链接后，需要在MetaMask中进行确认，随后代理会在区块链上验证交易。

## 工作流程

1. 代理收集支付信息（收款人地址、金额、区块链、代币类型）。
2. 代理运行链接生成脚本，获取MetaMask的深度链接。
3. 代理将链接发送给用户。
4. 用户点击链接后，MetaMask会自动打开并显示转账界面，用户需进行确认。
5. 用户确认“发送”后，代理会在区块链上验证交易。

## 钱包检测

在生成链接之前，代理需要知道用户使用的钱包类型。只需询问一次，之后即可永久记住用户的偏好。

**支持原生深度链接的钱包：**

| 钱包 | `--wallet` 标志 | 深度链接格式 |
|--------|----------------|-----------------|
| MetaMask | `metamask`（默认） | `https://link.metamask.io/send/...` |
| Trust Wallet | `trust` | `https://link.trustwallet.com/send?...` |

**不支持生成深度链接的钱包：**
- Rabby：仅支持应用内浏览器操作，无直接发送链接功能。
- Coinbase Wallet：仅提供Dapp浏览器链接，无直接发送功能。
- Phantom：需要加密握手过程，无法通过简单URL进行发送。

如果用户使用的钱包不被支持，系统将默认使用MetaMask（最常用的钱包），或通知用户更换钱包。

系统应记录用户的钱包偏好设置，以避免重复询问。代理需将用户的偏好保存在本地会话上下文中（例如内存文件中），用户可随时要求代理清除该信息。

## 必需输入参数

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| `--to` | 是 | 收款人地址（格式：`0x...`） |
| `--amount` | 是 | 便于阅读的金额（例如：`1.5`） |
| `--chain-id` | 否 | 区块链ID（默认：`8453` Base） |
| `--asset` | 否 | 交易资产类型（默认：`ETH` 或 `ERC20`） |
| `--token` | 否 | 代币合约地址（对于USDC，系统会自动检测对应的区块链） |
| `--decimals` | 否 | 代币的小数位数（USDC默认为`6`，ETH默认为`18`） |
| `--symbol` | 否 | 代币符号（用于显示，默认为`USDC` 或 `ETH`） |
| `--wallet` | 否 | 钱包类型（默认：`metamask`） |

## 命令

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
- `deeplink`：MetaMask的深度链接地址
- `messageTemplate`：可供用户使用的发送提示信息

### 验证交易

用户确认“发送”后，代理会在区块链上验证交易：
```bash
skills/evm-usdc-wallet-poc/scripts/evm-verify-tx.sh \
  --chain-id 11155111 \
  --from 0xSENDER \
  --to 0xRECIPIENT \
  --asset ETH \
  --amount 0.001 \
  --blocks 50
```

如果找到匹配的交易记录，将返回交易哈希；否则返回“未找到”。

## 支持的区块链

| 区块链 | ID | 默认使用的USDC地址 |
|-------|----|-------------|
| Ethereum | 1 | `0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| Base | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bDa02913` |
| Sepolia | 11155111 | `0x1c7d4b196cb0c7b01d743fbc6116a902379c7238` |
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCf7e` |

## 用户提示信息

在发送链接时，务必包含以下内容：
1. 交易金额 + 代币类型 + 使用的区块链
2. 收款人地址（部分隐藏）
3. “点击链接打开MetaMask并完成确认”
4. “如果收款人地址或金额有误，请拒绝”

### 查询钱包余额

可以查询用户所有支持区块链上的原生货币及主要ERC20代币的余额：
```bash
# All chains at once
scripts/evm-balance.sh --address 0x1234...5678

# Single chain
scripts/evm-balance.sh --address 0x1234...5678 --chain-id 8453
```

输出结果为JSON格式，包含各区块链上的原生货币余额以及USDC、USDT、WETH、WBTC、DAI的余额。

无需API密钥，系统直接使用公共RPC接口进行查询。

## 生成交易收据

交易验证成功后，系统会生成结构化的交易收据：
```bash
skills/evm-usdc-wallet-poc/scripts/evm-receipt.sh \
  --tx-hash 0xabc123... \
  --chain-id 8453 \
  --memo "order-42" \
  --merchant "Cool Store"
```

选项：
- `--format json` | `markdown` | `both`（默认：`both`）
- `--out <directory>` | 将收据文件保存到指定目录（JSON + markdown格式）
- `--memo` | 交易订单ID或备注信息
- `--merchant` | 商家/收款人名称

收据内容包括：交易状态、金额、代币类型、发送方/接收方地址、Gas费用、区块信息以及区块浏览器链接、时间戳。

收据可用于向用户发送确认信息、用于记账，或转发给商家。

## RPC配置

默认情况下，脚本使用公共RPC接口。您可以通过以下方式调整配置：

**选项1：环境变量**（优先级最高）：
```bash
export RPC_1="https://my-private-eth-node.com"
export RPC_8453="https://my-base-rpc.com"
```

**选项2：配置文件**（将`config.example.json`复制到`config.json`）：
```json
{
  "rpc": {
    "1": "https://my-private-eth-node.com",
    "8453": "https://my-base-rpc.com"
  }
}
```

**选项3：公共备用接口**（默认设置，无需额外配置）：
当环境变量或配置文件未设置时，系统会自动使用公共RPC接口。使用公共接口（如`eth.llamarpc.com`）时，第三方服务可能会看到用户的钱包地址和交易哈希。

**安全与隐私注意事项：**
- 钱包操作由用户自行控制，代理无法强制执行交易。
- 系统仅验证区块链上的实际交易记录，不依赖用户的声明。
- 本功能为测试性质，不涉及后端服务或政策执行。
- 严禁存储或处理用户的私钥。
- **RPC隐私设置**：如果使用公共备用RPC接口，第三方服务可能会看到用户的钱包地址和交易哈希。请通过环境变量或配置文件设置自定义RPC接口。
- **钱包偏好记录**：代理会记录用户偏好的钱包类型（MetaMask或Trust Wallet），但仅保存钱包名称，不包含私钥或敏感数据。用户可随时要求代理清除这些信息。