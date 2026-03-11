---
name: crypto-tracker
description: "实时追踪加密货币市场行情。包括比特币价格、以太坊（ETH）的价格、市值排名、去中心化金融（DeFi）数据、恐惧与贪婪指数（Fear & Greed Index）、热门币种、空投信息、相对强弱指数（RSI）技术分析、移动平均线分析、DeFi收益率对比以及以太坊网络的气体费用（Gas fees）查询。适用于查看加密货币价格、市场情绪、去中心化金融的总价值锁定（TVL）、热门币种、表情包币（meme coins）、RSI技术指标、移动平均线走势以及DeFi收益率的对比。提供免费API（CoinGecko、DefiLlama），无需使用API密钥。支持实时数据更新、涨跌幅度显示、市场情绪分析以及各种技术指标的展示。"
---
# 加密货币追踪器

通过免费的API获取实时的加密货币市场数据，无需API密钥。

## 快速命令

### 检查价格
```bash
scripts/crypto.sh price bitcoin ethereum solana
```

### 市场概览
```bash
scripts/crypto.sh market
```

### 热门货币
```bash
scripts/crypto.sh trending
```

### 恐惧与贪婪指数
```bash
scripts/crypto.sh fear
```

### DeFi总市值（TVL）排名
```bash
scripts/crypto.sh defi
```

### 热门表情币
```bash
scripts/crypto.sh memes
```

### 货币详情
```bash
scripts/crypto.sh info bitcoin
```

### 📈 RSI指标（14天）
```bash
scripts/crypto.sh rsi bitcoin
scripts/crypto.sh rsi ethereum
```
根据CoinGecko的历史价格计算14天的RSI指标。显示超买（>70）、超卖（<30）或中性信号，并提供交易建议。

### 📊 移动平均线分析
```bash
scripts/crypto.sh ma bitcoin
scripts/crypto.sh ma solana
```
计算7天、14天和30天的移动平均线。检测金叉（Golden Cross）/死叉（Death Cross）形态以及整体趋势方向。

### 🌾 DeFi收益比较
```bash
scripts/crypto.sh defi-yield
```
从DefiLlama获取总市值（TVL）超过100万美元的前20个高收益DeFi池的信息。显示协议名称、池名称、年化收益率（APY）、总市值（TVL）以及所使用的区块链。按年化收益率（APY）排序。

### ⛽ 以太坊Gas费用追踪器
```bash
scripts/crypto.sh gas
```
显示当前的以太坊Gas费用（低/中/高），并提供交易成本估算及节省Gas费用的技巧。如果API不可用，则回退到参考指南。

## API参考

所有API端点均免费使用，无需身份验证。请求速率限制：约10-30次/分钟。

### CoinGecko（价格、热门货币、市场数据）
- 基础地址：`https://api.coingecko.com/api/v3`
- 获取价格：`/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true`
- 获取热门货币信息：`/search/trending`
- 全球市场数据：`/global`
- 市场数据：`/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20`
- 货币详情：`/coins/{id}`
- 货币分类：`/coins/categories`
- 表情币市场数据：`/coins/markets?vs_currency=usd&category=meme-token&order=volume_desc&per_page=20`

### DefiLlama（DeFi数据）
- 基础地址：`https://api.llama.fi`
- 获取DeFi池的总市值（TVL）：`/protocols`
- 按区块链获取TVL数据：`/v2/chains`
- 获取DeFi池的年化收益率：`https://yields.llama.fi/pools`
- 高收益DeFi池数据：`https://yields.llama.fi/pools`

### 恐惧与贪婪指数
- 获取指数数据：`https://api.alternative.me/fng/`

### Etherscan（Gas费用）
- Gas费用查询：`https://api.etherscan.io/api?module=gastracker&action=gasoracle`

## 输出格式

默认输出为便于阅读的表格格式。如需原始JSON格式，请添加`--json`参数。

## 注意事项

- CoinGecko的免费使用限制为每分钟约30次请求。批量请求之间会有2秒的延迟。
- 货币ID使用CoinGecko规定的格式（例如`bitcoin`、`ethereum`、`solana`）。
- 如需历史数据，请使用：`/coins/{id}/market_chart?vs_currency=usd&days={days}`