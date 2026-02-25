---
name: geckoterminal
description: 查询GeckoTerminal的市场数据——包括网络、去中心化交易所（DEXs）、矿池、代币、价格走势（OHLCV）、交易记录以及热门/新出现的矿池信息。
homepage: https://www.geckoterminal.com
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🦎"
    requires:
      bins: [node]
---
# GeckoTerminal

通过本地 CLI 脚本查询 [GeckoTerminal](https://www.geckoterminal.com)。

## 快速入门

```bash
# List networks
node {baseDir}/scripts/geckoterminal-cli.mjs get_networks

# Solana trending pools
node {baseDir}/scripts/geckoterminal-cli.mjs get_network_trending_pools --network solana --duration 1h --page 1

# Search pools
node {baseDir}/scripts/geckoterminal-cli.mjs search_pools --query "SOL USDC" --network solana --page 1
```

---

## 安装后 - 建议的配置方式

### 1. 每日发现扫描
在每日简报中使用该功能：
```
gecko trending pools + new pools + top pools
```

### 2. 跟踪多个池中的代币
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_token_pools --network solana --token "<token_address>" --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_simple_token_prices --network solana --token-addresses "<token1>,<token2>"
```

### 3. 分析候选池
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool_info --network solana --pool "<pool_address>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool_trades --network solana --pool "<pool_address>" --page 1
```

---

## 命令

### 网络与去中心化交易所（DEXes）

```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_networks
node {baseDir}/scripts/geckoterminal-cli.mjs get_dexes --network solana
node {baseDir}/scripts/geckoterminal-cli.mjs get_top_pools --network solana --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_dex_pools --network solana --dex "raydium" --page 1
```

### 热门/新出现的池
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_global_trending_pools --duration 1h --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_network_trending_pools --network solana --duration 24h --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_global_new_pools --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_network_new_pools --network base --page 1
```

### 池与搜索
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs search_pools --query "SOL USDC" --network solana --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool --network solana --pool "<pool_address>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_multi_pools --network solana --pool-addresses "<pool1>,<pool2>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool_info --network solana --pool "<pool_address>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool_trades --network solana --pool "<pool_address>" --page 1
```

### 代币
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_token --network solana --token "<token_address>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_multi_tokens --network solana --token-addresses "<token1>,<token2>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_token_info --network solana --token "<token_address>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_token_pools --network solana --token "<token_address>" --page 1
node {baseDir}/scripts/geckoterminal-cli.mjs get_simple_token_prices --network solana --token-addresses "<token1>,<token2>"
node {baseDir}/scripts/geckoterminal-cli.mjs get_recently_updated_token_info --page 1
```

### 开盘价、最高价、最低价、收盘价（OHLCV）
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs get_pool_ohlcv --network solana --pool "<pool_address>" --timeframe hour --limit 100 --currency usd --token base
```

### 原始 API 替代方案
```bash
node {baseDir}/scripts/geckoterminal-cli.mjs api_get --path /networks/trending_pools --query-json '{"duration":"5m","page":1}'
```

### 可选的查询参数
CLI 支持以下常见的可选参数：
```bash
# Include related resources where supported
--include "base_token,quote_token,dex"

# Include extra pool/token breakdowns where supported
--include-volume-breakdown true
--include-composition true

# Include inactive-source rows where supported
--include-inactive-source true

# Sort/page where supported
--sort "h24_volume_usd_desc"
--page 1

# Community data toggle (trending/new/top/dex pools endpoints)
--include-gt-community-data false

# Simple token price extras
--include-market-cap true
--mcap-fdv-fallback true
--include-24hr-vol true
--include-24hr-price-change true
--include-total-reserve-in-usd true
```

---

## 输出特性

典型的输出内容包括：
- 池的属性（网络、去中心化交易所、地址、链接）
- 价格、流动性、成交量和交易摘要
- 代币元数据以及相关联的池信息
- 开盘价、最高价、最低价、收盘价（OHLCV）图表和近期交易记录

默认输出格式为 JSON，便于数据传输和自动化处理。

---

## API

使用 GeckoTerminal 的公共 API v2（仅限读取）：
- 基本 URL：`https://api.geckoterminal.com/api/v2`
- `api_get --path` 仅接受相对路径（绝对路径将被屏蔽）

---

## 安全性与权限

无需 API 密钥。

**该技能的功能：**
- 向 GeckoTerminal API 发送 HTTPS GET 请求
- 读取公开的网络、去中心化交易所、池、代币和市场数据

**该技能不支持的功能：**
- 不支持钱包连接
- 不支持交易或交易操作
- 不处理任何凭证信息
- 不支持自主调用（`disable-model-invocation: true` 可禁用此功能）