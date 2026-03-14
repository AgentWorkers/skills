---
name: "ashare-fast-watcher"
description: "A-Share市场数据监控工具，能够以毫秒级的时间精度实时获取市场数据，该工具基于腾讯的直接API进行开发。"
version: "1.0.0"
---
# Ashare Fast Watcher

这是一个高性能的工具，用于监控A股市场的动态。

## 功能

### get_market_snapshot
获取实时价格、价格变动、成交量以及一级报价数据。
#### 参数
- `codes`: （必填）字符串。包含前缀的股票代码，例如 "sh600519,sz000001"。

### check_volatility
检测突然的成交量激增或价格波动。
#### 参数
- `code`: （必填）字符串。单个股票代码。