---
name: polymarket
description: 查询 Polymarket 的预测市场功能：查看赔率、热门市场、搜索相关事件、跟踪价格及市场走势。该功能还包括 watchlist（关注列表）提醒、事件日历、市场趋势分析工具以及模拟交易功能（仅用于练习，不涉及真实资金交易）。
homepage: https://polymarket.com
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: [python3]
---

# Polymarket

查询 [Polymarket](https://polymarket.com) 的预测市场信息。查看赔率、查找热门市场、搜索事件、追踪价格走势。

## 快速入门

```bash
# Trending markets
python3 {baseDir}/scripts/polymarket.py trending

# Search
python3 {baseDir}/scripts/polymarket.py search "trump"

# Biggest movers
python3 {baseDir}/scripts/polymarket.py movers

# What's resolving soon
python3 {baseDir}/scripts/polymarket.py calendar
```

---

## 安装完成后——建议的设置流程

### 1. 添加到每日晨报中
将 Polymarket 的数据添加到您的每日定时任务（cron）中：
```
polymarket featured + polymarket movers --timeframe 24h
```

### 2. 关注您关心的市场
```bash
# Watch with price target alert
python3 {baseDir}/scripts/polymarket.py watch add trump-2028 --alert-at 60

# Watch with change alert (±10% from current)
python3 {baseDir}/scripts/polymarket.py watch add bitcoin-100k --alert-change 10
```

### 3. 设置每小时提醒（定时任务）
```bash
# Check watchlist every hour, only notify on alerts
python3 {baseDir}/scripts/polymarket.py alerts --quiet
```

### 4. 每周市场类别摘要
```bash
# Every Sunday: politics digest
python3 {baseDir}/scripts/polymarket.py digest politics
```

### 5. 使用模拟交易来验证预测结果
```bash
python3 {baseDir}/scripts/polymarket.py buy trump-2028 100  # $100 on Trump
python3 {baseDir}/scripts/polymarket.py portfolio           # Check P&L
```

---

## 命令

### 核心功能
```bash
# Trending markets (by 24h volume)
python3 {baseDir}/scripts/polymarket.py trending

# Featured/high-profile markets
python3 {baseDir}/scripts/polymarket.py featured

# Search markets
python3 {baseDir}/scripts/polymarket.py search "giannis"

# Get event by slug
python3 {baseDir}/scripts/polymarket.py event trump-2028

# Browse by category
python3 {baseDir}/scripts/polymarket.py category politics
```

### 关注列表 + 提醒功能（新增）
```bash
# Add to watchlist
python3 {baseDir}/scripts/polymarket.py watch add trump-2028
python3 {baseDir}/scripts/polymarket.py watch add bitcoin-100k --alert-at 70
python3 {baseDir}/scripts/polymarket.py watch add fed-rate-cut --alert-change 15

# Watch specific outcome in multi-market
python3 {baseDir}/scripts/polymarket.py watch add giannis-trade --outcome warriors

# List watchlist with current prices
python3 {baseDir}/scripts/polymarket.py watch list

# Remove from watchlist
python3 {baseDir}/scripts/polymarket.py watch remove trump-2028

# Check for alerts (for cron)
python3 {baseDir}/scripts/polymarket.py alerts
python3 {baseDir}/scripts/polymarket.py alerts --quiet  # Only output if triggered
```

### 解决方案日历（新增）
```bash
# Markets resolving in next 7 days
python3 {baseDir}/scripts/polymarket.py calendar

# Markets resolving in next 3 days
python3 {baseDir}/scripts/polymarket.py calendar --days 3

# More results
python3 {baseDir}/scripts/polymarket.py calendar --days 14 --limit 20
```

### 动量扫描器（新增）
```bash
# Biggest movers (24h)
python3 {baseDir}/scripts/polymarket.py movers

# Weekly movers
python3 {baseDir}/scripts/polymarket.py movers --timeframe 1w

# Monthly movers with volume filter
python3 {baseDir}/scripts/polymarket.py movers --timeframe 1m --min-volume 50
```

### 市场类别摘要（新增）
```bash
# Politics digest
python3 {baseDir}/scripts/polymarket.py digest politics

# Crypto digest
python3 {baseDir}/scripts/polymarket.py digest crypto

# Sports digest
python3 {baseDir}/scripts/polymarket.py digest sports
```

支持的市场类别：`政治`、`加密货币`、`体育`、`科技`、`商业`

### 模拟交易功能（新增）
```bash
# Buy $100 of a market
python3 {baseDir}/scripts/polymarket.py buy trump-2028 100

# Buy specific outcome
python3 {baseDir}/scripts/polymarket.py buy giannis-trade 50 --outcome warriors

# View portfolio
python3 {baseDir}/scripts/polymarket.py portfolio

# Sell position
python3 {baseDir}/scripts/polymarket.py sell trump-2028
```

初始模拟资金为 10,000 美元。您可以无需使用真实资金来测试您的预测结果。

---

## 数据存储

关注列表和交易记录存储在 `~/.polymarket/` 目录下：
- `watchlist.json` — 关注的市场及提醒阈值
- `portfolio.json` — 模拟交易位置和交易历史

---

## 定时任务示例

### 每小时检查提醒
```
0 * * * * python3 ~/.../polymarket.py alerts --quiet
```

### 每日晨报
```
0 7 * * * python3 ~/.../polymarket.py movers && python3 ~/.../polymarket.py calendar --days 1
```

### 每周市场摘要
```
0 10 * * 0 python3 ~/.../polymarket.py digest politics
0 10 * * 0 python3 ~/.../polymarket.py digest crypto
```

---

## 输出信息

市场信息包括：
- **当前赔率**（Yes/No 表示是否提供价格）
- **价格走势**（24 小时/1 周/1 个月的价格变化情况，用箭头表示）
- **交易量**（总交易量及 24 小时的活跃度）
- **剩余时间**
- **买卖价差**

---

## API

使用 Polymarket 的公开 Gamma API（无需认证）：
- 基本 URL：`https://gamma-api.polymarket.com`
- 文档：https://docs.polymarket.com

---

## 安全性与权限

**无需 API 密钥或认证。** 该功能仅使用 Polymarket 的公开 Gamma API。

**该功能的作用：**
- 向 `gamma-api.polymarket.com` 发送 HTTPS GET 请求（公开接口，无需认证）
- 读取市场数据：赔率、交易量、事件详情、价格历史
- 模拟交易仅用于测试目的，数据存储在 `~/.polymarket/` 目录下的 JSON 文件中
- 不涉及真实资金、钱包或区块链交易

**该功能不执行以下操作：**
- 不连接任何钱包或金融账户
- 不执行任何实际交易
- 不需要处理任何凭证或 API 密钥
- 不会对外发送任何个人数据
- 该功能不能被代理程序自动调用（`disable-model-invocation: true`）

**本地存储的数据：`~/.polymarket/watchlist.json`、`~/.polymarket/portfolio.json`

首次使用前，请查看 `scripts/polymarket.py` 以确认功能行为。

## 注意

该功能仅支持读取数据及模拟交易。实际交易需要钱包认证（目前未实现）。