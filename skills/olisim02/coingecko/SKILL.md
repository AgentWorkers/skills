---
name: coingecko
description: 从 CoinGecko 的免费 API 中获取加密货币的价格、市场数据以及代币信息。当用户询问加密货币的价格、市值、24 小时价格变化、热门加密货币或代币信息时，可以使用该功能。该 API 支持 BTC、ETH、SOL 以及数千种山寨币的数据查询；同时也可以通过合约地址查询 Solana 代币的相关信息。
---

# CoinGecko 加密货币价格技能

该技能通过 CoinGecko 的免费 API 获取加密货币市场数据（无需密钥，但每分钟请求次数有限制，约为 30 次）。

## 命令

### 检查货币价格（一个或多个货币）
```bash
python3 scripts/price.py bitcoin ethereum solana
```
返回：每种货币的价格、24 小时内的价格变化、市值和成交量。

### 按名称/代码查找货币
```bash
python3 scripts/search.py "pepe"
```
返回：匹配的货币 ID、符号以及市值排名。

### 根据合约地址查找代币（Solana、Ethereum 等）
```bash
python3 scripts/token.py solana <contract_address>
```
返回：代币名称、价格、24 小时内的价格变化、市值和流动性信息。

### 热门货币
```bash
python3 scripts/trending.py
```
返回：CoinGecko 上的热门货币列表。

## 货币 ID
CoinGecko 使用特定的 slug 格式来标识货币（例如 `bitcoin`、`ethereum`、`solana`、`dogecoin`）。如果不确定货币的 ID，可以使用 `search.py` 来查找正确的 ID。

## 请求限制
免费 API：每分钟最多 30 次请求。进行批量查询时请使用缓存结果。避免在循环中频繁调用该 API。