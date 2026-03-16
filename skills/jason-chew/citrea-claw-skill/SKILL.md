# citrea-claw-skill

本工具用于监控 Citrea 的比特币 Layer2 生态系统，提供 DEX 池、流动性、套利机会、代币价格以及钱包余额等信息的实时更新。所有数据均直接从 Citrea 主网获取，无需使用第三方 API。

## 命令

### balance
查询指定钱包地址的 cBTC 和代币余额（以 USD 为单位）。
- **用法:** `balance <地址>`
- **示例:** `balance 0xYourAddress`

### price
从 RedStone 在链上的预言机获取代币的当前 USD 价格。
- **用法:** `price <代币>`
- **示例:** `price wcBTC`
- **支持的代币:** wcBTC, ctUSD, USDC.e, USDT.e, WBTC.e, JUSD

### pool:price
并列显示每个 DEX 上某代币对的隐含价格及其与预言机价格的偏差。
- **用法:** `pool:price <代币A> <代币B>`
- **示例:** `pool:price wcBTC USDC.e`

### pools:recent
列出过去 N 小时内在 JuiceSwap 和 Satsuma 中创建的所有新 DEX 池。
- **用法:** `pools:recent [小时数]`
- **示例:** `pools:recent 24`

### pools:latest
显示每个 DEX 上最新创建的 DEX 池。
- **用法:** `pools:latest`

### pools:monitor
实时监控新 DEX 池的创建情况。当任何支持的 DEX 上创建新池时，会发送 Telegram 警报。
- **用法:** `pools:monitor`

### pool:liquidity
显示某个 DEX 池的 TVL（总价值锁定）和代币储备情况。支持输入池地址、代币对或单个代币。
- **用法:** `pool:liquidity <池地址|代币A 代币B|代币>`
- **示例:**
  - `pool:liquidity wcBTC USDC.e`
  - `pool:liquidity 0xPoolAddress`
  - `pool:liquidity wcBTC`

### arb:check
检查指定代币对在 JuiceSwap 和 Satsuma 中的套利机会。
- **用法:** `arb:check <代币A> <代币B>`
- **示例:** `arb:check wcBTC USDC.e`

### arb:scan
一次性扫描所有代币对，查找套利机会。显示价格差、预估利润、手续费及净利润。
- **用法:** `arb:scan`

### arb:monitor
持续监控所有代币对的套利机会。当检测到盈利机会且利润超过配置阈值时，会发送 Telegram 警报。
- **用法:** `arb:monitor`

### txns
显示指定钱包地址的近期代币转账记录。
- **用法:** `txns <地址> [小时数]`
- **示例:** `txns 0xYourAddress 24`

## 支持的代币

| 符号        | 描述                                      |
|------------|-----------------------------------------|
| wcBTC       | 包装的 Citrea 比特币                             |
| ctUSD       | Citrea 的 USD 稳定币                               |
| USDC.e       | 连接至 LayerZero 的 USDC                             |
| USDT.e       | 连接至 LayerZero 的 USDT                             |
| WBTC.e       | 连接至 LayerZero 的包装比特币                         |
| JUSD        | 由 BTC 支持的稳定币（JuiceDollar）                     |

## 支持的 DEX

| DEX         | 类型                                      | 手续费等级                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| JuiceSwap     | Uniswap V3                                   | 0.05%, 0.30%, 1.00%                             |
| Satsuma      | Algebra                                    | 每个池的手续费动态调整                         |

## 配置

请在 `.env` 文件中设置以下参数：

| 变量        | 描述                                      | 默认值                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| TELEGRAM_BOT_TOKEN | 用于与 Telegram 机器人通信的机器人令牌             | —                                      |
| TELEGRAM_chat_ID | 你的聊天 ID（来自 @userinfobot）                   | —                                      |
| ARB_ALERT_THRESHOLD_BPS | 触发套利警报的最低利润（基点）                   | 50                                        |
| ARB_MONITOR_INTERVAL_SEC | 套利机会扫描间隔（秒）                         | 15                                        |

## 注意事项

- 所有数据均直接从 Citrea 主网获取，不使用第三方 API。
- 价格信息来自部署在 Citrea 上的 RedStone 预言机。
- 套利机会的检测结果仅供参考，执行操作前请务必在链上核实。
- JuiceSwap 中的 JUSD 对使用 svJUSD 作为内部结算货币，处理过程透明。
- RPC 请求地址：`https://rpc.mainnet.citrea.xyz`