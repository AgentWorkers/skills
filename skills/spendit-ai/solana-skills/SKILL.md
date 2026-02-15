---
name: solana
description: Solana钱包操作指南：

- 创建钱包：  
  - 使用Solana官方工具或第三方钱包应用程序来创建新的Solana钱包。

- 查看余额：  
  - 登录钱包，进入“账户”或“钱包”页面，即可查看当前的SOL币或其他代币余额。

- 发送SOL/代币：  
  - 选择要发送的代币，输入接收地址，然后输入发送数量，确认后即可完成交易。

- 通过Jupiter进行代币交换：  
  - Jupiter是一个用于Solana代币交易的平台。您可以在Jupiter上查找所需的代币对，进行买入或卖出操作。

- 在Pump.fun上发布代币：  
  - Pump.fun是一个用于代币发行的平台。开发者可以在该平台上创建代币项目，吸引投资者购买，从而筹集资金。

请注意：在进行任何交易之前，请确保您了解相关风险，并遵守Solana社区的规定。
triggers:
  - solana
  - wallet
  - sol balance
  - send sol
  - send token
  - swap
  - jupiter
  - pumpfun
  - pump.fun
  - launch token
metadata:
  clawdbot:
    emoji: "◎"
    requires:
      env:
        - SOLANA_PRIVATE_KEY
        - JUPITER_API_KEY
    primaryEnv: SOLANA_PRIVATE_KEY
---

# Solana 钱包 ◎

用于 AI 代理的 Solana 钱包管理和代币操作。

## 设置

```bash
pip install -r requirements.txt
```

## 初始化钱包

首先，创建一个新的钱包，并将私钥保存到 `.env` 文件中：

```bash
python3 {baseDir}/scripts/initialize.py
```

这将：
- 生成一个新的 Solana 密钥对
- 显示公钥（钱包地址）
- 将私钥以 base58 格式保存到 `.env` 文件中，文件名为 `SOLANA_PRIVATE_KEY`

**重要提示**：运行 `initialize.py` 后，请将私钥导出到您的环境变量中：
```bash
export SOLANA_PRIVATE_KEY=$(grep SOLANA_PRIVATE_KEY .env | cut -d '=' -f2)
```

或者直接加载 `.env` 文件：
```bash
source .env
```

## 钱包操作

### 查看 SOL 余额
```bash
python3 {baseDir}/scripts/wallet.py balance
python3 {baseDir}/scripts/wallet.py balance <wallet_address>
```

### 查看代币余额
```bash
python3 {baseDir}/scripts/wallet.py token-balance <token_mint_address>
python3 {baseDir}/scripts/wallet.py token-balance <token_mint_address> --owner <wallet_address>
```

### 发送 SOL
```bash
python3 {baseDir}/scripts/wallet.py send <recipient_address> <amount_in_sol>
```

### 发送 SPL 代币
```bash
python3 {baseDir}/scripts/wallet.py send-token <token_mint_address> <recipient_address> <amount>
```

### 获取钱包地址
```bash
python3 {baseDir}/scripts/wallet.py address
```

## Jupiter 交易服务

### 获取交易报价
```bash
python3 {baseDir}/scripts/jup_swap.py quote <input_token> <output_token> <amount>
python3 {baseDir}/scripts/jup_swap.py quote SOL USDC 1
```

### 执行交易
```bash
python3 {baseDir}/scripts/jup_swap.py swap <input_token> <output_token> <amount>
python3 {baseDir}/scripts/jup_swap.py swap SOL USDC 0.1
```

### 列出已知代币
```bash
python3 {baseDir}/scripts/jup_swap.py tokens
```

支持的代币符号：SOL、USDC、USDT、BONK、JUP、RAY、PYTH（或使用完整的代币发行地址）

## Pump.fun 代币发行

### 发行代币
```bash
python3 {baseDir}/scripts/pumpfun.py launch --name "Token Name" --symbol "TKN" --image ./logo.png
```

### 使用开发者购买功能发行代币
```bash
python3 {baseDir}/scripts/pumpfun.py launch --name "Token Name" --symbol "TKN" --image ./logo.png --buy 0.5
```

### 使用自定义发行地址发行代币
```bash
python3 {baseDir}/scripts/pumpfun.py launch --name "Token Name" --symbol "TKN" --image ./logo.png --mint-key <base58_key>
```

建议使用以 ‘pump’ 结尾的虚拟地址（vanity address）来发行代币，这样代币看起来更正规。生成虚拟地址的方法如下：
```bash
solana-keygen grind --ends-with pump:1
```

### 命令参数示例：
- `--name` - 代币名称（必填）
- `--symbol` - 代币符号（必填）
- `--image` - 代币图片路径（必填）
- `--description` 或 `-d` - 代币描述
- `--buy` 或 `-b` - 开发者购买数量（单位：SOL）
- `--mint-key` 或 `-m` - 自定义发行私钥（base58 格式）

## 网络配置

默认情况下，所有钱包操作都在 **mainnet** 上进行。可以使用 `--network` 参数切换网络：
```bash
python3 {baseDir}/scripts/wallet.py balance --network devnet
python3 {baseDir}/scripts/wallet.py balance --network testnet
```

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `SOLANA_PRIVATE_KEY` | 基于 base58 编码的私钥（必填） |
| `JUPITER_API_KEY` | Jupiter 交易服务的 API 密钥（必填） |
| `SOLANA_RPC_URL` | 自定义的 RPC 端点（可选） |

## 示例

```bash
# Initialize new wallet
python3 {baseDir}/scripts/initialize.py

# Check your SOL balance
python3 {baseDir}/scripts/wallet.py balance

# Send 0.1 SOL to another wallet
python3 {baseDir}/scripts/wallet.py send 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 0.1

# Check USDC balance (mainnet USDC mint)
python3 {baseDir}/scripts/wallet.py token-balance EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

# Send 10 USDC to another wallet
python3 {baseDir}/scripts/wallet.py send-token EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 10

# Quote swap: 1 SOL to USDC
python3 {baseDir}/scripts/jup_swap.py quote SOL USDC 1

# Swap 0.5 SOL to USDC
python3 {baseDir}/scripts/jup_swap.py swap SOL USDC 0.5

# Launch token on Pump.fun
python3 {baseDir}/scripts/pumpfun.py launch --name "My Token" --symbol "MTK" --image ./logo.png

# Launch with dev buy
python3 {baseDir}/scripts/pumpfun.py launch --name "My Token" --symbol "MTK" --image ./logo.png --buy 1
```

## 常见 Solana 代币的发行地址

| 代币 | 发行地址 |
|-------|--------------|
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| BONK | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` |

## 使用场景

- 为新 Solana 账户创建钱包
- 查看 SOL 或其他 SPL 代币的余额
- 发送 SOL 用于支付或转账
- 发送代币以进行 SPL 代币的交易
- 通过 Jupiter 交易服务进行代币交易
- 在 Pump.fun 平台上使用自定义图片和开发者购买功能发行代币
- 使用 `--network devnet` 在开发网络（devnet）上进行测试