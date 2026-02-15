# crypto-watcher

监控加密货币钱包和去中心化金融（DeFi）资产状况。当有变化时，系统会发出警报。

## 功能

- **钱包追踪**：支持追踪多个区块链上的 ETH 及代币余额
- **去中心化金融资产**：显示锁定资金（LP）情况、借贷状态以及质押奖励
- **Gas 费用提醒**：在交易费用较低时发出通知
- **大额转账提醒**：监测目标代币上的大额转账行为

## 使用方法

### 设置
```bash
# Add a wallet to watch
crypto-watcher add 0x1234...abcd --name "main" --chains eth,arb,base

# Configure alerts
crypto-watcher config --gas-alert 20 --balance-change 5%
```

### 命令行操作
```bash
# Check all positions
crypto-watcher status

# Check specific wallet
crypto-watcher status main

# Gas prices
crypto-watcher gas

# DeFi positions (via DefiLlama)
crypto-watcher defi 0x1234...abcd
```

### 与 HEARTBEAT 服务集成

将 crypto-watcher 集成到 HEARTBEAT 服务中：
```markdown
### Crypto Check
- Run `crypto-watcher status --quiet` 
- Alert if any position health < 1.5 or balance dropped > 10%
- Check gas, alert if < 15 gwei (good time for L1 txs)
```

## 配置文件

配置文件路径：`~/.config/crypto-watcher/config.json`
```json
{
  "wallets": [
    {
      "address": "0x...",
      "name": "main",
      "chains": ["eth", "arb", "base"]
    }
  ],
  "alerts": {
    "gasThreshold": 20,
    "balanceChangePercent": 5,
    "healthFactorMin": 1.5
  }
}
```

## 数据来源

- **余额信息**：通过公共 RPC 接口获取（无需 API 密钥）
- **去中心化金融数据**：使用 DefiLlama API（免费）
- **Gas 费用**：通过 `eth_gasPrice` RPC 接口获取
- **价格信息**：使用 CoinGecko API（免费 tier）

## 支持的区块链

| 区块链 | ID | RPC 接口 |
|-------|-----|-----|
| Ethereum | eth | https://eth.llamarpc.com |
| Arbitrum | arb | https://arb1.arbitrum.io/rpc |
| Base | base | https://mainnet.base.org |
| Optimism | op | https://mainnet.optimism.io |
| Polygon | matic | https://polygon-rpc.com |