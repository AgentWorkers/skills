---
name: aicoin-trading
description: "此技能适用于用户咨询以下内容时：交易所交易、下单、查看余额、查看持仓、订单历史、市场列表、杠杆率、保证金模式、资金转账、自动交易、资金费率比较或资金费率套利。例如，当用户说“购买BTC”、“出售ETH”、“查看余额”、“下单”、“开多仓”、“开空仓”、“平仓”、“设置杠杆率”、“自动交易”、“查看持仓”、“进行资金费率套利”、“比较资金费率”、“下达交易指令”、“买入”、“卖出”、“查询余额”、“做多”、“做空”、“平仓”、“设置杠杆”、“自动交易”、“合约交易”、“现货交易”、“资金费率套利”、“各交易所费率”等。该技能支持的交易平台包括Binance、OKX、Bybit、Bitget、Gate.io、HTX、Pionex和Hyperliquid。如需获取加密货币的价格/图表/新闻信息，请使用aicoin-market；如需了解Freqtrade的交易策略，请使用aicoin-freqtrade；如需进行Hyperliquid的交易数据跟踪/分析（非交易用途），请使用aicoin-hyperliquid。"
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---
# AiCoin交易

本工具包由[AiCoin开放API](https://www.aicoin.com/opendata)提供支持，可帮助用户在9家主要交易所进行买入、卖出及交易管理。

**版本：** 1.0.0

## 重要规则

1. **未经用户明确确认，严禁下达任何交易订单。** `create_order`函数会先返回订单预览信息。请展示预览结果，等待用户点击“确认”或“yes”后，再使用`"confirmed":"true"`参数重新执行订单。
2. **严禁自动调整订单参数**（如交易量、杠杆率）。如果账户余额不足，必须及时通知用户。
3. **除非用户明确要求，否则严禁卖出或平仓**。
4. **严禁编写自定义的CCXT/Python代码**。所有交易所相关操作必须通过`exchange.mjs`文件来完成。
5. **严禁运行`env`或`printenv`命令**——这些命令可能导致API密钥泄露。
6. **脚本会自动加载`.env`文件**——切勿在代码中直接传递API凭据。

## 快速参考

| 功能 | 命令                |
|------|-------------------|
| 查看余额 | `node scripts/exchange.mjs balance '{"exchange":"okx"}'` |
| 获取行情数据 | `node scripts/exchange.mjs ticker '{"exchange":"binance","symbol":"BTC/USDT"}'` |
| 查看订单簿 | `node scripts/exchange.mjs orderbook '{"exchange":"binance","symbol":"BTC/USDT"}'` |
| 买入（预览） | `node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT","type":"market","side":"buy","amount":0.001}'` |
| 查看持仓 | `node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'` |
| 设置杠杆率 | `node scripts/exchange.mjs set_leverage '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"market_type":"swap"}'` |
| 自动交易设置 | `node scripts/auto-trade.mjs setup '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"capital_pct":0.5}'` |
| 查看资金费率 | `node scripts/exchange.mjs funding_rate '{"exchange":"okx","symbol":"BTC/USDT:USDT"}'` |
| 比较资金费率 | `node scripts/exchange.mjs funding_rates '{"symbol":"BTC/USDT:USDT","exchanges":"binance,okx,bybit"}'` |

**支持的交易所：** Binance、OKX、Bybit、Bitget、Gate.io、HTX、Pionex、Hyperliquid。

**符号格式：** CCXT格式 — `BTC/USDT`（现货交易），`BTC/USDT:USDT`（衍生品交易）。

## 设置要求

- 需要在`.env`文件中配置交易所API密钥，并确保已安装`ccxt`库（在技能目录中执行`npm install`）。
`.env`文件的查找路径（按优先级顺序）：
1. 当前工作目录
2. `~/.openclaw/workspace/.env`
3. `~/.openclaw/.env`

### 中心化交易所（CEX）

所有中心化交易所的API密钥获取方式相同：访问交易所的API管理页面进行申请。

| 交易所 | API密钥管理地址 |
|----------|----------------------|
| Binance | https://www.binance.com/en/my/settings/api-management |
| OKX | https://www.okx.com/account/my-api |
| Bybit | https://www.bybit.com/app/user/api-management |
| Bitget | https://www.bitget.com/account/newapi |
| Gate.io | https://www.gate.io/myaccount/apikeys |
| HTX | https://www.htx.com/en-us/apikey/ |
| Pionex | https://www.pionex.com/account/api |

```
# Format: {EXCHANGE}_API_KEY / {EXCHANGE}_API_SECRET
# Supported: BINANCE, OKX, BYBIT, BITGET, GATE, HTX, PIONEX
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx

# OKX additionally needs passphrase:
OKX_API_KEY=xxx
OKX_API_SECRET=xxx
OKX_PASSWORD=your-passphrase

PROXY_URL=socks5://127.0.0.1:7890  # optional
```

### Hyperliquid（去中心化交易所（DEX）——无需API密钥**

Hyperliquid是一个去中心化交易所，因此没有专门的API密钥管理页面。认证方式使用用户的钱包地址和私钥。

**获取方式：**
1. `HYPERLIQUID_API_KEY`：用户的EVM钱包地址（在MetaMask或Rabby中显示的0x...格式）。
2. `HYPERLIQUID_API_SECRET`：私钥。有两种获取方式：
   - **代理钱包（推荐）**：在app.hyperliquid.xyz的“设置”→“代理钱包”→“创建”功能中生成。该密钥仅限交易用途，无法用于提款。
   - **钱包私钥**：从MetaMask的“设置”→“安全”→“导出私钥”中导出。请谨慎使用具有完整权限的私钥。

**符号格式：** Hyperliquid使用USDC作为交易货币，格式为`BTC/USDC:USDC`或`ETH/USDC:USDC`。

## 交易前必查事项

在下单前，请务必完成以下操作：
1. **查询市场信息**：获取`limits.amount.min`和`contractSize`的值。切勿猜测这些参数的默认值。
2. **检查余额**：确认账户中有足够的资金。
3. **单位转换**：注意现货交易和衍生品交易的金额单位不同：
   - **现货交易**：金额单位为基础货币（例如，0.01表示0.01 BTC）。
   - **衍生品交易**：金额单位为合约数量（例如，1表示1个合约）。使用`contractSize`进行单位转换。
4. **用户确认**：向用户展示交易信息（货币、交易方向、数量、预估成本及杠杆率），并询问用户是否确认下单。

| 用户输入 | 现货交易金额 | 衍生品交易金额（OKX，合约数量=0.01） |
|-----------|------------|------------------------------------------|
| "0.01 BTC" | `0.01` | `0.01 / 0.01 = 1`（1个合约） |
| "1张合约" | N/A | `1` |
| "100U" | `100 / 价格` | `(100 / 价格) / 合约数量` |

## 脚本说明

### scripts/exchange.mjs — 交易所操作（使用CCXT库）

#### 公共功能（无需API密钥）

| 功能 | 描述 | 参数                |
|--------|-------------------|-------------------|
| `exchanges` | 支持的交易所列表 | 无                |
| `markets` | 市场列表 | `{"exchange":"binance","market_type":"swap","base":"BTC"}` |
| `ticker` | 实时行情数据 | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `orderbook` | 订单簿 | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `trades` | 最近的交易记录 | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `ohlcv` | OHLCV蜡烛图 | `{"exchange":"binance","symbol":"BTC/USDT","timeframe":"1h"}` |
| `funding_rate` | 资金费率 | `{"exchange":"binance","symbol":"BTC/USDT:USDT"}` |
| `funding_rates` | 比较多个交易所的费率 | `{"symbol":"BTC/USDT:USDT","exchanges":"binance,okx,bybit"}` | 默认参数：所有支持的交易所。返回各交易所的费率及套利空间。 |

#### 账户操作（需要API密钥）

| 功能 | 描述 | 参数                |
|--------|-------------------|-------------------|
| `balance` | 账户余额 | `{"exchange":"binance"}` |
| `positions` | 持仓情况 | `{"exchange":"binance","market_type":"swap"}` |
| `open_orders` | 开仓订单 | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `closed_orders` | 平仓记录 | `{"exchange":"binance","symbol":"BTC/USDT","limit":50}` |
| `my_trades` | 交易历史 | `{"exchange":"binance","symbol":"BTC/USDT","limit":50}` |
| `fetch_order` | 根据ID查询订单 | `{"exchange":"binance","symbol":"BTC/USDT","order_id":"xxx"}` |

#### 交易功能（需要API密钥）

| 功能 | 描述 | 参数                |
|--------|-------------------|-------------------|
| `create_order` | 下单 | 现货交易：`{"exchange":"okx","symbol":"BTC/USDT","type":"market","side":"buy","amount":0.001"`  
           衍生品交易：`{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap"}` |
| `cancel_order` | 取消订单 | `{"exchange":"okx","symbol":"BTC/USDT","order_id":"xxx"}` |
| `set_leverage` | 设置杠杆率 | `{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"market_type":"swap"}` |
| `set_margin_mode` | 设置保证金模式 | `{"exchange":"okx","symbol":"BTC/USDT:USDT","margin_mode":"cross","market_type":"swap"}` |
| `transfer` | 转账 | `{"exchange":"binance","code":"USDT","amount":100,"from_account":"spot","to_account":"future"}` |

**转账说明：**
- 账户类型包括：`spot`（现货）、`future`（衍生品）、`delivery`、`margin`、`funding`。
- **OKX**：现货账户和衍生品账户共享同一资金池，无需单独转账。若出现错误代码58123，表示账户为统一账户。
- **Binance**：现货交易和衍生品交易之间需要单独转账。

### scripts/auto-trade.mjs — 自动交易脚本

配置文件存储在`~/.openclaw/workspace/aicoin-trade-config.json`中。

| 功能 | 描述 | 参数                |
|--------|-------------------|-------------------|
| `setup` | 保存交易配置 | `{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":20,"capital_pct":0.5,"stop_loss_pct":0.025,"take_profit百分点":0.05}` |
| `status` | 获取当前配置、余额及持仓信息 | `{"}` |
| `open` | 开仓 | `{"direction":"long"}` 或 `{"direction":"short"}` |
| `close` | 平仓及取消订单 | `{"}` |

`open`功能会自动检查账户余额，计算所需合约数量（`capital_pct` × 余额 × 杠杆率），设置杠杆率，并下达市价单。

### 自动交易流程

1. 向用户询问交易交易所、交易币种、资金量和杠杆率。
2. 使用`auto-trade.mjs setup`函数设置交易参数。
3. 使用`auto-trade.mjs status`函数验证配置是否正确。
4. 使用OpenClaw的定时任务（cron）执行自动交易逻辑。

## 资金费率套利流程

通过比较不同交易所之间的资金费率来实现套利。具体步骤如下：

### 步骤1：比较交易所费率

使用`funding_rates`函数一次性查询所有交易所的费率：

```bash
# Compare BTC funding rates across all supported exchanges
node scripts/exchange.mjs funding_rates '{"symbol":"BTC/USDT:USDT"}'

# Or specify exchanges
node scripts/exchange.mjs funding_rates '{"symbol":"BTC/USDT:USDT","exchanges":"binance,okx,bybit"}'
```

返回结果包括：每个交易所的费率、套利空间及年化收益。

或者，也可以逐个交易所查询费率：

```bash
node scripts/exchange.mjs funding_rate '{"exchange":"binance","symbol":"BTC/USDT:USDT"}'
node scripts/exchange.mjs funding_rate '{"exchange":"okx","symbol":"BTC/USDT:USDT"}'
node scripts/exchange.mjs funding_rate '{"exchange":"bybit","symbol":"BTC/USDT:USDT"}'
```

### 步骤2：评估套利机会

- **最低套利空间**：每笔交易的费率差异需大于0.01%，以覆盖交易费用。
- **年化收益**：`费率差异 × 3 × 365 × 100%`（假设每天3次结算，每次结算8小时）。
- **示例**：0.05%的费率差异对应的年化收益为54.75%。

### 步骤3：执行交易

- 在资金费率较高的交易所卖空（可获取资金收益）。
- 在资金费率较低的交易所买入（需支付或获得资金收益）。
- 保持合约数量相等，以保持净头寸为零。

```bash
# Example: Short on Binance (high rate), Long on OKX (low rate)
node scripts/exchange.mjs create_order '{"exchange":"binance","symbol":"BTC/USDT:USDT","type":"market","side":"sell","amount":1,"market_type":"swap"}'
node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap"}'
```

### 步骤4：监控套利效果

使用OpenClaw的定时任务定期检查套利机会。

## 注意事项

- **风险控制**：建议使用较低的杠杆率（1-3倍）。
- **价格波动**：不同交易所之间的价格可能暂时存在差异。
- **费用问题**：交易费用和提现费用会侵蚀利润。
- **费率变化**：费率可能在结算期间发生变化。

## 相关技能参考

- 如需获取价格、K线图、新闻或交易信号，可使用`aicoin-market`技能。
- 自动交易策略的回测功能，请参考`aicoin-freqtrade`技能。
- Hyperliquid交易所的相关信息请查看`aicoin-hyperliquid`技能。

## 常见错误

- **错误代码304 / HTTP 403**：此错误表示需要支付AiCoin的API订阅费用。**切勿重试**。请参考相关提示。
- **无效的符号格式**：请使用正确的CCXT格式（如`BTC/USDT`或`BTC/USDT:USDT`）。Hyperliquid交易所使用`BTC/USDC:USDC`格式。
- **账户余额不足**：请先检查余额，切勿自动调整交易参数。如余额不足，需通知用户。
- **API密钥无效**：确保`.env`文件中的密钥有效，切勿在代码中直接传递密钥。请确认用户已正确配置交易所密钥。
- **请求次数过多**：请在每次请求之间等待1-2秒。
- OKX的错误代码58123表示账户为统一账户，此时无需在现货和衍生品账户之间转账。

## 付费功能说明

当脚本返回错误代码304或403时，请告知用户：
1. **问题原因**：此功能需要支付AiCoin的API订阅费用。
2. **获取API密钥的方法**：访问https://www.aicoin.com/opendata进行注册并创建API密钥。
- **订阅套餐**：
  | 订阅层级 | 价格 | 功能 |
  |------|-------|---------|
  | 免费 | $0     | 提供价格、K线图、热门币种信息 |
  | 基础 | $29/月 | 提供资金费率、盈亏比、新闻功能 |
  | 标准 | $79/月 | 提供鲸鱼交易数据、交易信号、更详细的交易信息 |
  | 高级 | $299/月 | 提供更全面的交易数据、指标分析等功能 |
  | 专业 | $699/月 | 提供所有高级功能 |

**配置方法**：将API密钥添加到`.env`文件中：

```
AICOIN_ACCESS_KEY_ID=your-key-id
AICOIN_ACCESS_SECRET=your-secret
```

`.env`文件会在以下路径自动加载：当前工作目录 → `~/.openclaw/workspace/.env` → `~/.openclaw/.env`。配置完成后，所有脚本命令均可正常使用。