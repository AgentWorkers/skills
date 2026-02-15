---
name: polymarket
description: 查询 Polymarket 预测市场：查看赔率、热门市场、搜索事件、追踪价格。
homepage: https://polymarket.com
metadata: {"clawdbot":{"emoji":"📊"}}
---

# Polymarket

查询 [Polymarket](https://polymarket.com) 的预测市场信息。查看赔率、查找热门市场、搜索相关事件。

## 命令

```bash
# Trending/active markets
python3 {baseDir}/scripts/polymarket.py trending

# Search markets
python3 {baseDir}/scripts/polymarket.py search "trump"
python3 {baseDir}/scripts/polymarket.py search "bitcoin"

# Get specific market by slug
python3 {baseDir}/scripts/polymarket.py event "fed-decision-in-october"

# Get markets by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
python3 {baseDir}/scripts/polymarket.py category sports
```

## 示例对话使用

- “特朗普在2028年获胜的赔率是多少？”
- “Polymarket上哪些市场最热门？”
- “在Polymarket上搜索‘比特币’”
- “美联储利率决议的点差是多少？”
- “有哪些有趣的加密货币市场？”

## 输出结果

市场信息包括：
- 问题/标题
- 当前赔率（支持“是”/“否”选项）
- 交易量
- 结束日期

## API

使用公开的Gamma API（读取数据无需认证）：
- 基本URL：`https://gamma-api.polymarket.com`
- 文档：https://docs.polymarket.com

## 注意

该功能仅支持数据读取，进行交易需要钱包认证（目前尚未实现）。