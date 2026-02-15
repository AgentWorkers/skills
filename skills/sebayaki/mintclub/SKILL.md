# Mint Club V2 — 代理技能

使用 `mc` CLI 与 Mint Club V2 的债券曲线代币进行交互。

## 设置

```bash
npm install -g mint.club-cli
```

设置您的私钥：
```bash
mc wallet --set-private-key 0x...
# Or export PRIVATE_KEY=0x...
```

## 命令

### 读取操作（无需输入密钥）

```bash
mc info <token>          # Token info (supply, reserve, price, curve)
mc price <token>         # Price in reserve + USD
mc wallet                # Wallet address and balances
```

### 交易

```bash
# Buy/sell via bonding curve (reserve token)
mc buy <token> -a <amount>                    # Buy tokens
mc sell <token> -a <amount>                   # Sell tokens

# Zap: buy/sell with any token (auto-routes via Uniswap)
mc zap-buy <token> -i ETH -a 0.01            # Buy with ETH
mc zap-sell <token> -a 100 -o USDC           # Sell for USDC

# Direct Uniswap swap (any pair, V3 + V4)
mc swap -i ETH -o HUNT -a 0.001              # Swap tokens
mc swap -i HUNT -o USDC -a 100 -s 0.5        # Custom slippage
```

### 创建代币

```bash
mc create -n "My Token" -s MYT -r HUNT -x 1000000 \
  --curve exponential --initial-price 0.01 --final-price 100
```

曲线预设：`linear`（线性）、`exponential`（指数）、`logarithmic`（对数）、`flat`（平坦）

### 转移

```bash
mc send <address> -a 0.01                     # Send ETH
mc send <address> -a 100 -t HUNT              # Send ERC-20
```

## 代币解析

使用地址或已知符号：`ETH`、`WETH`、`USDC`、`HUNT`、`MT`

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `PRIVATE_KEY` | 钱包私钥（或使用 `~/.mintclub/.env`） |

## 注意事项

- 所有操作都在 **Base**（链号 8453）上进行
- 默认滑点：1%
- 创建代币时的默认费用：1% 的铸造费用 + 1% 的销毁费用
- 代币地址会自动保存到 `~/.mintclub/tokens.json` 文件中
- 社区网站：https://onchat.sebayaki.com/mintclub