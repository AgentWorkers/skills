# Bitpanda 投资组合功能

通过命令行界面（CLI）查看 Bitpanda 的加密货币投资组合、钱包余额及交易记录。

## 认证

API 密钥的获取顺序如下：
1. 从 `BITPANDA_API_KEY` 环境变量中读取
2. 从 `~/.openclaw/credentials/bitpanda/config.json` 文件中读取（格式为 `{"api_key": "..."}`）

API 密钥可以在以下链接生成：https://web.bitpanda.com/my-account/apikey
推荐的访问权限范围：**Balance**（余额）、**Trade**（交易记录）、**Transaction**（交易详情）

## 命令

```bash
bitpanda portfolio                    # Non-zero wallets grouped by crypto/fiat/index
bitpanda wallets                      # All non-zero wallets with balances
bitpanda transactions --limit 20      # Recent trades
bitpanda transactions --flow buy      # Buy trades only
bitpanda transactions --flow sell     # Sell trades only
bitpanda asset BTC                    # Current price + your balance
```

## 注意事项：

- 该功能仅支持查看数据，不支持进行交易或资金转移。
- 通过 Bitpanda 的“Earn/Staking”（赚取/质押）功能获得的资产不会在余额中显示。
- `asset` 命令使用公开的股票代码（无需认证）来获取资产价格。
- 数据分页功能是自动实现的。
- 需要安装并使用以下工具：`curl`、`jq`、`bc`。